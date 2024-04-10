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

fatto partire il controller questa volta nella mia cartella  
`ryu-manager sdn-project/sdn-lab-template/2_hub/hub2.py flowmanager/flowmanager.py`

E viste le nuove regole su flowmanager su firefox allo stesso indirizzo
http://127.0.0.1:8080/home/index.html


