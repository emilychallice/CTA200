#!/usr/bin/python3
import numpy as np
import struct

def get_particle_positions(filename):
	f = open(filename, "rb")
	Npart = {"gas":0, "halo":0, "disk":0, "bulge":0, "stars":0, "bndry":0}
	positions = {"gas":[], "halo":[], "disk":[], "bulge":[], "stars":[], "bndry":[]}

	blocksize = int.from_bytes(f.read(4), "little")
	for particletype in Npart.keys():
		Npart[particletype] = int.from_bytes(f.read(4), "little")

	f.seek(blocksize + 4, 0)
	f.read(4)

	# particle positions
	f.read(4)

	for particletype in Npart.keys():
		for n in range(Npart[particletype]*3):
			positions[particletype].append(struct.unpack('f', f.read(4))[0])
		positions[particletype] = np.reshape(positions[particletype], (Npart[particletype],3))

	f.read(4)

	# close file
	f.close()

	return positions