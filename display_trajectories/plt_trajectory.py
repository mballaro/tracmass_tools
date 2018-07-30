import matplotlib
matplotlib.use('Agg')
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from sys import argv


input_file = argv[1]
time_step = float(argv[2])

# Read Dataset
nc = Dataset(input_file, 'r')
track = nc.variables['track'][:]
lon = nc.variables['lon'][:]
lat = nc.variables['lat'][:]
time = nc.variables['j1'][:]
nc.close()


def plt_map(local_time):
    """

    :param local_time:
    :return:
    """

    plt.figure()
    map = Basemap(llcrnrlon=270., llcrnrlat=15., urcrnrlon=330., urcrnrlat=47.,
                  projection='lcc', lat_1=20., lat_2=40., lon_0=300.,
                  resolution='l', area_thresh=1000.)

    map.drawcoastlines()
    map.drawcountries()
    map.drawmapboundary()
    map.fillcontinents(color='0.', lake_color='#99ffff')
    map.drawparallels(np.arange(10, 70, 20), labels=[1, 1, 0, 0])
    map.drawmeridians(np.arange(-100, 0, 20), labels=[0, 0, 0, 1])
    plt.title("Simulated particule trajectories from AVISO maps")

    timestep_particule = np.ma.masked_where((time > local_time + 2) | (time < local_time - 2), track)
    timestep_lon = np.ma.masked_where((time > local_time + 2) | (time < local_time - 2), lon)
    timestep_lat = np.ma.masked_where((time > local_time + 2) | (time < local_time - 2), lat)

    # loop over timestep particule trajectory
    for particule in np.unique(timestep_particule):
        particule_lon = np.ma.masked_where(timestep_particule != particule, timestep_lon).compressed()
        particule_lat = np.ma.masked_where(timestep_particule != particule, timestep_lat).compressed()

        XX, YY = map(particule_lon, particule_lat)
        if XX.size:
            map.scatter(XX[XX.size - 1], YY[YY.size - 1], c='orange', s=20, edgecolors=None, linewidths=0)
            map.plot(XX, YY, linewidth=1, color='orange')  # np.random.rand(3,1))
            map.etopo()

    plt.savefig('trajectories_%04d.png' % int(local_time))
    plt.close()


plt_map(time_step)
