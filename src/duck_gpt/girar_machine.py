import rospy
import smach

"""
class Avanzar(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'], input_keys=['distance'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Avanzar')
        rospy.loginfo('Avanzar ' + str(userdata.distance) + ' metros')
        return 'succeeded'
"""

class Girar(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'], input_keys=['direction', 'angle'])
    
    def execute(self, userdata):
        rospy.loginfo('Executing state Girar')
        rospy.loginfo('Girar ' + userdata.direction + ' ' + str(userdata.angle) + ' grados')
        return 'succeeded'