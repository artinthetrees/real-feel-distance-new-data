import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
#from matplotlib import pyplot

src = rasterio.open("./downloads/year2021-month7-day15-hour14-minute0-MRT-mask.tif")
print(src)
print(src.name)
print(src.mode)
print(src.closed)


# array=src.read(1)
# print(array.shape)

# # Plot with rasterio.plot, which provides Matplotlib functionality
# plt.figure(figsize=(5, 5), dpi=300)  # adjust size and resolution
# show(src, title='Digital Surface Model', cmap='gist_ncar')


from pygris import counties, tracts, places
import matplotlib.pyplot as plt

# Get the default TIGER/Line file for counties in Michigan
il_tiger = counties(state = "IL", cache = True)

# Get the cartographic boundary file with cb = True
il_cartographic = counties(state = "IL", cb = True, cache = True)

# Plot the two side-by-side to compare them
fig, ax = plt.subplots(ncols = 2)
il_tiger.plot(ax = ax[0])
il_cartographic.plot(ax = ax[1])

ax[0].set_title("TIGER/Line")
ax[1].set_title("Cartographic")
plt.show()

from pygris import tracts
import webbrowser
cook_il_tracts = tracts(state = "IL", county = "Cook", cb = True, cache = True, year=2021)

cook_il_tracts_map = cook_il_tracts.explore()
#Display the map
cook_il_tracts_map.save("map.html")
webbrowser.open("map.html")

