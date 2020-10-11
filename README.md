# cumulative-heatmap-calculation
fast calculation of heatmap from given points.

## introduction
This code is a follow-up project for calculating a heat map using a recursive algorithm: [**recursive-HeatMap-calculation**](https://github.com/EtzionData/recursive-HeatMap-calculation). Calculating a heat map is a complex task, because since the user selects a more detailed resolution, the runtime of the calculation increases accordingly. The main difficulty in the calculation is in the sum of all the coordinates for the boundaries of each cell in the heatmap. 

The recursive method has managed to result a significant improvement in the runtime of the code ([**see here**](https://github.com/EtzionData/recursive-HeatMap-calculation/blob/master/Pictures/compare.png)). But, there are still modifications that can be made even better results. To calculate the heatmap, the code [**cumulative_heatmap.py**]( https://github.com/EtzionData/cumulative-HeatMap-calculation/blob/master/cumulative_heatmap.py) applied different approach from the previous project, and use **Flooring Division** to improve the runtime of the code:

-	**Step One:** Define the **division** parameter for the points 2D space, so that we know the length of a **side** of each square we want to calculate.
-	**Step Two:** We will use a loop through all the points, and calculate for each point its the row and column, using **flooring division**:
   col = (x _{i}-min(x))//side
   
-	**Step Three:** Now, split each square into four small squares in equal size. We will perform **Step Two** for each of these new squares, but now it will only be performed on the coordinates that matched the boundaries of the original square.
-	**Step Four:** Repeat the process recursively until we reach squares size of the desired resolution.

If we encounter during the process a square that does not intersect at all with the coordinates, we will stop its division. Now, we will save all the squares we calculated with intersection count bigger than zero. Now we got a heat map with the required resolution! As can be seen, the runtime of the calculation using the recursive algorithm is significantly lower than the naive algorithm:

![runtime](https://github.com/EtzionData/recursive-HeatMap-calculation/blob/master/Pictures/compare.png)

The resolution of the heat map can be adjusted using the **"depth"** variable. This variable determines how many splits to make in each of the first squares. The larger the "depth" variable, the higher the resolution we get. You can see a diagram describing the split into squares, by each depth:

![square size](https://github.com/EtzionData/recursive-HeatMap-calculation/blob/master/Pictures/squares.png)

As mentioned, it is important to make sure that a suitable resolution is chosen for the calculation, since different values for the "depth" variable will lead to different results. A simple example based on the file [**circle.csv**](https://github.com/EtzionData/recursive-HeatMap-calculation/blob/master/examples/circle.csv) illustrates how different values resulted different outputs:

![six_plots](https://github.com/EtzionData/recursive-HeatMap-calculation/blob/master/Pictures/diff_depth.png)

The heat map is calculation performed using the **HeatMap** object. This object receives a Python list consisting of tuples of X and Y coordinates. Also, the desired depth also must be set for the object. Using the data about the coordinates, the HeatMap calculates the initial squares and performs the recursive calculation on them. At the end of the process, the squares that compose the heat map are calculated, as can be seen in the example process figure (based on the file [**rome_100000.shp**](https://github.com/EtzionData/recursive-HeatMap-calculation/blob/master/examples/rome_100000.shp) that contain **100,000** points coordinates!):

![input output](https://github.com/EtzionData/recursive-HeatMap-calculation/blob/master/Pictures/process.png)

The final squares can be accessed as one of the data of the object: **HeatMap (xy_tpl_lst, depth = 5) .heatmap**. It is also possible to **create a plot** based on the results of the heat map using the function built into the object, as in the following example:
``` sh
from smart_heatmap import HeatMap, loadcsv 
xy = loadcsv(r'example\circle.csv','x','y')
hm = HeatMap(xy, depth=4)
hm.plot()
```
![hm.plot() example](https://github.com/EtzionData/recursive-HeatMap-calculation/blob/master/Pictures/HeatMap_Output_depth%3D4_number_of_points%3D5000.png)

In addition, the calculation results can be exported and saved as files in various formats using the **save_map** function of the object, as can be seen in the [**implementation.py**](https://github.com/EtzionData/recursive-HeatMap-calculation/blob/master/implementation.py) file. The function allows to save the results in **SHP**, **KML** and **CSV** format. It should be noted that saving the results as layers is automatically set to  geographic coordinate system of **WGS_1984_DD**. 

Also, the data that saved to a KML file gets a color corresponding to the count of its intersection. Example for such output you can see [**here**](https://www.google.com/maps/d/edit?mid=1VJ0SwJSOOVDwZDDhKAilDdkR0XbxY3rM&usp=sharing) as interactive **MYMAPS** page. This output based on the [**Gibraltar.kml**](https://github.com/EtzionData/recursive-HeatMap-calculation/blob/master/examples/Gibraltar.kml) example file and the output also available here: [**Gibraltar_Output.kml**](https://github.com/EtzionData/recursive-HeatMap-calculation/blob/master/output/Gibraltar_Output.kml). Also, for convenience, the code contains three XY-tuple-list load functions from **SHP**, **KML** and **CSV** files:
- **loadshp**
- **loadkml**
- **loadcsv**    (this function required also the X & Y fields names)


## libraries
The code uses the following libraries in Python:

**matplotlib**

**shapefile**

**simplekml**

**pandas**

**numpy**

## application
An application of the code is attached to this page under the name: 

[**implementation.py**](https://github.com/EtzionData/recursive-HeatMap-calculation/blob/master/implementation.py)

the examples outputs are also attached here.

## example for using the code
To use this code, you just need to import it as follows:
``` sh
# import
from smart_heatmap import HeatMap, loadshp

# load data
xy = loadshp(r'examples\feature_class.shp')

# define depth variable
depth = 5

# application
hm = HeatMap(xy, depth)

# plot
hm.plot()

# save data as csv
hm.save_map('filename','csv')
```

When the variables displayed are:

**xy:** the given xy coordiantes list.

**depth** the required depth for the recursion, define the output resolution.


## License
MIT © [Etzion Harari](https://github.com/EtzionData)
