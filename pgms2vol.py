import os
import subprocess

from pathlib import Path
from natsort import natsorted

work_dir = Path('./')
pgm_path = work_dir.joinpath('./pgm')
vol_path = work_dir.joinpath('./vol')

def pgm2vol(pgm_file, vol_path):
    pgm_dirs = [f for f in pgm_file.glob('*') if f.is_dir()]
    pgm_images = natsorted([natsorted([f for f in pgm_dir.glob('*')]) for pgm_dir in pgm_dirs]) # list of lists of pgm files

    vol_path = vol_path.joinpath(str(pgm_images[0][0]).split('\\')[1])
    if not vol_path.exists():
        vol_path.mkdir(parents=True)

    for i, pgm_image in enumerate(pgm_images):
        vol_file = vol_path.joinpath(f'volume_{i}.vol')
        pgm_args = ' .\\'.join([str(pgm) for pgm in pgm_image])
        arg1 = ' -i ' + '.\\' + pgm_args
        arg2 = ' -o ' + '.\\' + str(vol_file)

        command = r'C:/PersonalDocuments/projects/DGtalTools/build/converters/Release/slice2vol.exe' + arg1 + arg2
        file_command = open('create_vol.bat', 'a') 
        file_command.write(command + '\n')
        file_command.close()

def main(pgm_path, vol_path):
    file_command = open('create_vol.bat', 'w') # dummy operation to create the file
    file_command.close()
    pgm_files = sorted([f for f in pgm_path.glob('*') if f.is_dir()])
    for pgm_file in pgm_files:
        pgm2vol(pgm_file, vol_path)


if __name__ == "__main__" :
    main(pgm_path, vol_path)