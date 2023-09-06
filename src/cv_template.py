#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32 # importar mensajes de ROS tipo String y tipo Int32
from geometry_msgs.msg import Twist, Point # importar mensajes de ROS tipo geometry / Twist
from sensor_msgs.msg import Image # importar mensajes de ROS tipo Image
import cv2 # importar libreria opencv
from cv_bridge import CvBridge # importar convertidor de formato de imagenes
import numpy as np # importar libreria numpy



class Template(object):
	def __init__(self, args):
		super(Template, self).__init__()
		self.args = args
		#Suscribrirse a la cámara
		self.Sub_Cam = rospy.Subscriber("topico", Image, self.procesar_img)
        #Publicar imagen(es)
		self.pub_img = rospy.Publisher("topico", Image, queue_size = 1)
		#self.pub_img = rospy.Publisher("mas", Image, queue_size = 1)


	def procesar_img(self, msg):
		#Transformar Mensaje a Imagen
		bridge = CvBridge()
		image = bridge.imgmsg_to_cv2(msg, "bgr8")

		#Espacio de color

			#cv2.COLOR_RGB2HSV
			#cv2.COLOR_RGB2GRAY
			#cv2.COLOR_RGB2BGR
			#cv2.COLOR_BGR2HSV
			#cv2.COLOR_BGR2GRAY
			#cv2.COLOR_BGR2RGB

		image_out = cv2.cvtColor(image, "Espacio de color") 

		#Definir rangos para la mascara

		lower_limit = np.array([ , , ])
		upper_limit =np.array([ , , ])

		#Mascara
		mask = cv2.inRange(image_out, lower_limit, upper_limit)
		image_out = cv2.bitwise_and(image, image, mask=mask)

		# Operaciones morfológicas, normalmente se utiliza para "limpiar" la mascara
		kernel = np.ones(('ancho' , 'largo'), np.uint8)
		img_erode = cv2.erode(mask, kernel, iterations="numero de iteraciones") #Erosion
		img_dilate = cv2.dilate(img_erode, kernel, iterations="numero de iteraciones") #Dilatar 

		# Definir blobs
		_,contours, hierarchy = cv2.findContours(img_dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		for cnt in contours:
			AREA = cv2.contourArea(cnt)
			if AREA>"Tamaño area en pixeles": #Filtrar por tamaño de blobs
				x,y,w,h = cv2.boundingRect(cnt)
				cv2.rectangle(image, ("coordenada","coordenada"), ("coordenada","coordenada"), ("rojo","azul","verde"), "tamaño del rectangulo en pixeles")
			else:
				None

		# Publicar imagen final
		msg = bridge.cv2_to_imgmsg(image, "bgr8")
		self.pub_img.publish(msg)

def main():
	rospy.init_node('test') #creacion y registro del nodo!

	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()