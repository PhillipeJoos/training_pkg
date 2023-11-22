#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32, Float32# importar mensajes de ROS tipo String y tipo Int32
from geometry_msgs.msg import Twist, Point # importar mensajes de ROS tipo geometry / Twist
from duckietown_msgs.msg import WheelsCmdStamped


class Template(object):
	def __init__(self, args):
		super(Template, self).__init__()
		self.args = args

		#suscribir a duckiebot/posicionPato
		self.sub_min_distance = rospy.Subscriber("/duckiebot/posicionPato", Point, self.callback_posicionPato)

		#suscribimos a possible_cmd
		self.sub_possible_cmd = rospy.Subscriber("/duckiebot/possible_cmd", WheelsCmdStamped, self.callback_possible_cmd)

		#publicar la intrucciones del control en possible_cmd
		self.publi = rospy.Publisher("/duckiebot/wheels_driver_node/wheels_cmd", WheelsCmdStamped, queue_size = 10)

		self.posicionPato = Point()
		self.wheels = WheelsCmdStamped()

		# error de posicion del pato
		self.error_x = 60
		self.error_y = 0.5
		self.error_z = 7
		self.z = 35

		# dimensiones de la camara
		self.cam_width = 320
		self.cam_height = 240

		# velocidad de movimiento
		self.vel = 0.5

	def callback_possible_cmd(self, msg):
		self.wheels = msg
		self.stalker()

	def callback_posicionPato(self, msg):
		print(msg)
		self.posicionPato = msg
		self.stalker()
	
	def stalker(self):

		print(self.posicionPato.x)
		print("posicionPato.z", self.posicionPato.z)

		if (self.posicionPato.z == 100000):
			self.wheels.vel_left = 0
			self.wheels.vel_right = 0
		# primero avanzamos en la direccion del pato hasta que estemos a 20 cm
		elif (self.posicionPato.z > self.z + self.error_z):
			self.wheels.vel_left = -self.vel
			self.wheels.vel_right = -self.vel
		elif (self.posicionPato.z < self.z - self.error_z):
			self.wheels.vel_left = self.vel
			self.wheels.vel_right = self.vel
		# luego giramos hasta que el pato este en el centro de la imagen
		elif (self.posicionPato.x > self.cam_width/2 + self.error_x):
			self.wheels.vel_left = self.vel
			self.wheels.vel_right = -self.vel
		elif (self.posicionPato.x < self.cam_width/2 - self.error_x):
			self.wheels.vel_left = -self.vel
			self.wheels.vel_right = self.vel
		else:
			self.wheels.vel_left = 0
			self.wheels.vel_right = 0
		
		self.publi.publish(self.wheels)
		return


	def freno_de_emergencia(self):
		# Si se intenta mover hacia adelante
		# y hay un pato a menos de 20 cm
		# se detiene en seco el auto.
		print("posicionPato: " + str(self.posicionPato))
		print("vel_left: " + str(self.wheels.vel_left))
		print("vel_right: " + str(self.wheels.vel_right))

		cond_1 = self.wheels.vel_left < 0 and self.wheels.vel_right < 0
		cond_2 = self.posicionPato.z < 20
		if (cond_1 and cond_2):
			self.wheels.vel_left = 0
			self.wheels.vel_right = 0
		
		self.publi.publish(self.wheels)


def main():
	rospy.init_node('controller') #creacion y registro del nodo!

	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()
