# change the source name 
objets = Tissue_triple_relation.objects.filter(source__source='text-mining-test')

source_obj = Data_source.objects.get(source='Text-mining')
objets.update(source=source_obj)


