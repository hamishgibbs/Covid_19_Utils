#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 09:59:58 2020

@author: hamishgibbs
"""

import os
import glob
import quadkey
from shapely.wkt import loads
from shapely.geometry import Polygon
import pandas as pd
import geopandas as gpd
import numpy as np
#%%
_args = ['code', '/Users/hamishgibbs/Documents/Covid-19/covid_facebook_mobility/data/Facebook_Data/Britain_mobility']
#%%
mobility = pd.concat([pd.read_csv(file) for file in glob.glob(_args[1] + '/*.csv')])
#drop null linestrings - check that this is good practice
mobility = mobility[[type(line) == str for line in mobility['geometry']]]
#%%

lines = [loads(line) for line in mobility['geometry']]
mobility = gpd.GeoDataFrame(mobility, geometry = lines)
mobility.crs = "EPSG:4326"
#need to transform to web mercator
mobility = mobility.to_crs("EPSG:3857")

#%%

def get_line_quadkey(line, position = 'start'):
    
    if position == 'start':
        point = line.coords[0]
        
        return(quadkey.webmercator2quadint(int(point[0]), int(point[1])))
        
    if position == 'end':
        point = line.coords[1]
        
        return(quadkey.webmercator2quadint(int(point[0]), int(point[1])))

    else:
        'Unknown position'
        exit()
        
def create_polygon(coords):
    bottom_l = [coords[0], coords[1]]
    bottom_r = [coords[2], coords[1]]
    top_l = [coords[0], coords[3]]
    top_r = [coords[2], coords[3]]
    
    return(Polygon([bottom_l, bottom_r, top_r, top_l]))
#%%
mobility['start_quadkey'] = [get_line_quadkey(line, position = 'start') for line in mobility['geometry']]
mobility['end_quadkey'] = [get_line_quadkey(line, position = 'end') for line in mobility['geometry']]

#%%
unique_tiles = pd.DataFrame({'quadkey':list(np.unique(list(mobility['start_quadkey']) + list(mobility['end_quadkey'])))})
#%%
unique_tiles['coords'] = [quadkey.tile2bbox(qk, 12) for qk in unique_tiles['quadkey']]
unique_tiles = gpd.GeoDataFrame(unique_tiles, geometry = [create_polygon(coords) for coords in unique_tiles['coords']])
unique_tiles = unique_tiles.loc[:, ['quadkey', 'geometry']]
unique_tiles.crs = "EPSG:4326"

#%%
mobility = mobility.loc[:, ['date_time', 'n_crisis', 'length_km', 'start_quadkey', 'end_quadkey']]
#%%
mobility.to_csv("/Users/hamishgibbs/Documents/Covid-19/covid_facebook_mobility/data/Mobility_Output/Britain/Mobility_Referenced.csv")

#%%
unique_tiles.to_file("/Users/hamishgibbs/Documents/Covid-19/covid_facebook_mobility/data/Tile_Data/bing_tiles.shp")







