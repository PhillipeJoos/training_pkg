import os
import rospy
from std_msgs.msg import String, Int32 # importar mensajes de ROS tipo String y tipo Int32
import smach
import smach_ros
from listen_machine import Listen
from avanzar_machine import Avanzar
from bailar_machine import Bailar
from girar_machine import Girar
from chat_machine import Chat
from openai import OpenAI
import typer
from rich import print

class GPT(smach.State):
	def __init__(self):
		#Publicar en el topic /duckiebot/voz/resp
		self.pub_instruccion = rospy.Publisher("/duckiebot/voz/resp", String, queue_size=1)
		
		with open("../api_key/api_key.txt", "r") as f:
			key = f.read().strip()
			self.client = OpenAI(api_key=key)

		smach.State.__init__(self,
					   outcomes=['succeeded', 'aborted', 'avanzar', 'girar', 'bailar', 'chat'],
					   input_keys=['prompt'],
					   output_keys=['distance', 'direction', 'time', 'angle', 'response'])


		self.context = {"role": "system",
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

								3. Si lo recibido es similar a "bailar" una cierta cantidad de tiempo
								responder "bailar X". Si no se especifica una cantidad, responder "bailar 5".
							    
								4. Si lo recibido es similar a "chiste" responder un chiste original
								
								5. Si lo recibido es similar a "adiós" o "apagar" responder "shutdown" y terminar la conversación."""}
		self.messages = [self.context]


	def execute(self, userdata):
		content = userdata.prompt

		self.messages.append({"role": "user", "content": content})

		if not content:
			print("🤷‍♂️ No has dicho nada")
			return "aborted"
		
		response = self.client.chat.completions.create(model="gpt-4", messages=self.messages)

		response_content = response.choices[0].message.content

		self.messages.append({"role": "assistant", "content": response_content})

		print(f"[bold green]> [/bold green] [green]{response_content}[/green]")
		# reemplazar los caracteres especiales por espacios
		response_content = response_content.replace("¿", " ")
		response_content = response_content.replace("¡", " ")
		#Publicamos el la respuesta de chat_gpt en el topic /duckiebot/voz/resp
		#self.pub_instruccion.publish(response_content)

		if response_content == "shutdown":
			return "succeeded"
		
		instruccion = response_content.split()[0]

		if instruccion == "avanzar":
			userdata.distance = response_content.split()[1]
			return "avanzar"
		elif instruccion == "girar":
			userdata.direction = response_content.split()[1]
			userdata.angle = response_content.split()[2]
			return "girar"
		elif instruccion == "bailar":
			userdata.time = response_content.split()[1]
			return "bailar"
		else:
			userdata.response = response_content
			return "chat"
		

def getInstance():

	rospy.init_node('gpt_machine')
	
	sm = smach.StateMachine(outcomes=[
		'succeeded',
		'aborted',
		])
	
	with sm:

		smach.StateMachine.add('Listen', Listen(), 
							   transitions = {
								   'succeeded':'GPT',
								   'failed': 'Listen',
								   'aborted': 'aborted'
								   })
						 

		smach.StateMachine.add('GPT', GPT(),
							   transitions = {
								   'aborted': 'Listen',
								   'succeeded': 'succeeded',
								   'avanzar': 'Avanzar',
								   'girar': 'Girar',
								   'bailar': 'Bailar',
								   'chat': 'Chat'
								   })
		
		smach.StateMachine.add('Avanzar', Avanzar(),
							   transitions = {
								   'succeeded':'Listen'
								   })
		
		smach.StateMachine.add('Girar', Girar(),
							   transitions = {
								   'succeeded':'Listen'
								   })

		smach.StateMachine.add('Bailar', Bailar(),
							   transitions = {
								   'succeeded':'Listen'
								   })
		
		smach.StateMachine.add('Chat', Chat(),
							   transitions = {
								   'succeeded':'Listen'
								   })
						 

	sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
	sis.start()

	sm.execute()

	rospy.spin()
	sis.stop()

if __name__ == '__main__':
	getInstance()
