#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32 # importar mensajes de ROS tipo String y tipo Int32
from geometry_msgs.msg import Twist # importar mensajes de ROS tipo geometry / Twist
import pyttsx3
import os
import threading
import time
from duckietown_msgs.msg import WheelsCmdStamped
import random

class Template(object):
	def __init__(self, args):
		super(Template, self).__init__()
		self.args = args

		# subscribers
		self.sub_instruccion = rospy.Subscriber("/duckiebot/voz/resp", String, self.callback_instruccion)
		
		# publishers
		self.pub_wheels = rospy.Publisher("/duckiebot/wheels_driver_node/wheels_cmd", WheelsCmdStamped, queue_size = 10)
		self.wheels = WheelsCmdStamped()

		self.engine = pyttsx3.init()
		self.engine.setProperty('voice', 'spanish-latin-am')
		self.engine.setProperty('volume', 15.0)
		self.engine.setProperty('rate', 150)

		self.instrucciones = {
			"avanzar": self.avanzar,
			"bailar": self.bailar,
		}

		self.dance_music = "portal_radio_song.mp3"
		self.rickroll_music = "rickroll.mp3"

		self.rickroll_probability = 1.0

		self.velocidad = 38 # cm/s

		self.engine.say("Quack quack!!!")
		self.engine.runAndWait()

	def callback_instruccion(self, msg):
		mensaje = msg.data.split()
		instruccion = mensaje[0]
		parametros = mensaje[1:]
		
		if instruccion in self.instrucciones:
			self.instrucciones[instruccion](parametros)
		else:
			self.engine.say(msg.data)
			self.engine.runAndWait()
	
	def avanzar(self, parametros):
		distancia = parametros[0]
		# avanzar una cantidad "distancia"
		tiempo = float(distancia) / self.velocidad
		self.engine.say("Avanzando " + distancia + " centimetros")
		self.engine.runAndWait()

		# publicar instruccion
		self.wheels.vel_left = -1
		self.wheels.vel_right = -1

		self.pub_wheels.publish(self.wheels)

		time.sleep(tiempo)

		# detenerse
		self.wheels.vel_left = 0
		self.wheels.vel_right = 0

		self.pub_wheels.publish(self.wheels)

		self.engine.say("Listo mi rey")
		self.engine.runAndWait()

	def bailar(self, parametros):
		tiempo = parametros[0]

		self.engine.say("Asi se baila en Duckietown")
		self.engine.runAndWait()

		threading.Thread(target=self.play_music, args=(float(tiempo),)).start()

		vel_baile = 0.7

		# alternar entre girar derecha y girar izquierda
		for i in range(int(tiempo) // 2):
			self.wheels.vel_left = vel_baile
			self.wheels.vel_right = -vel_baile

			self.pub_wheels.publish(self.wheels)

			time.sleep(0.5)

			self.wheels.vel_left = -vel_baile
			self.wheels.vel_right = vel_baile

			self.pub_wheels.publish(self.wheels)

			time.sleep(0.5)
		
		for i in range(int(tiempo) // 2):
			self.wheels.vel_left = vel_baile
			self.wheels.vel_right = vel_baile

			self.pub_wheels.publish(self.wheels)

			time.sleep(0.5)

			self.wheels.vel_left = -vel_baile
			self.wheels.vel_right = -vel_baile

			self.pub_wheels.publish(self.wheels)

			time.sleep(0.5)

		self.wheels.vel_left = 0
		self.wheels.vel_right = 0

		self.pub_wheels.publish(self.wheels)

		self.engine.say("Como te quedo el ojo?")
		self.engine.runAndWait()

		os.system("pkill mpg123")

	def play_music(self, tiempo):
		if random.random() < self.rickroll_probability:
			os.system("mpg123 " + self.rickroll_music)
		else:
			os.system("mpg123 " + self.dance_music) 

		exit()

def main():
	rospy.init_node('escucha') #creacion y registro del nodo!

	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#obj.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()
