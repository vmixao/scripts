#/usr/bin/env	python3

"""
Add columns of tsv files to a main metadata table

By Veronica Mixao
@INSA
"""

import os
import sys
import argparse
import textwrap
import pandas

# functions	----------

def data2metadata(data, mx_metadata):
	""" 
	create a combined matrix with metadata and information from other files
	"""

	sample_column = mx_metadata.columns[0]
	mx_data = pandas.read_table(data, dtype = str)
	sample_column_data = mx_data.columns[0]

	# check for duplicated samples in metadata
	metadata_samples = mx_metadata[mx_metadata.columns[0]].values.tolist()
	
	if len(metadata_samples) != len(set(metadata_samples)):
		print("\tWARNING!! You have duplicated samples in the metadata table! I cannot continue!")
		print("\tWARNING!! You have duplicated samples in the metadata table! I cannot continue!", file = log)
		sys.exit()
	
	data_samples = mx_data[mx_data.columns[0]].values.tolist()
	if len(data_samples) != len(set(data_samples)):
		print("\tWARNING!! You have duplicated columns in the partitions table! I cannot continue!")
		print("\tWARNING!! You have duplicated columns in the partitions table! I cannot continue!", file = log)
		sys.exit()
		
	a = mx_metadata.set_index(sample_column, drop = True)
	b = mx_data.set_index(sample_column_data, drop = True)	
	c = pandas.concat([a, b], axis=1)
		
	c = c.reset_index(drop = False)
	c.rename(columns={c.columns[0]: mx_metadata.columns[0]}, inplace=True)

	return c

if __name__ == "__main__":
    
	# argument options
    
	parser = argparse.ArgumentParser(prog="merge_tables.py", formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent("""\
									############################################################################             
									#                                                                          #
									#                             merge_tables.py                              #
									#                                                                          #
									############################################################################ 
									                            
									Add columns of tsv files to a main metadata table.
									
									-------------------------------------------------------------------------------"""))
										
	parser.add_argument("-m", "--metadata", dest="metadata", required=True, type=str, help="[MANDATORY] Main metadata file in .tsv format")
	parser.add_argument("-f", "--files", dest="files", required=True, type=str, help="[MANDATORY] Comma-separated list of .tsv files with new info")
	parser.add_argument("-o", "--output", dest="output", required=False, default="Merged", type=str, help="[OPTIONAL] Tag for output file name (default = Merged)")			
			
	args = parser.parse_args()
	
	if "," in args.files:
		filenames = args.files
		list_files = filenames.split(",")
	else:
		list_files = [args.files]
	
	mx = pandas.read_table(args.metadata, dtype = str)
	
	for f in list_files:
		mx = data2metadata(f, mx)
	
	mx.to_csv(args.output + ".tsv", index = False, header=True, sep ="\t")
	
	

