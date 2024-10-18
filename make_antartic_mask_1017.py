import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
from pyshtools.spectralanalysis import Curve2Mask

if __name__ == "__main__":
    nlat = 180
    nlon = 360
    lon = np.linspace(0, 360, nlon, endpoint=False)
    lat = np.linspace(90, -90, nlat, endpoint=False)
    lon_x, lat_y = np.meshgrid(lon, lat)

    ais = np.loadtxt('D:\\tvg_toolkit\\fingerprint_approach\\antarctic.txt')
    ais_df = pd.DataFrame(ais, columns=['lat', 'lon', 'id'])
    grouped_ais_df = ais_df.groupby('id')
    masks = np.zeros_like(lon_x)
    # mask = np.zeros_like(lon_x)
    for id, df in grouped_ais_df:
        print(id)
        lats = df[['lat']].to_numpy()
        lons = df[['lon']].to_numpy()
        lons[lons < 0] += 360
        boundary = np.hstack((lats, lons))
        mask = Curve2Mask(nlat, boundary, 0, sampling=2)
        masks += mask
        np.savetxt(
            f'D:/tvg_toolkit/masking/data/mask/aismask/ais_{id:.0f}_1deg.mask', 
            np.c_[lon_x.ravel(), lat_y.ravel(), mask.ravel()]
        )
        
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111, projection=ccrs.SouthPolarStereo())
    ax.spines['geo'].set_linewidth(0.8)
    ax.set_extent((-180, 180, -60, -90), crs=ccrs.PlateCarree()) # type: ignore
    ax.coastlines() # type: ignore
    p = ax.pcolormesh(lon_x, lat_y, masks, clim=(0, 2), transform=ccrs.PlateCarree(), cmap='jet')
    plt.show()


