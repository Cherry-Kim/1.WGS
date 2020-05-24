import os,glob,string,sys

### Input format: Sample.1.fq.gz ###

co=0
Cohort='TEST'
PATH='/home/FASTQ/'

fp=glob.glob('*.1.fq.gz')
for fname in fp:
	co+=1
	a=string.split(fname,'.')
	Sample=a[0]
	print '### Sample',co,Sample

	print "### STEP0. Pre-processing"
	os.system('java -jar Trimmomatic-0.36/trimmomatic-0.36.jar PE -threads 16 -phred33 '+Sample+'.1.fq.gz '+Sample+'.2.fq.gz '+Sample+'.r1.trim.fq '+Sample+'.r1.unpair.fq '+Sample+'.r2.trim.fq '+Sample+'.r2.unpair.fq ILLUMINACLIP:Trimmomatic-0.36/adapters/TruSeq3-PE-2.fa:2:151:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36')

	print "### STEP1. Map to Reference using BWA mem"
	os.system('bwa mem -t 16 -R "@RG\\tPL:Illumina\\tID:TEST\\tSM:'+Sample+'\\tLB:HiSeq" /home/REF/hg19.fa '+Sample+'.r1.trim.fq '+Sample+'.r2.trim.fq > '+Sample+'.sam')

	print "### STEP2. MarkDuplicates using Picard"
	if not os.path.isdir('TEMP_PICARD'):
	       os.mkdir('TEMP_PICARD')
	os.system('java -Xmx8g -jar picard.jar AddOrReplaceReadGroups TMP_DIR=TEMP_PICARD VALIDATION_STRINGENCY=LENIENT SO=coordinate I='+Sample+'.sam O='+Sample+'_sorted.bam RGID=YUHL RGLB=HiSeq RGPL=Illumina RGPU=unit1 RGSM='+Sample+' CREATE_INDEX=true')
	os.system('java -Xmx8g -jar picard.jar MarkDuplicates TMP_DIR=TEMP_PICARD VALIDATION_STRINGENCY=LENIENT I='+Sample+'_sorted.bam O='+Sample+'.dedup.sam M='+Sample+'.duplicate_metrics REMOVE_DUPLICATES=true AS=true')
	os.system('java -Xmx8g -jar picard.jar SortSam TMP_DIR=TEMP_PICARD VALIDATION_STRINGENCY=LENIENT SO=coordinate I='+Sample+'.dedup.sam O='+Sample+'_dedup.bam CREATE_INDEX=true')

	print "STEP3-1. Base Quality Score Recalibration - first pass"
	os.system('java -Xmx8g -jar gatk-package-4.0.11.0-local.jar BaseRecalibrator -R hg19.fa -I '+Sample+'_dedup.bam --known-sites 1000GENOMES-phase_3_indel.vcf --known-sites dbsnp_138.hg19.vcf -O '+Sample+'_recal_pass1.table')
	os.system('java -Xmx8g -jar gatk-package-4.0.11.0-local.jar ApplyBQSR -R hg19.fa -I '+Sample+'_dedup.bam -bqsr '+Sample+'_recal_pass1.table -O '+Sample+'_recal_pass1.bam')
	print "STEP3-2. Base Quality Score Recalibration - second pass"
	os.system('java -Xmx8g -jar gatk-package-4.0.11.0-local.jar BaseRecalibrator -R hg19.fa -I '+Sample+'_recal_pass1.bam --known-sites 1000GENOMES-phase_3_indel.vcf --known-sites dbsnp_138.hg19.vcf -O '+Sample+'_recal_pass2.table')
	os.system('java -Xmx8g -jar gatk-package-4.0.11.0-local.jar ApplyBQSR -R hg19.fa -I '+Sample+'_recal_pass1.bam -bqsr '+Sample+'_recal_pass2.table -O '+Sample+'_recal_pass2.bam')
	os.system('java -Xmx8g -jar gatk-package-4.0.11.0-local.jar AnalyzeCovariates -before '+Sample+'_recal_pass1.table -after '+Sample+'_recal_pass2.table -plots '+Sample+'.BQSR.pdf')

	print "STEP4-1. Calling variants for all samples with HaplotypeCaller"
	os.system('java -Xmx8g -jar gatk-package-4.0.11.0-local.jar HaplotypeCaller -R hg19.fa -I '+Sample+'_recal_pass2.bam -O '+Sample+'.rawVariants.g.vcf -ERC GVCF --genotyping-mode DISCOVERY --standard-min-confidence-threshold-for-calling 20')

print "STEP4-2. Combining all samples with CombineGVCFs"
file_list=os.listdir(PATH)
file_list_py= [file for file in file_list if file.endswith(".g.vcf")]
vcf_list=file_list_py
print vcf_list
os.system('java -Xmx8g -jar gatk-package-4.0.11.0-local.jar CombineGVCFs -R hg19.fa '+" ".join(map(lambda z:"--variant "+z, vcf_list))+' -O '+Cohort+'.g.vcf')

print "STEP4-3. Applying GenotypeGVCFs"
os.system('java -Xmx8g -jar gatk-package-4.0.11.0-local.jar GenotypeGVCFs -R hg19.fa -V '+Cohort+'.g.vcf -O '+Cohort+'_genotype.vcf')

print "STEP5-1. Extracting the SNPs and Indels with SelectVariants"
os.system('java -Xmx8g -jar gatk-package-4.0.11.0-local.jar SelectVariants -R hg19.fa -V '+Cohort+'_genotype.vcf --select-type-to-include SNP -O '+Cohort+'.rawSNPs.vcf')
os.system('java -Xmx8g -jar gatk-package-4.0.11.0-local.jar SelectVariants -R hg19.fa -V '+Cohort+'_genotype.vcf --select-type-to-include INDEL -O '+Cohort+'.rawINDELs.vcf')

print "STEP5-2. Applying hard-filtering on the SNPs and Indels with VariantFiltration"
os.system('java -Xmx8g -jar gatk-package-4.0.11.0-local.jar VariantFiltration -R hg19.fa -V '+Cohort+'.rawSNPs.vcf -O '+Cohort+'.rawSNPs.filtered.vcf --filter-expression "QD < 2.0  || FS > 60.0  ||   MQ < 40.0  || HaplotypeScore > 13.0  ||  MappingQualityRankSum < -12.5  ||  ReadPosRankSum < -8.0 " --filter-name "."')
os.system('java -Xmx8g -jar gatk-package-4.0.11.0-local.jar VariantFiltration -R hg19.fa -V '+Cohort+'.rawINDELs.vcf -O '+Cohort+'.rawINDELs.filtered.vcf --filter-expression "QD < 2.0  ||  FS > 200.0  ||  ReadPosRankSum < -20.0"  --filter-name "."')

print "STEP5-3. Merge the file for SNPs and Indels with CombineVariants"
os.system('java -Xmx8g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar SortVcf -I '+Cohort+'.rawSNPs.filtered.vcf -I '+Cohort+'.rawINDELs.filtered.vcf -O '+Cohort+'.Filtered.Variants.vcf')

print "STEP6. Annotation using Annovar"
os.system('egrep "^#|PASS" '+Cohort+'.Filtered.Variants.vcf > '+Cohort+'.Filtered.Variants.PASS.vcf')
os.system('perl annovar/table_annovar.pl '+Cohort+'.Filtered.Variants.PASS.vcf annovar/humandb/ -buildver hg19 -out '+Cohort+'.annov.vcf -remove -otherinfo -protocol refGene,cytoBand,exac03,gnomad211_exome,gnomad211_genome,avsnp147,dbnsfp33a,popfreq_max_20150413,clinvar_20190305 -operation g,r,f,f,f,f,f,f,f -nastring . -vcfinput -polish')

##print "STEP6. Annotation using SnpEff"
##os.system('java -jar snpEff/SnpSift.jar annotate clinvar_20200419.vcf test.SnpEff.dbSNP138.vcf > test.SnpEff.dbSNP138.clinva.vcf')
'''
