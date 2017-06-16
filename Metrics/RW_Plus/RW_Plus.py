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

# Usage: python RW_Plus.py <Output_File> <IDs_File>

import sys, os, subprocess


def main(argv):

	if(len(argv) < 2):
		print("Error! RW_Plus.py requires 2 arguments: <Output_File> and <IDs_File>")
		sys.exit(2)

	#Get the Results File Name
	try:
		input_file = os.environ.get('TOOLHOME') + "/Results/Step_" + argv[1] + ".txt"
		output_file = os.environ.get('TOOLHOME') + "/Results/" + argv[0]
		
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
	
	#Set Permission
	os.system("chmod 777 calRWplus")
	
	#Display Progress
	print("Extracting RWPlus from \"" + "Step_" + argv[1] + ".txt\"")
	
	#Iterate IDs
	for id_num in ids:
		
		#Get Model File
		model_file = models_folder + "ID_" + id_num + ".pdb"

		#Get RW_Plus
		process = subprocess.Popen(["./calRWplus", model_file], stdout=subprocess.PIPE)
		out, err = process.communicate()

		#Write Results
		out_file.write(id_num + "\t" + out.split()[3] + "\n")
	
	
	#Finally...
	out_file.close()
	
	#Return to Previous Working Directory
	os.chdir(previious_dir)	


#DEFINE MAIN
if __name__ == "__main__":
	try:
		main(argv[1:])
	except NameError:
		main(sys.argv[1:])
