### 20240412
Riguardato lab 4
 - esercizio 1  

Docker non salva le credenziali per git mi sa.
Fatto partire la topologia incasinata con  
`sudo mn --arp --mac --topo torus,3,3 --controller remote`  
fatto partire il controller con interfaccia con il discovery della topologia con:  
`ryu-manager --observe-links sdn-project/sdn-lab-template/3_switch/lab4.py flowmanager/flowmanager.py`  
e controllato su firefox che andase tutto. nella sezione flows si possono vedere le tabelle di routing aggiornate. 



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


