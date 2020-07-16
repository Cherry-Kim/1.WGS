import string,os,glob,sys

### STEP1. Create a new GenomicDB databaseDB datastore from GVCFs
cohort='TEST'
file_list=os.listdir('/home/DATA/')
#vcf_list= [file for file in file_list if file.endswith("rawVariants.g.vcf")]
CHR=[str(k) for k in range(1,23)]
CHR.append('X')
CHR.append('Y')
CHR.append('M')
for i in CHR:
	os.system('java -Xmx64g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar GenomicsDBImport '+" ".join(map(lambda z:"-V "+z, vcf_list))+' --genomicsdb-workspace-path test_DB'+i+' --intervals chr'+i)

	### STEP2. Joint-call samples in a GenomicDB datastore
	os.system('java -Xmx4g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar GenotypeGVCFs -R /home/hykim/REF/hg19.fa -V gendb://test_DB'+i+' -O chr'+i+'.Genotype.vcf')
	os.system('grep "^#" chr'+i+'.Genotype.vcf > chr'+i+'.Genotype2_head.vcf')
	os.system('grep -v "#" chr'+i+'.Genotype.vcf > chr'+i+'.Genotype2.vcf')
gvcf_list = [file for file in file_list if file.endswith("Genotype2.vcf")]
os.system('cat chr1.Genotype2_head.vcf '+" ".join(gvcf_list)+' > '+cohort+'.g.vcf')
os.system('grep "^#" '+cohort+'.g.vcf > '+cohort+'_sort.g.vcf')
os.system('grep -v "^#" '+cohort+'.g.vcf | sort -k1,1V -k2n >> '+cohort+'_sort.g.vcf')
