#!/usr/bin/python3
import sys
import glob
import numpy as np
import pynbody
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from readsnap import get_particle_positions

simulation_name = sys.argv[1]
num_snaps = len(glob.glob("./simulations/{}/snapshots/*".format(simulation_name)))

if num_snaps == 0:
	print("No snapshot files found for simulation named \'{}\'.".format(simulation_name))
	sys.exit(1)

dt = 0
with open("simulations/{}/{}.param".format(simulation_name, simulation_name)) as paramfile:
    while dt == 0:
    	line = paramfile.readline()
    	if "TimeBetSnapshot" in line:
    		dt = float(line.split()[1])

# Getting the positions of the particles
xyzs = []
for i in range(num_snaps):
	filename = "simulations/{}/snapshots/snapshot_{:03d}".format(simulation_name, i)
	#snap = pynbody.load(filename)

	particle_dict = get_particle_positions(filename)
	xyzs.append(particle_dict)

def plot_2d():
	fig = plt.figure()
	ax = plt.axes()
	ax.set_facecolor('k')

	halo = ax.scatter(xyzs[0]['halo'][:,0], xyzs[0]['halo'][:,1], marker='.', s=0.01, color='b')
	bulge = ax.scatter(xyzs[0]['bulge'][:,0], xyzs[0]['bulge'][:,1], marker='.', s=0.01, color='r')
	disk = ax.scatter(xyzs[0]['disk'][:,0], xyzs[0]['disk'][:,1], marker='.', s=0.01, color='w')

	def update(frame):
		halo.set_offsets(np.c_[xyzs[frame]['halo'][:,0], xyzs[frame]['halo'][:,1]])
		disk.set_offsets(np.c_[xyzs[frame]['disk'][:,0], xyzs[frame]['disk'][:,1]])
		bulge.set_offsets(np.c_[xyzs[frame]['bulge'][:,0], xyzs[frame]['bulge'][:,1]])

		return halo,disk,bulge,

	## Removes axes and margins just to save as a slightly prettier video
	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)
	plt.autoscale(tight=True)
	plt.gcf().set_facecolor('black')
	plt.axis("off")

	animation_2d = anim.FuncAnimation(fig, update, interval=dt*1000, frames=num_snaps)
	plt.show()
	animation_2d.save("animations/{}_anim2d.mp4".format(simulation_name), writer=anim.writers['ffmpeg'](fps=15,bitrate=1800))
	
def plot_3d():
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	plt.gcf().set_facecolor('k')
	ax.set_facecolor('k')
	ax.xaxis.label.set_color('w')
	ax.yaxis.label.set_color('w')
	ax.zaxis.label.set_color('w')
	ax.w_xaxis.set_pane_color((0,0,0,1))
	ax.w_yaxis.set_pane_color((0,0,0,1))
	ax.w_zaxis.set_pane_color((0,0,0,1))
	ax.tick_params(axis='x', colors='w')
	ax.tick_params(axis='y', colors='w')
	ax.tick_params(axis='z', colors='w')

	halo = ax.scatter(xyzs[0]['halo'][:,0], xyzs[0]['halo'][:,1], xyzs[0]['halo'][:,2], marker=',', s=0.01, c='b')
	disk = ax.scatter(xyzs[0]['disk'][:,0], xyzs[0]['disk'][:,1], xyzs[0]['disk'][:,2], marker=',', s=0.01, c='w')
	bulge = ax.scatter(xyzs[0]['bulge'][:,0], xyzs[0]['bulge'][:,1], xyzs[0]['bulge'][:,2], marker=',', s=0.01, c='r')

	def update(frame):
		halo._offsets3d = (xyzs[frame]['halo'][:,0], xyzs[frame]['halo'][:,1], xyzs[frame]['halo'][:,2])
		disk._offsets3d = (xyzs[frame]['disk'][:,0], xyzs[frame]['disk'][:,1], xyzs[frame]['disk'][:,2])
		bulge._offsets3d = (xyzs[frame]['bulge'][:,0], xyzs[frame]['bulge'][:,1], xyzs[frame]['bulge'][:,2])

		return halo,disk,bulge,

	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)
	ax.get_zaxis().set_visible(False)
	plt.autoscale(tight=True)
	plt.gcf().set_facecolor('black')
	plt.axis("off")

	animation_3d = anim.FuncAnimation(fig, update, interval=dt*1000, frames=num_snaps)
	animation_3d.save("animations/{}_anim3d.mp4".format(simulation_name), writer=anim.writers['ffmpeg'](fps=15,bitrate=1800))

	plt.show()

if len(sys.argv) > 2:
	if sys.argv[2] == "2d":
		plot_2d()
	if sys.argv[2] == "3d":
		plot_3d()
