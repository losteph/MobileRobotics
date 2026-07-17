import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Vector3, Twist

class ControlNode(Node):
    def __init__(self):
        super().__init__('control_node')
        
        # Sottoscrizione ai dati (puliti) del LiDAR
        self.sub = self.create_subscription(
            Vector3, '/perception', self.perception_callback, 10)
            
        # Publisher ai motori di Gazebo
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Parametri della I/O Linearization
        self.b = 0.15      # Distanza del punto B (dove sta il LiDAR) dal centro ruote (in metri)
        self.v_max = 0.4   # Velocità di crociera (m/s)

        
        self.kp = 0.4      # Guadagno Proporzionale (quanto sterza bruscamente, reattività)
        self.ki = 0.01      # Guadagno Integrale (correzione di piccoli errori a regime)
        self.kd = 0.07      # Guadagno Derivativo (smorzamento per evitare effetto zig-zag)
        

        # Memoria per il calcolo Integrale e Derivativo
        self.integral_error = 0.0 
        self.prev_error = 0.0

    def perception_callback(self, msg):
        front_dist = msg.x
        left_dist = msg.y
        right_dist = msg.z


        # Errore naturale (se siamo perfettamente al centro, left - right = 0)
        error_y_base = left_dist - right_dist


        target_offset = 0.0 # Di base vogliamo stare in centro
        u_x = self.v_max #velocità in avanti
        state = "LANE_FOLLOWING"



        # ---
        # FSM (macchina a stati finiti) per sorpasso e frenata

        # Se l'ostacolo è troppo vicino, inchioda per sicurezza
        if front_dist < 0.3:
            state = "EMERGENCY_STOP"
            u_x = 0.0
        # Se l'ostacolo è in zona di guardia, valutiamo il sorpasso
        elif front_dist < 1.2:
        
            if (left_dist - right_dist) > 0.3:
                state = "OVERTAKE_LEFT"
                target_offset = 0.6  # Spostiamo il centro ideale verso sinistra
                
         
            elif (right_dist - left_dist) > 0.3:
                state = "OVERTAKE_RIGHT"
                target_offset = -0.6 # Spostiamo il centro ideale verso destra
                
            else:
                state = "NARROW_PASSAGE" 
                u_x = 0.2
                target_offset = 0.0

        # ---
        # Controllore PID

        # L'errore effettivo che il PID deve annullare (tiene conto di eventuali sorpassi)
        e = error_y_base - target_offset
            
        # Calcolo Derivativo (velocità di variazione dell'errore)
        derivative = e - self.prev_error
            
        # Calcolo Integrale (accumulo dell'errore)
        self.integral_error += e
            
        # Calcolo dinamico dell'Anti-Windup
        self.u_y_max = 1.5 * self.b #u_y_max = omega_max * b
        self.antiwindup = self.u_y_max / self.ki

        # Anti-windup per il termine integrale (evita che esploda se ci incastriamo)
        if self.integral_error > self.antiwindup: self.integral_error = self.antiwindup
        if self.integral_error < - self.antiwindup: self.integral_error = - self.antiwindup


        # Equazione del PID completa
        u_y = (self.kp * e) + (self.ki * self.integral_error) + (self.kd * derivative)

        # Salviamo l'errore per il prossimo ciclo
        self.prev_error = e
        if state == "EMERGENCY_STOP" and abs(e) < 0.05:
            self.integral_error = 0.0 


        # ---
        # 2. Matrice di Disaccoppiamento 

        # Trasformiamo le forze virtuali in velocità lineare (v) e angolare (omega)
        v = u_x
        omega = u_y / self.b

        # Limitiamo la velocità di rotazione massima per non farlo impazzire
        if omega > 1.5: omega = 1.5 #omega_max
        if omega < -1.5: omega = -1.5

        # Pubblichiamo i comandi ai motori
        twist = Twist()
        twist.linear.x = float(v)
        twist.angular.z = float(omega)
        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = ControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
