import os
import json

'''
TODO:

	Check if other directories like GEM have cert files.
	Check if there exists GB STID folders without cert files.

'''

CERT_FILES_DIR = "C:\\Users\\lgeuser\\Desktop"


def read_json(directory):
	with open(directory) as f:
		d = json.load(f)
		return d


def test1():
	used_dict = read_json("output/used_GB.txt")
	unused_dict = read_json("output/unused_GB.txt")

	total_STID_folders = 0
	total_amount_ecu_files = 0
	total_used_ecu_files = 0

	for f in os.listdir(CERT_FILES_DIR):
		if f[-2:] != 'GB':  # File directory has to end with GB
			print(f)
			for root, dirs, files in os.walk(os.path.join(CERT_FILES_DIR, f)):
				if os.path.basename(root).isdigit() and len(os.path.basename(root)) == 9:
					has_ecu = False
					for file in files:
						if file[-4:] == '.bin':
							print(file)
							has_ecu = True
							total_amount_ecu_files += 1
					total_STID_folders += 1
					if os.path.basename(root) in used_dict:
						if has_ecu:
							total_used_ecu_files += 1

	print("Total number of STID folders:", total_STID_folders)
	print("Total number of ECU files:", total_amount_ecu_files)
	print("Total number of used ECU files:", total_used_ecu_files)


def main():
	print(os.listdir("10.195.147.30"))
	used_dict = read_json("output/used_GB.txt")
	unused_dict = read_json("output/unused_GB.txt")

	total_STID_folders = 0
	total_amount_ecu_files = 0
	total_used_ecu_files = 0

	for f in os.listdir(CERT_FILES_DIR):
		if f[-2:] == 'GB':  # File directory has to end with GB
			print(f)
			for root, dirs, files in os.walk(os.path.join(CERT_FILES_DIR, f)):
				if os.path.basename(root).isdigit() and len(os.path.basename(root)) == 9:
					has_ecu = False
					for file in files:
						if file[-4:] == '.bin':
							print(file)
							has_ecu = True
							total_amount_ecu_files += 1
					total_STID_folders += 1
					if os.path.basename(root) in used_dict:
						if has_ecu:
							total_used_ecu_files += 1

	print("Total number of STID folders:", total_STID_folders)
	print("Total number of ECU files:", total_amount_ecu_files)
	print("Total number of used ECU files:", total_used_ecu_files)

if __name__ == "__main__":
    main()
