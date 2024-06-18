import os
import random
import pandas as pd

from pathlib import Path

work_dir = Path('./')
vol_path = work_dir.joinpath('./vol')
tree_path = work_dir.joinpath('./tree')
coord_path = work_dir.joinpath('./coords')

def tree_command(vol, tree_path, coord):
    if not tree_path.joinpath(vol.stem).exists():
        tree_path.joinpath(vol.stem).mkdir(parents=True)
    tree_dir = tree_path.joinpath(vol.stem)
    vol_files = sorted([f for f in vol.glob('*') if f.is_file()])
    coord_files = sorted([f for f in coord.glob('*') if f.is_file()])
    for i, (vol_file, coord_file) in enumerate(zip(vol_files, coord_files)):
        df = pd.read_csv(coord_file)
        initial_point = df.iloc[0].values
        num_end_points = random.randint(2000, 4000)
        perfusion_volume = random.randint(120000, 160000)
        gamma = random.uniform(2.15, 2.5)
        arg1 = f' -n {num_end_points}'
        arg2 = f' -a {perfusion_volume}'
        arg3 = ' -d' + ' .\\' + str(vol_file)
        arg4 = ' -o' + ' .\\' + str(tree_dir) + '\\' + f'tree_{i}.obj' # or .off
        arg5 = ' -e' + ' .\\' + str(tree_dir) + '\\' + f'tree_{i}.xml'
        arg6 = ' -x' + ' .\\' + str(tree_dir) + '\\' + f'graph_{i}.xml'
        arg7 = f' -g {gamma}'
        arg8 = ' -m 1'
        arg9 = f' -p {initial_point[0]} {initial_point[1]} {initial_point[2]}'
        command = r'C:\PersonalDocuments\projects\vascular_tree_generation\OpenCCO\build\bin\Release\generateTree3D' \
                    + arg1 \
                    + arg2 \
                    + arg3 \
                    + arg4 \
                    + arg5 \
                    + arg6 \
                    + arg7 \
                    + arg8 \
                    + arg9
        file_command = open('create_tree.bat', 'a') 
        file_command.write(command + '\n')
        file_command.close()

def main(vol_path, tree_path, coord_path):
    file_command = open('create_tree.bat', 'w') # dummy operation to create the file
    file_command.close()
    vol_dirs = sorted([f for f in vol_path.glob('*') if f.is_dir()])
    coord_dirs = sorted([f for f in coord_path.glob('*') if f.is_dir()])
    for vol, coord in zip(vol_dirs, coord_dirs):
        tree_command(vol, tree_path, coord)


if __name__ == "__main__" :
    main(vol_path, tree_path, coord_path)