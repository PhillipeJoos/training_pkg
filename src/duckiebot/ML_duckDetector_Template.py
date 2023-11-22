#!/usr/bin/env python

from geometry_msgs.msg import Twist, Point # importar mensajes de ROS tipo geometry / Twist
import numpy as np # importar libreria numpy
import rospy #importar ros para python
from sensor_msgs.msg import Image # importar mensajes de ROS tipo Image
import cv2 # importar libreria opencv
from cv_bridge import CvBridge, CvBridgeError # importar convertidor de formato de imagenes

class Nodo(object):
	def __init__(self, args):
		super(Nodo, self).__init__()
		self.args = args
		self.sub = rospy.Subscriber("/duckiebot/camera_node/image/rect", Image, self.callback)
		self.detector = cv2.CascadeClassifier("cascade3_LBP.xml")
		self.pub = rospy.Publisher("/duckiebot/camera_node/image/processed", Image, queue_size=10)
		self.pub_posicionPato = rospy.Publisher("/duckiebot/posicionPato", Point, queue_size = 1)

		self.bridge = CvBridge()


	def callback(self,msg):

		image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
		#crop image to remove the upper part of the image
		image = image[120:240, 0:320]
		image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		dets = self.detector.detectMultiScale(image_gray, 1.3 , 10)

		distance_min = 100000
		x_min = 0
		y_min = 0

		for patos in dets:
			x,y,w,h=patos
			area = 400 #intenten variar este valor
			if w*h>area:
				cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)

			#calcular la distancia a partir de la distancia enter el borde inferior del rectangulo y el borde inferior de la imagen
			distance = 120 - (y+h)
			cv2.putText(image, str(distance), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
			
			if distance < distance_min:
				distance_min = distance
				x_min = x
				y_min = y

		posicion = Point()
		posicion.x = x_min
		posicion.y = y_min
		posicion.z = distance_min
		self.pub_posicionPato.publish(posicion)

		msg = self.bridge.cv2_to_imgmsg(image, "bgr8")
		self.pub.publish(msg)
		
def main():
	rospy.init_node('test') #creacion y registro del nodo!

	obj = Nodo('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()