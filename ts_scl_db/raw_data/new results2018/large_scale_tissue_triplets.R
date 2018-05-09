
## Evaluation 

# library('mygene')
#-------------------------------------------------#

args = c('DB_result/new/Zscore_all_tissueCL_scl_pubmed_ID.txt_Tissue_2018-01-02_a_0.6_ws_3_wa_0.2_human.csv',
         'HPA_CellLine_SCL_ground_truth.csv', 'empty', 'hpa_go_scl_map_with_celljunction.txt', 'TRUE')
args = c('DB_result/new/Zscore_all_tissueCL_scl_pubmed_ID.txt_Tissue_2018-01-02_a_0.6_ws_0.2_wa_3_human.csv',
         'HPA_CellLine_SCL_ground_truth.csv', 'empty', 'hpa_go_scl_map_with_celljunction.txt', 'TRUE')

file_result= args[1]
benchmark= args[2]
pre_mapped_file= args[3]
go_goals_file = args[4]
refresh = args[5]

# evaluation = function(file_result,benchmark,pre_mapped_file,go_goals_file,refresh){
library('ROCR')
library('pROC')

  #--------------------------------------------------------------#
  
  pre_result = read.csv(file_result)
  head(pre_result)
  nrow(pre_result)
  
  result_eva = na.omit(pre_result)[,c('protein','scl','tissue','score')]
  
  #----------------#
  predicted_gene = as.character(unique(result_eva[,'protein']))
  print(paste0(length( predicted_gene),' genes.'))
  predicted_GO = as.character(unique(result_eva[,'scl']))
  print(paste0(length(predicted_GO),' scls.'))
  predicted_BTO = as.character(unique(result_eva[,'tissue']))
  print(paste0(length(predicted_BTO),' tissues.'))

  #----------------#  
  summary(result_eva[,'score'])
  
  # for CellLine_mined_distribution.pdf
  dens <- density(result_eva[,'score'])
  # pdf('/Users/zhulu/Desktop/Lu_work/Thesis/Lu-phd-thesis-draft_131107/Chapter5/Figs/CellLine_mined_distribution.pdf'
  # ,height = 5.8,width = 8.3 )
  plot(dens,xlim=c(-1,2),main = "",xlab='Scores')
  po = which.max(dens$y)
  grid()
  polygon(c(dens$x[1:po],dens$x[po]),c(dens$y[1:po],0), col="darkgrey", border='darkgrey',xlim=c(-1,5))
  polygon(c(dens$x[po],dens$x[po:length(dens$x)]),c(0,dens$y[po:length(dens$y)]), col="steelblue", border='grey',xlim=c(-1,5))
  axis(1, at=-0.5,labels='-0.5', las=1)
  legend('topright', pch=15,col=c("darkgrey","steelblue"),c("Background","Positive"),bt='n')
  
  scores = result_eva[,'score']
  nb = length(scores[scores<dens$x[po]])
  interval = c(dens$x[po],0,0.5,1,3)
  for(x in 1:length(interval)){
    y = x+1
    lower = interval[x]
    upper = interval[y]
    nb = c(nb,length(scores[scores>=lower & scores<upper]))
  }
  # nb=c(nb,length(scores[scores>3]))
  names(nb) = c(paste0('< ',round(dens$x[po],2)),paste0(round(dens$x[po],2),'~',0),paste0(0,'~',0.5),paste0(0.5,'~',1),paste0(1,'~',3),paste0('>',3))
  
  
  
  ## for CellLine_mined_distribution.pdf
  darkgrey = rgb(128, 128, 128,max=255,alpha = 128)
  steelblue = rgb(0, 89, 179,max=255,alpha = 200)
  dens <- density(result_eva[,'score'])
  # pdf('/Users/zhulu/Desktop/Lu_work/Thesis/Lu-phd-thesis-draft_131107/Chapter5/Figs/CellLine_mined_distribution.pdf'
  # ,height = 5.8,width = 8.3 )
  plot(dens,xlim=c(-1,2),main = "",xlab='Scores')
  # po = which.max(dens$y)
  po = min(which(dens$x>0))
  grid()

  polygon(c(dens$x[1:po],dens$x[po]),c(dens$y[1:po],0), col=darkgrey, border=grey ,xlim=c(-1,5))
  polygon(c(dens$x[po],dens$x[po:length(dens$x)]),c(0,dens$y[po:length(dens$y)]), col=steelblue, border='grey',xlim=c(-1,5))
  axis(1, at=-0.5,labels='-0.5', las=1)
  legend('topright', pch=15,col=c(darkgrey,steelblue),c("Background","Positive"),bt='n')
  
  scores = result_eva[,'score']
  nb = length(scores[scores<dens$x[po]])
  interval = c(dens$x[po],0,0.5,1,3)
  for(x in 1:length(interval)){
    y = x+1
    lower = interval[x]
    upper = interval[y]
    nb = c(nb,length(scores[scores>=lower & scores<upper]))
  }
  # nb=c(nb,length(scores[scores>3]))
  names(nb) = c(paste0('< ',round(dens$x[po],2)),paste0(round(dens$x[po],2),'~',0),paste0(0,'~',0.5),paste0(0.5,'~',1),paste0(1,'~',3),paste0('>',3))
  
  
  