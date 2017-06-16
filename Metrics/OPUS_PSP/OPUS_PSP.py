#   This file is part of SnapFi.
#   Copyright 2017 Rafael Cauduro Oliveira Macedo
#
#   SnapFi is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   SnapFi is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with SnapFi. If not, see <http://www.gnu.org/licenses/>.

# Usage: python OPUS_PSP.py <Output_File> <IDs_File>

import sys, os

def main(argv):
    
	#Get Inputs
	if(len(argv) < 2):
		print("Error! OPUS_PSP.py requires 2 argument: <Output_File> and <IDs_File>")
		sys.exit(2)

	#Get the Results File Name
	try:
		input_file = os.environ.get('TOOLHOME') + "/Results/Step_" + argv[1] + ".txt"
		output_file = os.environ.get('TOOLHOME') + "/Results/" + argv[0]
		os.environ["OPUS_PSPHOME"] = "" #Change this line to your GOAP instalation folder
		
	except TypeError:
		print("TOOLHOME Environment not Set. Are you running Main.py?")
		sys.exit(2)

	#Get IDs & Models Folder Locations
	try:
		ids = open(input_file).read().split()
		models_folder = ids[0]
		ids = ids[1:]
		
	except:
		print("Specified <IDs_File> could not be located or is invalid")
		sys.exit(2)

	#Delete Previous Runs & Write Header
	out_file = open(output_file, 'w+')
	out_file.write(models_folder + "\n")

	#Save Previous Working Directory
	previious_dir = os.getcwd()
		
	#Change Current Working Directory
	os.chdir(os.path.dirname(__file__))

	#First create the config.psp file (needed for the program to work)
	try:
		temp = open('config.psp', 'w')
		temp.write(os.environ.get('OPUS_PSPHOME') + "/energy_dir/")
		temp.close()
		
	except:
		print("OPUS_PSPHOME Environment not Set. Please set the OPUS_PSPHOME environment before using this script")
		sys.exit(2)

	#File containing the list of pdb's to be calculated
	pdb_list = ''

	#Iterate IDs
	for id_num in ids:

		#Get Model File
		model_file = models_folder + "ID_" + id_num + ".pdb"

		#Add the name to the list in OPUS_PSP
		pdb_list += os.path.basename(model_file) + "\n"
		
		#Remove the Hydrogens of the pdb (optional)
		os.system('phenix.trim_pdb ' + "\"" + model_file + "\"")

		#Move the pdb file without the H's to the working directory (where this python script is located) and change the name
		os.system('mv ' + os.path.splitext(os.path.basename(model_file))[0] + '_no_h.pdb ' + os.path.basename(model_file))


	# Create the input file for OPUS_PSP
	psp_in = open("OPUS_PSP.inp", 'w+')
	psp_in.write(pdb_list)
	psp_in.close()

	#Display Progress
	print("Extracting OPUS_PSP from \"" + "Step_" + argv[1] + ".txt\"")

	# Run OPUS_PSP
	os.system("opus_psp < OPUS_PSP.inp | grep 'ID_' | awk '{print $2}' >> temp.txt")
	
	#Get Results from Temporary File
	pos = 0
	temp_file = open("temp.txt")
	for line in temp_file.readlines():
		out_file.write(ids[pos] + "\t" + line)
		pos += 1
	temp_file.close()

	#Finally...
	out_file.close

	# Delete Temporary Files
	os.remove("OPUS_PSP.inp")
	os.remove("temp.txt")
	os.remove("config.psp")

	for id_num in ids:
		os.remove("ID_" + id_num + ".pdb")	
	
	#Return to Previous Working Directory
	os.chdir(previious_dir)	


#DEFINE MAIN
if __name__ == "__main__":
	try:
		main(argv[1:])
	except NameError:
		main(sys.argv[1:])
















