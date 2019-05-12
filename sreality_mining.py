#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import codecs
from selenium import webdriver
import datetime


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def hasItem(item, title):
	value = None
	tmp = item.find_elements_by_css_selector("span.icon-ok")
	if len(tmp) > 0:
		return 1
	tmp = item.find_elements_by_css_selector("span.icon-cross")
	if len(tmp) > 0:
		return 0
	tmp = item.find_elements_by_css_selector("strong.param-value span")[0].text	
	if tmp and RepresentsInt(tmp):
		return 1
	if value is None:
		print("!!! Value not found for " + title)
		return 0
	else:
		return value



options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')
browser = webdriver.Chrome("chromedriver.exe", options=options)


kraje = [
	"vysocina-kraj",
	"zlinsky-kraj",
	"moravskoslezsky-kraj",
	"pardubicky-kraj",
	"jihocesky-kraj",
	"praha",
	"stredocesky-kraj",
	"kralovehradecky-kraj",
	"liberecky-kraj",
	"ustecky-kraj",
	"plzensky-kraj",
	"karlovarsky-kraj",
	"jihomoravsky-kraj",
	"olomoucky-kraj"
]

for kraj in kraje:
	print("--------------------------------------------------------------------")
	print("-------------- " + kraj + " --------------")
	print("--------------------------------------------------------------------")

	file = codecs.open("sreality-" + str(datetime.date.today()) + "-" + kraj + ".csv", "w", "utf-8")
	file.write("pokoje;m2;podlaží;energetická hodnota;terasa;balkon;lodzie;sklep;parkovani;garaz;vytah;vlastnictví;stav;stavba;město;ulice;cena;url\n")	

	urls = []
	krajUrl = "https://www.sreality.cz/hledani/prodej/byty/" + kraj + "?stari=mesic&bez-aukce=1&strana="
	
	count = 1
	while(1):
		krajUrlPaged = krajUrl + str(count)
		
		print(krajUrlPaged)	
		browser.get(krajUrlPaged)
		
		items = browser.find_elements_by_css_selector("div.dir-property-list h2 a.title")
		if (len(items) == 0):
			break;
		
		for link in items:
			href = link.get_attribute("href")
			if href not in urls:
				#print(href)
				urls.append(href)
		
		count = count + 1
	
	size = len(urls)
	
	print("--------------------------------------------------------------------")
	print("-------------- " + str(size) + " --------------")
	print("--------------------------------------------------------------------")
			
	for url in urls:
		print(url)
		browser.get(url)

		pokoje = None
		m2 = None
		podlazi = None
		energetickaHodnota = None
		terasa = None
		balkon = None
		lodzie = None
		sklep = None
		parkovani = None
		garaz = None
		vytah = None
		vlastnictvi = None
		stav = None
		stavba = None
		mesto = None
		ulice = None
		cena = None
		
		try:
			items = browser.find_elements_by_css_selector("h1.error-description")
			if (len(items) != 0):
				size = size - 1
				print("inzerat uz neexistuje")
				continue;
			
			items = browser.find_elements_by_css_selector("h1 span.name")
			regex = re.search('Prodej bytu ([^\s]+) ([\d]+)', items[0].text)
			pokoje = regex.group(1)
			m2 = regex.group(2)
			
			items = browser.find_elements_by_css_selector("h1 span.location")
			tmp = items[0].text
			
			if tmp.startswith("ulice "):
				tmp = tmp.replace("ulice ", "")
				regex = re.search('([^,]+), ([^-]+)', tmp)
				ulice = regex.group(1)
				mesto = regex.group(2).strip()
			else:
				#print("!!! Bez ulice")
				ulice = ""
				regex = re.search('([^-]+)', tmp)
				mesto = regex.group(1).strip()

			items = browser.find_elements_by_css_selector("div.params ul li.param")
			for item in items:
				label = item.find_elements_by_css_selector("label.param-label")[0].text
				if label == "Podlaží:":
					tmp = item.find_elements_by_css_selector("strong.param-value span")[0].text
					if (tmp == "přízemí"):
						podlazi = "1"
					else:
						podlazi = re.search('([\d]+)', tmp).group(1)
				elif label == "Energetická náročnost budovy:":
					tmp = item.find_elements_by_css_selector("strong.param-value span")[0].text
					tmp = tmp.replace("Třída ", "")
					energetickaHodnota = re.search('([A-Z]+)', tmp).group(1)
				elif label == "Terasa:":
					terasa = hasItem(item, label)
				elif label == "Balkón:":
					balkon = hasItem(item, label)
				elif label == "Lodžie:":
					lodzie = hasItem(item, label)
				elif label == "Sklep:":
					sklep = hasItem(item, label)
				elif label == "Parkování:":
					parkovani = hasItem(item, label)
				elif label == "Garáž:":
					garaz = hasItem(item, label)
				elif label == "Výtah:":
					vytah = hasItem(item, label)
				elif label == "Vlastnictví:":
					vlastnictvi = item.find_elements_by_css_selector("strong.param-value span")[0].text
				elif label == "Stav objektu:":
					stav = item.find_elements_by_css_selector("strong.param-value span")[0].text			
				elif label == "Stavba:":
					stavba = item.find_elements_by_css_selector("strong.param-value span")[0].text				
				elif label == "Celková cena:":
					tmp = item.find_elements_by_css_selector("strong.param-value span")[0].text
					tmp = tmp.replace(" ", "")
					cena = re.search('([\d]+)', tmp).group(1)
					
			if pokoje == None:
				print("pokoje not found")
				pokoje = ""
			if m2 == None:
				print("m2 not found")
				m2 = ""
			if podlazi == None:
				print("podlazi not found")
				podlazi = ""
			if energetickaHodnota == None:
				#print("energetickaHodnota not found")
				energetickaHodnota = "0"
			if terasa == None:
				#print("terasa not found")
				terasa = 0
			if balkon == None:
				#print("balkon not found")
				balkon = 0
			if lodzie == None:
				#print("lodzie not found")
				lodzie = 0
			if sklep == None:
				#print("sklep not found")
				sklep = 0
			if parkovani == None:
				#print("parkovani not found")
				parkovani = 0
			if garaz == None:
				#print("garaz not found")
				garaz = 0
			if vytah == None:
				#print("vytah not found")
				vytah = 0
			if vlastnictvi == None:
				print("vlastnictvi not found")
				vlastnictvi = ""
			if stav == None:
				print("stav not found")
				stav = ""
			if stavba == None:
				print("stavba not found")
				stavba = ""
			if mesto == None:
				print("mesto not found")
				mesto = ""
			if ulice == None:
				print("ulice not found")
				ulice = ""
			if cena == None:
				size = size - 1
				print("cena not found")
				continue;		
				
			file.write(pokoje + ";" + m2 + ";" + podlazi + ";" + energetickaHodnota + ";" + str(terasa) + ";" + str(balkon) + ";" + str(lodzie) + ";" + str(sklep) + ";" + str(parkovani) + ";" + str(garaz) + ";" + str(vytah) + ";" + vlastnictvi + ";" + stav + ";" + stavba + ";" + mesto + ";" + ulice + ";" + cena + ";" + url + "\n")
		except Exception as e:
			print("!!! " + url)
			print(e)
			size = size - 1
	
	print("---- CELKEM " + str(size) + " pro " + kraj + " ----")
	file.close()

browser.close()


