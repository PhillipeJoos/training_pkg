import rospy
import smach
from std_msgs.msg import String
from speak import speak
import time
from play_music import play_music
import random

class Bailar(smach.State):
    
        def __init__(self):
            smach.State.__init__(self, outcomes=['succeeded'], input_keys=['time'])

            # publishers    
            self.pub_instruccion = rospy.Publisher("/duckiebot/voz/resp", String, queue_size=1)

        def execute(self, userdata):
            # imprimir mensaje de estado 
            rospy.loginfo('Executing state Bailar')
            rospy.loginfo('Bailar ' + str(userdata.time) + ' segundos')

            # reproducir mensaje de voz con la instruccion
            speak("Bailando " + str(userdata.time) + " segundos")

            # ejecutar la instruccion
            self.pub_instruccion.publish("bailar " + str(userdata.time))

            # esperamos el tiempo necesario para bailar el tiempo deseado
            tiempo = float(userdata.time)
            
            # reproducir música
            canciones = ["chipi.mp3", "portal.mp3", "rickroll.mp3"]
            play_music(random.choice(canciones), tiempo)

            # reproducir mensaje de completado
            speak("Listo")

            return 'succeeded'