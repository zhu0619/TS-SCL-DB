tissue_data <- read_csv("~/Desktop/Lu_work/text-mining-project/TSCL-DB/mysite/polls/raw_data/new results2018/pmids_abs_Zscore_all_tissueCL_scl_pubmed_ID.txt_Tissue_2018-01-24_a_0.8_ws_3_wa_0.2_human.csv")

head(tissue_data)
summary(tissue_data)
#nb of abstracts
nb_abs = length(unique(tissue_data[,'PMID']))

tissue_data_bis <- read_csv("~/Desktop/Lu_work/text-mining-project/TSCL-DB/mysite/polls/raw_data/new results2018/Zscore_all_tissueCL_scl_pubmed_ID.txt_Tissue_2018-01-24_a_0.8_ws_3_wa_0.2_human.csv")
head(tissue_data_bis)

score = tissue_data_bis[,'score']
length(which(score<=0))
length(which(score>0))
length(which(score>=0 & score <0.5))
length(which(score>=0.5 & score <1))
length(which(score>=1 & score <3))
length(which(score>=3))
nrow(score)

nrow(unique(tissue_data_bis[which(score>=0),'protein']))

nrow(unique(tissue_data_bis[which(score<0),'tissue']))
nrow(unique(tissue_data_bis[which(score<0),'scl']))
nrow(unique(tissue_data_bis[which(score<0),'protein']))

nrow(unique(tissue_data_bis[which(score>=0 & score <0.5),'tissue']))
nrow(unique(tissue_data_bis[which(score>=0 & score <0.5),'scl']))
nrow(unique(tissue_data_bis[which(score>=0 & score <0.5),'protein']))

nrow(unique(tissue_data_bis[which(score>=0.5 & score <1),'tissue']))
nrow(unique(tissue_data_bis[which(score>=0.5 & score <1),'scl']))
nrow(unique(tissue_data_bis[which(score>=0.5 & score <1),'protein']))

nrow(unique(tissue_data_bis[which(score>=1 & score <3),'tissue']))
nrow(unique(tissue_data_bis[which(score>=1 & score <3),'scl']))
nrow(unique(tissue_data_bis[which(score>=1 & score <3),'protein']))

nrow(unique(tissue_data_bis[which(score>=3),'tissue']))
nrow(unique(tissue_data_bis[which(score>=3),'scl']))
nrow(unique(tissue_data_bis[which(score>=3),'protein']))
