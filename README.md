# Autonomous Navigation Robot with I/O Linearization (ros2 & Gazebo)

Repository contenente il progetto per il corso di Mobile Robotics.
L'obiettivo del progetto è lo sviluppo di un sistema di guida autonoma per un robot *Differential Drive*, in grado di navigare in un circuito chiuso ed evitare ostacoli statici (macchine e strettoie) utilizzando un controllo puramente reattivo basato sui dati di un sensore LiDAR.

---

## Architettura del Sistema

Il progetto non utilizza algoritmi di navigazione globale (come SLAM e Nav2), né filtri di localizzazione (Kalman), ma si basa interamente su un **Controllo Reattivo a feedback visivo** strutturato in due nodi ROS 2:

### 1. Nodo di Percezione (`perception_node.py`)
Agisce come l'occhio del robot. Si iscrive al topic `/scan` del LiDAR (con un field of view ottimizzato a 180° frontali). Il nodo estrae due metriche fondamentali:
* **Distanza Frontale:** Per la frenata di emergenza.
* **Errore Laterale ($e_y$):** Calcolato usando una tecnica di *Look-Ahead* (lettura dei raggi a $\pm 45^\circ$) per garantire la stabilità di rotta ed evitare oscillazioni di imbardata.
I dati vengono pubblicati verso il controllore tramite un'interfaccia tipizzata personalizzata (`autonomous_nav_interfaces/msg/PerceptionData`).

### 2. Nodo di Controllo (`control_node.py`)
Implementa la legge di controllo del movimento basata sulla **Input/Output Linearization**.
Poiché il robot è un sistema non-olonomo, il punto di controllo è stato traslato dal centro dell'asse ruote a un punto virtuale $B$ situato a $0.15 \text{m}$ sull'asse longitudinale (coincidente fisicamente con il posizionamento del LiDAR sul robot).
Il controllore applica un guadagno proporzionale ($K_p$) per annullare l'errore laterale e utilizza la matrice di disaccoppiamento per generare le velocità reali al motore ($v$, $\omega$) pubblicate sul topic `/cmd_vel`.

---

## L'Ambiente di Simulazione

Il robot è testato su una mappa `.sdf` creata provando a stressare il controllore tramite:
* **Corsia principale:** Larghezza di 1.5 metri.
* **Ostacoli sfalsati:** Macchine parcheggiate ai lati della corsia per testare la correzione della traiettoria.
* **Restringimento della Corsia:** Sul finale il robot dovrà attraversare un varco più stretto (di soli 0.5 metri).

---

## Istruzioni

Per Windows11 con WSL2, dopo aver aperto la cartella del progetto su VSCode ed aver aperto il terminale (trasformandolo da powershell in linux digitando all'interno `wsl`) possiamo iniziare la simulazione.

* Avviamo (un container docker, l'immagine docker con ros2? da rivedere) digitando `./run.sh` sul terminale
* (Se non funziona è perché non sono abilitati i permessi di esecuzione al file, aggiungerli così: `chmod +x *.sh` (il * serve a dare i permessi a tutti i file .sh nella directory corrente, senza doverlo rifare per ogni nome)
* ((Prima devo spiegare il build del dlockerfile, poi da aggiungere sopra dopo) `cd docker_ws` -> `./build.sh`), se non va disabilità il BuildKit e riprova `export DOCKER_BUILDKIT=0`)))
* `cd root/ros_workspace`
* `colcon build`
* `source install/setup.bash`
* `ros2 launch autonomous_nav display_launch.py` Per il debugging visivo del robot (apre rviz)
* `ros2 launch autonomous_nav simulation_launch.py` Apre la mappa gazebo e posiziona il robot allo start, ma sta fermo, si può guidare manualmente aprendo `./exec.sh` su un altro terminale e digitando poi `ros2 run teleop_twist_keyboard teleop_twist_keyboard` (con la "i" si va avanti, con "k" si frena, con la "u" gira a sinistra andando avanti, con "j" gira sul posto a sinistra, con "o" gira a destra andando avanti, con "l" gira a destra sul posto)

Debug
* `ros2 topic list` Vedere la lista di tutti i canali di comunicazione attivi
* `ros2 topic echo /scan` Leggere in diretta i dati del sensore
* ros2 topic hz /scan (Vedere la frequenza di pubblicazone (messaggi al secondo madati dal LiDAR)
* ros2 topic echo /cmd_vel (Leggere i comandi inviati ai motori dal Controllore

Da migliorare, correggere, finire

---

## Struttura Repo

```
📦 MobileRobotics
 ┣ 📂 docker_ws/
 ┃ ┣ 📄 Dockerfile.project
 ┃ ┗ 📄 build.sh
 ┣ 📂 ros_ws/
 ┃ ┣ 📂 scr/
 ┃ ┃ ┃ ┣ 📂 autonomous_nav/
 ┃ ┃ ┃ ┃ ┣ 📂 autonomous_nav/
 ┃ ┃ ┃ ┃ ┣ 📂 launch
 ┃ ┃ ┃ ┃ ┗ 📂 da finire..
 ┣ 📄 README.md
 ┣ 📄 chown_me.sh
 ┣ 📄 exec.sh
 ┣ 📄 run.sh
 ┗ 📄 Report.pdf (ancora da creare) 
(bozza, da migliorare dopo)
```

---

### 👥 Autori

- Stefano Di Lena.

- Marco Cappelluti Pappagallo.

- Nicolas Nicoletti.
