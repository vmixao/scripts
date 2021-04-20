#/usr/bin	python

"""
Pipeline: This script is used to generate the summary table of all isolates
Input: tab delimited table with the following columns:
"strain" \t "date" \t "division" \t "location" \t "lineage"

NOTE: DATE FORMAT REQUIRED DD/MM/YYYY

Launch the script:
python3 get_summary_table.py input.tsv output.tsv

By Veronica Mixao 
@INSA
vmixao@gmail.com

Last modified: 13/04/2021
"""

import pandas
import numpy
import sys

filename  = sys.argv[1]

data = pandas.read_table(filename)
data_out = {"lineage": [], "first_seq_date": [], "last_seq_date": [], "n_District": [], "n_Municipality": [], "n_sequences": []}

lineages = data["lineage"].values.tolist()

for lin in set(lineages):
	flt_data = data[data.lineage == lin] #filter the dataframe
	if len(flt_data.strain.unique()) != len(flt_data.lineage): #compare number of unique sequences with the number of lines
		#print(flt_data.strain.unique(), flt_data.lineage)
		print("Warning!!! You have a repetitive sequence in lineage ", lin)
			
	n_seq = len(flt_data.strain.unique()) #number of different sequences
	n_mun = len(flt_data.location.unique()) #number of different locations
	n_dis = len(flt_data.division.unique()) #number of different divisions
	date = pandas.to_datetime(flt_data.date, dayfirst=True).dt.date #converting date format
		
	data_out["lineage"].append(lin)
	data_out["first_seq_date"].append(min(date))
	data_out["last_seq_date"].append(max(date))
	data_out["n_District"].append(n_dis)
	data_out["n_Municipality"].append(n_mun)
	data_out["n_sequences"].append(n_seq)

new_data = pandas.DataFrame(data = data_out)

out = new_data.sort_values(by=["n_sequences"], ascending=False) #modify according to the sorting parameter

out.to_csv(sys.argv[2], index = False, header=True, sep ="\t")
