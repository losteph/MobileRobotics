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
        self.kp = 0.5      # Guadagno Proporzionale (quanto sterza bruscamente)
        self.v_max = 0.6   # Velocità di crociera (m/s)

    def perception_callback(self, msg):
        front_dist = msg.x
        error_y = msg.y

        # ---
        # 1. Calcolo Ingressi Virtuali (u_x, u_y)
        
        # Velocità in avanti (u_x)
        if front_dist < 1.0:
            u_x = 0.0 # Frena di colpo se l'ostacolo è a meno di 1 metro!
            self.get_logger().warn("Ostacolo rilevato!")
        else:
            u_x = self.v_max # Va avanti normalmente

        # Correzione laterale (u_y) tramite legge proporzionale
        u_y = self.kp * error_y

        # ---
        # 2. Matrice di Disaccoppiamento 

        # Trasformiamo le forze virtuali in velocità lineare (v) e angolare (omega)
        v = u_x
        omega = u_y / self.b

        # Limitiamo la velocità di rotazione massima per non farlo impazzire
        if omega > 1.5: omega = 1.5
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