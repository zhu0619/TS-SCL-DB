# delete repeated data

# pmid data



kd_obj = Tissue_triple_relation.objects.filter(source__source = "Knowledge")

kd_obj.update(review='Yes')