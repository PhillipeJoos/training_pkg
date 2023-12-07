import rospy
import smach
from std_msgs.msg import String

class Chat(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'], input_keys=['response'])
    
        self.pub_instruccion = rospy.Publisher("/duckiebot/voz/resp", String, queue_size=1)

    def execute(self, userdata):
        rospy.loginfo('Executing state Chat')
        rospy.loginfo('Chat ' + userdata.response)

        self.pub_instruccion.publish(userdata.response)
        return 'succeeded'
