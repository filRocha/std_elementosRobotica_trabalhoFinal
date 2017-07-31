#!/usr/bin/env python
import rospy
import roslib
import math
#import sys

#================ TRABALHO FINAL DE ELEMENTOS DE ROBOTICA ========================================

# Os limites das juntas do robo sao (em graus e radianos em parenteses):
	# theta_1 = -180 (-3.14)	a 	180 (3.14)
	# theta_2 = -90	(-1.57)		a 	150 (2.62)
	# theta_3 = -180 (-3.14) 	a 	75 (1.30)
	# theta_4 = -400 (-6.98)	a 	400 (6.98)
	# theta_5 = -125 (-2.18)	a 	120 (2.1)
	# theta_6 = -400 (-6.98)	a 	400 (6.98)


#=================================================================================================


#imports de mensagens
from geometry_msgs.msg import Accel


#Cria a classe do noo para publicar no motor
class ControleRobo():

	#Metodo criador da classe
	def __init__(self):

		#Enviando uma informacao para o usuario
		rospy.loginfo("Node de Controle do Robo ABB IRB inicializado")

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
				comandoJunta[x]=0.5

			print(comandoJunta)
			
			#vEtor onde estao as posicoes das juntas
			#self.posJuntaGraus[]


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


	# theta_1 = -180 (-3.14)	a 	180 (3.14)
	# theta_2 = -90	(-1.57)		a 	150 (2.62)
	# theta_3 = -180 (-3.14) 	a 	75 (1.30)
	# theta_4 = -400 (-6.98)	a 	400 (6.98)
	# theta_5 = -125 (-2.18)	a 	120 (2.1)
	# theta_6 = -400 (-6.98)	a 	400 (6.98)
	
		#Montando a variavel que sera publicada

		# Theta 1
		if data[0] < -3.14:
			comandoPub.linear.x = -3.14
		elif data[0] > 3.14:
			comandoPub.linear.x = 3.14
		else:
			comandoPub.linear.x = data[0]

		# Theta 2
		if data[1] < -1.57:
			comandoPub.linear.y = -1.57
		elif data[1] > 2.62:
			comandoPub.linear.y = 2.62
		else:
			comandoPub.linear.y = data[1]

		# Theta 3
		if data[2] < -3.14:
			comandoPub.linear.z = -3.14
		elif data[2] > 1.30:
			comandoPub.linear.z = 1.30
		else: 
			comandoPub.linear.z = data[2]

		# Theta 4
		if data[3] < -6.98:
			comandoPub.angular.x = -6.98
		elif data[3] > 6.98:
			comandoPub.angular.x = 6.98
		else: 
			comandoPub.angular.x = data[3]

		# Theta 5
		if data[4] < -2.18:
			comandoPub.angular.y = -2.18
		elif data[4] > 2.1:
			comandoPub.angular.y = 2.1
		else: 
			comandoPub.angular.y = data[4]

		# Theta 6
		if data[5] < -6.98:
			comandoPub.angular.z = -6.98
		elif data[5] > 6.98:
			comandoPub.angular.z = 6.98
		else: 
			comandoPub.angular.z = data[5]

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
