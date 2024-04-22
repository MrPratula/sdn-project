
### 20240422

Le regole fatte con l'OPFMatch devono avere i prerequisiti che dice il prof nelle slide lab5, altrimenti esce  
`ErrorMsg, 1, 4, 9`  
Fatto questo si possono mettere le regole con prio diversa e match diversi sui diversi campi per far passare solo i 
ping, gli arp e i lldp senza mettere ancora regole per TCP.

Andare avanti mettendo regole match per syn e syn ack in modo da iniziare tcp e poi riconoscere http.


### 20240420 

Docker non è persistente. I problemi che avevo non erano dovuti a IPv6, ma a Docker.  
Ho spostato la repo del progetto nella cartella sdn-labs del prof che è persistente, così adesso dovrebbe andare tutto.  
Se ci sono ancora problemi riavviare la macchina virtuale non è detto riavvii Docker, quindi bisogna stoppare docker
con un comando che non ricordo e farlo ripartire. 

Adesso posso andare avanti con l'indicazione di ignorare IPv6.

Se faccio:  
`sudo mn --mac --topo single,3 --controller remote`  
non funziona, mentre se faccio:  
`sudo mn --arp --mac --topo single,3 --controller remote`  
perdo alcuni pacchetti, poi va. 
 - uno switch che non ha mai parlato non si può raggiungere, per questo i pacchetti iniziali si perdono.
 - le regole sono installate la prima volta. I ping successivi non passano dal controller.
  
In ogni caso dopo devo fare   
`ryu-manager --observe-links sdn-labs/sdn-project/project/test1.py flowmanager/flowmanager.py`  

A questo punto:
 - A cosa serve il `--arp`? 
   - a riempire le tabelle di routing degli switch?
     - no altrimenti il ping andrebbe subito invece non va subito, ma prima deve perdere dei pacchetti
     - però serve perchè altrimenti non va niente. Quindi a cosa serve?
 - Come faccio a far passare i pacchetti una volta sola? 
   - A me serve farli passare all'inizio e poi decidere se far passare il flusso TCP con la GET
     - Io faccio il check solo nella logica dell controller, poi la regola fa passare tutto, probabilmente devo mettere un filtro nella regola e far passare solo quello che matcho prima. 

In ogni caso in questo momento il codice ha il controller che capisce quali sono i pacchetti ICMP, ARP, IPv6 e IPv4, ma 
poi la regola la mette su tutti i pacchetti (probabilmente), quindi prossima volta parti a lavorare da questo: **il 
match sulla regola**


### 20240417

Ho questo pacchetto che è un icmpv6. lo riconosco come ipv6 ma devo prenderlo come icmpv6 e non riesco a riconoscerlo
`ethernet(dst='33:33:00:00:00:02',ethertype=34525,src='00:00:00:00:00:02'), ipv6(dst='ff02::2',ext_hdrs=[],flow_label=0,hop_limit=255,nxt=58,payload_length=16,src='fe80::200:ff:fe00:2',traffic_class=0,version=6), icmpv6(code=0,csum=31530,data=nd_router_solicit(option=nd_option_sla(data=None,hw_src='00:00:00:00:00:02',length=1),res=0),type_=133)`

`ipv6(dst='ff02::2',ext_hdrs=[],flow_label=0,hop_limit=255,nxt=58,payload_length=16,src='fe80::200:ff:fe00:2',
traffic_class=0,version=6)`


### 20240415

Implementato in test1 la funzione should_pass() per decidere se il pacchetto deve passare o no.  
Devono passare:
 - Ethernet LLDP: per il network discovery;
 - IPv4 ICMP: per testare i ping;
 - IPv4 OSPF: per trovare lo shortest path;
 - TCP ACK e SYN ACK: per permetter l'handshake TCP;
 - HTTP GET: da consegna;
 - HTTP RESPONSE che rispondono a una GET precedente: da consegna.


### 20240413
Riguardato lab 5

Aprire una topologia a stella con 3 nodi:  
`sudo mn --mac --topo single,3 --controller remote`

Poi apro un servizio in ascolto sulla porta 80 in h2 in modo da potergli far ricevere il traffico  
`mininet/util/m h2 nc -l -p 80`

E apro un'altro processo in un altro terminale in ascolto sulla porta 8080  
`mininet/util/m h2 nc -l -p 8080`

Poi apriamo su h1 un processo che si collega ad h2 sulla porta 80  
`mininet/util/m h1 nc 10.0.0.2 80`

In questo momento quello che scrivo da h1 a h2 sulla porta 80, dovrebbe arrivare ad h2 sulla porta 80.  



### 20240412
Riguardato lab 4
 - esercizio 1  

Docker non salva le credenziali per git mi sa.
Fatto partire la topologia incasinata con  
`sudo mn --arp --mac --topo torus,3,3 --controller remote`  
fatto partire il controller con interfaccia con il discovery della topologia con:  
`ryu-manager --observe-links sdn-project/sdn-lab-template/3_switch/lab4.py flowmanager/flowmanager.py`  
e controllato su firefox che andase tutto. nella sezione flows si possono vedere le tabelle di routing aggiornate. 

 - esercizio 2 ez


### 20240411

Deciso che devo riguardare i lab. Ho guardato lab 3.  
Gli switch sono tanti. Il controllore è uno solo ed è un nodo a parte.  
Gli switch di base mandano tutto al controllore. Il controllore ha le tabelle di routing di tutti gli switch.  
Il controllore legge gli indirizzi dei pacchetti e asocial porte degli switch, id degli switch e mac di destinazione
dei pacchetti.  
In pratica il controllore ha una mega tabella di tabelle, la `mac_to_port` che contiene la tabella di routing di ogni 
switch.  
A ogni pacchetto ricevuto mette dentro lo switch da cui l'ha ricevuto, la porta dello switch e l'indirizzo eth da cui 
è arrivato.  
Poi controlla se sa dove mandare quel pacchetto. Se lo sa glie lo manda, altrimenti lo manda in FLOOD. 


### 20240410

Visto esercizio 3 del lab open flow. Ogni host è collegato alla porta 1 dello switch, per questo il check è sempre su
indirizzo dell'host, ma l'uscita è sempre la porta 1.

Inizio lab 3. Guardato solo teoria.


### 20240408

Fatto con ryu il flood e lo switch classico con i mac hardcodati.

- switch flood:

Fatto partire topologia a stella con 3 host  
`sudo mn --mac --topo single,3 --controller remote`

Fatto partire il controller con <br>
`ryu-manager sdn-labs/2_hub/hub1.py flowmanager/flowmanager.py`

E poi controllato la regola su firefox a  
http://127.0.0.1:8080/home/index.html

- switch classico:

Nella cartella su docker non ci sono tutti gli esempi, quindi ho clonato la repo di github dentro docker  
`git clone https://github.com/MrPratula/sdn-project`  
e poi ho fatto in modo che non mi chieda le credenziali ogni volta che faccio una pull o una push  
`git config --global credential.helper store`

Poi uguale allo switch prima fatto partire topologia a stella con 3 host  
`sudo mn --mac --topo single,3 --controller remote`

Fatto partire il controller questa volta nella mia cartella  
`ryu-manager sdn-project/sdn-lab-template/2_hub/hub2.py flowmanager/flowmanager.py`

E viste le nuove regole su flowmanager su firefox allo stesso indirizzo
http://127.0.0.1:8080/home/index.html


