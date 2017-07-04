#!/usr/bin/env python
import rospy
import roslib
import math
#import sys

#imports de mensagens
from geometry_msgs.msg import Accel


#Cria a classe do noo para publicar no motor
class ControleRobo():

	#Metodo criador da classe
	def __init__(self):

		#Enviando uma informacao para o usuario
		rospy.loginfo("No de Controle do Robo ABB IRB inicializado")

		#Variavel que carrega a posicao atual das juntas em radianos
		self.posJunta = [0 for x in range(6)]

		#Variavel que carrega a posicao atual das juntas em graus
		self.posJuntaGraus = [0 for x in range(6)]

		#Variavel que carrega o comando de posicao a ser enviado para as juntas
		comandoJunta = [0 for x in range(6)]


		#Criando os publishers e subscribers do ROS
		self.pub = rospy.Publisher('/vrep_ros_interface/ABBIRB/atuarNasJuntas', Accel, queue_size=1)
		rospy.Subscriber('/vrep_ros_interface/ABBIRB/posicaoAtualJuntas',Accel,self.juntaPosCallback)
		#rospy.spin()

#====================================================================================================
		#INICIO DO LOOP INFINITO DE CONTROLE DO ROBO
		#SEU CODIGO VAI AQUI
#====================================================================================================
		while not rospy.is_shutdown():
			
			for x in range(0,6):
				comandoJunta[x]=-2

			print(comandoJunta)

			self.aplicarComandoJuntas(comandoJunta)


#========= FIM DA PARTE QUE VOCE DEVE EDITAR O COMANDO ==============================================
#====================================================================================================
			



			
	#Funcao que eh chamada sempre que uma mensagem nova chega no topico de posicao das juntas
	def juntaPosCallback(self,data):

		self.posJunta[0]=data.linear.x
		self.posJunta[1]=data.linear.y
		self.posJunta[2]=data.linear.z
		self.posJunta[3]=data.angular.x
		self.posJunta[4]=data.angular.y
		self.posJunta[5]=data.angular.z

		#Converte o valor para graus em outra variavel
		i=0
		for x in self.posJunta:
			self.posJuntaGraus[i]=math.degrees(x)

	 	#print(self.posJunta)
	 	#print(self.posJuntaGraus)
		#print("------------")

	#Funcao que publica um valor de posicao para as juntas
	def aplicarComandoJuntas(self,data):

		#Variavel que receber o comando a ser enviado para as juntas
		comandoPub=Accel()

		#Montando a variavel que sera publicada
		comandoPub.linear.x=data[0]
		comandoPub.linear.y=data[1]
		comandoPub.linear.z=data[2]
		comandoPub.angular.x=data[3]
		comandoPub.angular.y=data[4]
		comandoPub.angular.z=data[5]

		#Publicando o comando a ser enviado
		self.pub.publish(comandoPub)		


#Funcao main que chama a classe criada
if __name__ == '__main__':

	#Inicializa o nosso no com o nome
	rospy.init_node('controleAbb', anonymous=True)

	#Instancia a classe e entra em um regime de tratamento de eventuais erros
	try:
		obj_no = ControleRobo()
	except rospy.ROSInterruptException: pass
