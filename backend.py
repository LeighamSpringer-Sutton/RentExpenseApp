import requests
from bs4 import BeautifulSoup
from db import Db
import sqlite3
import os




CITIES = ["Vancouver", "Edmonton", "Toronto", "Montreal", "Ottawa", \
          "Calgary", "Hamilton", "Winnipeg", "Quebec-City", "Newmarket-ON-Canada","Halifax"]


PROVINCES = ["Ontario","Quebec","British Columbia","Alberta","Manitoba","Saskatchewan",\
             "Nova Scotia","New Brunswick",]



PROVINCES_CITIES ={"Toronto,Ottawa,Hamilton,Newmarket-ON-Canada":"Ontario","Montreal,Quebec-City":"Quebec",\
                   "Vancouver":"British Columbia","Edmonton,Calgary":"Alberta",
                    "Winnipeg":"Manitoba","Halifax":"NovaScotia"}



def create_and_store(pc):
    counter2 =1
    endtg = '<'
    db = Db("CityExpenses")
    db.create_table()
    for city in CITIES:

        r = requests.get("https://www.numbeo.com/cost-of-living/in/"+city)
        soup = BeautifulSoup(r.text,features="lxml")
        counter = 0
        pricing = {}
        b = soup.body
        for i in b.find_all('td', class_="tr_highlighted"):
            data = str(i).split('>')[1]
            data = data[0:data.index(endtg)]
            if "span" not in data and len(data) > 1:
                counter += 1

                if counter % 2 != 0:
                    pricing[data] = 0
                    prev = data
                else:
                    pricing[prev] = float(''.join([i for i in data if i.isdigit() or i == '.']))
        one_apr = pricing["Apartment (1 bedroom) Outside of Centre "]
        three_apr = pricing["Apartment (3 bedrooms) Outside of Centre "]
        province = get_province(city,pc)
        description = wiki_data(city)
        db.insert_into(city, one_apr, three_apr,description,province)
        counter2+=1
    db.close_database()
def wiki_data(city):
    cityformated = 0
    if city == 'Quebec-City':
        cityformated = "Quebec"
    elif city == 'Newmarket-ON-Canada':
        cityformated = "Newmarket,_Ontario"
    elif city == 'Hamilton':
        cityformated = "Hamilton,_Ontario"
    elif city == "Halifax":
        cityformated = "Halifax, _Nova_Scotia"
    if cityformated:
        url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles="+cityformated
    else:
        url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=" + city
    r = requests.get(url)
    r = r.text.split(":")
    data = r[-1]
    return data

def get_netincome(province,salary):
    url = "https://neuvoo.ca/tax-calculator/?iam=&salary=+" + str(salary)+"+&from=year&region="+province
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="xml")
    soup = soup.body
    soup_label  = soup.find_all('div', class_="deduction-label")
    soup_deduction =soup.find_all('div', class_="deduction-value")
    tax_deduction_data = {}
    for label,soup_deduction in zip(soup_label,soup_deduction):
        label = str(label).split(">")[1].split("<")[0]
        deduction = ("".join([i for i in str(soup_deduction).split(">")[1].split("<")[0] if i.isdigit()\
                              or i =='.' or i =='$' or i ==',']))
        if label != "Salary":
            tax_deduction_data[label] =deduction
    return tax_deduction_data

def get_province(city,pc):
    for cities, province in pc.items():
        if city in cities:
            return pc[cities]











