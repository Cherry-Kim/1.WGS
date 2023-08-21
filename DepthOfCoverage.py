import string,sys,os,subprocess
  
def step1():
    path,co = './',0
    file_list = os.listdir(path)
    bam_list = sorted([file for file in file_list if file.endswith('.sort.bam')])
    for i in bam_list:
        co += 1
        sample = i.split('.sort.bam')[0]
        print(co,i)
        os.system('samtools depth '+sample+'.sort.bam > '+sample+'.sort.bam.depth')

def step2():
    path = './'
    bam_files = sorted([file for file in os.listdir(path) if file.endswith('.sort.bam.depth')])

    open('Depth.out2', 'w').close()

    for i,depth_file in enumerate(bam_files):
        sample = depth_file.split('.sort.bam.depth')[0]
        print(f"Processing sample {i + 1}: {sample}")

        wc_output = subprocess.check_output(['wc', '-l', depth_file]).decode().strip()
        num_lines = int(wc_output.split()[0])

        avg_depth_output = os.popen(f'awk \'{{sum+=$3}} END {{print "Average Depth of Coverage for {sample}: ", sum/{num_lines}}}\' '+ sample + '.sort.bam.depth').read().strip()
        print(avg_depth_output)

        with open('Depth.out2', 'a') as output_file:
            output_file.write(avg_depth_output+'\n')

def main():
    #step1()
    step2()
main()
