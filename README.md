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

## Istruzioni di Installazione e Compilazione

... finisco di compilare questa parte dopo ..

---

## Struttura Repo

```
|- docker_ws
|- ros_ws
|- report.pdf (da creare aggiungere dopo)
|- run.sh
|- exec.sh
(bozza, da migliorare dopo)
```

---

### 👥 Autori

- Stefano Di Lena.

- Marco Cappelluti Pappagallo.

- Nicolas Nicoletti.
