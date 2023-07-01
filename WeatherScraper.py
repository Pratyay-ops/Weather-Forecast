import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search


def getURL(location):
    query = "IBM Weather Channel" + location + "Today Weather"
    for i in search(query,tld="com",stop=1):
        url = i
    if "https://weather.com/en-IN/weather/today/l/" in url:
        return url
    else: 
        return -1

def get_html(url):
    html = requests.get(url)
    htmlContent = html.content
    return htmlContent

def parseHTML(html):
    soup = BeautifulSoup(html, features="html.parser")
    return soup

def get_current_Data(soup):
    location ="".join(soup.find("header",{"class":"Card--cardHeader--3NRFf"}).h2.get_text().split()[3:])  ## WHY DOES THIS GOVE NONE FOR CHENNAI?????
    feels_like = soup.find("span",{"class":"TodayDetailsCard--feelsLikeTempValue--2icPt"}).get_text() + "C"
    wind_direction_num = int(str(soup.find("svg",{"class":"Icon--icon--2aW0V Icon--darkTheme--1PZ-8","name":"wind-direction"}).get_attribute_list("style")).split("rotate(")[1].split("deg")[0])
    if(wind_direction_num>0 and wind_direction_num<90):
        wind_direction = "SW"
    if(wind_direction_num>90 and wind_direction_num<180):
        wind_direction = "NW"
    if(wind_direction_num>180 and wind_direction_num<270):
        wind_direction = "NE"
    if(wind_direction_num>270 and wind_direction_num<360):
        wind_direction = "SE"
    wind_speed_kmh = float(soup.find("span",{"class":"Wind--windWrapper--3Ly7c undefined"}).get_text().split("Direction")[1].split(" ")[0])
    current_temp = soup.find("span",{"class":"CurrentConditions--tempValue--MHmYY"}).get_text()+"C"
    condition = soup.find("div",{"class":"CurrentConditions--phraseValue--mZC_p"}).get_text()
    humidity = soup.find("span",{"data-testid":"PercentageValue"}).get_text()
    visibility= soup.find("span",{"data-testid":"VisibilityValue"}).get_text()
    pressure  = soup.find("span",{"data-testid":"PressureValue"}).get_text()
    
    
    conditions = {"Location":location,"Feels like":feels_like,"Wind direction":wind_direction,"Wind Speed":str(wind_speed_kmh)+" kmh","Current Temp":current_temp,"Condition":condition,"Humidity":humidity,"Visibility":visibility,"Pressure":pressure}
    return conditions


def main():
    location = input("Enter Location:")
    url = getURL(location)
    if(url == -1):
        print("Cannot get URL.Please visit IBM Weather Channel, find the page for today's forecast of your place and enter the url.")
        url = input("Enter URL:")
    html = get_html(url)
    soup = parseHTML(html)
    conditions = get_current_Data(soup)
    
    print("________________CURRENT__________________")
    for key in conditions:
        print(key +":"+ str(conditions[key]))


main()