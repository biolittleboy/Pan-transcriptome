# -*- encoding:UTF-8 -*-
#Version-01: 计算栽培和改良两个分类的CV值

import sys,getopt,os,json,numpy
from functools import reduce
from decimal import *

def dic1(PATH):
	dic = {}
	n = 0
	for file in os.listdir(PATH):
		print n 
		n += 1
		dic.setdefault(file.split('.txt')[0],{})
		for line in open(PATH+'/'+file).readlines()[1:]:
			dic[file.split('.txt')[0]].setdefault(line.strip().split()[-1],[])
			dic[file.split('.txt')[0]][line.strip().split()[-1]].append(float(line.strip().split()[0]))
	return dic

def main(PATH,OUTPUT):
	fpkm = dic1(PATH)
	output = open(OUTPUT,'w')
	output.write('Gene\timprovement\tlandraces\n')
	genes = fpkm.keys()
	genes.sort()
	dic = {}
	for gene in genes:
		output.write(gene)
		for i in fpkm[gene]:
			sd = numpy.std(fpkm[gene][i])
			mean = numpy.mean(fpkm[gene][i])
			if mean < 0.01: ##
				cv = 0
			else:
				cv = round(Decimal(sd)/Decimal(mean),5)
			output.write('\t'+str(cv))
			if gene.startswith('Ppy'):
				dic.setdefault('Ref',{})
				dic['Ref'].setdefault(i,[])
				dic['Ref'][i].append(cv)
			else:
				dic.setdefault('Non_ref',{})
				dic['Non_ref'].setdefault(i,[])
				dic['Non_ref'][i].append(cv)
		output.write('\n')
	output.close()
	for i in dic:
		for t in dic[i]:
			mean = numpy.mean(dic[i][t])
			print i,t,round(mean,5)


if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], "hp:o:")
	for opt, arg in opts:
		if opt == '-h':
			print '\nUsage: python 08_CV_cal.py -p <03-expression_level/genes_file> -o <OUTPUT>\n'
			sys.exit()
		elif opt == '-p':
			PATH = arg
		elif opt == '-o':
			OUTPUT =arg
	main(PATH,OUTPUT)
