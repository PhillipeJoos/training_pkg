#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32 #importa mensajes de ROS tipo String y Int32
from sensor_msgs.msg import Joy # impor mensaje tipo Joy
from geometry_msgs.msg import Twist # importar mensajes de ROS tipo geometry / Twist
from duckietown_msgs.msg import WheelsCmdStamped


class Template(object):
    def __init__(self, args):
        super(Template, self).__init__()
        self.args = args
        #sucribir a joy
        self.sub = rospy.Subscriber("/duckiebot/joy", Joy, self.callback)
        #publicar la intrucciones del control en possible_cmd
        self.publi = rospy.Publisher("/duckiebot/wheels_driver_node/wheels_cmd", WheelsCmdStamped, queue_size = 10)
        #self.twist = Twist2DStamped()
	self.wheels = WheelsCmdStamped()

    #def publicar(self, msg):
        #self.publi.publish(msg)

    def callback(self,msg):
        a = msg.buttons[1]
	y_left = msg.axes[2]
        y_right = msg.axes[5]
        x = msg.axes[0]
        z = msg.axes[3]

	factor_v = 0.7
	if abs(x) <= 0.15: x = 0
	
	velocity = ((y_right - 1) - (y_left - 1)) * factor_v
        print(y_left, y_right, x, z)
	#if (x == 0):
#		self.wheels.vel_left = velocity
#        	self.wheels.vel_right = velocity
	if (y_left == 1 and y_right == 1):
		self.wheels.vel_left = -x if x > 0 else 0 
		self.wheels.vel_right = x if -x > 0 else 0
	else:
		self.wheels.vel_left = velocity * (1 + x) * factor_v
		self.wheels.vel_right = velocity * (1 - x) * factor_v

        if a == 1:
            self.wheels.vel_left = 0
            self.wheels.vel_right = 0

        self.publi.publish(self.wheels)





def main():
    rospy.init_node('test') #creacion y registro del nodo!

    obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

    #obj.publicar() #llama al metodo publicar del objeto obj de tipo Template

    rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
    main()
