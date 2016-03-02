from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import MySQLdb

browser = webdriver.Firefox()
url = 'https://42matters.com/app-market-explorer/android'
browser.get(url)
time.sleep(5)
browser.find_element_by_xpath('//*[@id="query-form"]/div/div[1]/div[1]/button[3]').click()
time.sleep(5)
browser.find_element_by_xpath('//*[@id="aql-results"]/div[1]/select[1]/option[contains(text(), "Downloads")]').click()
time.sleep(5)
# browser.find_element_by_xpath('//*[@id="aql-results"]/div[1]/select[2]/option[contains(text(), "Ascending")]').click()
# time.sleep(5)

page_no = 1
while page_no<139:
	browser.find_element_by_xpath('//*[@id="aql-results"]/div[1]/button[1]').click()
	page_no = page_no +1
	time.sleep(5)

count = 39020

while page_no<501:
	scroll = 0
	i = 0
	while scroll<15:
		browser.find_element_by_class_name("list-title").send_keys(Keys.SPACE)
		time.sleep(1)
		scroll = scroll + 1

	parse = BeautifulSoup(browser.page_source, "html.parser")
	
	prices = parse.findAll('p', {'class':'list-price'})
	titles = parse.select('a[class=ng-binding]')
	
	while i<len(titles):
		title = str((titles[i].getText()).encode('ascii', 'ignore'))
		print "Game No " + str(count) + " " + title + " of page " + str(page_no)
		link = str(titles[i].get('href'))
		price_value = prices[i].getText()
		if ( price_value == 'FREE'):
			amount = 0
		else:
			amount = float(str(price_value[1:]))
		
		db = MySQLdb.connect(user= 'root', passwd = 'suna', db = 'dataset', host = 'localhost')
		cursor = db.cursor()
		try:
		   cursor.execute("INSERT INTO url VALUES(%d, '%s', '%s', %f);"%(count, title, link, amount))
		   db.commit()
		except:
		   db.rollback()
		i = i + 1
		count = count + 1

	browser.find_element_by_xpath('//*[@id="aql-results"]/div[3]/button[1]').click()
	page_no = page_no +1
	time.sleep(5)

db.close()
