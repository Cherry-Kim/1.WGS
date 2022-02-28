import string,sys,glob,os
  
def STEP1_Preprocessing(sample,PATH):
    os.system('fastqc -t 48 --nogroup '+PATH+sample)
    os.system('fastqc -t 48 --nogroup '+PATH+sample)

def Main():
    #REF = '/REF/hg38/'
    #SP = 'mm10' #'hg38'
    #adapter = 'illumina' #'nextera'
    PATH = './'
    file_list=os.listdir(PATH)
    f_list=[file for file in file_list if file.endswith("_1.fq.gz")]
    for sample in f_list:
        print sample
        STEP1_Preprocessing(sample,PATH)
Main()
