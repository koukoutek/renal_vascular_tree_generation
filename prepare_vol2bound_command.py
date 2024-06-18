import os

from pathlib import Path

work_dir = Path('./')
vol_path = work_dir.joinpath('./vol')
vol_boundary_path = work_dir.joinpath('./vol_boundary')

def tree_command(vol, vol_boundary_path):
    if not vol_boundary_path.joinpath(vol.stem).exists():
        vol_boundary_path.joinpath(vol.stem).mkdir(parents=True)
    vol_boundary_dir = vol_boundary_path.joinpath(vol.stem)
    vol_files = sorted([f for f in vol.glob('*') if f.is_file()])
    for i, vol_file in enumerate(vol_files):
        arg1 = ' -i' + ' .\\' + str(vol_file)
        arg2 = ' -o' + ' .\\' + str(vol_boundary_dir) + '\\' + f'vol_boundary_{i}.obj'
        command = r'C:/PersonalDocuments/projects/DGtalTools/build/converters/Release/volBoundary2obj' \
                    + arg1 \
                    + arg2 
        file_command = open('create_boundary.bat', 'a') 
        file_command.write(command + '\n')
        file_command.close()

def main(vol_path, vol_boundary_path):
    file_command = open('create_boundary.bat', 'w') # dummy operation to create the file
    file_command.close()
    vol_dirs = sorted([f for f in vol_path.glob('*') if f.is_dir()])
    for vol in vol_dirs:
        tree_command(vol, vol_boundary_path)


if __name__ == "__main__" :
    main(vol_path, vol_boundary_path)