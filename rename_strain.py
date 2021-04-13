#!/usr/bin/env python

"""
Pipeline: Convert strain names in file names or fasta sequences using a conversion table
Last modified: 04/03/2021

By Veronica Mixao
INSA (Portugal)
vmixao@gmail.com
"""

import argparse
import os

parser = argparse.ArgumentParser(description="Converting strain names in your filenames or fasta sequences (requires a conversion table)")
parser.add_argument("-c", "--conv_table", dest="conv_table", action="store", required=True, help="Conversion table with the structure: original name \"t\" final name")
parser.add_argument("-a", "--action", dest="action", action= "store", default="filename", help="Action to be performed: rename file names [filenames] or rename sequences in fasta file [sequences]. \nDefault = filenames")
parser.add_argument("-i", "--input", dest="input", action= "store", required=True, nargs="+", help="Files to modify")

args = parser.parse_args()


##################
#CONVERSION TABLE#
##################

def conversion_table(conversion_table):
	conv = {}

	conv_table_open = open(conversion_table, "r")
	conv_table = conv_table_open.readlines()

	for line in conv_table:
		l = line.split("\t")
		
		if len(l) != 2:
			print("WARNING!!! Your conversion table does not have the correct number of columns!")
		else:
			conv[l[0]] = l[1].split("\n")[0]
	
	return conv


####################
#RENAMING SEQUENCES#
####################

def	sequences(conv, filenames):
	
	for filename in filenames:
		print("\nWorking on file", filename, "\n")
		
		if filename.endswith(".fa") or filename.endswith("fasta"):
			with open(filename.rsplit(".", 1)[0] + ".renamed." + filename.split(".")[-1], "w+") as out:
				with open(filename, "r") as f_open:
					f = f_open.readlines()
					
					for line in f:
						l = line.split("\n")
						if ">" in line:
							sequence_name = l[0].split(">")[1]
							if sequence_name in conv.keys():
								new_sequence_name = conv[sequence_name]
								print(">" + new_sequence_name, file = out)
								print("Old name: ", sequence_name, " ; New name: ", new_sequence_name)
							else:
								print("Error!! ", sequence_name, " was not found in the conversion table!")
								print(l[0], file = out)
						else:
								print(l[0], file = out)		
		
		else:
			print("ERROR! This option only accepts fasta files!") 


####################
#RENAMING FILENAMES#
####################

def	filenames(conv, filenames):
	
	for filename in filenames:		
		if ".fq" in filename or ".fastq" in filename: #fastqfile
			if "_S" in filename and "_L" in filename: #possible MiSeq
				check_for_L = filename.rsplit("_L", 1)[0]
				if "_S" in check_for_L:
					strain = check_for_L.rsplit("_S", 1)[0]
					plus = "_" + "_".join(filename.split("_")[-2:])
				
				else: #this is not MiSeq
					strain = filename.rsplit("_", 2)[0]
					plus = "_" + "_".join(filename.split("_")[-2:])
			
			else: #this is not MiSeq
				strain = filename.rsplit("_", 2)[0]
				plus = "_" + "_".join(filename.split("_")[-2:])
		
		else: #this is not fastq
			strain = filename.split(".",1)[0]
			plus = "." + filename.split(".", 1)[1]
		
		#converting the name
		if strain in conv.keys():
			new_name = conv[strain] + plus
			if os.path.exists(new_name):
				print("ERROR! THE NEW OS PATH EXISTS!", new_name)
			else:
				print("Old name: ", filename, " ; New name: ", new_name)
				os.rename(filename, new_name)
		else:
			print("WARNING!!! Strain", strain, " was not found in the conversion table!\n")

###########
#EXECUTING#
###########

conversion_dict = conversion_table(args.conv_table)

if args.action == "sequences":
	sequences(conversion_dict,args.input)
else:
	if args.action == "filenames":
		filenames(conversion_dict,args.input)
	else:
		print("This action is not valid!")
