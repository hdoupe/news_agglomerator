from bs4 import BeautifulSoup
from datetime import datetime
from my_email import Email
from sqlite_tools.sqlite_helper import Sqlite_Helper
import os
import sqlite3
import re
import urllib2
		
class Article_Getter_sql(Sqlite_Helper):
	def __init__(self,url,tag,table,table_name):
		super(Article_Getter_sql,self).__init__(table,table_name)
		source = self.html_source(url)
		self.articles = self.parse(source,tag)
		if os.path.exists(table):
			self.connection,self.cursor = Sqlite_Helper.set_db(self)
		else:
			header = "NAME TEXT PRIMARY KEY,PUBLISHER TEXT,LINK TEXT,DATE TEXT"
			Sqlite_Helper.create(self,header)
			self.connection,self.cursor = Sqlite_Helper.set_db(self)

	def html_source(self, url):
		response = urllib2.urlopen(url)
		page_source = response.read()
		return page_source

	def parse(self,source,tag):
		
		soup = BeautifulSoup(source,'html.parser')
		
		articles = {}
		
		for node in soup.find_all(tag):
			name = str(node.get_text().replace('\n','').replace('\t','').encode('ascii','ignore'))
			for a in node.find_all('a'):
				articles[name] = str(a.get('href').encode('ascii','ignore'))
		
		return articles
	
	def insert_data(self,articles):
		self.cursor.execute("SELECT date('now')")
		todays_date = self.cursor.fetchall()[0][0]
		rows = []
		for article in articles:
			
			rows.append([article,'fivethirtyeight',str(articles[article]),todays_date])
		
		Sqlite_Helper.insert_rows(self,4,rows)

def main():
	ag = Article_Getter_sql("http://fivethirtyeight.com/",re.compile("h2|h3"),'article_getter_db.sqlite','articles')
	articles = ag.articles
	ag.insert_data(articles)
	now = datetime.now()
	d = [str(now.hour),str(now.day),str(now.month),str(now.year)+'.txt']
	path = '_'.join(d)
	txt = open(path,'w')
	txt.write(now.strftime("%H : %M %p %A %d, %B %Y") + '\n')
	ag.cursor.execute("SELECT NAME,PUBLISHER,DATE,LINK FROM articles WHERE julianday('now')-julianday(DATE) < 3 ORDER BY julianday('now')-julianday(DATE)")
	articles = ag.cursor.fetchall()
	data = {}
	for article in articles:
		if article['PUBLISHER'] in data:
			data[article['PUBLISHER']].append({'NAME':article['NAME'],
				'LINK':article['LINK'],'DATE':article['DATE']})
		else:
			data[article['PUBLISHER']] = []
			data[article['PUBLISHER']].append({'NAME':article['NAME'],
				'LINK':article['LINK'],'DATE':article['DATE']})
				
	for publisher in data:
		article_list = data[publisher]
		txt.write(publisher + '\n')
		for article in article_list:
			name = article['NAME']
			link = article['LINK']
			date = article['DATE']
			txt.write(date + '|' + name + '|' + link + '\n\n')
		txt.write('\n\n')
	txt.close()
	
	with open(path) as f: 
		data = f.read()
	
	email = Email(data)
	email.send()

if __name__ == '__main__':
	main()
