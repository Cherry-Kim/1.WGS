import string,sys,os,glob

G1_START=int(1000)
G1_END=int(1005)
G2_START=int(2000)
G2_END=int(2005)

co=0
fp=glob.glob('*.temp.vcf')
for fname in fp:
	co+=1
	print 'Sample',co,fname

	fp=open(fname,'r')
	a=string.split(fname,'.')
	fpout=open(a[0]+'.CYP3A.vcf','w')
	
	for line in fp.xreadlines():
		if line.startswith('#'):
			fpout.write(line)
		else:
			CHROM, POS = line.split('\t')[:2]
			if CHROM == 'chr1' and (G1_START<=int(POS)<=G1_END or G2_START<=int(POS)<=G2_END):
				fpout.write(line)
fp.close()
fpout.close()
