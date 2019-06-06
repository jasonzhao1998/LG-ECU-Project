import os
import json
import time
import shutil
import datetime
import multiprocessing

'''
TODO:
	ECUID.bin
	
INFO:
	GEM only has few cert files, so this can be done manually.
	This program only works on the old computer.
	There exists GB STID folders without cert files.
	MY19(20) GB: MX: 4080, NA: 3410, EU: 4726, CN: 4722.
	STID folders on the excel sheets are not moved. 
'''

# r'C:\Users\sarah.pentescu\Desktop\copy cert files'
CONSENT = False
CERT_FILES_DIR = "Z:\\Engineering\\01.OnStar\\11.Flashing\\01.Reflash\\Gen11 Cert Files"
TOTAL_INFO_OUTPUT_DIR = "output/" + "output-" + datetime.datetime.now().strftime("%m-%d-%Y-%H-%M") + '.txt'
DIRS_TO_PROCESS = ('MY19(20) GB', 'MY20 TCP ERA GB')# 'MY21 TCP GB')

def consent():
	# Remove previous output files
	if os.path.exists('output'):
		shutil.rmtree('output')
	
	global CONSENT
	val = input("Type 'yes' to move ECUIDs: ")
	if val == 'yes':
		CONSENT = True

def read_json(directory):
	with open(directory) as file:
		dictionary = json.load(file)
		return dictionary


USED_DICT = read_json("reader_output/used_GB.txt")
UNUSED_DICT = read_json("reader_output/unused_GB.txt")


def walk(input, consent):
	directory = input[0]
	total_STID_folders, total_amount_ecu_files, total_used_ecu_files = 0, 0, 0
	ecu_counter = 0
	
	print("Processing:", directory)
	
	sub_info_file = open(os.path.join("output", input[1] + '-' + str(os.getpid()) + '.txt'), 'w')
	cut_file = open(os.path.join('output', 'CUT', 'CUT_' + os.path.basename(directory)[:9] + '.txt'), 'w')
	buffer_file = open(os.path.join('output', 'BUFFER', 'BUFFER_' + os.path.basename(directory)[:9] + '.txt'), 'w')
	log_file = open(os.path.join('output', 'LOG_' + os.path.basename(directory)[:9] + '.txt'), 'w')
	
	# Determining the amounts of cuts needed
	total_cut_needed, cur_cut = 0, 0
	if os.path.basename(directory) == "vehicle_ERA GB":
		total_cut_needed = 1600
	elif os.path.basename(directory)[:2] == 'CH':
		total_cut_needed = 4600
	elif os.path.basename(directory)[:2] == 'MX':
		total_cut_needed = 3800
	elif os.path.basename(directory)[:2] == 'EU':
		total_cut_needed = 4600
	elif os.path.basename(directory)[:2] == 'NA':
		total_cut_needed = 3000
	
	for root, dirs, files in os.walk(directory):
		# If we are in a STID folder
		STID = os.path.basename(root)
		if STID.isdigit() and len(STID) == 9:
			total_STID_folders += 1
			
			has_ecu = False
			file_dirs = []
			ecu_file_dir = ''
			ecu_dir_name = ''
			
			has_txt = False
			for file in files:
				if file[-4:] == '.bin':
					total_amount_ecu_files += 1
					has_ecu = True
					ecu_file_dir = os.path.join(root, file)
					file_dirs.append(os.path.join(root, file))
					ecu_dir_name = file[:-4]
				elif file[-4:] == '.txt':
					has_txt = True
					file_dirs.append(os.path.join(root, file))
			
			if has_ecu:
				if STID in USED_DICT or STID in UNUSED_DICT:
					total_used_ecu_files += 1
					log_file.write(STID + ' -> ' + ecu_dir_name + ' ' + 'USED   ' + os.path.basename(directory) + '\n')
				else:  # Unusd ECUID
					if cur_cut < total_cut_needed:
						if os.path.exists('output/ECUID/' + ecu_dir_name):
							ecu_counter += 1
							ecu_dir_name += str(ecu_counter)
						os.mkdir('output/ECUID/' + ecu_dir_name)
						
						if consent:
							for dir in file_dirs:
								pass# shutil.move(dir, "output/ECUID/" + ecu_dir_name)
						cut_file.write(ecu_file_dir + '\n')
						cur_cut += 1
						log_file.write(STID + ' -> ' + ecu_dir_name + ' ' + 'CUT   ' + os.path.basename(directory) + '\n')
					else:
						buffer_file.write(ecu_file_dir + '\n')
						log_file.write(STID + ' -> ' + ecu_dir_name + ' ' + 'BUFFER   ' + os.path.basename(directory) + '\n')
						
	sub_info_file.write(str(total_STID_folders) + '\n')
	sub_info_file.write(str(total_amount_ecu_files) + '\n')
	sub_info_file.write(str(total_used_ecu_files) + '\n')
	sub_info_file.close()
	cut_file.close()
	buffer_file.close()
	log_file.close()
	
	print("Done:", directory)
	

def integrate():
	info_output = open(TOTAL_INFO_OUTPUT_DIR, 'w')
	log_output = open("output/log_file.txt", 'w')
	
	for file in os.listdir('output'):
		if file[:3] == 'LOG':
			with open('output/' + file, 'r') as subfile:
				log_output.write("".join(subfile.readlines()))
			os.remove('output/' + file)
			
	for directory in DIRS_TO_PROCESS:
		info_output.write(directory + '\n')
		data = [0] * 3  # 3 is the number of parameters
		for file in os.listdir('output'):
			if directory in file:
				with open('output/' + file, 'r') as subfile:
					for idx, info in enumerate([int(line.strip()) for line in subfile.readlines()]):
						data[idx] += info
				os.remove('output/' + file)
		for num in data:
			info_output.write(str(num))
			info_output.write('\n')
		info_output.write('\n')
		
	info_output.close()
	log_output.close()
	
	
def main():
	# Make directories if do not exist
	if not os.path.exists('output'):
		os.mkdir('output')
	if not os.path.exists('output/ECUID'):
		os.mkdir('output/ECUID')
	if not os.path.exists('output/BUFFER'):
		os.mkdir('output/BUFFER')
	if not os.path.exists('output/CUT'):
		os.mkdir('output/CUT')
		
	# Initialize file and directory
	info_output = open(TOTAL_INFO_OUTPUT_DIR, 'w')
	info_output.close()
	
	dir_list = []
	for directory in os.listdir(CERT_FILES_DIR):
		if directory[-2:] == 'GB' and directory in DIRS_TO_PROCESS:
			dir_list += [
				(
					os.path.join(os.path.join(CERT_FILES_DIR, os.path.basename(directory)), i),
					os.path.basename(directory)
				) for i in os.listdir(os.path.join(CERT_FILES_DIR, os.path.basename(directory)))
				if os.path.isdir(os.path.join(os.path.join(CERT_FILES_DIR, os.path.basename(directory)), i))
			]
	
	# Assign tasks to processes
	process_list = []
	while dir_list:
		process = multiprocessing.Process(target=walk, args=(dir_list.pop(0), CONSENT,))
		process.start()
		process_list.append(process)
	
	# Wait until all processes finish
	for process in process_list: process.join()
	

if __name__ == "__main__":
    consent()
    main()
    integrate()
