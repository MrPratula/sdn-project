# sdn-project

Project for the Software defined network course.

(All the material in the folder sdn-lab-template are scripts provided by the professor available on his GitHub repo)

The aim of the project is to use OpenFlow architecture to install rules on SDN switches to block all traffic that is
not HTTP GET.

The project is implemented on Python using RYU library. 

The project is first tested on mininet simulator, then on a real testbed.

The topology used for testing is the following one:

![Original Image](https://github.com/MrPratula/sdn-project/blob/main/resources/topology.jpg)

The switch works in this way:
- When it receives a packet it forwards it to the controller.
- the controller will install rules in the switch to forward it or ignore it.

The controller:
- Allow functional packets:
  - ARP
  - ICMP
  - SYN
  - ACK
- Allow HTTP GET packets
- Allow HTTP responses to a previous GET 
- Won't forward other packets

Also, there are simple script to test the connection once the controller is online. 

Client and server script must be run passing the ip addresses and the port as argument to set up the connection.   
If the controller is online, only the HTTP connection will work.

![Original Image](https://github.com/MrPratula/sdn-project/blob/main/resources/pkt_flow.jpg)

Since this is a simple topology and test scenario the only functional packets allowed are the mentioned one.  
Other control packet should be allowed in  different scenario, like LLDP, BGP and other control packets.
