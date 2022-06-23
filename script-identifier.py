from bs4 import BeautifulSoup
import requests
import argparse
from termcolor import cprint
import os


class Identifier():
	def __init__(self):
		parser = self.setupParser()
		self.args = parser.parse_args()

		if(self.args.file):
			# If file specified. Get urls from the file.
			urlList = self.grabURLsFromFile(self.args.file)

		else:
			# Default behavior. User will input the urls.
			urlList = self.grabUrls()

		self.finder(urlList)
		


	def setupParser(self):
		# Start parser
		parser = argparse.ArgumentParser(description='Script Identifier')
		parser.add_argument('-f', '--file', help='Supply a file containing a list of urls to search for internal scripts.')
		return parser


	def grabUrls(self):
		# Method responsible for getting user URL inputs
		cprint("[I] Enter URLs bellow:", "cyan", attrs=["bold"])
		cprint("[I] Type \"END\" when your're done.", "cyan", attrs=["bold"])
		urls = []
		while 1:
			url = input("")
			if(url == "END"): break
			urls.append(url)

		urls = list(set(urls))
		return urls


	def grabURLsFromFile(self, filepath):
		# Method responsible for getting URL from a specified file
		cprint("[I] Reading from file.", "cyan", attrs=["bold"])
		if(not os.path.isfile(filepath)):
			cprint("[E] File not found.", "red", attrs=["bold"])
			exit()
		
		urls = open(filepath, "r").read().splitlines()
		return urls


	def finder(self, urlList):
		# Method responsible for web crawling
		cprint("\n"+"-"*50, "white", attrs=["bold"])

		resultCounter = 0

		for url in urlList:
			res = requests.get(url)
			soup = BeautifulSoup(res.content, 'html.parser')
			scrapedElementList = []



			# /\/\/\/ Add tags to grab from source code bellow
			# Example: for TAG-NAME in soup.select("TAG-NAME"): scrapedElementList.append(TAG-NAME)
			for script in soup.select("script"): scrapedElementList.append(script)
			
			# /\/\/\/ Add tags to grab from source code above


			# /\/\/\/ Add attributes to grab from source code bellow
			# Example: for ATTRIB-NAME in soup.find_all(ATTRIB-NAME=True): scrapedElementList.append(ATTRIB-NAME)
			for onclick in soup.find_all(onclick=True): scrapedElementList.append(onclick)
			
			# /\/\/\/ Add attributes to grab from source code Above

			

			filteredscrapedElementList = []
			for scrapeElement in scrapedElementList:


				# /\/\/\/ Things to filter out from the scraped data bellow
				# Example: if("KEYWORD-TO-FILTER" in str(scrapeElement)): continue
				if("labHeader.js" in str(scrapeElement)): continue
				
				# /\/\/\/ Things to filter out from the scraped data above


				# Filtering checks pass. Now add the data to final list.
				filteredscrapedElementList.append(scrapeElement)


			if(len(filteredscrapedElementList) >= 1):
				cprint("\n[+] URL: {}".format(url), "yellow", attrs=["bold"])
				
				for i in filteredscrapedElementList:
					cprint(i.prettify(), "white")
				
				print("\n")
				resultCounter += 1


		if(resultCounter == 0): cprint("[+] Nothing found", "green")




def main():
	identifier = Identifier()


if __name__ == '__main__':
	main()



		

