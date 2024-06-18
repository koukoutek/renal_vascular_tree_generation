import numpy as np
import nibabel as nib
import cc3d
import pandas as pd
import os
import matplotlib.pyplot as plt

from PIL import Image
from pathlib import Path
from utils import *


work_dir = Path('./')
nifti_file = work_dir.joinpath('./nifti')
pgm_file = work_dir.joinpath('./pgm')
coord_file = work_dir.joinpath('./coords')

def nifti2pgm(nifti_file, pgm_file, coord_file):
    image = nib.load(nifti_file)
    file_num = nifti_file.stem.split('.')[0] # get the seg id
    header = image.header
    affine = image.affine
    data = image.get_fdata()
    data[data != 0] = 1 # binarize the tumor/cyst/organ mask

    # data = np.transpose(data, (0, 2, 1)) # kits23 data convention
    data = np.transpose(data, (1, 0, 2)) # in-house arterial data convention

    # get the 2 kidneys separately
    kidneys = cc3d.largest_k(data, k=2, connectivity=26, delta=0, return_N=False)
    values = np.unique(kidneys)
    num_segments = len(values) - 1 # 0 is background
    if num_segments != 2:
        print(f'Error: {num_segments} segments found in {nifti_file}')
        return
    segment_1 = kidneys == 1
    segment_2 = kidneys == 2

    # interpolate the segment to have 1mm isotropic voxels for in-house data
    segment_1 = interpolate_image(segment_1.astype(np.float32), header['pixdim'][3], header['pixdim'][1], header['pixdim'][2], [1, 1, 1])
    segment_2 = interpolate_image(segment_2.astype(np.float32), header['pixdim'][3], header['pixdim'][1], header['pixdim'][2], [1, 1, 1])
    segment_1[segment_1 < 0.5] = 0
    segment_2[segment_2 < 0.5] = 0
    segment_1[segment_1 >= 0.5] = 1
    segment_2[segment_2 >= 0.5] = 1

    segment_1 = (segment_1*255).astype(np.uint8)
    segment_2 = (segment_2*255).astype(np.uint8)

    # crop the segment around its borders
    indx_1 = np.argwhere(segment_1 == 255)
    z_crop = np.min(indx_1[:, 2]) - 10, np.max(indx_1[:, 2]) + 10
    y_crop = np.min(indx_1[:, 1]) - 10, np.max(indx_1[:, 1]) + 10
    x_crop = np.min(indx_1[:, 0]) - 10, np.max(indx_1[:, 0]) + 10
    segment_1 = segment_1[x_crop[0]:x_crop[1], y_crop[0]:y_crop[1], z_crop[0]:z_crop[1]]

    # choose initial point for the tree generation
    indx_1n = np.argwhere(segment_1 == 255)
    # pos_z_1 = ((np.max(indx_1n[:, 2]) + np.min(indx_1n[:, 2])) // 2) - 7
    # pos_x_1 = np.min(indx_1n[:, 1]) + 15
    # pos_y_1 = (np.max(indx_1n[:, 0]) + np.min(indx_1n[:, 0])) // 2 + 15
    min_x = indx_1n[indx_1n[:,1] == np.min(indx_1n[:,1])] # get the min x coord
    pos_x_1 = min_x[0, 0]
    pos_y_1 = min_x[0, 1]
    pos_z_1 = int(min_x[:, 2].mean()) 

    # crop the segment around its borders
    indx_2 = np.argwhere(segment_2 == 255)
    z_crop = np.min(indx_2[:, 2]) - 10, np.max(indx_2[:, 2]) + 10
    y_crop = np.min(indx_2[:, 1]) - 10, np.max(indx_2[:, 1]) + 10
    x_crop = np.min(indx_2[:, 0]) - 10, np.max(indx_2[:, 0]) + 10
    segment_2 = segment_2[x_crop[0]:x_crop[1], y_crop[0]:y_crop[1], z_crop[0]:z_crop[1]]

    # choose initial point for the tree generation
    indx_2n = np.argwhere(segment_2 == 255)
    # pos_z_2 = ((np.max(indx_2n[:, 2]) + np.min(indx_2n[:, 2])) // 2) - 7
    # pos_x_2 = np.max(indx_2n[:, 1]) - 15
    # pos_y_2 = (np.max(indx_2n[:, 0]) + np.min(indx_2n[:, 0])) // 2 + 15
    max_x = indx_2n[indx_2n[:,1] == np.max(indx_2n[:,1])] # get the max x coord
    pos_x_2 = max_x[0, 0]
    pos_y_2 = max_x[0, 1]
    pos_z_2 = int(max_x[:, 2].mean())   

    try:
        if not pgm_file.joinpath(file_num).joinpath('segment_1').exists():
            pgm_file.joinpath(file_num).joinpath('segment_1').mkdir(parents=True)
        if not pgm_file.joinpath(file_num).joinpath('segment_2').exists():
            pgm_file.joinpath(file_num).joinpath('segment_2').mkdir(parents=True)
        if not coord_file.joinpath(file_num).exists():
            coord_file.joinpath(file_num).mkdir(parents=True)
        if not coord_file.joinpath(file_num).exists():
            coord_file.joinpath(file_num).mkdir(parents=True)
        for i in range(segment_1.shape[2]):
            pil_image_1 = Image.fromarray(segment_1[:,:,i])
            pil_image_1.save(pgm_file / file_num / 'segment_1' / f'slice_{i}.pgm')
        df = pd.DataFrame({'x': [pos_x_1], 'y': [pos_y_1], 'z': [pos_z_1]})
        df.to_csv(coord_file / file_num / 'coords_0.csv', index=False)
        for i in range(segment_2.shape[2]):
            pil_image_2 = Image.fromarray(segment_2[:,:,i])
            pil_image_2.save(pgm_file / file_num / 'segment_2' / f'slice_{i}.pgm')
        df = pd.DataFrame({'x': [pos_x_2], 'y': [pos_y_2], 'z': [pos_z_2]})
        df.to_csv(coord_file / file_num / 'coords_1.csv', index=False)
        print(f'PGM files saved to {pgm_file}')
    except Exception as e:
        print(f'Error: {e}')

    return 

def main(nifti_file, pgm_file, coord_file):
    nifti_files = sorted([f for f in nifti_file.glob('*.nii*')])
    for nifti_file in nifti_files:
        nifti2pgm(nifti_file, pgm_file, coord_file)

if __name__ == '__main__':
    main(nifti_file, pgm_file, coord_file)