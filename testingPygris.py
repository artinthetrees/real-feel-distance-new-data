from pygris import tracts
#from rasterio.mask import mask
import rasterio
import rasterio.mask
import geopandas
from rasterio.plot import show
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import folium
import webbrowser
import rioxarray as rxr

#WGS84 lonlat (units: degree) - EPSG 4326 (https://epsg.io/4326)
#WSG84 utm, zone 16n (units: meter) - EPSG 32616 (https://epsg.io/32616)

#############################################################
# get my chicago tract boundary - will use this to clip MRT 
# raster file
#############################################################

cook_il_tracts = tracts(state = "IL", county = "Cook", cb = True, cache = True, year=2021)

cook_il_tracts_map = cook_il_tracts.explore()
#Display the map
cook_il_tracts_map.save("cook_il_tracts_interactive_map.html")
webbrowser.open("map.html")

my_tract = cook_il_tracts[cook_il_tracts["TRACTCE"].isin(["160400","160501","160502","160602"])]
print(my_tract.crs)

####################################
# convert to epsf 4326 - with wgs84
####################################
my_tract = my_tract.to_crs(epsg=4326)
print(my_tract.crs)

crop_rast_shape = my_tract["geometry"]


#############################################################
# open MRT raster file
#############################################################
#with rasterio.open("./downloads/year2021-month7-day15-hour14-minute0-MRT-mask.tif") as src:
with rasterio.open("./downloads/crs-converted-cog-year2021-month7-day15-hour10-minute0-MRT-mask.tif") as src:
    print(src)
    print("name: ",src.name)
    print("mode: ",src.mode)
    print("closed: ",src.closed)
    print("count: ",src.count)
    print("width: ",src.width)
    print("height: ",src.height)
    print("bounds: ",src.bounds)
    print("transform: ",src.transform)
    print("spatial pos of upper left corner: ",src.transform * (0, 0))
    print("spatial pos of lower right corner: ",src.transform * (src.width, src.height))
    print("crs: ",src.crs)
    print("crs, detail: ",src.crs.to_wkt())
    print("inddexes (bands): ",src.indexes)
    print("nodata: ",src.nodata)
    print("meta: ",src.profile)
    nodata_val = src.nodata
    # Get the bounds of the raster
    bounds = [[src.bounds.bottom, src.bounds.left], [src.bounds.top, src.bounds.right]]
    array=src.read(1)
    
 

#############################################################
# clip MRT raster file to my census tract boundary
#############################################################
    out_img, out_transform = rasterio.mask.mask(src, crop_rast_shape, crop=True)
    out_meta = src.meta

    print("src transform: ",src.transform)
    print("out transform: ",out_transform)
    print("src shape: ",src.shape)
    print("out shape: ",out_img.shape)

    height, width = out_img.shape[1:]
    left, bottom, right, top = rasterio.transform.array_bounds(height, width, out_transform)
    outBoundList = [left,bottom,right,top]
    print("out bound list: ",outBoundList)

    out_img_processed = np.squeeze(out_img)
    out_img_processed[out_img_processed == nodata_val] = np.nan # Convert nodata values to NaN
    
    out_img_processed_2 = np.nan_to_num(out_img_processed)
    #plt.imshow(out_img_processed_2)

    max_value = np.max(out_img_processed) # or arr.max()
    print(f"Maximum value: {max_value}")
    min_value = np.min(out_img_processed) # or arr.min()
    print(f"Minimum value: {min_value}")
    q1 = np.percentile(out_img_processed, 25) # First Quartile (25th percentile)
    q2 = np.percentile(out_img_processed, 50) # Second Quartile (Median, 50th percentile)
    q3 = np.percentile(out_img_processed, 75) # Third Quartile (75th percentile)
    print(f"First Quartile (Q1): {q1}")
    print(f"Second Quartile (Q2 - Median): {q2}")
    print(f"Third Quartile (Q3): {q3}")


    unique_raster_vals = np.unique(array)
    unique_cropped_raster_vals = np.unique(out_img_processed)

    # # Plot with rasterio.plot, which provides Matplotlib functionality
    # plt.figure(figsize=(5, 5), dpi=300)  # adjust size and resolution
    # show(src, title='Digital Surface Model', cmap='gist_ncar')
    plt.figure(figsize=(10, 8)) # Optional: adjust figure size
    show(out_img_processed, transform=src.transform, cmap='gist_ncar') # Use 'gray' for grayscale, or other colormaps

    ###########################
    rasLon = (outBoundList[3] + outBoundList[1])/2
    rasLat = (outBoundList[2] + outBoundList[0])/2
    mapCenter = [rasLon, rasLat]
    # Create a Folium map centered at a specific location
    m = folium.Map(location=mapCenter, zoom_start=20)

    # Add raster overlay
    image = folium.raster_layers.ImageOverlay(
        image=out_img_processed,
        bounds=[[outBoundList[1], outBoundList[0]], [outBoundList[3], outBoundList[2]]],
        opacity=0.6,
        interactive=True,
        cross_origin=False,
        colormap=cm.get_cmap("viridis")
    )
    image.add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Display the map
    #m
    m.save("raster_map.html")
    webbrowser.open("raster_map_2.html")
    
    
    #################
    # Delete
    #################
    
    # ########
    # # Create a Folium map centered on the raster
    # m = folium.Map(location=[(src.bounds.bottom + src.bounds.top) / 2, (src.bounds.left + src.bounds.right) / 2], zoom_start=10)

    # # Add the raster data as an image overlay
    # folium.raster_layers.ImageOverlay(
    #     image=out_img_processed,
    #     bounds=bounds,
    #     colormap=lambda x: show(out_img_processed, cmap='viridis').get_figure().get_axes()[0].get_images()[0].cmap(x), # Example colormap
    #     opacity=0.7,
    #     name='Raster Layer'
    # ).add_to(m)

    # # Add layer control to toggle layers
    # #folium.LayerControl().add_to(m)

    # # Display the map (in a Jupyter environment) or save to HTML
    # #m
    # m.save("select_tracts_mrt_raster_interactive_map.html")
    # webbrowser.open("select_tracts_mrt_raster_interactive_map.html")
    # ########
    
    

    
    
    
    








