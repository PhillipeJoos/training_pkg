#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32 # importar mensajes de ROS tipo String y tipo Int32
from geometry_msgs.msg import Twist # importar mensajes de ROS tipo geometry / Twist
import pyttsx3
import os

class Template(object):
	def __init__(self, args):
		super(Template, self).__init__()
		self.args = args

		self.sub_instruccion = rospy.Subscriber("/duckiebot/voz/resp", String, self.callback_instruccion)
		self.engine = pyttsx3.init()

	def callback_instruccion(self, msg):
		print(msg.data)
		self.engine.say(msg.data)
		self.engine.runAndWait()

def main():
	rospy.init_node('escucha') #creacion y registro del nodo!

	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#obj.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()
