from astropy.io import fits
import matplotlib.pyplot as plt
import os
import numpy as np

dark_lists = {}
dat_dir = '/global/cfs/cdirs/desi/spectro/data/'
recent_exps = [20200607,20200608,20200609]
for date in recent_exps:
    exp_ids = os.listdir(os.path.join(dat_dir,str(date)))
    for exp_id in exp_ids:
        exp_dir = os.path.join(dat_dir,str(date),str(exp_id))
        files = os.listdir(exp_dir)
        for f in files:
            if 'desi-' in f:
                f_dir = os.path.join(exp_dir,f)
                with fits.open(f_dir) as hdul:
                    obstype = hdul[1].header['OBSTYPE']
                    if obstype == 'DARK':
                        dark_lists[exp_id] = f_dir
                        
np.save('/global/homes/k/kgb0255/packages/deepcr/dark_lists.npy', np.array(dark_lists))
