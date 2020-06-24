from astropy.io import fits
import matplotlib.pyplot as plt
import os
import numpy as np
import sys

def get_dark():
	dark_lists = {}
	raw_dark_dir = '/global/cfs/cdirs/desi/spectro/data/'
	#recent_exps = [20200607,20200608,20200609]
	recent_exps = os.listdir(raw_dark_dir)
	length = len(recent_exps)
	print('--------------------Searching for Dark Frames--------------------')
	for i,date in enumerate(recent_exps):
	    print(f'{i}/{length}', end = '\r')
	    if str(date) != 'README.html':
	        exp_ids = os.listdir(os.path.join(raw_dark_dir,str(date)))
	        for exp_id in exp_ids:
	            exp_dir = os.path.join(raw_dark_dir,str(date),str(exp_id))
	            files = os.listdir(exp_dir)
	            for f in files:
	                if 'desi-' in f:
	                    f_dir = os.path.join(exp_dir,f)
	                    with fits.open(f_dir) as hdul:
	                        try:
	                            obstype = hdul[1].header['OBSTYPE']
	                            if obstype == 'DARK':
	                                dark_lists[exp_id] = f_dir
	                        except:
	                            pass
	    else: continue
	                        
	np.save('/global/homes/k/kgb0255/packages/deepcr/dark_lists.npy', np.array(dark_lists))

	return None

def get_dark_preproc():
	preproc_dir = '/global/cfs/cdirs/desi/spectro/redux/andes/preproc/'
	recent_exps = os.listdir(preproc_dir)
	length = len(recent_exps)

	dark_lists = np.load('/global/homes/k/kgb0255/packages/deepcr/dark_lists.npy', allow_pickle = True)[()]
	dark_ids = list(dark_lists.keys())
	dark_preproc = {}

	print('\n----Matching existing dark frames with the preprocessed data-----')
	for i,date in enumerate(recent_exps):
		print(f'{i}/{length}', end = '\r')
		exp_ids = os.listdir(os.path.join(preproc_dir,str(date)))
		for exp_id in exp_ids:
			if exp_id in dark_ids:
				preproc_dir = os.path.join(preproc_dir,str(date),exp_id)
				_dir = dark_lists[exp_id]
				dark_preproc[exp_id] = (_dir,preproc_dir)
			else: continue

	np.save('/global/homes/k/kgb0255/packages/deepcr/dark_preproc.npy', np.array(dark_preproc))

	return None


if __name__== '__main__':
	update = sys.argv[1]
	query_type = sys.argv[2]

	if update:
		get_dark()
		get_dark_preproc()
	else: pass
	
	if query_type == 'dark':
		get_dark()
	
	elif query_type == 'dark_preproc':
		f_exist = os.isfile('/global/homes/k/kgb0255/packages/deepcr/dark_lists.npy')
		if f_exist:
			get_dark_preproc()
		else: 
			get_dark()
			get_dark_preproc()



