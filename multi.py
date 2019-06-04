import os
import json
import multiprocessing

'''
TODO:
	Check if there exists GB STID folders without cert files.

INFO:
	GEM only has few cert files, so this can be done manually.
	This program only works on the old computer.
'''

CERT_FILES_DIR = "Z:\\Engineering\\01.OnStar\\11.Flashing\\01.Reflash\\Gen11 Cert Files"


def read_json(directory):
	with open(directory) as f:
		d = json.load(f)
		return d


def main():
	used_dict = read_json("output/used_GB.txt")
	unused_dict = read_json("output/unused_GB.txt")

	total_STID_folders = 0
	total_amount_ecu_files = 0
	total_used_ecu_files = 0

	output = open("output/output.txt", 'w')
	output.close()
	
	for f in os.listdir(CERT_FILES_DIR):
		if f[-2:] == 'GB':  # File directory has to end with GB
			output = open("output/output.txt", 'a')
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
		

if __name__ == "__main__":
    main()
