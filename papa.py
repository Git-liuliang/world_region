#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 下午3:02
# @Author  : liuliangliang
# @Site    : 
# @File    : papa.py
# @Software: PyCharm

from bs4 import BeautifulSoup
import requests
import json



def get_data_by_bs(soup,res):
    for num,i in enumerate(soup.table.children,start=1):

        if num < 5 or i == '\n':
            pass
        else:
            ret = i.text.split('\n')
            if len(ret) > 4:
                item = [ret[1],ret[4].split(',')[-1].strip()]
                res.append(item)

    return res

def chosen_region():

 #    regions = {"United States": [], "Europe": [], "Asia": [], "South America": [], "India": [], "Canada": [],
 # "Japan": [], "Australia": []}
    regions = {"Americas":[],"Asia":[],"Europe":[],"Oceania":[],"Africa":[]}
    country_list = {}
    for regionname in regions:

        s = requests.get('https://restcountries.eu/rest/v2/region/%s'%regionname)
        res = json.loads(s.text)
        for im in res:
            if im.get('region') == 'Asia' or im.get('region') == 'Europe' or im.get('region') == 'Americas' :
                if im.get('subregion') == 'South America':
                    country_list[im.get('name')] = im.get('subregion')

                else:
                    country_list[im.get('name')] = im.get('region')
            else:
                if im.get('region') == 'Oceania':
                    country_list[im.get('name')] = 'Australia'
                if im.get('region') == 'Africa':
                     country_list[im.get('name')] = 'India'

    return country_list


def get_code():

    res = []
    for item in [chr(i) for i in range(65, 91)]:
        s = requests.get('https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code:_%s' % item)
        soup = BeautifulSoup(s.text, 'html.parser')

        res = get_data_by_bs(soup, res)

    return res



def switch(item):
    switcher = {
        "Iran": 'Asia',
        "Russia": 'Europe',
        "United Kingdom":'Europe',
        "Venezuela":'South America',
        "Syria":'Asia',
        "Republic of the Congo":'India',
        "Laos":'India',
        "Bolivia":'South America',
        "Tanzania":'India',
        "Ivory Coast":'India',
        "East Timor":'Asia',
        "North Korea":'Asia',
        "South Korea":'Asia',
        "Vietnam":'Asia',
        "British Overseas Territory of Turks and Caicos Islands":'Europe',
        "Macedonia":'Europe',
        "United States Virgin Islands":'Europe',
        "Simferopol":'Europe',
        "United States":'United States',
        "Democratic Republic of the Congo":'India',
        "Moldova":'Europe',
        "Federated States of Micronesia":'Australia',
        "1 Malaysia":'Asia',
        "2 Germany":'Europe',



    }
    return switcher.get(item,None)

def result_list():

    last = chosen_region()
    d = get_code()
    for item in d:
        if last.get(item[-1]):
            item.append(last.get(item[-1]))
        else:
            if switch(item[1]):
                item.append(switch(item[1]))
            else:
                item.append('Europe')
    return d


if __name__ == '__main__':

    final_dict = {}
    res = result_list()
    # print(res)
    for item in res:
        final_dict[item[0]] = item[-1]
        if item[-1] == 'Americas':
            if item[1] == 'Canada':
                final_dict[item[0]] = 'Canada'
            else:
                final_dict[item[0]] = 'United States'
        if item[-1] == 'Asia':
            final_dict[item[0]] = 'Asia'
            if item[1] == 'India':
                final_dict[item[0]] = 'India'
            if item[1] == 'Japan':
                final_dict[item[0]] = 'Japan'


    print(final_dict)

    with open('ITAT.json','w')as f:
        json.dump(final_dict,f)
        print('ok')









