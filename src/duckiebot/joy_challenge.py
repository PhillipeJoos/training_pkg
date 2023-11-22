#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32, Float32 #importa mensajes de ROS tipo String y Int32
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

		#publicamos en duckiebot/possible_cmd
		self.pub_possible_cmd = rospy.Publisher("/duckiebot/possible_cmd", WheelsCmdStamped, queue_size = 10)

	def callback(self,msg):
		
		# buttons
		A = msg.buttons[0]
		B = msg.buttons[1] # freno de mano
		X = msg.buttons[2]
		Y = msg.buttons[3]
		Select = msg.buttons[6]
		Start = msg.buttons[7]
		DPad_left = msg.buttons[11]
		DPad_right = msg.buttons[12]
		DPad_up = msg.buttons[13]
		DPad_down = msg.buttons[14]
		LT = msg.axes[2] # retroceder
		RT = msg.axes[5] # avanzar

		# joysticks
		JL_x = msg.axes[0] # virar izq-der
		JL_y = msg.axes[1]
		JR_x = msg.axes[3]
		JR_y = msg.axes[4]

		#print(f"B: {B}, LT: {LT}, RT: {RT}, JL_x: {JL_x}")
		print("B: " + str(B))
		print("LT: " + str(LT))
		print("RT: " + str(RT))
		print("JL_x: " + str(JL_x))


		factor_v = 1
		
		if abs(JL_x) <= 0.15: x = 0
		
		velocity = ((RT - 1) - (LT - 1)) / 2 * factor_v
		
		#print(, y_right, x, z)
		#if (x == 0):
	#		self.wheels.vel_left = velocity
	#        	self.wheels.vel_right = velocity
		
		if (LT == 1 and RT == 1): # quieto
			self.wheels.vel_left = -JL_x #if JL_x > 0 else 0 
			self.wheels.vel_right = JL_x #if -JL_x > 0 else 0
		else: # cuando se mueve
			JL_x *= 0.5
			self.wheels.vel_left = (velocity - JL_x) * factor_v
			self.wheels.vel_right = (velocity + JL_x) * factor_v

			# condiciones de freno
			#cond_1 = B == 1
			#cond_2 = self.min_distance < 20 if LT == 1.0 else False

			if B == 1:
				self.wheels.vel_left = 0
				self.wheels.vel_right = 0

		#print(f"vel_left: {self.wheels.vel_left}, vel_right: {self.wheels.vel_right}")
		print("velocity: " + str(velocity))
		print("vel_left: " + str(self.wheels.vel_left))
		print("vel_right: " + str(self.wheels.vel_right))

		self.publi.publish(self.wheels)

def main():
	rospy.init_node('joy_control') #creacion y registro del nodo!

	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#obj.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()
