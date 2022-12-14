#!/usr/bin/env python
#python 2.7.5 requires biopython
#fetchClusterSeqs.py
#Version 1. Adam Taranto, April 2015
#Contact, Adam Taranto, adam.taranto@anu.edu.au

''' 
fetchClusterSeq is a helper tool for processing output from the R Package Corset (Davidson and Oshlack, 2014)

Takes as input: a list of target cluster names,
transcript-to-cluster mapping file generated by corset, and a fasta file containing transcript 
sequences. 

Returns: Fasta file of transcripts belonging to query clusters, with Cluster ID 
appended to their original sequence name. 
'''

import csv
import sys
import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from os.path import basename

def main(inFasta=None, targetClust=None, outFasta='filtered_seqs.fa', clustMap=None, getLong=False):
    if inFasta is None:
        sys.exit('No input fasta provided')

    if targetClust is None:
        print('No target cluster list provided. Reporting for all clusters.')

    if clustMap is None:
        sys.exit('No cluster mapping file provided')

    #Read transcript-to-cluster map into dictionary object called 'clustMem'.
    clustMem = clustDict(clustMap)

    #Read fasta records into dictionary called 'SeqMaster'.
    SeqMaster = getFasta(inFasta)

    #Open list of target clusters
    if targetClust:
        with open(targetClust) as f:
            reader = [line.rstrip('\n').split() for line in f]
        getClusters = list()
        for row in reader:
            if not getClusters.count(row[0]):
                getClusters.append(row[0])
    else:
        getClusters = clustMem.keys()

    #Open output fasta
    fasta_file = open(outFasta,'w')

    #Open log file for names not found in master set
    if targetClust:
        error_list = open(str('NotFound_' + basename(targetClust) + '.log'),'w')
    else:
        error_list = open(str('NotFound_Clusters_Transcripts.log'),'w')

    if getLong:
        reportLongSeqs(getClusters,fasta_file,error_list,clustMem,SeqMaster)
    else:
        reportSeqs(getClusters,fasta_file,error_list,clustMem,SeqMaster)

def reportSeqs(getClusters,fasta_file,error_list,clustMem,SeqMaster):
    #Write records for transcripts belonging to target clusters to new fasta
    for name in getClusters:
        #Check if target cluster exists in cluster-map dictionary
        if name in clustMem:
            #For each transcript belonging to target cluster
            for trans in clustMem[name]:
                #Check if target transcript exists in fasta dictionary
                try:
                    SeqMaster[trans]
                #If target transcript not in fasta, log error.
                except:
                    print('Transcript not in ref fasta: ' + name + ': ' + trans)
                    error_list.write(name + "\t" + trans + "\n")
                #If target transcript is in fasta, append cluster name and print to output fasta.
                else:
                    fasta_name= ">%s" % (name + '_' + trans)
                    fasta_seq= "%s" %(SeqMaster[trans])
                    fasta_file.write(fasta_name+"\n")
                    fastaLines(seq=fasta_seq, n=80, file=fasta_file)
        #If target cluster was not in map file, log error.
        else:
            print('Target cluster not in Map file: ' + name)
            error_list.write(name + "\n")
    fasta_file.close()
    error_list.close()

def reportLongSeqs(getClusters,fasta_file,error_list,clustMem,SeqMaster):
    #Write records for transcripts belonging to target clusters to new fasta
    for name in getClusters:
        longestSeqLen = 0
        #Check if target cluster exists in cluster-map dictionary
        if name in clustMem:
            #For each transcript belonging to target cluster
            for trans in clustMem[name]:
                #Check if target transcript exists in fasta dictionary
                try:
                    SeqMaster[trans]
                #If target transcript not in fasta, log error.
                except:
                    print('Transcript not in ref fasta: ' + name + ': ' + trans)
                    error_list.write(name + "\t" + trans + "\n")
                #If target transcript is in fasta, append cluster name and print to output fasta.
                else:
                    if len(SeqMaster[trans]) >= longestSeqLen:
                        longSeq = SeqMaster[trans]
                        longestSeqLen = len(SeqMaster[trans])
                        longSeqName = trans
            #print longest
            fasta_name= ">%s" % (name + '_' + longSeqName)
            fasta_seq= "%s" %(longSeq)
            fasta_file.write(fasta_name+"\n")
            fastaLines(seq=fasta_seq, n=80, file=fasta_file)
        #If target cluster was not in map file,log error.
        else:
            print('Target cluster not in Map file: ' + name)
            error_list.write(name + "\n")
    fasta_file.close()
    error_list.close()

def fastaLines(seq=None, n=80, file=None):
    """Yield successive n-sized chunks from seq."""
    for i in range(0, len(seq), n):
        file.write(seq[i:i+n] + "\n")

def clustDict(clustMap):
    #Read transcript-to-cluster mapping file into dict object.
    #Sample data row:
    #TranscriptID   ClusterID
    #nnt3Ldvymb Cluster-0.0
    with open(clustMap) as mapFile:
        readMap = [line.rstrip('\n').split() for line in mapFile]
    clustMem={}
    #Write records for seqs in name file to new fasta
    for row in readMap:
        transID=row[0]
        clustID=row[1]
        if clustID not in clustMem:
            clustMem[clustID] = list()
        clustMem[clustID].append(transID)
    return clustMem
    
def getFasta(inFasta):
    #Create empty dictionary
    SeqMaster={}
    #Populate dictionary with master set of fasta records
    for seq_record in SeqIO.parse(inFasta, "fasta"):
        SeqMaster[seq_record.id]=str(seq_record.seq)
    return SeqMaster

def mainArgs():
    """Process command-line arguments"""
    parser = argparse.ArgumentParser(description='Takes as input: a list of target cluster names, \
        transcript-to-cluster mapping file generated by corset, and a fasta file containing transcript \
        sequences. Returns: Fasta file of transcripts belonging to target clusters, with Cluster ID \
        appended to their original sequence name.', prog='fetchClusterSeqs')
    parser.add_argument("-i","--inFasta", 
                        required=True, 
                        help="Multi fasta to extract subset from")
    parser.add_argument("-t","--targetClust", 
                        default=None,
                        help="Text file with target cluster names in column one. If not provided \
                        will return transcripts for all clusters.")
    parser.add_argument("-o","--outFasta", 
                        default='filtered_seqs.fa', 
                        help="Directory for new sequence file to be written to.")
    parser.add_argument("-c","--clustMap", 
                        required=True, 
                        help="Corset transcript-to-cluster mapping file.")
    parser.add_argument("-l","--longest", 
                        action='store_true', 
                        default=False, 
                        help="If set, return only longest transcript per cluster.")
    args = parser.parse_args()
    return args

if __name__== '__main__':
    args = mainArgs()
    main(inFasta=args.inFasta, targetClust=args.targetClust, outFasta=args.outFasta, clustMap=args.clustMap, getLong=args.longest)