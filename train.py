from deepCR import deepCR
from deepCR import train
import matplotlib.pyplot as plt
from astropy.io import fits
import os
import numpy as np
import gc

if __name__ == '__main__':
    data_dir = os.path.join(os.environ.get('DEEPCR_DIR'),'more_filters')
    test_data_dir = os.path.join(data_dir,'test_segmented_data.npy')
    train_data_dir = os.path.join(data_dir,'training_segmented_data.npy')
    print('Loading data...\n')
    train_data = np.load(train_data_dir, allow_pickle = True)[()]
    print('Data loaded...\n')
    images = []
    masks = []
    ignores = []
    length = len(list(train_data.keys()))
    print('Data parsing...\n')
    for i,val in enumerate(train_data.values()):
        print(f'{i+1}/{length}', end = '\r')
        img, mask, ign = val
        images.append(img)
        mask = np.ones_like(mask) - mask
        ign = np.ones_like(ign).astype(int) - ign
        masks.append(mask)
        ignores.append(ign)
        del img, mask, ign

    train_images = np.array(images)
    train_masks = np.array(masks)
    train_ignores = np.array(ignores)
    print('Data parsed...\n')
    del train_data, images, masks, ignores
    
    gc.collect()
    # images = []
    # masks = []
    # ignores = []

    # for val in test_data.values():
    #   img, mask, ign = val
    #   images.append(img)
    #   mask = np.ones_like(mask) - mask
    #   masks.append(mask)
    #   ignores.append(ign)
    #   del img, mask, ign

    # test_images = np.array(images)
    # test_masks = np.array(masks)
    # test_ignores = np.array(ignores)

    # del test_data, images, masks, ignores
    print('Training...\n')
    trainer = train(train_images, train_masks, ignore = train_ignores, name='with_ign', gpu=True, epoch=50, 
                    save_after=20, plot_every=10, use_tqdm=False)
    
    del train_images, train_masks
    gc.collect()
    trainer.train()
    f_name = trainer.save()
    np.save('with_ign_loss.npy',np.array(trainer.validation_loss))

    #trainer = train(train_images, train_masks, ignore=train_ignores,name='with_ign', gpu=True, epoch=1,
                    # save_after=1, plot_every=10, use_tqdm=False)
    #trainer.train()
    #f_name = trainer.save()
    #np.save('w/o_ign_loss.npy',np.array(trainer.validation_loss))




