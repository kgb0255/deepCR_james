from deepCR import deepCR
from deepCR import evaluate
import os
import numpy as np
import gc
import sys

def test(mdl_name,test_data_dir,save_path):
    print('Loading data...\n')
    test_data = np.load(test_data_dir, allow_pickle = True)[()]
    print('Data loaded...\n')

    images = []
    masks = []
    ignores = []
    length = len(list(test_data.keys()))
    print('Data parsing...\n')
    for i,val in enumerate(test_data.values()):
        print(f'{i+1}/{length}', end = '\r')
        img, mask, ign = val
        images.append(img)
        mask = np.ones_like(mask) - mask
        ign = np.ones_like(ign).astype(int) - ign
        masks.append(mask)
        ignores.append(ign)
        del img, mask, ign

    test_images = np.array(images)
    test_masks = np.array(masks)
    test_ignores = np.array(ignores)
    print('Data parsed...\n')
    del test_data, images, masks, ignores
    
    gc.collect()

    print('Model loading...\n')
    mdl = deepCR(mask=f'/global/home/users/kgb0255/projects/deepCR/james_codes/{mdl_name}/{mdl_name}.pth', hidden=32)
    
    print('Model testing...\n')
    tpr, fpr = evaluate.roc(mdl, image = test_images, mask = test_masks, ignore = test_ignores)
    
    np.save(save_path,np.array([tpr,fpr]))
    return

if __name__ == '__main__':
    mdl_name = sys.argv[1]
    if '.pth' in mdl_name:
        idx = mdl_name.index('.pth')
        mdl_name = mdl_name[:idx]

    dataset = sys.argv[2]
    _type = sys.argv[3]

    if _type == 'total':
        data_dir = os.path.join(os.environ.get('DEEPCR_DIR'),dataset)
        test_data_dir = os.path.join(data_dir,'test_segmented_data.npy')
        if not os.path.exists(f'/global/home/users/kgb0255/projects/deepCR/james_codes/{mdl_name}/testing/{dataset}/{_type}'):
            os.makedirs(f'/global/home/users/kgb0255/projects/deepCR/james_codes/{mdl_name}/testing/{dataset}/{_type}')
        save_path = f'/global/home/users/kgb0255/projects/deepCR/james_codes/{mdl_name}/testing/{dataset}/{_type}/tpr_fpr_{mdl_name}_{dataset}_{_type}_testing.npy'
        test(mdl_name,test_data_dir, save_path)


    elif _type == 'categorized':
        data_dir = os.path.join(os.environ.get('DEEPCR_DIR'),dataset,'categorized_testing')
        test_data_lists = os.listdir(data_dir)
        for test_data_dir in test_data_lists:
            if '.npy' in test_data_dir:
                if 'eg_field' in test_data_dir:
                    category = 'eg_field'
                elif 'globular' in test_data_dir:
                    category = 'globular_cluster'
                elif 'resolved_gal' in test_data_dir:
                    category = 'resolved_gal'
                else:
                    raise ValueError
                print(f'Categorized Testing: {category}\n')
                if not os.path.exists(f'/global/home/users/kgb0255/projects/deepCR/james_codes/{mdl_name}/testing/{dataset}/{_type}'):
                    os.makedirs(f'/global/home/users/kgb0255/projects/deepCR/james_codes/{mdl_name}/testing/{dataset}/{_type}')
                
                save_path = f'/global/home/users/kgb0255/projects/deepCR/james_codes/{mdl_name}/testing/{dataset}/{_type}/tpr_fpr_{mdl_name}_{dataset}_{_type}.{category}_testing.npy'
                test_data_dir = os.path.join(data_dir,test_data_dir)
                test(mdl_name,test_data_dir, save_path)

            else: continue

    else:
        raise ValueError 
