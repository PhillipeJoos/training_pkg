import rospy
import smach
from std_msgs.msg import String
from speak import speak
import time

class Girar(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'], input_keys=['direction', 'angle'])

        # publishers
        self.pub_instruccion = rospy.Publisher("/duckiebot/voz/resp", String, queue_size=1)

    def execute(self, userdata):
        # imprimir mensaje de estado
        rospy.loginfo('Executing state Girar')
        rospy.loginfo('Girar ' + userdata.direction + ' ' + str(userdata.angle) + ' grados')

        # reproducir mensaje de voz con la instruccion
        speak("Girando " + userdata.direction + " " + str(userdata.angle) + " grados")

        # ejecutar la instruccion
        self.pub_instruccion.publish("girar " + userdata.direction + ' ' + str(userdata.angle))

        # esperamos el tiempo necesario para girar el angulo deseado
        tiempo = (float(userdata.angle)) / 171.5 # 171.5 es un valor que se obtuvo experimentalmente
        time.sleep(tiempo)

        # reproducir mensaje de completado
        speak("Listo")
        
        return 'succeeded'