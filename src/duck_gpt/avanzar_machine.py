import rospy
import smach
import smach_ros

class Avanzar(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'], input_keys=['distance'])

        self.pub_instruccion = rospy.Publisher("/duckiebot/voz/resp", String, queue_size=1)

    def execute(self, userdata):
        rospy.loginfo('Executing state Avanzar')
        rospy.loginfo('Avanzar ' + str(userdata.distance) + ' centimetros')

        self.pub_instruccion.publish("Avanzar " + str(userdata.distance) + " centimetros")
        return 'succeeded'
        
