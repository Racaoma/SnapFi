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

#Usage: python DOPE.py <Output_File> <IDs_File>

import sys, os
from modeller import *
from modeller.scripts import complete_pdb


def main(argv):

	#Get Inputs
	if(len(argv) < 2):
		print("Error! DOPE.py requires 2 arguments: <Output_File> , <IDs_File>")
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

	#Setup DOPE Environment
	try:
		#Setup Log
		log.level(output=0, notes=0, warnings=0, errors=1, memory=0)

		#Setup Environment
		env = environ()
		env.libs.topology.read(file='$(LIB)/top_heav.lib')
		env.libs.parameters.read(file='$(LIB)/par.lib')
		
	except:
		print("Could not setup DOPE environment")
		sys.exit(2)

	#Open Output File
	output = open(output_file, "w+")
	output.write(models_folder + "\n")

	#Save Previous Working Directory
	previious_dir = os.getcwd()
		
	#Change Current Working Directory
	os.chdir(os.path.dirname(__file__))

	#Display Progress
	print("Extracting DOPE from \"" + "Step_" + argv[1] + ".txt\"")

	#Iterate IDs
	for id_num in ids:
		
		#Get Model File
		model_file = models_folder + "ID_" + id_num + ".pdb"

		# Read a model previously generated by Modeller's automodel class
		mdl = complete_pdb(env, model_file)

		# Select all atoms in the first chain
		atmsel = selection(mdl.chains[0])
		
		#Calculate Dope Score
		score = atmsel.assess_dope()

		# Write Results
		output.write(id_num + "\t" + str(score) + "\n")
		
		
	# Finally...
	output.close	

	#Return to Previous Working Directory
	os.chdir(previious_dir)	



#DEFINE MAIN
if __name__ == "__main__":
	try:
		main(argv[1:])
	except NameError:
		main(sys.argv[1:])

#The DOPE model score is designed for selecting the best structure from a collection of models built by MODELLER.
# (For example, you could build multiple automodel models by setting automodel.ending_model,
#  and select the model that returns the lowest DOPE score.) The score is unnormalized with respect to the protein size 
#  and has an arbitrary scale, therefore scores from different proteins cannot be compared directly. If you wish to do this, 
#  use model.assess_normalized_dope() instead, which returns a Z-score.
