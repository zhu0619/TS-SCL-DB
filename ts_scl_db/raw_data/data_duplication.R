bto = read.csv('bto_filtered_090118.vocab.txt',sep='\t',header = F)
head(bto)
words = bto[,2]

bto[bto[,2] %in% words[duplicated(words)],]



bto = read.csv('subcellular_go_2211.vocab.txt',sep='\t',header = F)
head(bto)
words = bto[,2]

dup = words[duplicated(words)] 

bto[bto[,2] %in% dup,]
