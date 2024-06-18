How to run the project
1.  Run nifti2pgm.py in order to convert nifti images to pgm format (will crop images around the kidneys)
2.  Run pgms2vol.py in order to prepare the bash command for pgm to vol convertion
3   Run create_vol.bat file. This converts the stack of 2D pgm images to a 3D .vol file
4.  Run prepare_tree_command.py to construct the bash command for 3D vascular tree generation
5.  Run create_tree.bat command. This generates the 3D vascular tree based on the .vol files
6.  Optionally, run the prepare_vol2bound_command.py in order to prepare the bash command for .vol to boundary convertion
7.  Run create_boundary.bat in order to generate the boundary file from the 3D .vol file (extracts the boundary)
8.  Run prepare_merge_boundary_tree.py to construct the bash command for merging the boundary file with the 3D vascular tree
9.  Run merge_boundary_tree.bat to construct the merged object (boundary + 3D tree)

For plotting the bifurcation level / radius 
10. Run xml2graph on the exported XML graph (xml2graph in OpenCCO/build/tools/graphAnalysis) to create .dat files 
11. Run graph2statBifRad stat.dat vertex.dat edges.dat radius.dat (graph2statBifRad in OpenCCO/build/tools/graphAnalysis) to create the stat.dat
12. Run gnuplot plotStatRadius.plt (plotStatRadius in OpenCCO/.ipol/helpers/) to create the final .pdf file with the plot