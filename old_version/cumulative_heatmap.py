from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
from simplekml import Kml
import shapefile as shp
import pandas as pd
import numpy as np

COL = ['b3006100','b300803c','b300a16b','b300c4a4','b300ebdf','b300eaff','b300bbff','b30091ff','b30062ff','b30022ff']

PRJ = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],' \
      'PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],VERTCS["EGM96_Geoid",' \
      'VDATUM["EGM96_Geoid"],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]]'

GEO = '				<coordinates>'

KML = 'kml'
SHP = 'shp'
CSV = 'csv'

class HeatMap:
    """
    HeatMap calculation object
    """
    def __init__(self, data, division):
        """
        initialize the heatmap parameters
        :param data: list of xy tuples
        :param division: required square number for the shortest side
        """
        self.division = division
        self.xy = data
        self.x = [x for x,_ in self.xy]
        self.y = [y for _,y in self.xy]
        self.x_min, self.y_min = min(self.x), min(self.y)
        self.x_max, self.y_max = max(self.x), max(self.y)
        self.x_len = self.x_max-self.x_min
        self.y_len = self.y_max-self.y_min
        self.side = min(self.x_len, self.y_len)/division
        self.col, self.row = self.length_width()
        self.heatmap = self.square_intersection()

    def square_intersection(self):
        """
        calculate the count of the intersection
        between the square to the given points
        :return: squares with count value
        """
        dct ={}
        for x,y in self.xy:
            key_x = (x-self.x_min) // self.side
            key_y = (y-self.y_min) // self.side
            key = (key_x,key_y)
            if key in dct:
                dct[key]+= 1
            else:
                dct[key] = 1
        return dct

    def calculate_coordinates(self, key):
        """
        calculate the coordinates for the square polygon
        :param x: number of x columns
        :param y: number of y rows
        :return: coordinates for the square polygon
        """
        x, y = key
        x_min = (x * self.side) + self.x_min
        y_min = (y * self.side) + self.y_min
        x_max = min(((x + 1) * self.side) + self.x_min, self.x_max)
        y_max = min(((y + 1) * self.side) + self.y_min, self.y_max)
        return [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max), (x_min, y_min)]

    def get_map(self):
        lst = []
        for key in self.heatmap:
            lst.append({'xy': self.calculate_coordinates(key),
                        'count': self.heatmap[key]})
        return lst

    def length_width(self):
        """
        calculate the length & width of the extent
        :return: length and width values
        """
        col = int(self.x_len//self.side)
        row = int(self.y_len//self.side)
        if self.x_len > self.y_len:
            return col+1, row
        elif self.x_len < self.y_len:
            return col, row+1
        else:
            return col, row

    def plot(self,size=6):
        """
        plot the heatmap results
        :param size: the plot size
        """
        fig, ax = plt.subplots(1, 1, figsize=((self.col/max(self.col,self.row))*size,
                                              (self.row/max(self.col,self.row))*size))

        ax.set_title(f'HeatMap Output\n(division={self.division}, number of points={len(self.xy)})')
        poly = [Polygon(self.calculate_coordinates(key), True) for key in self.heatmap]
        p = PatchCollection(poly, cmap = 'autumn')
        p.set_array(np.array([self.heatmap[key] for key in self.heatmap]))
        ax.add_collection(p)

        ax.set_xlim(self.x_min, self.x_max)
        ax.set_ylim(self.y_min, self.y_max)
        fig.colorbar(p, ax=ax)
        plt.tight_layout()
        plt.savefig(f'HeatMap_Output_division={self.division}_number_of_points={len(self.xy)}.png')
        plt.show()

    def save_map(self,filename, format=SHP):
        """
        save the heatmap results to file
        :param filename: name of the file
        :param format: file format (default: shp)
        """
        if format==KML:
            self.create_kml(filename)
        elif format==SHP:
            self.create_shp(filename)
        elif format==CSV:
            self.create_csv(filename)

    def create_kml(self,name):
        """
        create kml file from the HeatMap results
        :param name: filename
        """
        file = Kml()
        counts = [self.heatmap[key]**0.5 for key in self.heatmap]
        c_min, c_max = min(counts), max(counts)
        divisor= (c_max-c_min)/9
        for key in self.heatmap:
            single = file.newpolygon(name = str(self.heatmap[key]),
                                     outerboundaryis = self.calculate_coordinates(key))
            single.style.polystyle.color = COL[int(((self.heatmap[key]**0.5)-c_min)//divisor)]

        file.save(name+'.kml')

    def create_csv(self,name):
        """
        create csv file from the HeatMap results
        :param name: filename
        """
        lst=[]
        for key in self.heatmap:
            x,y = key
            coord = self.calculate_coordinates(key)
            lst.append((self.heatmap[key], x, y, coord[0][0],coord[0][1],coord[2][0],coord[2][1]))
        fields = ['count','x_col','y_row','x_min','y_min','x_max','y_max']
        pd.DataFrame(lst, columns=fields).to_csv(name+'.csv')

    def create_shp(self,name):
        """
        create shapefile from the HeatMap results
        :param name: filename
        """
        layer = shp.Writer(name+'.shp')
        layer.field('count', 'N')
        layer.field('x_col', 'N')
        layer.field('y_row', 'N')
        for key in self.heatmap:
            x, y = key
            layer.poly([self.calculate_coordinates(key)])
            layer.record(self.heatmap[key], x, y)
        layer.close()

        with open(name + '.prj', 'w+', encoding='utf-8') as prj:
            prj.write(PRJ)
            prj.close()

def loadkml(file):
    """
    load the kml file and convert the coordinates to new list
    :param file: path to the kml
    :return: xy-taple list
    """
    lst=[]
    kml = open(file, 'r', encoding='utf-8').read().split('\n')
    for line in kml:
        if GEO in line:
            x,y = line[len(GEO):].split(',')[:2]
            lst.append((float(x),float(y)))
    return lst

def loadshp(file):
    """
    load the shapefile and convert the coordinates to new list
    :param file: path to the shapefile
    :return: xy-taple list
    """
    data = shp.Reader(file)
    return [geo['geometry']['coordinates'] for geo in data.__geo_interface__['features']]

def loadcsv(file,x,y):
    """
    load the csv file and convert the coordinates to new list
    :param file: path to the csv
    :return: xy-taple list
    """
    df = pd.read_csv(file)
    x,y= list(df[x]),list(df[y])
    return [(x[i], y[i]) for i in range(len(x))]


