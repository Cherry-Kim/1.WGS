import string,sys,os
  
path,co = './',0
file_list = os.listdir(path)
bam_list = sorted([file for file in file_list if file.endswith('.sort.bam')])
for i in bam_list:
    co += 1
    sample = i.split('.sort.bam')[0]
    print(co,i)
    #os.system('samtools depth '+sample+'.sort.bam > '+sample+'.sort.bam.depth')

    avg_depth_output = os.popen("awk '{sum+=$3} END {print \"Sample " + sample + " Average Depth of Coverage: \", sum/3080419480}' " + sample + ".sort.bam.depth").read().strip()
    print(avg_depth_output)

    # Save the sample name and average depth into the output file
    with open('Depth.out', 'a') as output_file:
        output_file.write(avg_depth_output+'\n')

