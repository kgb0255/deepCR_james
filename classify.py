import numpy as np
import os
import sys

if __name_ == '__main__':
    paper = sys.arvg[1] == 'paper'
    if paper:
        sub_path = 'paper'
    else:
        sub_path = 'more_filters'


    data_dir = os.environ.get('DEEPCR_DIR')
    data_dir = os.path.join(data_dir,sub_path,'test_segmented_data.npy')
    print(data_dir)
    test_set = np.load(data_dir, allow_pickle = True)[()]
    keys = list(test_set.keys())

    eg_field = {}
    globular = {}
    resolved_gal = {}
    i = 0
    if paper:
        for k in keys:
            idx = k.index('_')
            k2 = k[:idx]
            if '44' in k2:
                eg_field[k] = test_set[k]
                i+=1
            elif '06' in k2 or '09' in k2:
                globular[k] = test_set[k]
                i+=1
            elif '28' in k2:
                resolved_gal[k] = test_set[k]
                i+=1
    else:
        for k in keys:
            idx = k.index('_')
            k2 = k[:idx]
            if 'j96q' in k2:
                resolved_gal[k] = test_set[k]
                i+=1
            elif 'jcdm' in k2:
                resolved_gal[k] = test_set[k]
                i+=1
            elif 'jb16' in k2:
                globular[k] = test_set[k]
                i+=1
            elif 'jc3f' in k2:
                eg_field[k] = test_set[k]
                i+=1
            elif 'j6lp' in k2:
                globular[k] = test_set[k]
                i+=1
            elif 'jbfl' in k2:
                eg_field[k] = test_set[k]
                i+=1
            elif 'jc8m' in k2:
                eg_field[k] = test_set[k]
                i+=1
            elif 'jcoy' in k2:
                resolved_gal[k] = test_set[k]
                i+=1
            elif 'j8xi' in k2:
                eg_field[k] = test_set[k]
                i+=1
            elif 'jcnw' in k2:
                resolved_gal[k] = test_set[k]
                i+=1
            elif 'j9l9' in k2:
                globular[k] = test_set[k]
                i+=1
            elif 'jbqj' in k2:
                globular[k] = test_set[k]
                i+=1

    assert i == len(keys)

    save_path_eg = os.path.join(os.environ.get('DEEPCR_DIR'),sub_path,'categorized_testing','test_eg_field.npy')
    save_path_glob = os.path.join(os.environ.get('DEEPCR_DIR'),sub_path,'categorized_testing','test_globular_cluster.npy')
    save_path_gal = os.path.join(os.environ.get('DEEPCR_DIR'),sub_path,'categorized_testing','test_resolved_gal.npy')

    np.save(save_path_gal,np.array(resolved_gal))
    np.save(save_path_glob,np.array(globular))
    np.save(save_path_eg,np.array(eg_field))
