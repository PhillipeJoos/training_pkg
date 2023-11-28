import os
import rospy
from std_msgs.msg import String, Int32 # importar mensajes de ROS tipo String y tipo Int32
import smach
import smach_ros
from listen_machine import Listen
import openai
import typer
from rich import print

class GPT(smach.State):
	def __init__(self):
		#Publicar en el topic /duckiebot/voz/resp
		self.pub_instruccion = rospy.Publisher("/duckiebot/voz/resp", String, queue_size=1)

		smach.State.__init__(self,
					   outcomes=['succeeded', 'aborted'],
					   input_keys=['prompt'])
		openai.api_key = "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"

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
								
								3. Si lo recibido es similar a "parar" o "detente" responder "parar".

								4. Si lo recibido es similar a "bailar" una cierta cantidad de tiempo
								responder "bailar X". Si no se especifica una cantidad, responder "bailar 5".
							    
								5. Si lo recibido es similar a "chiste" responder un chiste original"""}
		self.messages = [self.context]


	def execute(self, userdata):
		content = userdata.prompt

		self.messages.append({"role": "user", "content": content})

		if not content:
			print("🤷‍♂️ No has dicho nada")
			return "aborted"
		
		response = openai.ChatCompletion.create(
			model="gpt-4", messages=self.messages)

		response_content = response.choices[0].message.content

		self.messages.append({"role": "assistant", "content": response_content})

		print(f"[bold green]> [/bold green] [green]{response_content}[/green]")
		# reemplazar los caracteres especiales por espacios
		response_content = response_content.replace("¿", " ")
		response_content = response_content.replace("¡", " ")
		#Publicamos el la respuesta de chat_gpt en el topic /duckiebot/voz/resp
		self.pub_instruccion.publish(response_content)
		return 'succeeded'

def getInstance():

	rospy.init_node('gpt_machine')
	
	sm = smach.StateMachine(outcomes=[
		'succeeded',
		'aborted'
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
								   'succeeded':'Listen',
								   'aborted': 'Listen'
								   })

	sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
	sis.start()

	sm.execute()

	rospy.spin()
	sis.stop()

if __name__ == '__main__':
	getInstance()