from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from sys import argv
from os import system

input_file = argv[1]

cluster = True

# Read Dataset
nc = Dataset(input_file, 'r')
track = nc.variables['track'][:]
lon = nc.variables['lon'][:]
lat = nc.variables['lat'][:]
time = nc.variables['j1'][:]
nc.close()

for time_step in np.unique(time):

    CMD = 'python plt_trajectory.py %s %s' %(input_file, str(time_step))

    if cluster:
        BATCH_CMD = "BatchFerme " \
		    "--queue=veryshort " \
		    "--name=TRACMASS-PLOT " \
		    "--no-confirm " \
		    "--notify=n " \
		    "--cmd='%s' " \
		    "--memory=8000mb" % (CMD)

        system(BATCH_CMD)
        print BATCH_CMD

    else:

        system(CMD)
	CMD = "ffmpeg -framerate 10 -i trajectories_%04d.png -c:v libx264 -r 30 -pix_fmt yuv420p example_trajectories.mp4"
	system(CMD)
