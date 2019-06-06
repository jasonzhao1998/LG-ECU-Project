import os
import json
import time
import shutil
import datetime
import multiprocessing

'''
TODO:
	Cut 16000 from MY19(20) GB and 1600 from MY20 ERA GB of the unused ECUID files.
	Maintain a record of STID range what's left and what's cut out.
	Cut 3800 MX, 3000 NA, 4600 EU, 4600 CN
	
INFO:
	GEM only has few cert files, so this can be done manually.
	This program only works on the old computer.
	There exists GB STID folders without cert files.
	MY19(20) GB: MX: 4080, NA: 3410, EU: 4726, CN: 4722.
	STID folders on the excel sheets are not moved. 
'''

CERT_FILES_DIR = r'C:\Users\sarah.pentescu\Desktop\copy cert files'#"Z:\\Engineering\\01.OnStar\\11.Flashing\\01.Reflash\\Gen11 Cert Files"
TOTAL_INFO_OUTPUT_DIR = "output/" + "output-" + datetime.datetime.now().strftime("%m-%d-%Y-%H-%M") + '.txt'
DIRS_TO_PROCESS = ('MY19(20) GB', 'MY20 TCP ERA GB') # 'MY21 TCP GB', 


def read_json(directory):
	with open(directory) as file:
		dictionary = json.load(file)
		return dictionary


USED_DICT = read_json("output/used_GB.txt")
UNUSED_DICT = read_json("output/unused_GB.txt")


def walk(input):
	directory = input[0]
	total_STID_folders, total_amount_ecu_files, total_used_ecu_files = 0, 0, 0
	
	print("Processing:", directory)
	
	sub_info_file = open("output/" + input[1] + '-' + str(os.getpid()) + '.txt', 'w')
	cut_file = open(os.path.join('output', 'CUT_' + os.path.basename(directory)[:9] + '.txt'), 'w')
	buffer_file = open(os.path.join('output', 'BUFFER_' + os.path.basename(directory)[:9] + '.txt'), 'w')
	
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
		if os.path.basename(root).isdigit() and len(os.path.basename(root)) == 9:
			total_STID_folders += 1
			
			has_ecu = False
			file_dirs = []
			ecu_dir_name = ''
			for file in files:
				if file[-4:] == '.bin':
					total_amount_ecu_files += 1
					has_ecu = True
					file_dirs.append(os.path.join(root, file))
					ecu_dir_name = file[:-4]
				elif file[-4:] == '.txt':
					file_dirs.append(os.path.join(root, file))
			
			if has_ecu:
				if os.path.basename(root) in USED_DICT or os.path.basename(root) in UNUSED_DICT:
					total_used_ecu_files += 1
				else:  # Unusd ECUID
					if cur_cut < total_cut_needed:
						os.mkdir('output/ECUID/' + ecu_dir_name)
						for dir in file_dirs:
							shutil.move(dir, "output/ECUID/" + ecu_dir_name)
						cut_file.write(ecu_file_dir + '\n')
						cur_cut += 1
					else:
						buffer_file.write(ecu_file_dir + '\n')
						
	sub_info_file.write(str(total_STID_folders) + '\n')
	sub_info_file.write(str(total_amount_ecu_files) + '\n')
	sub_info_file.write(str(total_used_ecu_files) + '\n')
	sub_info_file.close()
	cut_file.close()
	buffer_file.close()
	
	print("Done:", directory)
	

def integrate():
	info_output = open(TOTAL_INFO_OUTPUT_DIR, 'w')
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
	
	
def main():
	# Initialize file and directory
	info_output = open(TOTAL_INFO_OUTPUT_DIR, 'w')
	info_output.close()
	
	# Make ECUID directory if does not exist
	if not os.path.exists('output/ECUID'):
		os.mkdir('output/ECUID')
	
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
		process = multiprocessing.Process(target=walk, args=(dir_list.pop(0),))
		process.start()
		process_list.append(process)
	
	# Wait until all processes finish
	for process in process_list: process.join()
	

if __name__ == "__main__":
    main()
    integrate()
