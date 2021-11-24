import MDAnalysis as mda
import os
import shutil
import subprocess as sub

def write_trj_as_cp2k_input(system_name, cell, types, type_map, positions):

    types = [type_map[t] for t in types]
    positions = positions.astype('str')
    with open(system_name, 'w') as fo:
        fo.write('&CELL\n')
        fo.write(f'  ABC {cell[0]} {cell[1]} {cell[2]}\n')
        fo.write(f'  ALPHA_BETA_GAMMA {cell[3]} {cell[4]} {cell[5]}\n')
        fo.write('&END CELL\n')
        fo.write('&COORD\n')
        for t, (x, y, z) in zip(types, positions):
            fo.write(' '.join(['  ', t, x, y, z, '\n']))
        fo.write('&END COORD\n')

def modify_input(cp2k_input, prj_name):
    with open(cp2k_input, 'r') as fi:
        cfg = fi.read()
    cfg = cfg.replace('@SET PRJ train', f'@SET PRJ {prj_name}')
    with open(cp2k_input, 'w') as fo:
        fo.write(cfg)

lammps_trj = './example/lammps/water.lammpstrj'
cp2k_format_dir = './cp2k_format'
u = mda.Universe(lammps_trj, format="LAMMPSDUMP")
type_map = {"1":'O', "2":'H'}

for i, t in enumerate(u.trajectory):
    os.makedirs(f'train_data/train_{i}', exist_ok=True)
    shutil.copy("./cp2k_format/train.inp", f'train_data/train_{i}/water_{i}.inp')
    for item in ['cp2k.dft', 'cp2k.dump', 'cp2k.potentials', 'cp2k.kinds']:
        shutil.copy(os.path.join(cp2k_format_dir, item), f'train_data/train_{i}/')
    write_trj_as_cp2k_input(f'train_data/train_{i}/water_{i}.system', u.dimensions, u.atoms.types, type_map, u.atoms.positions)
    modify_input(f'train_data/train_{i}/water_{i}.inp', f'water_{i}')
