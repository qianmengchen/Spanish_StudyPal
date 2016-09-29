#!/usr/bin/env python3
import json
import os
import random
import copy

config = {}

with open("config.json", "r") as f:
	config = json.load(f)

def init():
	with open(config["vocabPath"], "r") as f:
		data = json.load(f)
		return data

def update(data):
	print("\033[1;37;40m Before adding another box of cards, I recommand you try \'status\' to know if it is now a good time to go on.")
	print("When finish adding, enter \'q\' to quit.")
	while True:
		es = input("\033[1;32;40m New "+config["learning"]+" word: ").lower()
		if es == 'q':
			break
		data[es] = {'proficiency': 0}
		en = input("\033[1;37;40m The "+config["from"]+" meaning of "+es+": ").lower()
		data[es]["EN"] = en
		if len(data) % config["boxSize"] == 0:
			print("\033[1;31;40m The list size just reached "+len(data)+".")
			while True:
				quit = input("Are you going to continue adding vocabs(y/n)?: ").lower()
				if quit == 'y':
					break
				elif quit == 'n':
					return data
				else:
					print("Bad Input!")
	return data

def filt(data):
	processed = {
		"rare": {},
		"medium_rare": {},
		"medium": {},
		"medium_well": {},
		"well_done": {}
	}
	for key in data.keys():
		if(data[key]["proficiency"] == 0):
			processed["rare"][key] = data[key]
		elif(data[key]["proficiency"] < 0.3):
			processed["medium_rare"][key] = data[key]
		elif(data[key]["proficiency"] < 0.5):
			processed["medium"][key] = data[key]
		elif(data[key]["proficiency"] < 0.7):
			processed["medium_well"][key] = data[key]
		else:
			processed["well_done"][key] = data[key]
	return processed

def randomly_choose(data):
	cards = {}
	rare = medium_rare = medium = medium_well = well_done = 0
	count = 0
	filtered = filt(data)
	while (rare < config["rare"] and len(filtered["rare"]) > 0):
		key = random.sample(filtered["rare"].keys(), 1)[0]
		cards[key] = filtered["rare"][key]
		cards[key]["num"] = 0
		cards[key]["pass"] = False
		del filtered["rare"][key]
		rare += 1
	while (medium_rare < config["medium_rare"] and len(filtered["medium_rare"]) > 0):
		key = random.sample(filtered["medium_rare"].keys(), 1)[0]
		cards[key] = filtered["medium_rare"][key]
		cards[key]["num"] = 0
		cards[key]["pass"] = False
		del filtered["medium_rare"][key]
		medium_rare += 1
	while (medium < config["medium"] and len(filtered["medium"]) > 0):
		key = random.sample(filtered["medium"].keys(), 1)[0]
		cards[key] = filtered["medium"][key]
		cards[key]["num"] = 0
		cards[key]["pass"] = False
		del filtered["medium"][key]
		medium += 1 
	while (medium_well < config["medium_well"] and len(filtered["medium_well"]) > 0):
		key = random.sample(filtered["medium_well"].keys(), 1)[0]
		cards[key] = filtered["medium_well"][key]
		cards[key]["num"] = 0
		cards[key]["pass"] = False
		del filtered["medium_well"][key]
		medium_well += 1
	while (well_done < config["well_done"] and len(filtered["well_done"]) > 0):
		key = random.sample(filtered["well_done"].keys(), 1)[0]
		cards[key] = filtered["well_done"][key]
		cards[key]["num"] = 0
		cards[key]["pass"] = False
		del filtered["well_done"][key]
		well_done += 1
	while (len(cards) < config["boxSize"]):
		key = random.sample(data.keys(), 1)[0]
		if key in cards:
			continue
		cards[key] = data[key]
		cards[key]["num"] = 0
		cards[key]["pass"] = False
	return cards

def check(cards):
	for key in cards.keys():
		if cards[key]["pass"] == False:
			return False
	return True

def review(data):
	cards = randomly_choose(copy.deepcopy(data))
	print("\033[1;37;40m There are "+str(len(cards))+" vocabs in this run")
	while(not check(cards)):
		keys = list(cards.keys())
		random.shuffle(keys)
		for key in keys: 
			if cards[key]["pass"]:
				continue
			cards[key]["num"] += 1
			if(random.random() < .5):
				os.system("say -v "+config["voice"]+" "+key)
				guess = input(key+" in "+config["from"]+": ").lower()
				if guess == cards[key]["EN"]:
					print("Correct!")
					cards[key]["pass"] = True
				else:
					print("No! The answer is "+cards[key]["EN"])
			else:
				guess = input(data[key]["EN"]+" en español: ").lower()
				os.system("say -v "+config["voice"]+" "+key)
				if guess == key:
					print("Correct!")
					cards[key]["pass"] = True
				else:
					print("¡No!, la respuesta correcta es "+key)
	for key in data.keys():
		if key not in cards:
			continue
		if (data[key]["proficiency"] == 0):
			data[key]["proficiency"] = 1./cards[key]["num"]
		else:
			data[key]["proficiency"] = (data[key]["proficiency"] + 1./cards[key]["num"])/2.
	return data

def print_data(data):
	print(data)

def check_proficiency_rate(data):
	cards = filt(copy.deepcopy(data))
	well_done = len(cards["well_done"])/float(len(data))
	rare = len(cards["rare"])/float(len(data))
	medium_rare = len(cards["medium_rare"])/float(len(data))
	medium = len(cards["medium"])/float(len(data))
	medium_well = len(cards["medium_well"])/float(len(data))
	print("\033[1;37;40m Below is your current level of proficiency:")
	print("rare: "+str(rare))
	print("medium rare: "+str(medium_rare))
	print("medium: "+str(medium))
	print("medium_well: "+str(medium_well))
	print("well_done: "+str(well_done))

def main():
	data = init()
	print("\033[0m Actions:\n \'u\' or \'update\'\n \'r\' or \'review\'\n \'num\' to check the size of your vocab pool\n \'stats\' to know your current learning situation.")
	print(" \'q\' to quit this program")
	choice = input("Please enter your action: ").lower()
	if choice == 'u' or choice == 'update':
		data = update(data)
	elif choice == 'r' or choice == 'review':
		data = review(data)
	elif choice == 'num':
		print("\033[1;37;40m You currently have "+str(len(data))+" words in your vocabulary list.")
	elif choice == 'stats':
		check_proficiency_rate(data)
	elif choice == 'q':
		return False
	else:
		print("\033[1;37;40m Bad Input")

	with open(config["vocabPath"], "w") as f:
		json.dump(data, f, sort_keys=True, indent=4)
	return True

print("Welcome to flashcards by Qianmeng Chen.")
while main():
	pass
print("\033[1;37;40m Goodbye!")