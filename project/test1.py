
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import set_ev_cls, CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.ofproto import ofproto_v1_3
from ryu.topology import event, switches
from ryu.topology.api import get_all_switch, get_all_link, get_all_host
from ryu.lib.packet import packet, ethernet, ether_types, ipv4, tcp, ospf, bgp, icmp
import networkx as nx


def should_pass(pkt):

    if pkt.get_protocol(ethernet.ethernet).ethertype == ether_types.ETH_TYPE_IPV6:
        print("discarded IPv6 packet")
        print(pkt)
        return False

    elif pkt.get_protocol(ethernet.ethernet).ethertype == ether_types.ETH_TYPE_ARP:
        print("ARP packet")
        return True


    else:
        print()
        print("-------------------------------------")
        print(pkt)
        print("-------------------------------------")
        print()

        return False

    """
    
    eth = pkt.get_protocol(ethernet.ethernet)

    # Se il pacchetto è ehernet
    if eth.ethertype == ether_types.ETH_TYPE_IP:

        # se il pacchetto eth è un LLDP
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return True, "LLDP"

    # se il pacchetto è IPv4
    else:

        ip = pkt.get_protocol(ipv4.ipv4)
        print(ip)

        if ip.proto == ipv4.inet.IPPROTO_ICMP:
            return True, "ICMP"
        elif ip.proto == ipv4.inet.IPPROTO_OSPF:
            return True, "OSPF"

        elif ip.proto == ipv4.inet.IPPROTO_TCP:

            tcp_packet = pkt.get_protocol(tcp.tcp)

            # se il pacchetto è http (== porta 80)
            payload = pkt.protocols[-1]

            if payload.startswith(b"GET") or payload.startswith(b"POST") or payload.startswith(b"HTTP"):

                # se è http GET
                if b'GET' not in tcp_packet.data:
                    return True, "HTTP GET"
                else:

                    # TODO
                    # check if it is a response to a previously received http GET
                    condition = True

                    if condition:
                        return True, "HTTP RESPONSE"

            # Se il pacchetto è TCP e la porta no è 80
            else:

                # allow syn and ack for TCP handshake
                if tcp_packet.syn or tcp_packet.ack:
                    return True, "TCP HANDSHAKE"

    return False
    """


class Lab4SDN(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()

        actions = parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)

        instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, [actions])]

        # messaggio di tipo flow mod
        mod = parser.OFPFlowMod(datapath=datapath, priority=0, match=match, instructions=instructions)

        datapath.send_msg(mod)

    # questa serve dopo
    def find_destination_switch(self, mac_destination):
        for host in get_all_host(self):
            if host.mac == mac_destination:
                # host.port.dpid è il datapath id dello switch a cui l'host di destinazione è collegato
                # host.port.port_no è il numero di porta dello switch a cui l'host di destinazione è collegato
                # quindi la tupla (A, B) se sto cercando mario vuol dire:
                # mario è collegato allo switch A nella sua porta B
                return host.port.dpid, host.port.port_no
        return None, None

    def find_next_hop_destination(self, source_id, destination_id):
        topo = nx.DiGraph()
        for link in get_all_link(self):
            topo.add_edge(link.src.dpid, link.dst.dpid, port=link.src.port_no)

        path = nx.shortest_path(topo, source_id, destination_id)

        link_next_hop = topo[path[0]][path[1]]

        return link_next_hop["port"]

    """
    adesso andiamo a scrivere cosa deve fare il controller quando riceve un pacchetto:
    - prima lo parsa (lo mette nell'oggetto della classe packet)
    - poi controlla se la versione è giusta e se non ci sono problemi
    - trova lo switch di destinazione
    - trova lo shortest path verso quello switch
    - inoltra il pacchetto al next hop
    - installa la regola nello switch
    """
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):

        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        input_port = ev.msg.match["in_port"]

        # parsing del pacchetto

        pkt = packet.Packet(ev.msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        if not should_pass(pkt):
            return

        # trovare switch di destinazione

        mac_dst = eth.dst
        dpid, port_no = self.find_destination_switch(mac_dst)

        if dpid is None or port_no is None:
            # se l'host non esiste
            # o se l'host non ha mai parlato
            return

        # trovare shortest path verso destinazione

        if datapath.id == dpid:
            # lo switch siamo noi
            output_port = port_no
        else:
            # lo switch si trova a qualche hop da noi, quindi lo mandiamo al prossimo
            output_port = self.find_next_hop_destination(datapath.id, dpid)

        # inoltrare il pacchetto verso la destinazione

        actions = [parser.OFPActionOutput(output_port)]

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=ev.msg.buffer_id,
            in_port=input_port,
            actions=actions,
            data=ev.msg.data
        )

        datapath.send_msg(out)

        # inserire la regola nello switch

        match = parser.OFPMatch(eth_dst=mac_dst)

        actions = parser.OFPActionOutput(
            output_port
        )

        instructions = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                [actions]
            )
        ]

        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=10,
            match=match,
            instructions=instructions
        )

        datapath.send_msg(mod)
