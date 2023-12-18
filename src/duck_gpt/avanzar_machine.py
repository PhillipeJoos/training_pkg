import rospy
import smach
from std_msgs.msg import String
from speak import speak
import time

class Avanzar(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'], input_keys=['distance'])
        # publishers
        self.pub_instruccion = rospy.Publisher("/duckiebot/voz/resp", String, queue_size=1)

    def execute(self, userdata):
        # reproducir mensaje de estado
        rospy.loginfo('Executing state Avanzar')
        rospy.loginfo('Avanzar ' + str(userdata.distance) + ' centimetros')

        # reproducir mensaje de voz con la instruccion
        speak("Avanzando " + str(userdata.distance) + " centimetros")

        # ejecutar la instruccion
        self.pub_instruccion.publish("avanzar " + str(userdata.distance))

        # esperamos el tiempo necesario para avanzar la distancia deseada
        tiempo = float(userdata.distance) / 37 # cm/s valor obtenido experimentalmente
        time.sleep(tiempo)

        # reproducir mensaje de completado
        speak("Listo")
        return 'succeeded'