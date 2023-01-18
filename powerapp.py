from flask import Flask, render_template
import requests
import json
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


app = Flask(__name__)

@app.route('/')
def index():
	query_name = """query {
			  viewer {
			    name
			    homes {
			      address {
			        address1
			        city
			      }
			    }
  			  }
			} """

	query = """query {
	  viewer {
	    homes {
	      currentSubscription{
	        priceInfo{
	          current{
	            level
	            total
	            startsAt
        	  }
	          today {
        	    level
	            total
	            startsAt
        	  }
	          tomorrow {
        	    level
	            total
	            startsAt
        	  }
	        }
	      }
	      consumption(resolution: HOURLY, last: 5) {
              	nodes {
	 	from
	        to
		cost
		consumption
	        }
	      }
	    }
	  }
	}"""

	url = 'https://api.tibber.com/v1-beta/gql'
	headers = {"Authorization": "Bearer 5K4MVS-OjfWhK_4yrjOlFe1F6kJXPVf7eQYggo8ebAE"}
	r = requests.post(url, json={'query': query}, headers=headers)
	print(r.status_code)
	#print(r.text)

	json_data = json.loads(r.text)

	r2 = requests.post(url, json={'query': query_name}, headers=headers)
	print(r2.text)
	json_user = json.loads(r2.text)

#	print(json_data)
#	print(json_data['data']['viewer']['homes'][0]['consumption'])
	
	name = json_user['data']['viewer']['name']
	home = json_user['data']['viewer']['homes'][0]['address']
	consumption = json_data['data']['viewer']['homes'][0]['consumption']['nodes']
	subscription = json_data['data']['viewer']['homes'][0]['currentSubscription']
	today = subscription['priceInfo']['today']

# ### Printer hele consumption til console
#	for index in range(len(consumption)):
#		for key in consumption[index]:
#			print(consumption[index][key])
# ###
	print(str(subscription['priceInfo']['today']))
	print("Her:")
	print(str(subscription['priceInfo']['today'][0]))
	print("Price: " + str(subscription['priceInfo']['current']['total']))
	print("Level: " + str(subscription['priceInfo']['current']['level']))

	#for key in consumption[index]:
	#	print(consumption[index][key])


	#data = {'apple': 67, 'mango': 60, 'lichi': 58}
	# {'level': 'CHEAP', 'total': 0.6995, 'startsAt': '2023-01-18T00:00:00.000+01:00'}
	# namwes : ['level', 'total', 'startsAt']
	# values : ['CHEAP', 0.6995, '2023-01-18T00:00:00.000+01:00']

	print("Loop:")
	fig, ax = plt.subplots(figsize =(16, 10))
	#ax.set_ylable('NOK')
	#ax.bar_label(, labels=None)
	#fig, ax = plt.subplots(figsize =(4, 3))
	#ax.grid(b = True, color ='black', linestyle ='-.', linewidth = 0.1,alpha = 0.2)
	graphdataarray = subscription['priceInfo']['today']
	i = 0
	for row in graphdataarray:
		print(row)
		names = list(row.keys())
		values = list(row.values())
		ax.bar(i,values[1],tick_label=values[2], color="blue")
		#plt.text(3, 0.25, str(values[1]),fontsize = 10, fontweight ='bold',color ='grey')
		#plt.bar(i,values[1],tick_label=values[2], color="blue")
		#plt.plot(i,values[1],tick_label=values[2])
		i = i + 1
	
	plt.xticks(range(0,24), labels=['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'])	
	plt.title("Pris i dag")
	plt.savefig('static/new_plot.png', transparent=False)

	## Ny test BARS
	pricesToDay = subscription['priceInfo']['today']
	pricesToMorrow = subscription['priceInfo']['tomorrow']
	timestamp = []
	price = []
	toMorrow_timestamp = []
	toMorrow_price = []

	for row in pricesToDay:
		timestamp.append(row['startsAt'])
		price.append(round(float(row['total']),2))

	for row in pricesToMorrow:
		toMorrow_timestamp.append(row['startsAt'])
		toMorrow_price.append(round(float(row['total']),2))

	labels = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']

	x = np.arange(len(labels))  # the label locations
	width = 0.4  # the width of the bars

	fig, ax = plt.subplots(figsize=(27,10))
	rects1 = ax.bar(x - width/2, price, width, label='ToDay')
	rects2 = ax.bar(x + width/2, toMorrow_price, width, label='ToMorrow')

	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontsize(20)
	
	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('NOK', fontsize=20)
	ax.set_title('Pris pr time', fontsize=40)
	ax.set_xticks(x, labels, fontsize=20)
	ax.legend(fontsize=20)

	ax.bar_label(rects1, padding=4,fontsize=20)
	ax.bar_label(rects2, padding=4,fontsize=20)

	fig.tight_layout()
	
	plt.savefig('static/new_plot.png', transparent=True)

	## data = subscription['priceInfo']['today'][0]
	## names = list(data.keys())
	## values = list(data.values())
	##plt.bar(0,values[1],tick_label=values[2])
	#plt.bar(1,values[1],tick_label=names[1])
	#plt.bar(2,values[2],tick_label=names[2])
	#plt.xticks(range(0,3),names)
	##plt.savefig('static/new_plot.png')
	
	
	#json_data['data']['viewer']['homes'][0]['consumption']['nodes'])
	#print(json_data['data']['viewer']['homes'][0]['consumption']['nodes'][0])

#	df = pd.DataFrame.from_dict(json_data, orient='currentSubscription')

	#df_data = json_data['data']['viewer']['homes'][0]['consumption']['nodes']
	#df = pd.DataFrame(df_data)
	#print(df)

	#table = df.to_html(index=False)

	#timestr = str(json_data['data']['viewer']['homes'][0]['consumption']['nodes'][0]['from'])
	#print("HER:")
	#print(timestr)
	#print(datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S.%f%z'))
	#ret = datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S.%f%z')

	#return json_data #json_data['data']['viewer']['homes'][0]['consumption']['nodes'][4]

	#return json_data['data']['viewer']['homes'][0]['consumption']['nodes'][0]
	#return json_data
	#return table
	#return str(ret)

	#temp = df.todict('records')
	#columnNames = df.columns.values
	#return render_template('record.html', records=temp, colnames=columnNames)
	   
	return render_template("index.html", subscription=subscription, home=home, today=today, name = 'static/new_plot.png', url ='static/new_plot.png')
	
@app.route('/test')
def chartTest():

	data = {'apple': 67, 'mango': 60, 'lichi': 58}
	names = list(data.keys())
	values = list(data.values())
	plt.bar(0,values[0],tick_label=names[0])
	plt.bar(1,values[1],tick_label=names[1])
	plt.bar(2,values[2],tick_label=names[2])
	plt.xticks(range(0,3),names)
	plt.savefig('static/new_plot.png')
	#plt.savefig('fruit.png')
	#plt.show()
	
	#return render_template('untitled1.html', name = plt.show())
	return render_template('test.html', name = 'static/new_plot', url ='static/new_plot.png')
	
@app.route('/test2')
def plot_png():
	fig = create_figure()
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')

def create_figure():
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	xs = range(100)
	ys = [random.randint(1, 50) for x in xs]
	axis.plot(xs, ys)
	return fig
	
