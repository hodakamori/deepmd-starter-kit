import glob
import os
from logging import getLogger,StreamHandler,DEBUG
import logging
import MDAnalysis as mda
import numpy as np
import argparse

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
formatter = logging.Formatter('%(asctime)s : %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.setLevel(DEBUG)
logger.addHandler(handler)


def dump_virial(data_dir):
    stress_output = glob.glob(os.path.join(data_dir, '*.stress'))
    logger.info(f'Convert {stress_output[0]=}')
    stress = np.loadtxt(stress_output[0], skiprows=1, usecols=[2, 3, 4, 5, 6, 7, 8, 9, 10])
    np.savetxt(os.path.join(data_dir, 'virial.raw'), stress, delimiter=' ')
    logger.info('Virial is successfully converted.')

def dump_box(data_dir):
    cell_output = glob.glob(os.path.join(data_dir, '*.cell'))
    logger.info(f'Convert {cell_output[0]=}')
    box = np.loadtxt(cell_output[0], skiprows=1, usecols=[2, 3, 4, 5, 6, 7, 8, 9, 10])
    np.savetxt(os.path.join(data_dir, 'box.raw'), box, delimiter=' ')
    logger.info('box is successfully converted.')

def dump_force(data_dir):
    force_output = glob.glob(os.path.join(data_dir, '*-frc-*.xyz'))
    logger.info(f'Convert {force_output[0]=}')
    u = mda.Universe(force_output[0])
    trj = np.zeros((len(u.trajectory), len(u.atoms)*3))
    for i, t in enumerate(u.trajectory):
        trj[i] = u.atoms.positions.flatten()
    np.savetxt(os.path.join(data_dir, 'force.raw'), trj, delimiter=' ')
    logger.info('Force is successfully converted.')

def dump_coords(data_dir):
    coord_output = glob.glob(os.path.join(data_dir, '*-pos-*.xyz'))
    logger.info(f'Convert {coord_output[0]=}')
    u = mda.Universe(coord_output[0])
    trj = np.zeros((len(u.trajectory), len(u.atoms)*3))
    for i, t in enumerate(u.trajectory):
        trj[i] = u.atoms.positions.flatten()
    np.savetxt(os.path.join(data_dir, 'coord.raw'), trj, delimiter=' ')
    np.savetxt(os.path.join(data_dir, 'type_map.raw'), u.atoms.elements, delimiter=' ', fmt="%s", newline=" ")
    np.savetxt(os.path.join(data_dir, 'type.raw'), np.arange(len(u.atoms.elements)), delimiter=' ', fmt="%d", newline=" ")
    logger.info('Coordinats and type are successfully converted.')

def dump_energy(data_dir):
    energy_output = glob.glob(os.path.join(data_dir, '*.ener'))
    logger.info(f'Convert {energy_output[0]=}')
    energies = np.loadtxt(energy_output[0], skiprows=1, usecols=[2, 4])
    total_energy = energies[:, 0] + energies[:, 1]
    np.savetxt(os.path.join(data_dir, 'energy.raw'), total_energy, delimiter=' ')
    logger.info('Energy is successfully converted.')

def cp2k2deepmd(data_dir):
    dump_virial(data_dir)
    dump_force(data_dir)
    dump_coords(data_dir)
    dump_energy(data_dir)
    dump_box(data_dir)

if __name__=='__main__':
    parser = argparse.ArgumentParser() 
    parser.add_argument('-i', type=str, required=True) 
    args = parser.parse_args()
    data_dir = args.i
    cp2k2deepmd(data_dir)