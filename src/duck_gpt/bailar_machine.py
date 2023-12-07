import rospy
import smach

class Bailar(smach.State):
    
        def __init__(self):
            smach.State.__init__(self, outcomes=['succeeded'], input_keys=['time'])

        def execute(self, userdata):
            rospy.loginfo('Executing state Bailar')
            rospy.loginfo('Bailar ' + str(userdata.time) + ' segundos')
            return 'succeeded'