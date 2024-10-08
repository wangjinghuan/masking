from pathlib import Path

import numpy as np
import geopandas as gp
import regionmask
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def make_oceanmask(lon, lat, filepath, buf):
    nlat = len(lat)
    nlon = len(lon)
    filepath = Path(filepath)
    land = gp.read_file(filepath)
    # print(land)
    lon_x, lat_y = np.meshgrid(lon, lat)

    mask = regionmask.mask_geopandas(land, lon, lat, overlap=False).values
    mask = np.where(np.isnan(mask), 0, 1).astype(bool)

    land_mask = np.zeros_like(lon_x)
    land_mask[mask] = 1

    # fig = plt.figure(layout="constrained", figsize=(8, 12))
    # ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
    # ax1.spines["geo"].set_linewidth(0.8)
    # ax1.set_global()  # type: ignore
    # ax1.coastlines()  # type: ignore
    # p1 = ax1.pcolormesh(
    #     lon_x, lat_y, land_mask, transform=ccrs.PlateCarree(), cmap="jet", clim=(0, 2)
    # )
    # fig.colorbar(
    #     p1,
    #     ax=ax1,
    #     location="right",
    #     orientation="vertical",
    #     extend="both",
    #     shrink=0.6,
    #     ticks=np.linspace(-8, 8, 5),
    # )
    # plt.show()

    land_mask_out = np.roll(land_mask, -nlon // 2, axis=1)
    oc_mask_out = 1 - land_mask_out
    lon_out = np.linspace(0, 359, nlon)
    lat_out = np.linspace(90, -89, nlat)
    lon_x_out, lat_y_out = np.meshgrid(lon_out, lat_out)
    output = np.c_[lon_x_out.flatten(), lat_y_out.flatten(), oc_mask_out.flatten()]
    # np.savetxt(
    #     f"D:\\tvg_toolkit\\masking\\data\\mask\\oceanmask\\ocean_buf{buf:d}.txt",
    #     output,
    #     fmt="%10.1f",
    # )

    fig = plt.figure(layout="constrained", figsize=(8, 12))
    ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
    ax1.spines["geo"].set_linewidth(0.8)
    ax1.set_global()  # type: ignore
    ax1.coastlines()  # type: ignore
    p1 = ax1.pcolormesh(
        lon_x_out, lat_y_out, oc_mask_out, transform=ccrs.PlateCarree(), cmap="jet", clim=(0, 2)
    )
    fig.colorbar(
        p1,
        ax=ax1,
        location="right",
        orientation="vertical",
        extend="both",
        shrink=0.6,
        ticks=np.linspace(0, 2, 3),
    )
    plt.show()


def make_landmask(lon, lat, filepath, buf):
    nlat = len(lat)
    nlon = len(lon)
    filepath = Path(filepath)
    land = gp.read_file(filepath)
    # print(land)
    lon_x, lat_y = np.meshgrid(lon, lat)

    mask = regionmask.mask_geopandas(land, lon, lat, overlap=False).values
    mask = np.where(np.isnan(mask), 0, 1).astype(bool)

    land_mask = np.zeros_like(lon_x)
    land_mask[mask] = 1

    # fig = plt.figure(layout="constrained", figsize=(8, 12))
    # ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
    # ax1.spines["geo"].set_linewidth(0.8)
    # ax1.set_global()  # type: ignore
    # ax1.coastlines()  # type: ignore
    # p1 = ax1.pcolormesh(
    #     lon_x, lat_y, land_mask, transform=ccrs.PlateCarree(), cmap="jet", clim=(0, 2)
    # )
    # fig.colorbar(
    #     p1,
    #     ax=ax1,
    #     location="right",
    #     orientation="vertical",
    #     extend="both",
    #     shrink=0.6,
    #     ticks=np.linspace(-8, 8, 5),
    # )
    # plt.show()

    land_mask_out = np.roll(land_mask, -nlon // 2, axis=1)
    lon_out = np.linspace(0, 359, nlon)
    lat_out = np.linspace(90, -89, nlat)
    lon_x_out, lat_y_out = np.meshgrid(lon_out, lat_out)
    output = np.c_[lon_x_out.flatten(), lat_y_out.flatten(), land_mask_out.flatten()]
    # np.savetxt(
    #     f"D:\\tvg_toolkit\\masking\\data\\mask\\landmask\\land_buf{buf:d}.txt", output, fmt="%10.1f"
    # )

    fig = plt.figure(layout="constrained", figsize=(8, 12))
    ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
    ax1.spines["geo"].set_linewidth(0.8)
    ax1.set_global()  # type: ignore
    ax1.coastlines()  # type: ignore
    p1 = ax1.pcolormesh(
        lon_x_out, lat_y_out, land_mask_out, transform=ccrs.PlateCarree(), cmap="jet", clim=(0, 2)
    )
    fig.colorbar(
        p1,
        ax=ax1,
        location="right",
        orientation="vertical",
        extend="both",
        shrink=0.6,
        ticks=np.linspace(0, 2, 3),
    )
    plt.show()


if __name__ == "__main__":
    km = np.linspace(50, 300, 6, dtype=int)
    lon = np.linspace(-180, 179, 360)
    lat = np.linspace(90, -89, 180)
    make_landmask(
        lon, lat, "D:\\tvg_toolkit\\masking\\data\\shapefile\\land_shp\\ne_110m_land.shp", 0
    )
    make_oceanmask(
        lon, lat, "D:\\tvg_toolkit\\masking\\data\\shapefile\\land_shp\\ne_110m_land.shp", 0
    )
    for i in km:
        file = f"D:\\tvg_toolkit\\masking\\data\\shapefile\\land_shp\\buffer{i}km.shp"
        make_landmask(lon, lat, file, i)
        make_oceanmask(lon, lat, file, i)
