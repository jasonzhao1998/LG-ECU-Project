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
	
INFO:
	GEM only has few cert files, so this can be done manually.
	This program only works on the old computer.
	There exists GB STID folders without cert files.
	MY19(20) GB: MX: 4213, NA: 3416, EU: 4747, CN: 4733.
	STID folders on the excel sheets are not moved. 
'''

CERT_FILES_DIR = "Z:\\Engineering\\01.OnStar\\11.Flashing\\01.Reflash\\Gen11 Cert Files"
OUTPUT_DIR = "output/" + "output-" + datetime.datetime.now().strftime("%m-%d-%Y-%H-%M") + '.txt'
TRAVERSE_FOLDERS = ('MY19(20) GB', 'MY20 TCP ERA GB') # 'MY21 TCP GB', 


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
	output_path = "output/" + input[1] + '-' + str(os.getpid()) + '.txt'
	print("Processing:", directory)
	f = open(output_path, 'w')
	f2 = open(os.path.join('output', os.path.basename(directory) + '.txt'), 'w')
	
	total_cut_needed = 0
	cur_cut = 0
	if os.path.basename(directory) == "vehicle_ERA GB":
		total_cut_needed = 1600
	else:
		total_cut_needed = 10000
	
	for root, dirs, files in os.walk(directory):
		if os.path.basename(root).isdigit() and len(os.path.basename(root)) == 9:
			has_ecu = False
			ecu_file_dir = ''
			for file in files:
				if file[-4:] == '.bin':
					has_ecu = True
					total_amount_ecu_files += 1
					ecu_file_dir = os.path.join(root, file)
			total_STID_folders += 1
			if has_ecu:
				if os.path.basename(root) in USED_DICT:
					total_used_ecu_files += 1
				else if os.path.basename(root) not in UNUSED_DICT:
					if cur_cut <= total_cut_needed:
						# shutil.move(ecu_file_dir, r"C:\Users\sarah.pentescu\Desktop")
						f2.write(ecu_file_dir + '\n')
						cur_cut += 1
	
	f.write(str(total_STID_folders) + '\n')
	f.write(str(total_amount_ecu_files) + '\n')
	f.write(str(total_used_ecu_files) + '\n')
	f.close()
	f2.close()
	print("Done:", directory)
	

def integrate():
	print(OUTPUT_DIR)
	output = open(OUTPUT_DIR, 'w')
	for i in TRAVERSE_FOLDERS:
		output.write(i + '\n')
		data = [0] * 3
		for f in os.listdir('output'):
			if i in f:
				print(f)
				with open('output/' + f, 'r') as f2:
					for k, l in enumerate([int(j.strip()) for j in f2.readlines()]):
						data[k] += l
				os.remove('output/' + f)
		for i in data:
			output.write(str(i))
			output.write('\n')
		output.write('\n')
	output.close()
	
	
def main():
	output = open(OUTPUT_DIR, 'w')
	output.close()
	
	dir_list = []
	for f in os.listdir(CERT_FILES_DIR):
		if f[-2:] == 'GB' and f in TRAVERSE_FOLDERS:
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
	
	for p in p_list: p.join()
	

if __name__ == "__main__":
    main()
    integrate()
