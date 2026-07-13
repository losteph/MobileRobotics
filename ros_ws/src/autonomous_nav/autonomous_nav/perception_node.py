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
        front_rays = msg.ranges[80:100] 
        front_dist = min(front_rays)

        # 2. Distanze laterali (raggi a 45°, perché a 90° non andava bene si scontrava non riusciva a guardare bene avanti)
        right_dist = min(msg.ranges[20:60])  
        left_dist = min(msg.ranges[120:160])

        # Se il laser non vede il muro (es. infinito), limitiamo a un valore massimo
        if math.isinf(left_dist): left_dist = 2.0
        if math.isinf(right_dist): right_dist = 2.0

        # Creiamo il messaggio e pubblichiamo
        out_msg = Vector3()
        out_msg.x = float(front_dist)
        out_msg.y = float(left_dist)
        out_msg.z = float(right_dist)
        # Inviamo i dati grezzi filtrati al controllore.
        self.pub.publish(out_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()