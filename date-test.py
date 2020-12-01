from datetime import datetime, timedelta
def s2d(st):
	date = datetime.strptime(st, "%d.%m.%Y")
	
	return date
def d_delta(d,delta):
	d = d + timedelta(days=delta)
	return d
def is_in_range(d_range,c):
	if c>drange[0] and c<=drange[1]:
		return True
	
	return False
date = "08.01.2020"
dend = s2d(date)
dstart = d_delta(dend, -7)

drange = [dstart, dend]


check=["08.01.2020", "09.01.2020"]

for c in check:
	print(drange)
	print(c)
	print(is_in_range(drange, s2d(c)))