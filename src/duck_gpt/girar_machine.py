import rospy
import smach
from std_msgs.msg import String
from speak import speak

class Girar(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'], input_keys=['direction', 'angle'])
    
        self.pub_instruccion = rospy.Publisher("/duckiebot/voz/resp", String, queue_size=1)

    def execute(self, userdata):
        rospy.loginfo('Executing state Girar')
        rospy.loginfo('Girar ' + userdata.direction + ' ' + str(userdata.angle) + ' grados')

        speak("Girando " + userdata.direction + " " + str(userdata.angle) + " grados")

        self.pub_instruccion.publish("girar " + userdata.direction + ' ' + str(userdata.angle))

        speak("Listo")
        return 'succeeded'