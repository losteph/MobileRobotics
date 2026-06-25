import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Vector3
import math

class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')
        
        # Sottoscrizione al LiDAR
        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10)
            
        # Publisher dei dati elaborati
        self.pub = self.create_publisher(Vector3, '/perception', 10)
        self.get_logger().info("Nodo avviato!")

    def scan_callback(self, msg):
        # Il LiDAR ha 180 campioni (da -90° a +90°)
        
        # 1. Distanza frontale (media dei 10 gradi centrali: indici da 85 a 95)
        front_rays = msg.ranges[85:95] 
        front_dist = min(front_rays)

        # 2. Distanze laterali (raggi a 45°, perché a 90° non andava bene si scontrava non riusciva a guardare bene avanti)
        right_dist = msg.ranges[45]  
        left_dist = msg.ranges[135]

        # Se il laser non vede il muro (es. infinito), limitiamo a un valore massimo
        if math.isinf(left_dist): left_dist = 2.0
        if math.isinf(right_dist): right_dist = 2.0

        # 3. Calcolo errore laterale
        # Se left_dist = right_dist, l'errore è 0 (siamo in centro).
        # Se siamo troppo a destra, left_dist è grande, right_dist è piccolo -> errore positivo
        error_y = left_dist - right_dist

        # Creiamo il messaggio e pubblichiamo
        out_msg = Vector3()
        out_msg.x = float(front_dist)
        out_msg.y = float(error_y)
        out_msg.z = 0.0 # Non lo usiamo

        self.pub.publish(out_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()