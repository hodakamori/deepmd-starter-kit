from cp2k2deepmd import cp2k2deepmd
import dpdata

cp2k2deepmd('./cp2k')
d = dpdata.LabeledSystem('./cp2k', fmt='deepmd/raw')
print(d)
d.to('deepmd/npy', './cp2k', set_size=d.get_nframes())
