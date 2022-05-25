#!/usr/bin/env	python3

"""
Obtain a combined bed file including all the patterns detected by Phobos in a multiple sequence alignment

By Veronica Mixao
@INSA
""" 

import os
import argparse
import glob
from Bio import AlignIO


# functions	---------

def align2coords(alignment, reference):
	""" obtain reference coordinates from a sequence alignment 
	input: alignment
	output: dictionary
	"""
	
	align = AlignIO.read(alignment, "fasta")
	
	for record in align:
		if record.id == reference:
			ref_seq = record.seq
	
	ref_coord = 0
	align_coord = 0
	coords = {}		
	for nucl in ref_seq:
		align_coord += 1
		if nucl != "-":
			ref_coord += 1
		coords[align_coord] = ref_coord
	
	return coords


# pipeline	----------
parser = argparse.ArgumentParser()
parser.add_argument("-gff", "--phobos_gff", dest="gff", required=True, help="[MANDATORY] PHOBOS gff file with tandem repeats and sequence information")
parser.add_argument("-align", "--alignment", dest="fasta", required=True, help="[MANDATORY] Sequence alignment (fasta format) used to run PHOBOS")
parser.add_argument("-r", "--reference", dest="ref", required=True, help="[MANDATORY] Reference sequence in the alignment")
parser.add_argument("-c", "--contig", dest="contig", required=True, help="[MANDATORY] Contig name used for read alignment")

args = parser.parse_args()

ref = args.contig 

# get ref conversion
coords = align2coords(args.fasta, args.ref)

# process gff in bash
os.system(" grep -v '#' " + args.gff + " Phobos_results.txt | awk '{ print $1, $4, $5, $18}' |  awk -F '\"' '{ print $1}' > tmp.gff")

# generate a bed file per poly type
poly = {}
with open("tmp.gff") as ingff:
	outname = ""
	for line in ingff.readlines():
		lin = line.split("\n")
		l = lin[0].split(" ")
		sample = l[0]
		start = int(l[1])
		end = int(l[2])
		details = l[3]
		
		if details not in poly.keys():
			poly[details] = []
		info = str(coords[start-1]),str(coords[end])
		poly[details].append(info)

for key in poly:
	with open("poly_" + key + ".bed", "w+") as out:
		for start,end in poly[key]:
			print(ref + "\t" + start + "\t" + end + "\t" + key, file = out)
os.system("rm tmp.gff")

# intervals bedfile

for filename in glob.glob("poly_A.bed"):
	os.system("sort -k1,1 -k2,2n " + filename + " > tmp.bed")
	os.system("bedtools merge -i tmp.bed -c 4 -o distinct > " + filename + "; rm tmp.bed")

# generate a single bed file
os.system("cat *bed > Final.bed; rm poly_*.bed")
