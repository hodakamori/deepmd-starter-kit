from cp2k2deepmd import cp2k2deepmd
import dpdata
import glob

for output_dir in glob.glob('./train_data/*'):
    cp2k2deepmd(output_dir)
    d = dpdata.LabeledSystem(output_dir, fmt='deepmd/raw')
    d.to('deepmd/npy', output_dir, set_size=d.get_nframes())
