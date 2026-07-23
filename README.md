# Autonomous Navigation Robot with I/O Linearization (ros2 & Gazebo)

Repository contenente il progetto per il corso di Mobile Robotics.
L'obiettivo del progetto è lo sviluppo di un sistema di guida autonoma per un robot *Differential Drive*, in grado di navigare in un circuito chiuso ed evitare ostacoli statici (veicoli parcheggiati e strettoie) utilizzando un controllo puramente reattivo basato sui dati di un sensore LiDAR.

---

## Architettura del Sistema

Il progetto esclude intenzionalmente algoritmi di navigazione globale (come SLAM, PRM o Nav2) per concentrarsi su una Architettura di controllo Reattiva, strutturata in due nodi ROS 2 principali:

### 1. Nodo di Percezione (`perception_node.py`)
Agisce come l'occhio del robot. Si iscrive al topic `/scan` del LiDAR (con un field of view frontale di 180°). Il nodo estrae due metriche fondamentali:
* **Distanza Frontale**.
* **Distanze Laterali**.


I dati vengono pubblicati verso il controllore tramite un'interfaccia tipizzata personalizzata (`autonomous_nav_interfaces/msg/PerceptionData`).

### 2. Nodo di Controllo (`control_node.py`)
Rappresenta il cervello del sistema ed opera su due livelli:
- **High-Level (Finite State Machine):** Una Macchina a Stati Finiti valuta le distanze e gestisce i comportamenti logici del robot (LANE_FOLLOWING, OVERTAKE_LEFT/RIGHT, NARROW_PASSAGE, EMERGENCY_STOP).
- **Low-Level (I/O Linearizzation + PID):** Implementa la legge di controllo del movimento.

---

## L'Ambiente di Simulazione

Il robot è testato su mappe `.sdf` create per stressare il controllore tramite:
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



* `ros2 launch autonomous_nav display_launch.py` Per il debugging visivo del robot (apre rviz): Apre il visualizzatore 3D per controllare l'URDF del robot e il raggio del LiDAR senza simulare la gravità o la fisica.
* `ros2 launch autonomous_nav simulation_launch.py` Apre la mappa 1 gazebo e posiziona il robot allo start, ma sta fermo, si può guidare manualmente aprendo `./exec.sh` su un altro terminale (fare sempre il `source install/setup.bash`) e digitando poi `ros2 run teleop_twist_keyboard teleop_twist_keyboard` (con la "i" si va avanti, con "k" si frena, con la "u" gira a sinistra andando avanti, con "j" gira sul posto a sinistra, con "o" gira a destra andando avanti, con "l" gira a destra sul posto).
* `ros2 launch autonomous_nav new_launch.py` Apre la mappa 2 gazebo e posiziona il robot in attesa di comandi manuali.
* `ros2 launch autonomous_nav autonomous_launch.py` Avvia la navigazione autonoma sulla Mappa 1.
* `ros2 launch autonomous_nav complete_launch.py` Avvia la navigazione autonoma sulla Mappa 2.

comandi utili per Debug:
* `ros2 topic list` Vedere la lista di tutti i canali di comunicazione attivi
* `ros2 topic echo /scan` Stampa a schermo i valori grezzi letti dal sensore LiDAR in tempo reale.
* `ros2 topic hz /scan` Verifica la frequenza di aggiornamento del LiDAR (messaggi inviati al secondo)
* `ros2 topic echo /cmd_vel` Mostra le velocità lineari e angolari calcolate dal controllore e inviate ai motori.

Analisi Grafica:
* `ros2 run rqt_graph rqt_graph` Genera lo schema a nodi/topic dell'architettura.
* `ros2 run rqt_plot rqt_plot` Traccia in tempo reale l'andamento delle variabili scelte. 
* `ros2 run tf2_tools view_frames` Genera un PDF con l'albero delle trasformate cinematiche (TF) del robot.

---

## Struttura Repo

```
📦 MobileRobotics
 ┣ 📂 docker_ws/
 ┃ ┣ 📄 Dockerfile.project
 ┃ ┗ 📄 build.sh
 ┣ 📂 ros_ws/
 ┃ ┣ 📂 scr/
 ┃ ┃ ┃ ┗ 📂 autonomous_nav/  # (Pkg principale: launch files, urdf, mappe, nodi python)
 ┣ 📄 README.md
 ┣ 📄 chown_me.sh
 ┣ 📄 exec.sh
 ┣ 📄 run.sh
 ┗ 📄 Report.pdf 
```

---

### 👥 Autori

- Stefano Di Lena.

- Marco Cappelluti Pappagallo.

- Nicolas Nicoletti.
