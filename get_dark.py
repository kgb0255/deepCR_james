from astropy.io import fits
import matplotlib.pyplot as plt
import os
import numpy as np
import sys

def get_raw(search_type):
    '''
    Get raw images 

    param search_type: obstype to retreive - either 'DARK' or 'SCIENCE'
    '''
    raw_lists = {}
    raw_dir = '/global/cfs/cdirs/desi/spectro/data/'
    #recent_exps = [20200607,20200608,20200609]
    recent_exps = os.listdir(raw_dir)
    length = len(recent_exps)
    for i,date in enumerate(recent_exps):
        print(f'{i}/{length}', end = '\r')
        if str(date) != 'README.html':
            exp_ids = os.listdir(os.path.join(raw_dir,str(date)))
            for exp_id in exp_ids:
                exp_dir = os.path.join(raw_dir,str(date),str(exp_id))
                files = os.listdir(exp_dir)
                for f in files:
                    if 'desi-' in f:
                        f_dir = os.path.join(exp_dir,f)
                        with fits.open(f_dir) as hdul:
                            try:
                                obstype = hdul[1].header['OBSTYPE']
                                if obstype == search_type:
                                    raw_lists[exp_id] = f_dir
                            except:
                                pass
        else: continue
                            
    np.save(f'/global/homes/k/kgb0255/packages/deepcr/raw_lists_{search_type}.npy', np.array(raw_lists))

    return None

def get_preproc():
    '''
    Cross search the preprocessed science images based on the raw sceince images.

    '''
    science_lists = np.load('/global/homes/k/kgb0255/package/deepcr/raw_lists_SCIENCE.npy', allow_pickle = True)[()]
    preproc_dir = '/global/cfs/cdirs/desi/spectro/redux/andes/preproc/'
    preproc_lists = {}

    recent_exps = os.listdir(preproc_dir)
    length = len(recent_exps)
    for i, date in enumerate(recent_exps):
        print(f'{i}/{length}', end = '\r')
        exp_ids = os.listdir(os.path.join(preproc_dir,str(date)))
        for exp_id in exp_ids:
            exp_dir = os.path.join(preproc_dir,str(date),str(exp_id))
            files = os.listdir(exp_dir)
            preproc_files = []
            for f in files:
                if 'preproc' in f:
                    preproc_files.append(os.path.join(exp_dir,f))

            preproc_lists[exp_id] = preproc_files

    np.save(f'/global/homes/k/kgb0255/packages/deepcr/preproc_lists.npy',np.array(preproc_lists))

    return None


if __name__== '__main__':
    update = sys.argv[1] == 'True'
    search_type = sys.argv[2]

    if update:
        get_raw('DARK')
        get_raw('SCIENCE')
        get_preproc()
    
    else:
        if search_type == 'dark':
            get_raw('DARK')

        elif search_type == 'raw_science':
            get_raw('SCIENCE')

        elif search_type == 'preproc_science':
            f_exist = os.path.isfile('/global/homes/k/kgb0255/packages/deepcr/raw_lists_SCIENCE.npy')
            if f_exist:
                get_preproc()
            else:
                get_raw('SCIENCE')
                get_preproc()



