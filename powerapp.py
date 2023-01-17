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
	print('Test')

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
	print("Price: " + str(subscription['priceInfo']['current']['total']))
	print("Level: " + str(subscription['priceInfo']['current']['level']))

	#for key in consumption[index]:
	#	print(consumption[index][key])


	
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
	   
	return render_template("index.html", subscription=subscription, home=home, today=today)
	
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
	
