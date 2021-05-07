#!/usr/bin/env	python

"""
Pipeline: This script is used to generate the summary table of all mutations observed in the samples

Input: tab delimited table with the following columns:
"SAMPLE_ID" \t "Lineage" \t "mutationA" \t "mutationB" \t "mutationC" ...

By Veronica Mixao 
@INSA
vmixao@gmail.com
Last modified: 28/04/2021
"""

import argparse
import pandas
import numpy
import sys

parser = argparse.ArgumentParser(description="This script is used to generate the summary table of all mutations observed in the samples (filled with binary system). Input: tab delimited table with the following columns: 'SAMPLE_ID' \t 'Lineage' \t 'mutationA' \t 'mutationB' \t 'mutationC' ...")
parser.add_argument("-i", "--input", dest="input", action= "store", required=True, help="Input file")
parser.add_argument("-o", "--output", dest="output", action= "store", required=True, help="Output file")
parser.add_argument("-f", "--format", dest="format", action= "store", default="0", help="Output format: mutations in columns [0] or in rows [1]. Default [0]")

args = parser.parse_args()

def summary_mutations(infile, outfile, outformat):
	filename  = infile

	data = pandas.read_table(filename)
	data_out = {"lineage": [], "n_sequences": []}
	lineages = data["Lineage"].values.tolist()
	
	order_mutations = ["lineage", "n_sequences"]
	
	for lin in set(lineages):
		flt_data = data[data.Lineage == lin] #filter the dataframe
		if len(flt_data.SAMPLE_ID.unique()) != len(flt_data.Lineage): #compare number of unique sequences with the number of lines
			#print(flt_data.SAMPLE_ID.unique(), flt_data.lineage)
			print("Warning!!! You have a repetitive sequence in lineage ", lin)
		
		#getting lineage and stats	
		n_seq = len(flt_data.SAMPLE_ID.unique()) #number of different sequences
		data_out["lineage"].append(lin)
		data_out["n_sequences"].append(n_seq)
		
		#getting mutation summary
		for col in flt_data.columns:
			if col != "SAMPLE_ID" and col != "Lineage":
				counter = flt_data[col].sum()
				if col not in data_out.keys():
					data_out[col] = []
					order_mutations.append(col)
				data_out[col].append(counter)

	new_data = pandas.DataFrame(data = data_out, columns = order_mutations)
	
	if outformat == "0":
		out = new_data.sort_values(by=["n_sequences"], ascending=False) #modify according to the sorting parameter
		out.to_csv(outfile, index = False, header=True, sep ="\t")
	else:
		if outformat == "1":
			out = new_data.T
			out.to_csv(outfile, index = True, header= False, sep ="\t")
		else:
			print("Please use a valid output format code!!!!!")

summary_mutations(args.input, args.output, args.format)

