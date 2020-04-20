MAINDIR = ~/Documents/Covid-19/citymapper
OUTDIR = ${MAINDIR}/output
FILE = ${OUTDIR}/citymapper_data.csv
URL = https://citymapper.com/api/gobot_tab/data

all: update_data

update_data:
	/Users/hamishgibbs/anaconda3/bin/python main.py ${URL} ${FILE}
