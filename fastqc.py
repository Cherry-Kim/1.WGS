import string,sys,glob,os
  
def STEP1_Preprocessing(sample):
    os.system('fastqc -t 48 --nogroup '+sample+'_1.fq.gz')
    os.system('fastqc -t 48 --nogroup '+sample+'_2.fq.gz')

def Main():
    file_list=os.listdir('./')
    f_list=[file for file in file_list if file.endswith("_1.fq.gz")]
    for fname in f_list:
        sample = fname.split('_1.fq.gz')[0]
        print(sample)
        STEP1_Preprocessing(sample)
Main()
