import rospy
import smach

class Chat(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'], input_keys=['response'])
    
    def execute(self, userdata):
        rospy.loginfo('Executing state Chat')
        rospy.loginfo('Chat ' + userdata.response)
        return 'succeeded'
