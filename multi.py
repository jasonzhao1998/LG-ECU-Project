import os
import json
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


def read_json(directory):
	with open(directory) as f:
		d = json.load(f)
		return d


def traverse(directory):
	print(directory)
	"""
	output = open("output/output.txt", 'a')
	total_STID_folders = 0
	total_amount_ecu_files = 0
	total_used_ecu_files = 0
	print("Processing:", f)
	output.write("\nProcessing:" + f + '\n')
	for root, dirs, files in os.walk(os.path.join(CERT_FILES_DIR, f)):
		if os.path.basename(root).isdigit() and len(os.path.basename(root)) == 9:
			has_ecu = False
			for file in files:
				if file[-4:] == '.bin':
					output.write(file + ' ')
					has_ecu = True
					total_amount_ecu_files += 1
			total_STID_folders += 1
			if os.path.basename(root) in used_dict:
				if has_ecu:
					total_used_ecu_files += 1
	output.write("\nTotal number of STID folders: " + str(total_STID_folders) + '\n')
	output.write("Total number of ECU files: " + str(total_amount_ecu_files) + '\n')
	output.write("Total number of used ECU files: " + str(total_used_ecu_files) + '\n')
	output.close()
	total_STID_folders = 0
	total_amount_ecu_files = 0
	total_used_ecu_files = 0
	"""


def main():
	used_dict = read_json("output/used_GB.txt")
	unused_dict = read_json("output/unused_GB.txt")
	
	output = open(OUTPUT_DIR, 'w')
	output.close()
	
	dir_list = []
	for f in os.listdir(CERT_FILES_DIR):
		dir_list += [os.path.join(os.path.join(CERT_FILES_DIR, os.path.basename(f)), i) for i in os.listdir(os.path.join(CERT_FILES_DIR, os.path.basename(f)))]
	
	while dir_list:
		p = Process(target=traverse, args=(dir_list.pop(0),))
		p.start()


if __name__ == "__main__":
    main()
