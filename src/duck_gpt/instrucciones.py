#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32 # importar mensajes de ROS tipo String y tipo Int32
from geometry_msgs.msg import Twist # importar mensajes de ROS tipo geometry / Twist
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
		self.pub_wheels = rospy.Publisher("/duckiebot/wheels_driver_node/wheels_cmd", WheelsCmdStamped, queue_size = 1)
		self.wheels = WheelsCmdStamped()

		# definimos un diccionario de instrucciones
		self.instrucciones = {
			"avanzar": self.avanzar,
			"bailar": self.bailar,
			"parar": self.parar,
			"girar": self.girar
		}

		# fijamos una velocidad de avance
		self.velocidad = 37 # cm/s valor obtenido experimentalmente 

		print("Listo para recibir instrucciones")

	def callback_instruccion(self, msg):
		# seperar instruccion y parametros
		mensaje = msg.data.split()
		instruccion = mensaje[0]
		parametros = mensaje[1:]
		
		# ejecutar instruccion si esta en el diccionario
		if instruccion in self.instrucciones:
			self.instrucciones[instruccion](parametros)
	
	#instruccion para avanzar
	def avanzar(self, parametros):
		# obtener distancia
		distancia = parametros[0]
		print("Avanzando: " + distancia)
		# avanzar una cantidad "distancia"
		tiempo = float(distancia) / self.velocidad

		# publicar instruccion
		# fijar velocidades de las ruedas
		self.wheels.vel_left = -1
		self.wheels.vel_right = -1

		self.pub_wheels.publish(self.wheels)

		# esperar un tiempo para que avance la distancia deseada
		time.sleep(tiempo)

		# detenerse
		self.wheels.vel_left = 0
		self.wheels.vel_right = 0

		# publicar detencion
		self.pub_wheels.publish(self.wheels)

	#instruccion para bailar
	def bailar(self, parametros):
		# obtener tiempo
		tiempo = parametros[0]
		print("Baiando por: " + tiempo)
		
		#fijar una velocidad de baile
		vel_baile = 0.7

		# alternar entre girar derecha y girar izquierda publicando velocidades
		for i in range(int(tiempo) // 2):
			self.wheels.vel_left = vel_baile
			self.wheels.vel_right = -vel_baile

			self.pub_wheels.publish(self.wheels)

			time.sleep(0.5)

			self.wheels.vel_left = -vel_baile
			self.wheels.vel_right = vel_baile

			self.pub_wheels.publish(self.wheels)

			time.sleep(0.5)
		
		# alternar entre avanzar y retroceder publicando velocidades
		for i in range(int(tiempo) // 2):
			self.wheels.vel_left = vel_baile
			self.wheels.vel_right = vel_baile

			self.pub_wheels.publish(self.wheels)

			time.sleep(0.5)

			self.wheels.vel_left = -vel_baile
			self.wheels.vel_right = -vel_baile

			self.pub_wheels.publish(self.wheels)

			time.sleep(0.5)

		# detener el baile
		self.wheels.vel_left = 0
		self.wheels.vel_right = 0

		self.pub_wheels.publish(self.wheels)

	#instruccion para girar
	def girar(self, parametros):
		# obtener direccion y angulo
		direccion = parametros[0]
		angulo = parametros[1]
		print("Girando: " + direccion + " " + angulo)

		# girar una cantidad "angulo"
		

		# girar una cantidad "angulo"
		tiempo = (float(angulo)) / 171.5 # 171.5 es un valor que se obtuvo experimentalmente

		# publicar giro a partir de velocidades
		if direccion == "izquierda":
			self.wheels.vel_left = -1
			self.wheels.vel_right = 1

			self.pub_wheels.publish(self.wheels)
			
			time.sleep(tiempo)
			
		elif direccion == "derecha":
			self.wheels.vel_left = 1
			self.wheels.vel_right = -1

			self.pub_wheels.publish(self.wheels)

			time.sleep(tiempo)
	
		# detenerse
		self.wheels.vel_left = 0
		self.wheels.vel_right = 0

		self.pub_wheels.publish(self.wheels)

def main():
	rospy.init_node('escucha') #creacion y registro del nodo!

	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#obj.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()
