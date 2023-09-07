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
		#Suscribrirse a la camara
		self.Sub_Cam = rospy.Subscriber("/duckiebot/camera_node/image/raw", Image, self.procesar_img)
        #Publicar imagen(es)
		self.pub_img = rospy.Publisher("/duckiebot/camera_note/image/processed", Image, queue_size = 1)

		self.min_area = 100
		self.pub_mask_yellow = rospy.Publisher("/duckiebot/camera_note/image/mask_yellow", Image, queue_size = 1)
		self.pub_mask_orange = rospy.Publisher("/duckiebot/camera_note/image/mask_orange", Image, queue_size = 1)

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
		lower_limit_yellow = np.array([15, 100, 150])
		upper_limit_yellow = np.array([28, 255, 255])
 
		# Definir rangos para la mascara del color naranja
		lower_limit_orange = np.array([15, 100, 100])
		upper_limit_orange = np.array([20, 255, 255])

		#Mascara
		mask_yellow = cv2.inRange(image_out, lower_limit_yellow, upper_limit_yellow)
		mask_orange = cv2.inRange(image_out, lower_limit_orange, upper_limit_orange)
		image_out_yellow = cv2.bitwise_and(image, image, mask=mask_yellow)
		image_out_orange = cv2.bitwise_and(image, image, mask=mask_orange)

		# Operaciones morfologicas, normalmente se utiliza para "limpiar" la mascara
		kernel = np.ones((3 , 3), np.uint8)
		img_erode = cv2.erode(mask_yellow, kernel, iterations=4) #Erosion
		img_dilate = cv2.dilate(img_erode, kernel, iterations=4) #Dilatar 

		# Definir blobs
		_,contours, hierarchy = cv2.findContours(img_dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		for cnt in contours:
			AREA = cv2.contourArea(cnt)
			if AREA > self.min_area: #Filtrar por tamano de blobs
				x,y,w,h = cv2.boundingRect(cnt)
				cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
			else:
				None

		# Publicar imagen final
		msg = bridge.cv2_to_imgmsg(image, "bgr8")
		msg_mask_yellow = bridge.cv2_to_imgmsg(image_out_yellow, "bgr8")
		msg_mask_orange = bridge.cv2_to_imgmsg(image_out_orange, "bgr8")
		self.pub_img.publish(msg)
		self.pub_mask_yellow.publish(msg_mask_yellow)
		self.pub_mask_orange.publish(msg_mask_orange)

def main():
	rospy.init_node('test') #creacion y registro del nodo!

	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	#objeto.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()