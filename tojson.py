import json

fname= "data/tr-cities.json"
with open(fname) as jsonfile:
	print(jsonfile)
	o = json.load(jsonfile)

	oo  =open("data/tr-cities-modified.json","w")

	oo.write(json.dumps(o))
	oo.close()