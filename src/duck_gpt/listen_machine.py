import os
import rospy
import smach
import smach_ros
import speech_recognition as sr
from gtts import gTTS
from ctypes import *


ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
		
# ELIMINA ERRORES DE ALSALIB
def py_error_handler(filename, line, function, err, fmt):
	pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)

class Listen(smach.State):
	def __init__(self):
		smach.State.__init__(self,
					   outcomes=['succeeded', 'failed', 'aborted'],
					   output_keys=['prompt'])
		
		self.r = sr.Recognizer()


	def execute(self, userdata):
		try:
			with sr.Microphone() as source:
				audio = self.r.adjust_for_ambient_noise(source, duration=2) # listen for 1 second to calibrate the energy threshold for ambient noise levels
				audio = self.r.listen(source, phrase_time_limit=5, timeout=5)
			prompt = self.r.recognize_google(audio)
			print("Google Speech Recognition thinks you said " + prompt)
			userdata.prompt = prompt
			return 'succeeded'
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
			return 'failed'
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
			return 'aborted'
		except sr.WaitTimeoutError:
			print("No se ha detectado audio")
			return 'aborted'



def getInstance():

	rospy.init_node('listen_machine')

	sm = smach.StateMachine(outcomes=[
		'succeeded',
		'failed',
		'aborted'
		])

	with sm:

		smach.StateMachine.add('Listen', Listen(),
							   transitions = {
								   'succeeded':'succeeded',
								   'failed': 'Listen',
								   'aborted': 'aborted'
								   })
		
	sm.execute()

if __name__ == '__main__':
	getInstance()