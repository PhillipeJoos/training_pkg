import rospy
import smach
from std_msgs.msg import String
from speak import speak

class Chat(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'], input_keys=['response'])

        # publishers
        self.pub_instruccion = rospy.Publisher("/duckiebot/voz/resp", String, queue_size=1)

    def execute(self, userdata):
        # imprimir mensaje de estado
        rospy.loginfo('Executing state Chat')
        rospy.loginfo('Chat ' + userdata.response)

        # reproducir la respuesta del chatgpt
        speak(userdata.response)

        return 'succeeded'
