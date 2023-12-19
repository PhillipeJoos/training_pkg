import os
import rospy
import smach
import smach_ros
import speech_recognition as sr
from gtts import gTTS
from ctypes import *

# ELIMINA ERRORES DE ALSALIB, errores irrelevantes que dificultan la lectura en la consola
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
		
def py_error_handler(filename, line, function, err, fmt):
	pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')

asound.snd_lib_error_set_handler(c_error_handler)


class Listen(smach.State):
	def __init__(self):
		# Inicializamos el estado
		smach.State.__init__(self,
					   outcomes=['succeeded', 'failed', 'aborted'],
					   output_keys=['prompt'])
		
		# Inicializamos el reconocedor de voz
		self.r = sr.Recognizer()

	def execute(self, userdata):
		# Manejar reconocimiento de voz con try/except para elegir el siguiente estado de la máquina
		try:
			with sr.Microphone() as source:
				audio = self.r.adjust_for_ambient_noise(source, duration=2) 
				audio = self.r.listen(source, phrase_time_limit=5, timeout=5)
			prompt = self.r.recognize_google(audio, language="es-ES")
			print("Google Speech Recognition cree que dijiste " + prompt)
			userdata.prompt = prompt
			return 'succeeded'
		except sr.UnknownValueError:
			print("Google Speech Recognition no pudo entender tu mensaje")
			return 'failed'
		except sr.RequestError as e:
			print("No se pueden consultar resultados del servicio Google Speech Recognition; {0}".format(e))
			return 'aborted'
		except sr.WaitTimeoutError:
			print("No se ha detectado audio")
			return 'failed'

# Este getInstance() solo se ejecuta si este archivo es el principal
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
	
	sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
	sis.start()

	sm.execute()

	rospy.spin()
	sis.stop()
	
if __name__ == '__main__':
	
	getInstance()
