#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 01:54:37 2018

@author: zhulu
"""

import csv
from collections import defaultdict
import numpy as np


def main():
#    f_score = 'CellLine_all_tissueCL_scl_pubmed_ID.txtpmid_sent_log.csv_a_0.8_ws_3_wa_0.2_human.csv'
#    with open(f_score,'r') as f_sc:
#        scores = csv.reader(f_sc)
#        # next(abst, None)  # skip the headers
#        for row in scores:
#            break
    result = dict()
    f_abs_name = 'CellLine_all_tissueCL_scl_pubmed_ID.txtpmid_abs_log.csv'
    with open(f_abs_name,'r') as f_abst:
        abst = csv.reader(f_abst)
        next(abst, None)  # skip the headers
        for row in abst:
    #        triplet = '-'.join(row[1:4])
            triplet = (row[1],row[2],row[3])
            if triplet in score.keys():
                key = (row[0],row[1],row[2],row[3])
                result[key] = score[triplet]

def create_csv(result):
    """creates csv file of computed triplet with their score"""
    with open('result_out.csv', 'w') as csvfile:
        fieldnames = ['PMID','ENTREZ','GO','BTO','score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=",",lineterminator='\n')
        writer.writeheader()
        for [triplet,score] in result.items():
            writer.writerow({'PMID':triplet[0], 'ENTREZ':triplet[1],'GO':triplet[2], 'BTO':triplet[3], 'score':score})

    
    
def get_score(trip):
    score[0]
    return score
    
if __name__ == "__main__":
    main()
