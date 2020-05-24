import string,sys

fp=open("1000GENOMES-phase_3.vcf")
fpout = open('1000GENOMES-phase_3_indel.vcf','w')

VAR=[]
for line in fp:
	if line.startswith('#'):
		fpout.write(line)
	else:
		line_temp=string.split(line,"\t")
		info = string.split(line_temp[7],';')
		if ('TSA=indel' in info[1]) or ('TSA=deletion' in info[1]) or ('TSA=insertion' in info[1]):
			fpout.write('chr'+line)
			if not info[1] in VAR:
				VAR.append(info[1])	
print VAR

fp.close()
fpout.close()
