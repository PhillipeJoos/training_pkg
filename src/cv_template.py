#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32, Float32 # importar mensajes de ROS tipo String y tipo Int32
from geometry_msgs.msg import Twist, Point # importar mensajes de ROS tipo geometry / Twist
from sensor_msgs.msg import Image # importar mensajes de ROS tipo Image
import cv2 # importar libreria opencv
from cv_bridge import CvBridge # importar convertidor de formato de imagenes
import numpy as np # importar libreria numpy



class Template(object):
	def __init__(self, args):
		super(Template, self).__init__()
		self.args = args
		#Suscribrirse a la camara
		self.Sub_Cam = rospy.Subscriber("/duckiebot/camera_node/image/rect", Image, self.procesar_img)
        #Publicar imagen(es)
		self.pub_img = rospy.Publisher("/duckiebot/camera_note/image/processed", Image, queue_size = 1)

		self.min_area = 100
		self.pub_mask_yellow = rospy.Publisher("/duckiebot/camera_note/image/mask_yellow", Image, queue_size = 1)
		self.pub_mask_blue = rospy.Publisher("/duckiebot/camera_note/image/mask_blue", Image, queue_size = 1)

		self.pub_posicionPato = rospy.Publisher("/duckiebot/posicionPato", Float32, queue_size = 1)

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

		image_out = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 

		# Definir rangos para la mascara del color amarillo
		lower_limit_yellow = np.array([20, 100, 100])
		upper_limit_yellow = np.array([35, 255, 255])
 
		# Definir rangos para la mascara del color azul
		lower_limit_blue = np.array([105,  80, 100])
		upper_limit_blue = np.array([135, 255, 255])

		#Mascara
		mask_yellow = cv2.inRange(image_out, lower_limit_yellow, upper_limit_yellow)
		mask_blue = cv2.inRange(image_out, lower_limit_blue, upper_limit_blue)
		image_out_yellow = cv2.bitwise_and(image, image, mask=mask_yellow)
		image_out_blue   = cv2.bitwise_and(image, image, mask=mask_blue)

		# Operaciones morfologicas, normalmente se utiliza para "limpiar" la mascara
		kernel = np.ones((3 , 3), np.uint8)
		img_erode = cv2.erode(mask_yellow, kernel, iterations=4) #Erosion
		img_dilate = cv2.dilate(img_erode, kernel, iterations=4) #Dilatar 

		# Definir blobs
		_,contours, hierarchy = cv2.findContours(img_dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		# Distancia minima
		min_distance = 1000

		for cnt in contours:
			AREA = cv2.contourArea(cnt)
			if AREA > self.min_area: #Filtrar por tamano de blobs
				x,y,w,h = cv2.boundingRect(cnt)
				cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

				# Calculamos la distancia real (Dr)
				# Dr = (dr * f) / w
				f = 101 # valor calibrado
				dr = 3.9 # cm

				Dr = round((dr * f) / w, 3)

				# reasignamos la distancia minima
				if Dr < min_distance:
					min_distance = Dr

				# Imprimimos la distancia junto con el blob
				cv2.putText(image, str(Dr), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
			else:
				None

		# Publicar distancia minima
		self.pub_posicionPato.publish(min_distance)

		# Publicar imagen final
		msg = bridge.cv2_to_imgmsg(image, "bgr8")
		msg_mask_yellow = bridge.cv2_to_imgmsg(image_out_yellow, "bgr8")
		msg_mask_blue = bridge.cv2_to_imgmsg(image_out_blue, "bgr8")
		self.pub_img.publish(msg)
		self.pub_mask_yellow.publish(msg_mask_yellow)
		self.pub_mask_blue.publish(msg_mask_blue)

def main():
	rospy.init_node('camera_node') #creacion y registro del nodo!

	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()