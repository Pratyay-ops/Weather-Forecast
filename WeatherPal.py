#!/usr/bin/env python3

#Import all the required libraries
import requests , typer , os , time 
from dotenv import load_dotenv
#Create a typer object
app = typer.Typer()
@app.command()
#Create a function to get the weather data
def get_data_current():
    load_dotenv()
    #Print the banner
    banner = """
██╗    ██╗███████╗ █████╗ ████████╗██╗  ██╗███████╗██████╗
██║    ██║██╔════╝██╔══██╗╚══██╔══╝██║  ██║██╔════╝██╔══██╗
██║ █╗ ██║█████╗  ███████║   ██║   ███████║█████╗  ██████╔╝
██║███╗██║██╔══╝  ██╔══██║   ██║   ██╔══██║██╔══╝  ██╔══██╗
╚███╔███╔╝███████╗██║  ██║   ██║   ██║  ██║███████╗██║  ██║
 ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

               ██████╗  █████╗ ██╗
               ██╔══██╗██╔══██╗██║
               ██████╔╝███████║██║
               ██╔═══╝ ██╔══██║██║
               ██║     ██║  ██║███████╗
               ╚═╝     ╚═╝  ╚═╝╚══════╝


            """
    print(banner)
    #Get the location from the user
    location = input("[+]Enter location:")
    #Construct the url from base_url and location
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    url = construct_url(location,base_url)
    #Get the response from the url
    response = requests.get(url)
    #Check if the response is valid
    response = requests.get(url)
    if response.status_code == 404:
        print('Error: 404 City not found.')
    else:
        try:
            response.raise_for_status()
            data = response.json()
            prettify(data)
        except requests.exceptions.RequestException as e:
            print('Error:', e)
#create a function to cleanup the response from the api
def prettify(response):
    print("____LOCATION DATA__________")
    print(f"Longitude:{response['coord']['lon']} Latitude:{response['coord']['lat']}\n")
    print(f"Current date is:{time.gmtime(response['dt'])[2]}/{time.gmtime(response['dt'])[1]}/{time.gmtime(response['dt'])[0]}")
    print(f"The weather condition right now is {response['weather'][0]['main']}\n")
    print("____WEATHER DATA__________")
    print("1.Temperature")
    print(f"\tCurrent Temperature: {response['main']['temp']}"+chr(176)+"C")    
    print(f"\tFeels Like: {response['main']['feels_like']}"+chr(176)+"C")
    print(f"\tMinimum Temperature: {response['main']['temp_min']}"+chr(176)+"C")
    print(f"\tMaximum Temperature: {response['main']['temp_max']}"+chr(176)+"C")
    print(f"\tCurrent Temperature: {response['main']['temp']}"+chr(176)+"C")
    print(f"2.Pressure:{response['main']['pressure']} mb")
    print(f"3.Humidity: {response['main']['humidity']}")
    print("4.Wind")
    print(f"\tWind Speed: {response['wind']['speed']} km/h")
    print(f"\tWind Degree: {response['wind']['deg']}"+chr(176))
#create a function to construct the url for location
def construct_url(location,base_url):
    api_key = os.getenv('api_key')
    query_parameters = f"q={location}&appid={api_key}&units=metric"
    complete_url=base_url+query_parameters
    return complete_url

if __name__=="__main__":
    app()
