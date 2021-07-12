#!/usr/bin/python

import string,sys,os

CHR=[]
for i in range(1,23):
	CHR.append(str(i))
CHR.append('X')
CHR.append('Y')
CHR.append('M')

## Reference building ##
for i in CHR:
	os.system('wget http://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/chr'+i+'.fa.gz')
	os.system('gunzip '+ 'chr'+i+'.fa.gz') 

os.system('cat chrM.fa chr1.fa chr2.fa chr3.fa chr4.fa chr5.fa chr6.fa chr7.fa chr8.fa chr9.fa chr10.fa chr11.fa chr12.fa chr13.fa chr14.fa chr15.fa chr16.fa chr17.fa chr18.fa chr19.fa chr20.fa chr21.fa chr22.fa chrX.fa chrY.fa > hg38.fa')

## Reference indexing ##
#sudo apt update
#sudo apt install bowtie2
os.system('bowtie2-build hg38.fa hg38')
os.system('bwa index -a bwtsw hg38.fa')
#sudo apt install samtools
os.system('samtools faidx hg38.fa')
#wget https://github.com/broadinstitute/picard/releases/download/2.25.6/picard.jar
os.system('java -jar /home/picard.jar CreateSequenceDictionary R=hg38.fa O=hg38.dict')
