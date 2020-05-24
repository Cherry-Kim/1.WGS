#!usr/bin/python

import os,sys

def help():
	print ''
	print '[USAGE] *.py [sample]'
	print ''

def main(sample):
#	print "STEP0. Pre-processing"
#	os.system('java -jar /home/hykim/WGS/Trimmomatic-0.36/trimmomatic-0.36.jar PE -threads 16 -phred33 /home/hykim/WGS/0.DATA/%s_1.fq.gz /home/hykim/WGS/0.DATA/%s_2.fq.gz %s.r1.trim.fq %s.r1.unpair.fq %s.r2.trim.fq %s.r2.unpair.fq ILLUMINACLIP:/home/hykim/WGS/Trimmomatic-0.36/adapters/TruSeq3-PE-2.fa:2:151:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36'%(sample,sample,sample,sample,sample,sample))

#	print "STEP1. Map to Reference using BWA mem"
#	os.system('bwa mem -t 16 -R "@RG\tPL:Illumina\tID:YUHL\tSM:%s\tLB:HiSeq" /home/hykim/REF/Human/hg19/hg19.fa %s.r1.trim.fq %s.r2.trim.fq > %s.sam'%(sample,sample,sample,sample))

#	print "STEP2. MarkDuplicates using Picard"
#	os.mkdir('/home/hykim/WGS/TEMP_PICARD/')
#	os.system('java -Xmx8g -jar /home/hykim/REF/Human/picard.jar AddOrReplaceReadGroups TMP_DIR=/home/hykim/WGS/TEMP_PICARD VALIDATION_STRINGENCY=LENIENT SO=coordinate I=%s.sam O=%s_sorted.bam RGID=YUHL RGLB=HiSeq RGPL=Illumina RGPU=unit1 RGSM=%s CREATE_INDEX=true'%(sample,sample,sample))
#	os.system('java -Xmx8g -jar /home/hykim/REF/Human/picard.jar MarkDuplicates TMP_DIR=/home/hykim/WGS/TEMP_PICARD VALIDATION_STRINGENCY=LENIENT  I=%s_sorted.bam O=%s.dedup.sam  M=%s.duplicate_metrics REMOVE_DUPLICATES=true AS=true'%(sample,sample,sample))
#	os.system('java -Xmx8g -jar /home/hykim/REF/Human/picard.jar SortSam TMP_DIR=/home/hykim/WGS/TEMP_PICARD VALIDATION_STRINGENCY=LENIENT  SO=coordinate  I=%s.dedup.sam  O=%s.dedup.bam CREATE_INDEX=true'%(sample,sample))

#	print "STEP3-1. Base Quality Score Recalibration - first pass"
#	os.system('java -Xmx8g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar BaseRecalibrator -R /home/hykim/REF/Human/hg19/hg19.fa -I %s.dedup.bam --known-sites /home/hykim/REF/1000GENOMES-phase_3_indel.vcf --known-sites /home/hykim/REF/dbsnp_138.hg19.vcf -O %s.recal_pass1.table'%(sample,sample))
#	os.system('java -Xmx8g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar ApplyBQSR -R /home/hykim/REF/Human/hg19/hg19.fa -I %s.dedup.bam -bqsr %s.recal_pass1.table -O %s.recal.pass1.bam'%(sample,sample,sample))
#	print "STEP3-2. Base Quality Score Recalibration - second pass"
#	os.system('java -Xmx8g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar BaseRecalibrator -R /home/hykim/REF/Human/hg19/hg19.fa -I %s.recal.pass1.bam --known-sites /home/hykim/REF/1000GENOMES-phase_3_indel.vcf --known-sites /home/hykim/REF/dbsnp_138.hg19.vcf -O %s.recal_pass2.table'%(sample,sample))
#	os.system('java -Xmx8g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar ApplyBQSR -R /home/hykim/REF/Human/hg19/hg19.fa -I %s.recal.pass1.bam -bqsr %s.recal_pass2.table -O %s.recal.pass2.bam'%(sample,sample,sample))
#	os.system('java -Xmx8g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar AnalyzeCovariates -before %s.recal_pass1.table -after %s.recal_pass2.table -plots %s.BQSR.pdf'%(sample,sample,sample))

#	print "STEP4-1. Calling variants for all samples with HaplotypeCaller"
#	os.system('java -Xmx8g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar HaplotypeCaller -R /home/hykim/REF/Human/hg19/hg19.fa -I %s.recal.pass2.bam -O %s.rawVariants.g.vcf -ERC GVCF --genotyping-mode DISCOVERY --standard-min-confidence-threshold-for-calling 20'%(sample,sample))
######################################################################
#	print "STEP4-2. Combining all samples with CombineGVCFs"
#	os.system('java -Xmx8g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar CombineGVCFs -R /home/hykim/REF/Human/hg19/hg19.fa --variant YUHL353-21.rawVariants.g.vcf --variant YUHL298-21.rawVariants.g.vcf -O test.g.vcf')

#	print "STEP4-3. Applying GenotypeGVCFs"
#	os.system('java -Xmx8g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar GenotypeGVCFs -R /home/hykim/REF/Human/hg19/hg19.fa -V test.g.vcf -O test_genotype.vcf')

##	print "GenomicsDBImport"
##	os.system('gatk --java-options "-Xmx4g -Xms4g" GenomicsDBImport -V data/gvcfs/mother.g.vcf.gz -V data/gvcfs/father.g.vcf.gz -V data/gvcfs/son.g.vcf.gz genomicsdb-workspace-path /home/jakim/EWAS_case/output1 -L /home/jakim/WGS/WGS2/final/SeqCap_EZ_Exome_v3_hg19_capture_targets.bed'
##	print "GenotypeGVCFs"
##	os.system('gatk --java-options "-Xmx4g" GenotypeGVCFs -R Homo_sapiens_assembly38.fasta  -V gendb://my_database -O output.vcf.gz'

#	print "STEP5-1. Extracting the SNPs and Indels with SelectVariants"
#	os.system('java -Xmx8g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar SelectVariants -R /home/hykim/REF/Human/hg19/hg19.fa -V test_genotype.vcf --select-type-to-include SNP -O test.rawSNPs.vcf')
#	os.system('java -Xmx8g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar SelectVariants -R /home/hykim/REF/Human/hg19/hg19.fa -V test_genotype.vcf --select-type-to-include INDEL -O test.rawINDELs.vcf')

#	print "STEP5-2. Applying hard-filtering on the SNPs and Indels with VariantFiltration"
#	os.system('java -Xmx8g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar VariantFiltration -R /home/hykim/REF/Human/hg19/hg19.fa -V test.rawSNPs.vcf -O test.rawSNPs.filtered.vcf --filter-expression "QD < 2.0  || FS > 60.0  ||   MQ < 40.0  || HaplotypeScore > 13.0  ||  MappingQualityRankSum < -12.5  ||  ReadPosRankSum < -8.0 " --filter-name "."')
#	os.system('java -Xmx8g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar VariantFiltration -R /home/hykim/REF/Human/hg19/hg19.fa -V test.rawINDELs.vcf -O test.rawINDELs.filtered.vcf --filter-expression "QD < 2.0  ||  FS > 200.0  ||  ReadPosRankSum < -20.0"  --filter-name "."')
#	print "STEP5-3. Merge the file for SNPs and Indels with CombineVariants"
#	os.system('java -Xmx8g -jar /home/program/gatk-4.0.11.0/gatk-package-4.0.11.0-local.jar SortVcf -I test.rawSNPs.filtered.vcf -I test.rawINDELs.filtered.vcf -O test.Filtered.Variants.vcf')

#	print "STEP6. Annotation using SnpEff"
#	os.system('egrep "^#|PASS" test.Filtered.Variants.vcf > test.Filtered.Variants.PASS.vcf')
#	os.system('java -jar snpEff/snpEff.jar -v hg19 test.Filtered.Variants.PASS.vcf > test.SnpEff.vcf')
	#os.system('java -jar snpEff/SnpSift.jar annotate /home/hykim/REF/dbsnp_138.hg19.vcf test.SnpEff.vcf > test.SnpEff.dbSNP138.vcf')
#	os.system('java -jar snpEff/SnpSift.jar annotate /home/hykim/REF/clinvar_20200419.vcf test.SnpEff.dbSNP138.vcf > test.SnpEff.dbSNP138.clinva.vcf')

	os.system('perl /home/program/annovar/table_annovar.pl test.Filtered.Variants.vcf /home/program/annovar/humandb/ -buildver hg19 -out test.annov.vcf -remove -otherinfo -protocol refGene,cytoBand,exac03,gnomad211_exome,gnomad211_genome,avsnp147,dbnsfp33a,popfreq_max_20150413,clinvar_20190305 -operation g,r,f,f,f,f,f,f,f -nastring . -vcfinput -polish')

if __name__ == '__main__':
	
	 if len(sys.argv) < 2:
		 sys.exit(help())

	 main(sys.argv[1])
