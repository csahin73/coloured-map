import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as colors
import json
import os
import math
import matplotlib.gridspec as gridspec
from animate import make_animation, make_video, make_mp4

MONTHS= {
	"01" : "Oca",
	"02" : "Sub",
	"03" : "Mar",
	"04" : "Nis",
	"05" : "May",
	"06" : "Haz",
	"07" : "Tem",
	"08" : "Agu",
	"09" : "Eyl",
	"10" : "Eki",
	"11" : "Kas",
	"12" : "Ara"
}

def read_basemap(geojson):
	data = gpd.read_file(geojson)
	return data

def locate_cities(map_data, search):
	cities = map_data.name
	mapping = {
		"Istanbul": "İstanbul", 
		"Kahramanmaras": 'Kahramanmaraş',
		"Diyarbakir": "Diyarbakır",
		"Elazig": "Elazığ",
		"Tekirdag": "Tekirdağ",
		"Usak": "Uşak",
		"Ankara_Weekly": "Ankara"
	}
	result = {}
	for i,city in enumerate(search):

		print("Searching for {} ...".format(city))
		city_inmap = city.title()
		city_inmap = mapping.get(city_inmap, city_inmap)
		
		try:
			result[city] = np.where(cities == city_inmap)[0].tolist()[0]
		except:
			print("{} not found ...".format(city_inmap))
			print(map_data.name.tolist())
			pass
	return result

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    
    color_list = 'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval)
    
    new_cmap = colors.LinearSegmentedColormap.from_list(
        color_list,
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

def plot_style_custom():
	
	color_list = ['red', '#000000','#444444', 
		'#666666', '#ffffff', 'blue', 'orange'
		]
	cmap = colors.ListedColormap(color_list)
	vmin = -10
	vmax = 105
	bins = int((vmax - vmin)/len(color_list))
	boundaries = list(range(-10,105,bins))
	
	
	cmap.set_under("w")
	norm = colors.BoundaryNorm(boundaries, cmap.N) #, clip=True)

	return {
		"cmap": cmap,
		"norm": norm,
		"ticks": boundaries
	}

def plot_style():
	
	boundaries = list(range(-5,105,5))
	boundaries.insert(0, -30)
	cmap2 = truncate_colormap(plt.get_cmap('YlOrBr'), 0.05, 1, 22)
	cmap2.set_under("w")
	norm = colors.BoundaryNorm(boundaries, cmap2.N) #, clip=True)

	return {
		"cmap": cmap2,
		"norm": norm,
		"ticks": boundaries
	}

def plot_map(map_data, data, week):
	arr = np.full(len(map_data.name), -100)
	
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
	
	cb = fig.colorbar(sm, ticks= style['ticks'], 
						orientation='horizontal', extend="max")
	cb.set_label("Oransal artis %")
	
	map_data.plot(column = 'colors', ax = ax, 
							edgecolor='black',
							linewidth=0.5,
							cmap = style['cmap'],
							norm = style['norm'],
							legend = False)
	
	title = "Normal uzeri olum orani - Excess mortality rate" 
	plt.title(title, {'fontsize': 20})
	
	txt = "{}".format(format_week(week))
	fig.text(0.3, 0.22, txt, {'color': "blue", 'fontsize': 24}, alpha=1)

	
	ack = "Gorsel: @cihansah73\nData  : @GucluYaman"
	fig.text(0.016, 0.0, ack,{'color': 'blue', 'fontsize': 10}, alpha=.7)
	plt.tight_layout()
	fname = "images/em-{}.png".format(week)
	plt.savefig(fname, bbox_inches='tight')
	plt.close()

def format_week(week):
	print(week)
	week2, week1 = week.split("-")
	print(week1,week2)
	month1 = MONTHS.get(week1[4:6], week1[4:6])
	month2 = MONTHS.get(week2[4:6], week2[4:6])

	week1 = "{} {}".format(week1[6:8], month1 )
	week2 = "{} {}".format(week2[6:8], month2 )
	
	week = "{}-{} {}".format(week1, week2, week[0:4])
	
	return week

from datetime import datetime, timedelta
def str_date(d_str):
	date = datetime.strptime(d_str, "%d.%m.%Y")
	return date

def d_delta(d,delta):
	d = d + timedelta(days=delta)
	return d

def is_date_in_range(drange, c):
	if c>drange[0] and c<=drange[1]:
		return True
	return False

def date_label(drange):
	label = []
	for d in drange:
		label.insert(0, d.strftime("%Y%m%d"))
	return "-".join(label)

def parse_data(csv_file, start_date, end_date):
	data = pd.read_csv(csv_file, delimiter=";")
	weekly_sum = 0
	last_year = 0
	daterange = []
	result = {}
	week_list = []
	data = data.dropna(axis=1, how='all') # Drop a year with all missing values
	years = len(data.values[0])
	print("Years accounted for: {} {}".format(years, csv_file))
	#end_date="01.03.2020"
	dfinal = str_date(end_date)
	dstart = str_date(start_date)
	dend = d_delta(dstart, 7)
	drange = [dstart, dend]
	for i,d in enumerate(data.values, 1):
		curdate = str_date(d[0])

		if (curdate > dfinal):
			break

		if (is_date_in_range(drange, curdate) ):
			datacols = d[1:years]
			datacols = datacols.astype(np.float)
			weekly_sum += np.nansum(datacols[0:-1])
			last_year += np.nansum(datacols[-1])
		
		if (curdate >= drange[1]):
			
			weekly_mean = weekly_sum*1./(years-2)
			change = (last_year - weekly_mean) / weekly_mean
			
			label = date_label(drange)			
			result[label] = change*100
			week_list.append(label)
			print(last_year, weekly_mean, change, label)
			weekly_sum = 0
			last_year = 0
			drange = [curdate, d_delta(curdate, 7)]

	return [result, week_list]

def XXXse_data(csv_file, start_date):
	data = pd.read_csv(csv_file, delimiter=";")
	weekly_sum = 0
	daterange = []
	result = {}
	week_list = []
	data = data.dropna(axis=1, how='all') # Drop a year with all missing values
	years = len(data.values[0])
	print("Years accounted for: {} {}".format(years, csv_file))
	for i,d in enumerate(data.values, 1):

		datacols = d[1:years]
		datacols = datacols.astype(np.float)
		weekly_sum += datacols
		if (i % 8 == 1):
			label = d[0].split(".")
			label.reverse()
		
		elif (i % 8 == 0):
			
			label1 = d[0].split(".")
			label1.reverse()
			label = "%s-%s" % ("".join(label1), "".join(label))
			
			last_el  = len(weekly_sum) - 1
			weekly_mean = np.nanmean(weekly_sum[0:last_el])
			this_year = weekly_sum[last_el]
			change = (this_year - weekly_mean) / weekly_mean
			result[label] = change*100
			week_list.append(label)
			weekly_sum = 0
			
	
	return [result, week_list]


if __name__ == "__main__":
	
	map_data = read_basemap('data/tr-cities-modified.json')

	city_list = ['Denizli','Istanbul', 'Bursa', 
				 'Kahramanmaras','Izmir', 'Gaziantep',
				 'diyarbakir', 'elazig', 'erzurum',
				 'hatay', 'kayseri', 'kocaeli',
				  'konya', 'malatya', 'sakarya', 
				  'sivas', 'tekirdag', 'usak', 'ankara_weekly'
				]

	#city_list = ['usak']

	city_indices = locate_cities(map_data, city_list)
	print(city_indices)
	DATADIR = "data"
	data = {}
	all_weeks = []
	week_start = "01.01.2020"
	week_end = "12.11.2020"

	for csv in city_list:
		csv_file = os.path.join(DATADIR,csv+".csv")
		city_data, week_list = parse_data(csv_file, week_start, week_end)
		all_weeks += week_list
		data[csv] = city_data

	all_weeks = sorted(list(set(all_weeks)))
	
	for week in all_weeks:

		print("Plotting ...", week)
		week_data = {}
		for city in city_list:
			week_data[city_indices[city]] = data[city][week]
		plot_map(map_data, week_data, week)

	
	
	make_video("images", "anim.avi")
	animgif = make_animation("images", "anim.gif")

	make_mp4(animgif, "images/anim.mp4")
