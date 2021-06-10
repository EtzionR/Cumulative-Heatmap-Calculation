from chm import HeatMap, loadshp, loadcsv, loadkml
import pandas as pd
import numpy as np


# Example 1:
xy = loadcsv(r'examples\random.csv','x','y')
hm = HeatMap(xy, 25)
hm.save_map(r'output\random_output','csv')
hm.plot()

# Example 2:
xy = loadshp(r'examples\paris.shp')
hm = HeatMap(xy, 80)
hm.save_map(r'output\paris_output','kml')
hm.plot()

# Example 3:
xy = loadkml(r'examples\Athens.kml')
hm = HeatMap(xy, 64)
hm.save_map(r'output\Athens_output','shp')
hm.plot()

# Example 4:
xy = np.load(r'examples\data.npy')
hm = HeatMap(xy, 128)
hm.save_map(r'output\data_output','csv')
hm.plot()


