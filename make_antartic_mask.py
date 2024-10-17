from pathlib import Path

import numpy as np
import geopandas as gpd
import regionmask
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import shapely.geometry as sgeom

def make_landmask(lon, lat, land):
    nlat = len(lat)
    nlon = len(lon)
    # print(land)
    lon_x, lat_y = np.meshgrid(lon, lat)

    mask = regionmask.mask_geopandas(land, lon, lat,overlap=False).values
    mask = np.where(np.isnan(mask), 0, 1).astype(bool)

    land_mask = np.zeros_like(lon_x)
    land_mask[mask] = 1

    # fig = plt.figure(figsize=(16, 9))
    # ax = fig.add_subplot(111, projection=ccrs.SouthPolarStereo())
    # ax.spines['geo'].set_linewidth(0.8)
    # ax.set_extent((-180, 180, -60, -90), crs=ccrs.PlateCarree()) # type: ignore
    # ax.coastlines() # type: ignore
    # p = ax.pcolormesh(lon_x, lat_y, land_mask, clim=(0, 2), transform=ccrs.PlateCarree(), cmap='jet')
    # plt.show()

    # land_mask_out = np.roll(land_mask, -nlon // 2, axis=1)
    # lon_out = np.linspace(0, 359, nlon)
    # lat_out = np.linspace(90, -89, nlat)
    # lon_x_out, lat_y_out = np.meshgrid(lon_out, lat_out)
    # output = np.c_[lon_x_out.flatten(), lat_y_out.flatten(), land_mask_out.flatten()]
    # # np.savetxt(
    # #     f"D:\\tvg_toolkit\\masking\\data\\mask\\aismask\\ais.mask", output, fmt="%10.1f"
    # # )
    # fig = plt.figure(figsize=(16, 9))
    # ax = fig.add_subplot(111, projection=ccrs.SouthPolarStereo())
    # ax.spines['geo'].set_linewidth(0.8)
    # ax.set_extent((0, 360, -60, -90), crs=ccrs.PlateCarree()) # type: ignore
    # ax.coastlines() # type: ignore
    # p = ax.pcolormesh(lon_x_out, lat_y_out, land_mask_out, clim=(0, 2), transform=ccrs.PlateCarree(), cmap='jet')
    # plt.show()
    return mask

if __name__ == "__main__":
    lon = np.linspace(-180, 179, 360)
    lat = np.linspace(90, -89, 180)
    lon_x, lat_y = np.meshgrid(lon, lat)
    ais = gpd.read_file(
        'C:\\Users\\huan\\Desktop\\基金本子\\参考文献\\geoBoundaries-ATA-ADM0_simplified.geojson'
    )
    ais = gpd.read_file(
        'D:\\tvg_toolkit\\masking\\data\\shapefile\\ant_basin\\ANT_Basins_IMBIE2_v1.6_new.shp'
    )
    breakpoint()
    mask = regionmask.mask_geopandas(ais, lon, lat,overlap=False).values
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111, projection=ccrs.SouthPolarStereo())
    ax.spines['geo'].set_linewidth(0.8)
    ax.set_extent((-180, 180, -60, -90), crs=ccrs.PlateCarree()) # type: ignore
    ax.coastlines() # type: ignore
    p = ax.pcolormesh(lon_x, lat_y, mask, clim=(0, 17), transform=ccrs.PlateCarree(), cmap='jet')
    plt.show()

    aisbool = make_landmask(lon, lat, ais)
    aismask = np.zeros_like(lon_x)
    aismask[aisbool] = 1

    ais = np.loadtxt('D:\\tvg_toolkit\\fingerprint_approach\\antarctic.txt')
    ais_df = pd.DataFrame(ais, columns=['lat', 'lon', 'id'])
    grouped_ais_df = ais_df.groupby('id')
    masks = []
    for id, df in grouped_ais_df:
        points = df[['lon', 'lat']].to_numpy()
        # if not np.allclose(points[0], points[-1]):
        #     points = np.vstack((points, points[0]))
        polygon = sgeom.Polygon(points)
        output_gdf = gpd.GeoDataFrame({'geometry': polygon}, index=[0]).set_crs('EPSG:4326')
        if int(id) == 17: # type: ignore
            id17_1 = make_landmask(lon, lat, output_gdf)
        else:
            masks.append(make_landmask(lon, lat, output_gdf))
    mask = np.any(masks, axis=0)

    except17 = np.zeros((180, 360))
    except17[mask] = 1
    id17_2 = aismask - except17

    id17 = id17_1*id17_2

    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111, projection=ccrs.SouthPolarStereo())
    ax.spines['geo'].set_linewidth(0.8)
    ax.set_extent((-180, 180, -60, -90), crs=ccrs.PlateCarree()) # type: ignore
    ax.coastlines() # type: ignore
    p = ax.pcolormesh(lon_x, lat_y, id17, clim=(0, 2), transform=ccrs.PlateCarree(), cmap='jet')
    plt.show()
   

