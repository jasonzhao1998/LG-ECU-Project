import os
import json
import time
import datetime
import multiprocessing

'''
TODO:
	Check if there exists GB STID folders without cert files.

INFO:
	GEM only has few cert files, so this can be done manually.
	This program only works on the old computer.
'''

CERT_FILES_DIR = "Z:\\Engineering\\01.OnStar\\11.Flashing\\01.Reflash\\Gen11 Cert Files"
OUTPUT_DIR = "output/" + "output-" + datetime.datetime.now().strftime("%m-%d-%Y-%H:%M") + '.txt'
GLOBAL_DICT = {
	'MY21 TCP GB': [
		[], [], []
	],
	'MY19(20) GB': [
		[], [], []
	],
	'MY20 TCP ERA GB': [
		[], [], []
	]
}

def read_json(directory):
	with open(directory) as f:
		d = json.load(f)
		return d


USED_DICT = read_json("output/used_GB.txt")
UNUSED_DICT = read_json("output/unused_GB.txt")

def traverse(input):
	directory = input[0]
	total_STID_folders = 0
	total_amount_ecu_files = 0
	total_used_ecu_files = 0
	print("Processing:", directory)
	
	for root, dirs, files in os.walk(directory):
		if os.path.basename(root).isdigit() and len(os.path.basename(root)) == 9:
			has_ecu = False
			for file in files:
				if file[-4:] == '.bin':
					has_ecu = True
					total_amount_ecu_files += 1
			total_STID_folders += 1
			if os.path.basename(root) in USED_DICT:
				if has_ecu:
					total_used_ecu_files += 1
	
	GLOBAL_DICT[input[1]][0].append(total_STID_folders)  # Total number of STID folders
	GLOBAL_DICT[input[1]][1].append(total_amount_ecu_files)  # Total number of ECU files
	GLOBAL_DICT[input[1]][2].append(total_used_ecu_files)  # Total number of used ECU files
	print("Done:", directory)
	

def main():
	output = open(OUTPUT_DIR, 'w')
	output.close()
	
	dir_list = []
	for f in os.listdir(CERT_FILES_DIR):
		if f[-2:] == 'GB':
			dir_list += [
				(
					os.path.join(os.path.join(CERT_FILES_DIR, os.path.basename(f)), i),
					os.path.basename(f)
				) for i in os.listdir(os.path.join(CERT_FILES_DIR, os.path.basename(f)))
				if os.path.isdir(os.path.join(os.path.join(CERT_FILES_DIR, os.path.basename(f)), i))
			]
	
	p_list = []
	while dir_list:
		p = multiprocessing.Process(target=traverse, args=(dir_list.pop(0),))
		p.start()
		p_list.append(p)
	
	while p_list:
		time.sleep(1)
		if not p_list[0].is_alive():
			p_list.pop(0)
	print(GLOBAL_DICT)


if __name__ == "__main__":
    main()
