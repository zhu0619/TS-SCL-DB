#!/bin/bash

python manage.py shell <  ts_scl_db/load_dictionary.py
echo 'dictionaries are imported!'
python manage.py shell <  ts_scl_db/load_data_resource.py
echo 'data resource are loaded'

python manage.py shell <  ts_scl_db/load_SCL_data.py
echo 'scl information are imported'


python manage.py shell <  ts_scl_db/load_tissue_data.py
echo 'tissue information are imported'

python manage.py shell <  ts_scl_db/load_knowledge_data.py
echo 'load_knowledge_data finished'

python manage.py shell < ts_scl_db/load_HPA.py
echo 'load_HPA old data finished'

python manage.py shell <  ts_scl_db/load_HPA_bis.py
echo 'load_HPA new finished'

python manage.py shell < load_pmid_meta_data.py
echo 'load_pmid_meta_data finished'