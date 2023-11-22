import os
import rospy
import smach
import smach_ros
import speech_recognition as sr
from gtts import gTTS

class Listen(smach.State):
	def __init__(self, robot):
		smach.State.__init__(self, outcomes=['succeeded', 'failed', 'aborted'])
		self.robot = robot
		#self.pub_instruccion = rospy.Publisher("/duckiebot/voz/resp", String, queue_size=10	)


	def execute(self):
		try:
			r = sr.Recognizer()
			with sr.Microphone() as source:
				audio = r.adjust_for_ambient_noise(source, duration=2) # listen for 1 second to calibrate the energy threshold for ambient noise levels
				audio = r.listen(source, phrase_time_limit=5, timeout=5)
			prompt = r.recognize_google(audio)
			print("Google Speech Recognition thinks you said " + prompt)
			#self.pub_instruccion.publish(msg)
			return 'succeeded'
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
			return 'failed'
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
			return 'aborted'



def getInstance(robot):

	sm = smach.StateMachine(outcomes=[
		'succeeded', 'failed', 'aborted'
		])

	with sm:

		smach.StateMachine.add('Listen', Listen(robot),
							   transitions = {
								   'succeeded':'succeeded',
								   'failed': 'Listen',
								   'aborted': 'aborted'
								   })
		
	return sm

if __name__ == '__main__':
	rospy.init_node('listen_machine')
	sm = getInstance(None)
	outcome = sm.execute()
	rospy.spin()