import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as colors
import json
import os
import math
from animate import make_animation

def read_basemap(geojson):
	data = gpd.read_file(geojson)
	return data

def locate_cities(map_data, search):
	cities = map_data.name
	mapping = {
		"Istanbul": "İstanbul", 
		"Kahramanmaras": 'Kahramanmaraş'
	}
	result = {}
	for i,city in enumerate(search):
		print("Searching for {} ...".format(city))
		city_inmap = mapping.get(city, city)
		try:
			result[city] = np.where(cities == city_inmap)[0].tolist()[0]
		except:
			print("{} not found ...".format(city))
			print(map_data.name.tolist())
			pass
	return result

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    
    color_list = 'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval)
    
    new_cmap = colors.LinearSegmentedColormap.from_list(
        color_list,
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap



def plot_style():
	cmap = colors.ListedColormap(
		['red', '#000000','#444444', 
		'#666666', '#ffffff', 'blue', 'orange'
		])
	
	boundaries = list(range(-10,105,5))
	print(plt.get_cmap('YlOrRd'))
	cmap2 = truncate_colormap(plt.get_cmap('YlOrRd'), 0, 1, 22)
	norm = colors.BoundaryNorm(boundaries, cmap2.N, clip=True) #cmap.N,

	return {
		"cmap": cmap2,
		"norm": norm
	}

def plot_map(map_data, data, week):
	arr = np.full(len(map_data.name), 0)
	
	for x in data.keys():
		if math.isnan(data[x]):
			arr[x] = -100
		else: 
			arr[x] = data[x]
	
	map_data['colors'] = arr
	
	fig, ax = plt.subplots(1, figsize=(8, 6))

	style = plot_style()
	
	sm = plt.cm.ScalarMappable(cmap=style['cmap'], 
				norm=style['norm'])
	cb = fig.colorbar(sm, orientation='horizontal')
	cb.set_label("Yuzdelik artis %")
	
	map_data.plot(column = 'colors', ax = ax, 
							edgecolor='grey',
							cmap = style['cmap'],
							norm = style['norm'],
							legend = False)
	
	
	plt.tight_layout()
	
	title = "Normal uzeri olum miktari (%) Hafta: {}".format(format_week(week))
	plt.title(title)
	
	fname = "images/er-%s.png" % week
	plt.savefig(fname, bbox_inches='tight')
	plt.close()

def format_week(week):
	week2, week1 = week.split("-")
	
	week1 = "{}.{}.{}".format(week1[6:8], week1[4:6], week1[0:4])
	week2 = "{}.{}.{}".format(week2[6:8], week2[4:6], week2[0:4])
	
	week = "{}-{}".format(week1, week2)
	
	return week

def parse_data(csv_file):
	data = pd.read_csv(csv_file, delimiter=";")
	weekly_sum = 0
	daterange = []
	result = {}
	week_list = []
	for i,d in enumerate(data.values, 1):
		weekly_sum += d[1:]
		
		if (i % 7 == 1):
			label = d[0].split(".")
			label.reverse()
		elif (i % 7 == 0):
			label1 = d[0].split(".")
			label1.reverse()
			label = "%s-%s" % ("".join(label1), "".join(label))
			last_el  = len(weekly_sum) - 1
			weekly_mean = weekly_sum[0:last_el].mean()
			this_year = weekly_sum[last_el]
			change = (this_year - weekly_mean) / weekly_mean
			change *= 100 # percentage
			result[label] = change
			week_list.append(label)
			weekly_sum = 0
			
	
	return [result, week_list]


if __name__ == "__main__":
	
	#search = ['Ankara', 'Kayseri', 'Istanbul', 'Mugla', 'Izmir', 'Kars', 'Mersin']
	
	map_data = read_basemap('data/tr-cities-modified.json')

	city_list = ['Denizli','Istanbul', 'Bursa', 'Kahramanmaras']
	city_indices = locate_cities(map_data, city_list)
	
	DATADIR = "data"
	data = {}
	all_weeks = []
	for csv in city_list:
		csv_file = os.path.join(DATADIR,csv+".csv")
		city_data, week_list = parse_data(csv_file)
		all_weeks += week_list
		data[csv] = city_data

	all_weeks = sorted(list(set(all_weeks)))

	week_start = "20190101"
	week_end = "20201115"

	for week in all_weeks:
		if (week > week_end or week < week_start):
			continue

		print("Plotting ...", week)
		week_data = {}
		for city in city_list:
			week_data[city_indices[city]] = data[city][week]
		plot_map(map_data, week_data, week)

	#print(map_data.name)
	print("Making animation ...")
	print(make_animation("images", "anim.gif"))