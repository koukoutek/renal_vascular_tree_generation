import os

from pathlib import Path

vol_boundary_path = Path('./vol_boundary')
merged_obj_path = Path('./merged_obj')
tree_path = Path('./tree')

def boundary_tree_merge_command(vol_boundary, merged_obj_path, tree_path):
    if not merged_obj_path.joinpath(vol_boundary.stem).exists():
        merged_obj_path.joinpath(vol_boundary.stem).mkdir(parents=True)
    merged_obj_dir = merged_obj_path.joinpath(vol_boundary.stem)
    vol_boundary_files = sorted([f for f in vol_boundary.glob('*') if f.is_file() and f.suffix == '.obj'])
    tree_files = sorted([f for f in tree_path.joinpath(vol_boundary.stem).glob('*') if f.is_file() and f.suffix == '.obj'])
    for i, (vol_boundary_file, tree_file) in enumerate(zip(vol_boundary_files, tree_files)):
        arg1 = ' -i' + ' .\\' + str(tree_file)
        arg2 = ' -a' + ' .\\' + str(vol_boundary_file)
        arg3 = ' -o' + ' .\\' + str(merged_obj_dir) + '\\' + f'merged_boundary_tree_{i}.obj'
        arg4 = ' --nameGrp1  vessel'
        arg5 = ' --nameGrp2  kidney'
        arg6 = ' --materialOne 0.7 0.2 0.2 1.0'
        arg7 = ' --materialTwo 0.4 0.4 0.5 0.2'
        command = r'C:\PersonalDocuments\projects\vascular_tree_generation\OpenCCO\build\tools\Release\mergeObj' \
                    + arg1 \
                    + arg2 \
                    + arg3 \
                    + arg4 \
                    + arg5 \
                    + arg6 \
                    + arg7
        file_command = open('merge_boundary_tree.bat', 'a') 
        file_command.write(command + '\n')
        file_command.close()

def main(vol_boundary_path, merged_obj_path, tree_path):
    file_command = open('merge_boundary_tree.bat', 'w') # dummy operation to create the file
    file_command.close()
    vol_boundary_dirs = sorted([f for f in vol_boundary_path.glob('*') if f.is_dir()])
    for vol_boundary in vol_boundary_dirs:
        boundary_tree_merge_command(vol_boundary, merged_obj_path, tree_path)


if __name__ == "__main__" :
    main(vol_boundary_path, merged_obj_path, tree_path)