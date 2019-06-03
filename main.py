import os
import json


CERT_FILES_DIR = "."


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

	read_json('output/used_GB.txt')
	for f in os.listdir(CERT_FILES_DIR):
		if file[-2:] == 'GB':
			for root, dirs, files in os.walk(f):
				for file in files:
					if file[-4:] == '.bin':
						print(file)
						total_amount_ecu_files += 1

				if root[2:].isdigit() and len(root[2:]) == 9:
					total_STID_folders += 1
					if root[2:] in used_dict:
						total_used_ecu_files += 1

				for d in dirs:
					pass

	print("Total number of STID folders:", total_STID_folders)
	print("Total number of ECU files:", total_amount_ecu_files)
	print("Total number of used ECU files:", total_used_ecu_files)

if __name__ == "__main__":
    main()
