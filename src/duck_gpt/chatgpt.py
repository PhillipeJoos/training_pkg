#!/usr/bin/env python

import rospy #importar ros para python
from std_msgs.msg import String, Int32 # importar mensajes de ROS tipo String y tipo Int32
from geometry_msgs.msg import Twist # importar mensajes de ROS tipo geometry / Twist
import time
from ctypes import *
import openai  # pip install openai
import typer  # pip install "typer[all]"
from rich import print  # pip install rich
from rich.table import Table
import speech_recognition as sr
from gtts import gTTS
import os
import rospy

# obtain audio from the microphone
r = sr.Recognizer()

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
	pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)



class Template(object):
	def __init__(self, args):
		super(Template, self).__init__()
		self.args = args

	
		self.pub_instruccion = rospy.Publisher("/duckiebot/voz/resp", String, queue_size=10	)

		#self.sub_voz = rospy.Subscriber("/duckiebot/voz/mensaje_prueba", String, self.callback)
		#rate = rospy.Rate(10) # 10hz
	
	def publicar(self):
		openai.api_key = "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"

		print("💬 [bold green]ChatGPT API en Python[/bold green]")

		table = Table("Comando", "Descripción")
		table.add_row("exit", "Salir de la aplicación")
		table.add_row("new", "Crear una nueva conversación")

		print(table)

		# Contexto del asistente
		context = {"role": "system",
				"content": """
								Nombre: DuckNorris
								Descripción: Eres un vehículo autónomo programado para los habitantes
								de una ciudad de patos llamada Duckietown con 100 habitantes. Tu misión es
								transportar a los patos de un lugar a otro de la ciudad,
								respondiendo a sus preguntas y resolviendo sus dudas. Responde
								todas las dudas de manera breve y concisa en español, sin tildes. ¡Buena suerte!
								Instrucciones: Toda instrucción recibida debe ser transformada a una de las siguientes
								opcines en el formato indicado y responder solamente eso. Si la instrucción no es ninguna de las siguientes
								responder según el contexto.

								1. Si lo recibido es similar a "avanzar" una cierta distancia
								responder "avanzar X cm".

								2. Si lo recibido es similar a "girar" en una cierta direccion un cierto angulo responder,
								"girar direccion angulo". Si no se especifica un angulo responder "girar direccion 360". Si no
								se especifica una direccion responder "girar izquierda angulo". 
								
								3. Si lo recibido es similar a "parar" o "detente" responder "parar".

								4. Si lo recibido es similar a "bailar" una cierta cantidad de tiempo
								responder "bailar X". Si no se especifica una cantidad, responder "bailar 5".
							    
								5. Si lo recibido es similar a "chiste" responder un chiste pero sin caracteres especiales,
								sin ¿ o ¡.
								"""}
		
		messages = [context]

		while True:

			content = self.__prompt()

			if content == "new":
				print("🆕 Nueva conversación creada")
				messages = [context]
				content = self.__prompt()

			messages.append({"role": "user", "content": content})

			if not content:
				print("🤷‍♂️ No has dicho nada")
				continue
			
			response = openai.ChatCompletion.create(
				model="gpt-4", messages=messages)

			response_content = response.choices[0].message.content

			messages.append({"role": "assistant", "content": response_content})

			print(f"[bold green]> [/bold green] [green]{response_content}[/green]")

			# publicar el texto en el topic /duckiebot/voz/instruccion
			msg = String()
			# reemplazar los caracteres especiales por un espacio
			msg.translate({ord('¿'):ord(' '), ord('¡'):ord(' ')})
			msg.data = str(response_content)
			self.pub_instruccion.publish(msg)

	def __prompt(self) -> str:
	
		print("\n¿Sobre qué quieres hablar?")

		with sr.Microphone() as source:
			audio = r.adjust_for_ambient_noise(source, duration=2) # listen for 1 second to calibrate the energy threshold for ambient noise levels
			audio = r.listen(source, phrase_time_limit=5)

		prompt = ""

		# recognize speech using Google Speech Recognition
		try:
			# for testing purposes, we're just using the default API key
			# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
			# instead of `r.recognize_google(audio)`
			prompt = r.recognize_google(audio)
			print("Google Speech Recognition thinks you said " + prompt)
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))


		if prompt == "exit":
			exit = typer.confirm("✋ ¿Estás seguro?")
			if exit:
				print("👋 ¡Hasta luego!")
				raise typer.Abort()

			return self.__prompt()

		return prompt


def main():
	rospy.init_node('PC') #creacion y registro del nodo!

	obj = Template('args') # Crea un objeto del tipo Template, cuya definicion se encuentra arriba

	obj.publicar() #llama al metodo publicar del objeto obj de tipo Template

	rospy.spin() #funcion de ROS que evita que el programa termine -  se debe usar en  Subscribers


if __name__ =='__main__':
	main()
