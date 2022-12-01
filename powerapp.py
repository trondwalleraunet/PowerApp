from flask import Flask, render_template
import requests
import json
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def my_app():
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
	headers = {"Authorization": "Bearer dUYmM7LqSBZ9YLadzZGYq1Rb7dxezY61QtS87v8919g"}
	r = requests.post(url, json={'query': query}, headers=headers)
	print(r.status_code)
	#print(r.text)

	json_data = json.loads(r.text)

#	print(json_data)
	print(json_data['data']['viewer']['homes'][0]['consumption'])


#	df = pd.DataFrame.from_dict(json_data, orient='currentSubscription')

	df_data = json_data['data']['viewer']['homes'][0]['consumption']['nodes']
	df = pd.DataFrame(df_data)
	print(df)

	table = df.to_html(index=False)

	timestr = str(json_data['data']['viewer']['homes'][0]['consumption']['nodes'][0]['from'])
	print("HER:")
	print(timestr)
	print(datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S.%f%z'))
	ret = datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S.%f%z')

	#return json_data #json_data['data']['viewer']['homes'][0]['consumption']['nodes'][4]
	#return table
	#return str(ret)
	temp = df.todict('records')
	columnNames = df.columns.values
	return render_template('record.html', records=temp, colnames=columnNames)