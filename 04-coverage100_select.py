# -*- encoding:UTF-8 -*-
#Version-01: 对过滤去冗余及最优转录本选择的cds制作bed文件

import sys,getopt

def text_open2dic(file_path):
        '''用于文件打开, 写入字典(以更快的方式)'''
        dic1 = {}
        dic2 = {}
        for line in open(file_path):
                line = line.strip()
                if line.startswith('>'):
                        head = line.split()[0]
                        dic1[head[1:]] = []
                else:
                        dic1[head[1:]].append(line)
        for line in dic1.keys():
                dic2[line] = ''.join(dic1[line])
        return dic2

def main(CDS,INPUT,OUTPUT):
	cds = text_open2dic(CDS)
	output = open(OUTPUT,'w')
	for line in open(INPUT).readlines()[1:]:
		# if line.split()[4] == '100.00':
		if not line.startswith('Ppy') and line.split()[4] == '100.00':
			output.write('>'+line.split()[0]+'\n')
			output.write(cds[line.split()[0]]+'\n')
	output.close()

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], "hg:i:o:")
	for opt, arg in opts:
		if opt == '-h':
			print '\nUsage: python 04-coverage100_select.py -g <CDS.fa> -i <chromosomes.report> -o <OUTPUT>\n'
			sys.exit()
		elif opt == '-g':
			CDS = arg
		elif opt == '-i':
			INPUT = arg
		elif opt == '-o':
			OUTPUT = arg	
	main(CDS,INPUT,OUTPUT)
