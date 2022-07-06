#!/usr/bin/env	python3

"""
This script processed the outputs of Kraken2 and filters a fasta file according to the desired Taxon IDs

By Veronica Mixao
@INSA
"""

import argparse
import textwrap
from Bio import SeqIO

# functions	----------

def get_ids(taxonid_file):
	""" Get the taxon ids
	input: list
	output: list """
	
	ids = []
	with open(taxonid_file) as tfile:
		for line in tfile.readlines():
			ids.append(line.split("\n")[0])
	return ids

def get_contigs(ids, kraken_output):
	""" Get contigs of iterest
	input: dictionary and kraken output
	outpu: list """
	
	contigs = []
	with open(kraken_output) as kfile:
		for line in kfile.readlines():
			l = line.split("\t")
			contig_name = l[1]
			taxon_id = l[2]
			
			if taxon_id in ids:
				contigs.append(contig_name)
	return contigs

def flt_fasta(contigs, assembly, out):
	""" Filter the fasta file
	input: dictionary and fasta
	output: fasta """
	
	with open(out + ".fasta", "w+") as output:
		for record in SeqIO.parse(assembly, "fasta"):
			if record.id in contigs:
				print(">" + str(record.id), file = output)
				print(str(record.seq), file = output)		
	
	
# main	----------

if __name__ == "__main__":
    
	# argument options
    
	parser = argparse.ArgumentParser(prog="partitioning_HC.py", formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent("""\
									###############################################################################             
									#                                                                             #
									#                     kraken_results2filter_assembly.py                       #
									#                                                                             #
									###############################################################################  
									                            
									Filter an assembly according to Kraken results.
									
									-----------------------------------------------------------------------------"""))
	
	group0 = parser.add_argument_group("Input/output specifications")
	group0.add_argument("-ko", "--kraken-output", dest="kraken_output", required=True, type=str, help="[MANDATORY] KRAKEN output")
	group0.add_argument("-t", "--taxonid", dest="taxonid", required=True, type=str, help="[MANDATORY] List of Taxon IDs of interest")
	group0.add_argument("-a", "--assembly", dest="assembly", type=str, required=True, help="[MANDATORY] Assembly (fasta)")
	group0.add_argument("-o", "--output", dest="output", type=str, required=True, help="[OPTIONAL] Tag for output file name")

	args = parser.parse_args()
	
	ids = get_ids(args.taxonid)
	contigs = get_contigs(ids, args.kraken_output)
	flt_fasta(contigs, args.assembly, args.output)
