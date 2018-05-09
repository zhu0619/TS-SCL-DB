# -*- coding: utf-8 -*-
import csv
from collections import defaultdict
import numpy as np


def main():   
    wa = 0.2
    ws = 3
    alpha = 0.8
    # for alpha in np.arange(0.1, 0.9, 0.1):
    #     for ws in np.arange(0.1,3,0.5):
    #         for wa in np.arange(0.1,3,0.5):
    calculation(alpha, ws, wa)
                
                
                
def calculation(alpha, ws, wa):  
    # f_sent_name = 'pmids_abs_score_benchmark170.csv_Tissue_2018-01-15_a_0.6_ws_3_wa_0.2_human.csv'
    # f_abs_name = 'pmids_abs_score_benchmark170.csv_Tissue_2018-01-15_a_0.6_ws_3_wa_0.2_human.csv'
    f_sent_name = 'CellLine_all_tissueCL_scl_pubmed_ID.txtpmid_sent_log.csv'
    f_abs_name = 'CellLine_all_tissueCL_scl_pubmed_ID.txtpmid_abs_log.csv'    
               
    dict_abst = defaultdict(float)

    with open(f_abs_name,'r') as f_abst:
        abst = csv.reader(f_abst)
        next(abst, None)  # skip the headers
        for row in abst:
    #        triplet = '-'.join(row[1:4])
            triplet = (row[1],row[2],row[3])
            if triplet not in dict_abst.keys():
                dict_abst[triplet] = wa
            else:
                dict_abst[triplet] += wa
 
    with open(f_sent_name,'r') as f_sent:
        sent = csv.reader(f_sent)
        next(sent , None)  # skip the headers
        for row in sent:
            triplet = (row[1],row[2],row[3])
            if triplet not in dict_abst.keys():
                dict_abst[triplet] = ws
            else:
                dict_abst[triplet] += ws
    
    score = score_data(dict_abst,alpha)
    
    zscore = Zscore_data(score)
    sorted_scores=sorted(zscore.items(), key=lambda x:x[1], reverse=True)
    fout = f_sent_name.split('_a_')[0]+'_a_'+str(alpha)+'_ws_'+str(ws)+'_wa_'+str(wa)+'_human.csv'
    fout = 'Zscore'+fout
    create_csv(sorted_scores,fout)

def score_data(triplet_dict,alpha):
    """computes the association score S(P,T,L)"""
    overall_sum=sum(triplet_dict.values())
#    alpha=0.6
    beta=1.0-alpha
    score_dict={}
    for triplet,triplet_score in triplet_dict.items():
        protein_score=sum(v for k,v in triplet_dict.items() if triplet[0] == k[0])
        tissue_score=sum(v for k,v in triplet_dict.items() if triplet[1] == k[1])
        scl_score=sum(v for k,v in triplet_dict.items() if triplet[2] == k[2])
        
        numerator=(triplet_score*np.power(overall_sum,2))
        denominator = (scl_score*tissue_score*protein_score)
        score=np.power(triplet_score,alpha)*np.power((numerator/denominator),beta)
        score_dict[triplet]=score
    return score_dict

def create_csv(sorted_scores,result_file):
    """creates csv file of computed triplet with their score"""
    with open(result_file, 'w') as csvfile:
        fieldnames = ['protein', 'tissue', 'scl', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=",",lineterminator='\n')
        writer.writeheader()
        for [triplet,score] in sorted_scores:
            writer.writerow({'protein':triplet[0], 'tissue':triplet[2], 'scl':triplet[1], 'score':score})

def Zscore_data(scores):
    """computes the Z scores"""
    all_scores = []
 #   all_zscores = []
    Zscores = scores
    for triplet, score in scores.items():
        all_scores.append(score)     
#    zs = stats.zscore(all_scores)
    mu = np.mean(all_scores)
    sd = np.std(all_scores)
    for triplet, score in Zscores.items():
        Zscores[triplet] = (score- mu ) / sd
#        all_zscores.append(Zscores[triplet])
    return Zscores


if __name__ == "__main__":
    main()
