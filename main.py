import os
import random
from colorama import *

class Player:
	def __init__(self, role, side, status, saved):
		self.role = role
		self.side = side
		self.status = status
		self.saved = saved

#for i in players:
#	print(i.role + ": " + i.status)

def reset():
	global players
	global nights
	global detmafia
	global verbose
	players = []
	nights = 1
	detmafia = "N/A"
	verbose = False

	players.append(Player("Godfather", "Mafia", "Alive", False))
	players.append(Player("Mafia", "Mafia", "Alive", False))
	players.append(Player("Detective", "Villager", "Alive", False))
	players.append(Player("Doctor", "Villager", "Alive", False))

	for i in range(15):
		players.append(Player(f'Villager {i + 1}', "Villager", "Alive", False))

def status():
	status = {}

	global nights
	vilcount = 0
	mafcount = 0
	for i in players:
		if i.status == "Alive" or i.status == "Saved":
			if i.side == "Mafia":
				mafcount += 1
			else:
				vilcount += 1
	statustext = f"""Nights Passed: {nights}
Villagers Alive: {vilcount}
Mafias Alive: {mafcount}
"""
	status["text"] = statustext
	status["vilcount"] = vilcount
	status["mafcount"] = mafcount
	return status

def wincheck():
	global nights
	current = status()
	mafcount = current["mafcount"]
	vilcount = current["vilcount"]
	if mafcount >= vilcount:
		print("Mafias Win!\n")
		print(current["text"])
		os._exit(1)
	elif mafcount == 0:
		print("Villagers Win!\n")
		print(current["text"])
		os._exit(1)
	else:
		print("No Winners Yet!\n")
		print(current["text"])
			
	

def newnight():
	global nights
	global detmafia
	print(f'Night {nights}')
	nights += 1
	
	# Mafia
	found = False
	for i in range(2,18):
		if players[i].saved:
			victim = players[i]
			found = True
			break
	
	if found == False:
		victim = players[random.randint(2,18)]
		while victim.status == "Dead":
			victim = players[random.randint(2,18)]
	print(f'Victim: {victim.role}')

	# Doctor
	doctor = players[3]
	if doctor.status != "Dead":
		print("Doctor Alive")
		saved = players[random.randint(0,18)]
		while saved.status != "Alive" and not saved.saved:
			saved = players[random.randint(0,18)]
		print(f'Saving: {saved.role}')
		if victim.role == saved.role:
			victim.saved = True
			print("Victim Was Saved!")
		else:
			victim.status = "Dead"
			print(f'Killed {victim.role}')
	else:
		print("Doctor Dead")
	print("\n")

	# Detective
	det = players[2]
	if det.status != "Dead":
		print("Detective Alive")
		checked = players[random.randint(0,18)]
		while checked.status == "Dead":
			checked = players[random.randint(0,18)]
		if checked.side == "Mafia":
			detmafia = checked
			print(f'Mafia Found: {checked.role}')
		else:
			print("Mafia Not Found")
			detmafia = "N/A"
	else:
		print("Detective Dead")
	print("\n\n\n")
		
	

def newday():
	global nights
	global detmafia
	global checked
	
	print(f'Day {nights}')

	# Lynch Time!
	if detmafia != "N/A":
		print(f'Lynched: {detmafia.role} From Det Info')
		detmafia.status = "Dead"
	else:
		lynch = players[random.randint(0,18)]
		while lynch.status == "Dead":
			lynch = players[random.randint(0,18)]
		lynch.status = "Dead"
		print(f'Lynched: {lynch.role} From Random Lynch')
	print("\n\n\n")

	
reset()
for i in range(15):
	newnight()
	wincheck()
	newday()
	wincheck()
	if verbose:
		input("Press Enter to Progress")
os._exit(1)