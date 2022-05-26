import os
import random
from colorama import *


def main():
	global finished
	games = []
	vilwins = 0
	mafwins = 0
	nowins = 0
	final = ""
	
	for i in range(100):
		reset()
		gameresult = game()
		games.append(gameresult)

	for i in range(len(games)):
		if games[i].winner == "Villagers":
			vilwins += 1
		elif games[i].winner == "Mafias":
			mafwins += 1
		elif games[i].winner == "None":
			nowins += 1
		else:
			print("Undetermined Winner: " + games[i].winner)
			os._exit(1)
		gamestr = Fore.GREEN + f"""Game {i + 1}: 
Winner: {games[i].winner}
Nights: {games[i].nights}
Villagers Alive: {games[i].vilalive}
Mafias Alive: {games[i].mafalive}

"""
		final += (gamestr)
		
	print(final)
	print(Fore.YELLOW + "Village Wins: " + str(vilwins))
	print(Fore.YELLOW + "Mafia Wins: " + str(mafwins))
	print(Fore.YELLOW + "No Wins: " + str(nowins))
	os._exit(1)

class Game:
	def __init__(self, winner, nights, vilalive, mafalive):
		self.winner = winner
		self.nights = nights
		self.vilalive = vilalive
		self.mafalive = mafalive

class Player:
	def __init__(self, role, side, status, saved):
		self.role = role
		self.side = side
		self.status = status
		self.saved = saved

#for i in players:
#	print(i.role + ": " + i.status)

def game():
	for i in range(15):
		finished = False
		if finished == False:
			newnight()
			if wincheck():
				return wincheck()
			newday()
			if wincheck():
				return wincheck()
			if verbose:
				input("Press Enter to Progress")
				os.system('clear')
	current = status()
	return Game("None", nights, current["vilcount"], current["mafcount"])

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
		if i.status != "Dead":
			if i.side == "Mafia":
				mafcount += 1
			else:
				vilcount += 1
	statustext = Fore.WHITE + f"""Nights Passed: {nights}
Villagers Alive: {vilcount}
Mafias Alive: {mafcount}
"""
	status["text"] = statustext
	status["vilcount"] = vilcount
	status["mafcount"] = mafcount
	return status

def wincheck():
	global nights
	global finished
	current = status()
	if current["mafcount"] >= current["vilcount"]:
		print(Fore.RED + "Mafias Win!\n")
		print(current["text"])
		finished = True
		return Game("Mafias", nights, current["vilcount"], current["mafcount"])
	elif current["mafcount"] == 0:
		print(Fore.GREEN + "Villagers Win!\n")
		print(current["text"])
		finished = True
		return Game("Villagers", nights, current["vilcount"], current["mafcount"])
	else:
		print(Fore.YELLOW + "No Winners Yet!\n")
		return False
		#print(current["text"])
			
	

def newnight():
	global nights
	global detmafia
	print(Fore.WHITE + f'Night {nights}')
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
	print(Fore.RED + f'Victim: {victim.role}\n')

	# Doctor
	doctor = players[3]
	if doctor.status != "Dead":
		print(Fore.GREEN + "Doctor Alive")
		saved = players[random.randint(0,18)]
		while saved.status != "Alive" and not saved.saved:
			saved = players[random.randint(0,18)]
		print(Fore.GREEN + f'Saving: {saved.role}')
		if victim.role == saved.role:
			victim.saved = True
			print(Fore.GREEN + "Victim Was Saved!")
		else:
			victim.status = "Dead"
			print(Fore.RED + f'Killed {victim.role}')
	else:
		print(Fore.RED + "Doctor Dead")
	print("\n")

	# Detective
	det = players[2]
	if det.status != "Dead":
		print(Fore.GREEN + "Detective Alive")
		checked = players[random.randint(0,18)]
		while checked.status == "Dead":
			checked = players[random.randint(0,18)]
		if checked.side == "Mafia":
			detmafia = checked
			print(Fore.GREEN + f'Mafia Found: {checked.role}')
		else:
			print(Fore.RED + "Mafia Not Found")
			detmafia = "N/A"
	else:
		print(Fore.RED + "Detective Dead")
	print("\n\n\n")
		
	

def newday():
	global nights
	global detmafia
	global checked
	
	print(Fore.WHITE + f'Day {nights}')

	# Lynch Time!
	if detmafia != "N/A":
		print(Fore.GREEN + f'Lynched: {detmafia.role} From Det Info')
		detmafia.status = "Dead"
	else:
		lynch = players[random.randint(0,18)]
		while lynch.status == "Dead" or lynch.saved == True:
			lynch = players[random.randint(0,18)]
		lynch.status = "Dead"
		if lynch.role == "Godfather" or lynch.role == "Mafia":
			print(Fore.GREEN)
		else:
			print(Fore.RED)
		print(f'Lynched: {lynch.role} From Random Lynch')
	print("\n\n\n\n")

if __name__ == "__main__":
    main()