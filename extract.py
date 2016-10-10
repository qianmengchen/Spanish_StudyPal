#!/usr/bin/env python3
import openpyxl
import json

sheet = openpyxl.load_workbook("西班牙语不规则变位表.xlsx").get_sheet_by_name('Sheet1')

collection = {}

i = 2
while(i < 122):
	key = sheet['A'+str(i)].value
	collection[key] = {}
	for j in range(ord('B'), ord('B')+6):
		for k in range(0, 6):
			collection[key][chr(j)+str(k)] = sheet[chr(j)+str(i+k)].value
			if collection[key][chr(j)+str(k)] == '/':
				collection[key][chr(j)+str(k)] = None
			#print(chr(j)+str(k), sheet[chr(j)+str(i+k)].value)
	#print(collection)
	i += 6

with open("conjugation.json", "w") as f:
	print(collection)
	json.dump(collection, f, sort_keys=True, indent=4)