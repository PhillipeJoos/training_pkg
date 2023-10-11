#!/usr/bin/env python

import rospy #importar ros para python
from sensor_msgs.msg import Image # importar mensajes de ROS tipo Image
import cv2 # importar libreria opencv
from cv_bridge import CvBridge, CvBridgeError # importar convertidor de formato de imagenes

class Nodo(object):
	def __init__(self, args):
		super(Nodo, self).__init__()
		self.args = args
		self.sub = rospy.Subscriber("camera topic", Image, self.callback)
		self.detector = cv2.CascadeClassifier("path to cascade3_LBP.xml")
		self.pub = rospy.Publisher("Image with detections topic", Image, queue_size=10)

		self.bridge = CvBridge()


	def callback(self,msg):

		image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
		image_gray = #Transformen de bgr a escala de grises!

		dets = self.detector.detectMultiScale(image_gray, 1.3 , 10)
		
		for patos in dets:
			x,y,w,h=patos
			area = 400 #intenten variar este valor
			if w*h>area:
				cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)

		msg = self.bridge.cv2_to_imgmsg(image, "bgr8")	 
		self.pub.publish(msg)
		
def main():
	rospy.init_node('test') #creacion y registro del nodo!

	obj = Nodo('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()