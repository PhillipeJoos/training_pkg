import rospy
import smach
import smach_ros


class Instruction(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])

    def execute(self, userdata):
        instr = userdata.instruction
        
