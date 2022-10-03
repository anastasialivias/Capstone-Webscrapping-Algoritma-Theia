from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data#panel',  headers = { 'User-Agent': 'Popular browser\'s user-agent', })
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('tbody')
row = table.find_all('th', attrs={'scope':'row','class':'font-semibold text-center'})
row_length = len(row)

row_2 = table.find_all('td', attrs={'class':'text-center'})
row_length_2 = len(row_2)

temp = [] #initiating a tuple

for i in range(0, row_length):
    period = table.find_all('th', attrs={'scope':'row','class':'font-semibold text-center'})[i].text
 
    temp.append(period)
    
temp

temp2 = [] #initiating a tuple
    
for i in range(1, row_length_2, 4): 


    volume = table.find_all('td', attrs={'class' : 'text-center'})[i].text
    
    volume = volume.strip()
    
    temp2.append(volume)
    
temp2

#change into dataframe
df = pd.DataFrame({
    'Date' : temp,
    'Volume' : temp2
}, columns=['Date','Volume'])

df_bydate = df.sort_values(by='Date', ascending=True)
df_bydate_index = df_bydate.set_index('Date')

#insert data wrangling here
df_bydate_index['Volume'] = df_bydate_index['Volume'].str.replace("$", "")
df_bydate_index['Volume'] = df_bydate_index['Volume'].str.replace(",","")
df_bydate_index['Volume'] = df_bydate_index['Volume'].astype('int64')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df_bydate_index["Volume"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df_bydate_index.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)