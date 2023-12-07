import rospy
import smach
from std_msgs.msg import String

class Bailar(smach.State):
    
        def __init__(self):
            smach.State.__init__(self, outcomes=['succeeded'], input_keys=['time'])

            self.pub_instruccion = rospy.Publisher("/duckiebot/voz/resp", String, queue_size=1)

        def execute(self, userdata):
            rospy.loginfo('Executing state Bailar')
            rospy.loginfo('Bailar ' + str(userdata.time) + ' segundos')

            self.pub_instruccion.publish("bailar " + str(userdata.time))
            return 'succeeded'