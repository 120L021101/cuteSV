#!/usr/bin/env python
# coding=utf-8
import sys
import argparse
import joblib
import logging
import time

# python gene_anno.py *.anno.jl *.vcf *.related.vcf *.intergenetic.vcf
def main_ctrl(args):
    annos = joblib.load(args.anno)
    length = len(annos)
    pos_list = []
    for i in range(length):
        to_check = annos.loc[i]
        start_pos = int(to_check["vcf_key"].split(':')[1].split('-')[0]) + 1 # corresponding pos in vcf
        if len(pos_list) == 0 or pos_list[-1] != start_pos:
            pos_list.append(start_pos)
    gene_related = open(args.gene, 'w')
    intergenetic = open(args.intergenetic, 'w')
    idx = 0
    with open(args.vcf, 'r') as f:
        for line in f:
            if line[0] == '#':
                gene_related.write(line)
                intergenetic.write(line)
            else:
                pos = int(line.strip().split('\t')[1])
                if idx < len(pos_list) and pos == pos_list[idx]:
                    gene_related.write(line)
                    idx += 1
                else:
                    intergenetic.write(line)
    logging.info('Finish')

# truvari anno bpovl -i LGY.vcf.gz -a changed.gtf.gz -o LGY.anno.jl -p gff
def main(argv):
	args = parseArgs(argv)
	setupLogging(False)
	starttime = time.time()
	main_ctrl(args)
	logging.info("Finished in %0.2f seconds."%(time.time() - starttime))

USAGE="""\
	Evaluate SV callset generated by simulations.
	Author: Shuqi Cao
	Email: sqcao@stu.hit.edu.cn
"""

def parseArgs(argv):
	parser = argparse.ArgumentParser(prog="evaluation on HWE/ExcHet/Hete/Known worldwide cohort", description=USAGE, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--anno", type=str, help="Gene region annotation from truvari anno bpovl.")
	parser.add_argument("--vcf", type=str, help="VCF file to be extracted.")
	parser.add_argument("--gene", type=str, help="SVs in gene-related regions.")
	parser.add_argument("--intergenetic", type=str, help="SVs in intergenetic regions.")
	args = parser.parse_args(argv)
	return args

def setupLogging(debug=False):
	logLevel = logging.DEBUG if debug else logging.INFO
	logFormat = "%(asctime)s [%(levelname)s] %(message)s"
	logging.basicConfig( stream=sys.stderr, level=logLevel, format=logFormat )
	logging.info("Running %s" % " ".join(sys.argv))

if __name__ == '__main__':
	main(sys.argv[1:])