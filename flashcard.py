#!/usr/bin/env python3
import json
import os
import random
import copy

datafile = "vocabulario.json"

def init():
	with open(datafile, "r") as f:
		data = json.load(f)
		return data

def update(data):
	while True:
		es = input("New spanish word: ").lower()
		if es == 'q':
			break
		data[es] = {'proficiency': 0}
		en = input("The English meaning of "+es+": ").lower()
		data[es]["EN"] = en
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
	while (rare < 40 and len(filtered["rare"]) > 0):
		key = random.sample(filtered["rare"].keys(), 1)[0]
		cards[key] = filtered["rare"][key]
		cards[key]["num"] = 0
		cards[key]["pass"] = False
		del filtered["rare"][key]
	while (rare < 30 and len(filtered["medium_rare"]) > 0):
		key = random.sample(filtered["medium_rare"].keys(), 1)[0]
		cards[key] = filtered["medium_rare"][key]
		cards[key]["num"] = 0
		cards[key]["pass"] = False
		del filtered["medium_rare"][key]
	while (rare < 15 and len(filtered["medium"]) > 0):
		key = random.sample(filtered["medium"].keys(), 1)[0]
		cards[key] = filtered["medium"][key]
		cards[key]["num"] = 0
		cards[key]["pass"] = False
		del filtered["medium"][key]
	while (rare < 10 and len(filtered["medium_well"]) > 0):
		key = random.sample(filtered["medium_well"].keys(), 1)[0]
		cards[key] = filtered["medium_well"][key]
		cards[key]["num"] = 0
		cards[key]["pass"] = False
		del filtered["medium_well"][key]
	while (rare < 5 and len(filtered["well_done"]) > 0):
		key = random.sample(filtered["well_done"].keys(), 1)[0]
		cards[key] = filtered["well_done"][key]
		cards[key]["num"] = 0
		cards[key]["pass"] = False
		del filtered["well_done"][key]
	return cards

def check(cards):
	for key in cards.keys():
		if cards[key]["pass"] == False:
			return False
	return True

def review(data):
	cards = randomly_choose(copy.deepcopy(data))
	while(not check(cards)):
		items = cards.items()
		random.shuffle(items)
		for key, value in items: 
			if value["pass"]:
				continue
			cards[key]["num"] += 1
			if(random.random() < .5):
				os.system("say -v Monica "+key)
				guess = input(key+" in English: ")
				if guess == value["EN"]:
					print("Correct!")
					cards[key]["pass"] = True
				else:
					print("No! The answer is "+value["EN"])
			else:
				guess = input(value["EN"]+" en español: ")
				os.system("say -v Monica "+key)
				if guess == key:
					print("Correct!")
					cards[key]["pass"] = True
				else:
					print("¡No!, la respuesta correcta es "+key)
	for key in data.keys():
		if (data[key]["proficiency"] == 0):
			data[key]["proficiency"] = 1./cards[key]["num"]
		else:
			data[key]["proficiency"] = (data[key]["proficiency"] + 1./cards[key]["num"])/2.
	return data

def print_data(data):
	print(data)

def main():
	data = init()
	choice = input("Please enter your action (update or review): ").lower()
	if choice == 'u' or choice == 'update':
		data = update(data)
	elif choice == 'r' or choice == 'review':
		data = review(data)
	else:
		print("Bad Input")

	with open(datafile, "w") as f:
		json.dump(data, f)
	print("Goodbye!")

main()