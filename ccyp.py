import requests
import re
from bs4 import BeautifulSoup
from datetime import date 
from os import path

class CCYP:
	site = "https://jobs.ccyp.com"
	start_url = "https://jobs.ccyp.com/Category?filter=normal"
	# get Category page url
	def get_urls(self, page_num=None):
		# page_num = page_num or self.page_limit
		urls = []
		# get 2 pages info 
		for i in range(1,2):
			page_url = f"https://jobs.ccyp.com/Category?page={i+1}&filter=normal"
			urls.append(page_url)
		# print(urls)
		return urls
	# get all single post urls under specific category
	def get_pages(self):
		urls = self.get_urls()
		links = []
		for url in urls:
			page = requests.get(url)
			# get href
			# get date
			list_soup = BeautifulSoup(page.content, 'html.parser')
			result = list_soup.find("table")
			if result:
				rows = result.find_all("tr")
				for row in rows:
					# release_date = row.find("span", class_="text-secondary h7").text
					# print(release_date)
					href_ = row.find("h6").find("a", href=True)
					link = "https://jobs.ccyp.com/"+href_['href']
					links.append(link)
					# print(link)
		return links
	# get email from that specific page 
	def get_emails(self):
		datestr = date.today().strftime("%Y%m%d")
		#  file exits: append to the end of the file 
		if path.exists(f"{datestr}.csv")==True:
			f = open(f"{datestr}.csv", "a")
		# file doesn't exit, create and write to new file 	
		else:
			f = open(f"{datestr}.csv", "w")
		links = self.get_pages()
		for url_ in links:
			print(url_)
			page = requests.get(url_)
			soup = BeautifulSoup(page.content, 'html.parser')
			results = soup.find("div", class_="job-details-content")
			if results:
				cate = results.find('h6', class_="card-title mb-4")
				print(cate.text)
				pure_email = self.trim_email(cate.text)
				#  string not empty then write to file 
				if pure_email !="":
					f.write(pure_email+"\n")
		f.close()
	#  get pure email out of text	
	def trim_email(self, text=None):
		if not text:
			return None
		else:
			try:
				ans = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
			except:
				ans = None
		# print(ans)
		# convert list to string 
		return ''.join(ans)
				
c = CCYP()
print(c.get_urls())
c.get_emails()