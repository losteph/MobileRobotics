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

* Assegnamo i permessi di esecuzioni a tutti gli script necessari (dopo esserci spostati nella directory corretta da teminale): `chmod +x *.sh`
* Costruiamo l'immagine Docker (da fare solo al psimissimo avvio): `cd docker_ws` -> `./build.sh` (se fallisce disabilita il BuildKit `export DOCKER_BUILDKIT=0` e riprova) 
* Avviamo il container digitando `./run.sh` sul terminale (dopo essere tornati indietro alla directory giusta con `cd ..`)

Una volta dentro il container Docker dobbiamo compilare i pacchetti del progetto:

* `cd root/ros_workspace`
* `colcon build`
* `source install/setup.bash`



* `ros2 launch autonomous_nav display_launch.py` Per il debugging visivo del robot (apre rviz): Apre il visualizzatore 3D per controllare l'URDF del robot e il raggio del LiDAR senza simulare la gravità o la fisica
* `ros2 launch autonomous_nav simulation_launch.py` Apre la mappa gazebo e posiziona il robot allo start, ma sta fermo, si può guidare manualmente aprendo `./exec.sh` su un altro terminale (fare sempre il `source install/setup.bash`) e digitando poi `ros2 run teleop_twist_keyboard teleop_twist_keyboard` (con la "i" si va avanti, con "k" si frena, con la "u" gira a sinistra andando avanti, con "j" gira sul posto a sinistra, con "o" gira a destra andando avanti, con "l" gira a destra sul posto)

Debug
* `ros2 topic list` Vedere la lista di tutti i canali di comunicazione attivi
* `ros2 topic echo /scan` Stampa a schermo i valori grezzi letti dal sensore LiDAR in tempo reale.
* `ros2 topic hz /scan` Verifica la frequenza di aggiornamento del LiDAR (messaggi inviati al secondo)
* `ros2 topic echo /cmd_vel` Mostra le velocità lineari e angolari calcolate dal controllore e inviate ai motori.

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
