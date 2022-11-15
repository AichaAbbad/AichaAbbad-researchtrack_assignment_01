from __future__ import print_function

import time
from sr.robot import *


""" float: Threshold for the control of the linear distance"""
a_th = 2.0

""" float: Threshold for the control of the orientation"""
d_th = 0.65

""" Initialze variables """

rss = 1
i = 0

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

""" Inialize arrays """

import array

mark = array.array('d',[0,0,0,0,0,0,0,0,0,0,0,0])
gs = array.array('d',[0,0,0,0,0,0])
rs  = array.array('d',[0,0,0,0,0,0])

R = Robot()

""" Drive function """

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
""" Turn function """

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
""" Find a silver token function """

def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
   	
""" Find a golden token function """

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y
   	
""" Get the box Id function """
   	
def get_id():
	marker = R.see()
	for m in marker:
		if m.info.code:
			Id = m.info.code	
	return Id
	
""" The main code """

while 1:
	if silver == True :
		dist, rot_y = find_silver_token() # Look for a silver token
		print("There you go !")
		drive(20,0.5)
	else :
		dist, rot_y = find_golden_token() # Look for a golden token
	if (dist == -1) :
		print("no token seen !")
		turn(5,1)
	elif dist < d_th :
		print("found the token !")
		if R.grab():
			print("got you !")
			gs[i] = get_id() # Get the Id of the silver token and store it on g[i]
			print(gs)
			if i == 0 :
				turn(17,3) # If i = 0 (First box) turn with speed 17 for 3 seconds
			else :
				turn(10,1) # for i > 0 turn with speed 10 for 1 second
			silver = not silver # set silver to false
			while silver == False : # while silver is false
				dist,rot_y = find_golden_token() # Look for a golden token
				if dist == -1 :
					print("no token seen !!")
					turn(-2,0.5)
				elif rss == rs[i-1]: # if current golden Id is equal to previous Id 
					rss = get_id()
					print("you have been here before !") 
					turn(-2,0.5)
				else: # If rss != r[i-1]
					if -a_th<= rot_y <= a_th: 
		 				print("drive")
		 				drive(15,0.5)
		 				if dist < d_th :
			 				print("release")
			 				R.release()
							rss = get_id()
							rs[i] = rss
							i = i + 1 # increment i 
							print(rs)
			 				drive (-30,2)
			 				turn (-18,2)
			 				silver = not silver
			 				if i == 6 : # The robot has placed all the tokens
			 					print("You are done !")
								exit() # exit the code
			 				break 
	 				elif rot_y < -a_th: 
	 					turn(-2, 0.5)
	 					print("left") # turn left
					elif rot_y > a_th:
						turn(+2, 0.5)
						print("right") # turn right
					else :
						print("I am close !")
		else :
			print("still far")
