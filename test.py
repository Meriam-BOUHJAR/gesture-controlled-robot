import cv2
import mediapipe as mp
import numpy as np
import time
import serial# les bib a utulisé
my_port = "COM3"#com a utulisé (declaration)


ser = serial.Serial(my_port, 9600, timeout=1) #objet qui contient la commande serial 

ser.flush() #debut de communication serie 
if ser.name: #verifier s'il ya communication ou non en mettant le non qu'on va utiliser 
	
	# get the name of the port being used
	port = ser.name
	
	# print a status message
	print(f'Serial comms established on port: {port}') #un message qui indique que la communication est etablie 
# Define the colours 
WHITE_COLOR = (224, 224, 224)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 128, 0)
BLUE_COLOR = (255, 0, 0)

mp_draw = mp.solutions.drawing_utils #lekhtout #iniitialiser les modules de mediapipe pour la detection du main 
draw_specs = mp_draw.DrawingSpec(color=BLUE_COLOR, thickness=2, circle_radius=2) #les pts du main
mp_pose = mp.solutions.hands 
pose = mp_pose.Hands(static_image_mode=False, # taux de precxison par la selection d'un e valeur min de confidance et valeur min de tracking 
               max_num_hands=1, 
               min_detection_confidence=0.85,
               min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0) #lancement du cam internee 
video_width = 640 # les dimension mtaak
video_height = 480
cap.set(3, video_width) 
cap.set(4, video_height) 

start_time = 0 # config de temps de debut

while True: # boucle infini
	success, image = cap.read() #lire l'image
	image = cv2.flip(image, 1)
	image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	results = pose.process(image_rgb) #traitement d'image 
	
	top_left = (25, 130) # definisser ue position rect dans lecran 
	bottom_right = (100, 200)
	cv2.rectangle(image, top_left, bottom_right, RED_COLOR, cv2.FILLED)
	h, w, c = image.shape
	blue_image = np.zeros((h, w, c))
	red_image = np.zeros((h, w, c)) + 255 #black or wihte bachkground 
	
	display_image = image # affichge d'image 

	if results.multi_hand_landmarks: #boucle pour chaque main detectee
		for hand_landmarks in results.multi_hand_landmarks: 
			
			x_list = [] # liste pour stocker les donnee capté
			y_list = []
			fingers_up = [0,0,0,0,0] #liste des doigts pour indiquer les doight elevee 
			mp_draw.draw_landmarks(display_image, hand_landmarks, mp_pose.HAND_CONNECTIONS, # dessigner les ligne sur l'image "
								draw_specs, draw_specs)


		#config des lieu de stock x,y
			for id, lm in enumerate(hand_landmarks.landmark):
				h, w, c = image.shape
				x = int(lm.x * w)
				y = int(lm.y * h)
				x_list.append(x)
				y_list.append(y)
				

			if x_list[4] <= x_list[5]: #verifier la config des doights ***********************************
				fingers_up[0] = 1
			
			if y_list[8] <= y_list[6]:
				fingers_up[1] = 1
			
			if y_list[12] <= y_list[10]:
				fingers_up[2] = 1
				
			if y_list[16]  <= y_list[14]:
				fingers_up[3] = 1
				
			if y_list[20] < y_list[18]:
				fingers_up[4] = 1
				
			
			print(fingers_up) # liste des doight (affichage )
			#envoyer la cammande  serie en fct de  config des doights 
			num_fingers_up = sum(fingers_up)
			if ser.name:
				if fingers_up == [0,0,0,0,0]:
					ser.write(b"1\n")
                #one
				if fingers_up == [0,0,0,0,1]:
					ser.write(b"2\n")
                   
				if fingers_up == [0,0,0,1,0]:ser.write(b"3\n")

				if fingers_up == [0,0,1,0,0]:ser.write(b"4\n")

				if fingers_up == [0,1,0,0,0]: ser.write(b"5\n")

				if fingers_up == [1,0,0,0,0]:ser.write(b"6\n")
                 #two
				if fingers_up == [0,0,0,1,1]:ser.write(b"7\n")
                   
				if fingers_up == [0,0,1,0,1]:ser.write(b"8\n")
				if fingers_up == [0,0,1,1,0]:ser.write(b"9\n")
				if fingers_up == [0,1,0,0,1]:ser.write(b"10\n")
				if fingers_up == [0,1,0,1,0]:ser.write(b"11\n")
				if fingers_up == [0,1,1,0,0]:ser.write(b"12\n")
                   
				if fingers_up == [1,0,0,0,1]:ser.write(b"13\n")
				if fingers_up == [1,0,0,1,0]:ser.write(b"14\n")
				if fingers_up == [1,0,1,0,0]:ser.write(b"15\n")
				if fingers_up == [1,1,0,0,0]:ser.write(b"16\n")
                
				#three    
				
				if fingers_up == [0,0,1,1,1]:ser.write(b"17\n")

				if fingers_up == [0,1,0,1,1]:
					ser.write(b"18\n")
				if fingers_up == [0,1,1,0,1]:
				
					ser.write(b"19\n")
				if fingers_up == [0,1,1,1,0]:ser.write(b"20\n")
				
				if fingers_up == [1,0,0,1,1]:
					ser.write(b"21\n")
                
				if fingers_up == [1,0,1,0,1]:
				
					ser.write(b"22\n")
                        
				if fingers_up == [1,0,1,1,0]:
				
					ser.write(b"23\n")
                    
				if fingers_up == [1,1,0,0,1]:
				
					ser.write(b"24\n")
				if fingers_up == [1,1,0,1,0]:
				
					ser.write(b"25\n")
				if fingers_up == [1,1,1,0,0]:
				
					ser.write(b"26\n")

				#four
				if fingers_up == [0,1,1,1,1]:
				
					ser.write(b"27\n")
                    
				if fingers_up == [1,0,1,1,1]:
				
					ser.write(b"28\n")
				if fingers_up == [1,1,0,1,1]:
				
					ser.write(b"29\n")
				if fingers_up == [1,1,1,0,1]:
				
					ser.write(b"30\n")
				if fingers_up == [1,1,1,1,0]:
				
					ser.write(b"31\n")
                    #five
				if fingers_up == [1,1,1,1,1]:
				
					ser.write(b"32\n")
                    

			cv2.putText(image, str(num_fingers_up), (50, 180), cv2.FONT_HERSHEY_PLAIN, 3,
			WHITE_COLOR, 3)
	current_time = time.time()
	fps = 1/(current_time - start_time)
	start_time = current_time
	#if cv2.waitKey(1) & 0xFF == ord('q'):
		#break
	#afficher carte vd de webcam 
	cv2.imshow('Video', display_image)
		