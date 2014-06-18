#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import urllib
import os
import logging
import json
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import datetime as datetime

def get_price(symbol):
	url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, 'l1')
	return urllib.urlopen(url).read().strip().strip('"')
	
class Portfolio(db.Model):
	portName = db.StringProperty()
	portDesc = db.StringProperty()

class Stock(db.Model):
	ticker = db.StringProperty()
	port = db.ReferenceProperty(Portfolio)
	shares = db.StringProperty()
	dtime = db.DateTimeProperty()
	price = db.StringProperty()

class stockhandler(webapp2.RequestHandler):
	def get(self):
		userAction = self.request.url.split("/")[4];
		logging.info("URL4 is "+userAction);
		if userAction == 'price':
			stksymbol = self.request.url.split("/")[5];
			price = get_price(stksymbol)
			resultDict = {'responseQuote': 'The stock price of ' + stksymbol + ' is: ' + price}
			curtime = datetime.datetime.now()
			logging.info("current time = " + str(curtime) +". Just looked up "+stksymbol)
			#newstock = Stock(dtime = curtime, ticker=stksymbol, price=price)
			#newstock.put()
			temp = os.path.join(
				os.path.dirname(__file__),
				'resQuote.html')
			outstr = template.render(
				temp,
				resultDict)
			self.response.out.write(outstr)
		elif userAction == 'delete':
			logging.info("GET delete for stocks")
			stksymbol = self.request.url.split("/")[5];
			portname = self.request.url.split("/")[6];
			stockRes = db.GqlQuery("SELECT * FROM Stock WHERE ticker = :1", stksymbol)
			for e in stockRes:
				if e.port.portName == portname:
					e.delete()
					logging.info("Deleted item")
				logging.info("In delete object area")
				portKey = e
			self.response.out.write('Deleted '+stksymbol +' in "'+portname+'" portfolio.')
		elif userAction == 'allStocks':
			logging.info("GET listAll for stocks")
			que = db.Query(Stock)
			results = que.fetch(limit=200)
			stockTable = []
			for eachstk in results:
				stockentry = {}
				stockentry['ticker'] = eachstk.ticker
				stockentry['shares'] = eachstk.shares
				portfolio_name = eachstk.port.portName
				logging.info(portfolio_name)
				stockentry['portfolio'] = portfolio_name
				stockTable.append(stockentry)
			str_json = json.dumps(stockTable)
			self.response.out.write(str_json)	
		else:
			self.response.out.write("hello123")
	def post(self):
		userAction = self.request.url.split("/")[4];
		logging.info("add or update stocks")
		stksymbol = self.request.get('ticker')
		numshares = self.request.get('shares')
		portname = self.request.get('portname')
		stockprice = get_price(stksymbol)
		logging.info("Ticker: " + str(stksymbol) + " Shares: " + str(numshares))
		curtime = datetime.datetime.now()
		q = Portfolio.all()
		q.filter("portName =", portname)
		portRes = q.get()
		logging.info("Right before query area")
		stockRes = db.GqlQuery("SELECT * FROM Stock WHERE port = :1 AND ticker = :2", portRes, stksymbol)
		temp = 0
		for e in stockRes:
			logging.info("In UPDATE area")
			e.ticker = stksymbol
			e.shares = numshares
			e.port = portRes
			e.price = stockprice
			e.dtime = curtime
			db.put(e)
			temp = temp + 1
			logging.info("UPDATING: "+stksymbol)
			self.response.out.write("Updated: " + str(numshares) + " shares of " + stksymbol +" in "+portname+" portfolio.")
		if temp == 0:
			logging.info("In ADD area")
			newstock = Stock(ticker=stksymbol, shares=numshares, port=portRes, price=stockprice, dtime = curtime)
			newstock.put()
			logging.info("ADDING: "+stksymbol)
			self.response.out.write("Added: " + str(numshares) + " shares of " + stksymbol +" in "+portname+" portfolio.")
		
			
class portfoliohandler(webapp2.RequestHandler):
	def get(self):
		userAction = self.request.url.split("/")[4];
		if userAction == 'fullList':
			logging.info("GET full list of portfolios")
			que = db.Query(Portfolio)
			outstr = ""
			results = que.fetch(limit=200)
			counter = 0
			for eachPort in results:
			#	price = get_price(eachstk.ticker)
			#	value = float(price) * float(eachstk.shares)
			#	portTotal = portTotal + value
				if counter == 0:
					outstr = outstr + str(eachPort.portName)
					counter = counter + 1
				else:
					outstr = outstr + ", " + str(eachPort.portName)
				logging.info("Portfolio: " + str(eachPort.portName))
				logging.info("Portlist: " + outstr)
			self.response.out.write("Portfolio List: " + outstr)
		elif userAction == 'portfolioDetails':
			portname = self.request.url.split("/")[5];
			#portfolio_k = db.Key.from_path('Portfolio', portname)
			#portfolio = db.get(portfolio_k)
			#portStocks = db.GqlQuery("SELECT * FROM Stock WHERE port = :1", portname)
			portRes = db.GqlQuery("SELECT * FROM Portfolio WHERE portName = :1", portname)
			stockInfo = ''
			logging.info('0')
			for e in portRes:
				logging.info('1')
				stockRes = db.GqlQuery("SELECT * FROM Stock WHERE port = :1", e)
				logging.info('2')
				portDescription = e.portDesc
				logging.info('3')
				counter = 0
				totalValue = 0
				for stock in stockRes:
					logging.info('4')
					sTicker = stock.ticker
					sShares = stock.shares
					currentPricePerShare = get_price(sTicker)
					currentValue = float(currentPricePerShare) * int(sShares)
					totalValue = totalValue + currentValue
					if counter == 0:
						stockInfo = stockInfo + 'The "'+portname+'" portfolio has the following stocks:<p> <p>- '+sShares+' shares of ' +sTicker +', currently valued overall at $'+str(currentValue)+'<p>'
						counter = counter + 1
					else:
						stockInfo = stockInfo + ' - '+sShares + ' shares of ' +sTicker +', currently valued overall at $'+str(currentValue)+'<p>'
			logging.info('5')
			outstr = 'The "'+portname+'" portfolio is described as "'+portDescription+'". '+stockInfo+' The total value of this portfolio is currently $'+str(totalValue)
			self.response.out.write(outstr)
		elif userAction == 'portfolioDelete':
			portname=self.request.get('portname')			
			logging.info("GET delete for a portfolio")
			portname = self.request.url.split("/")[5];
			portRes = db.GqlQuery("SELECT * FROM Portfolio WHERE portName = :1", portname)
			for e in portRes:
				stockRes = db.GqlQuery("SELECT * FROM Stock WHERE port = :1", e)
				for stock in stockRes:
					stock.delete()
				e.delete()
				logging.info("Deleted item")
			logging.info("In delete object area")
			self.response.out.write('Deleted "'+portname +'" portfolio.')
		
	def post(self):
		logging.info("post for portfolio")
		portname=self.request.get('portname')
		portdesc=self.request.get('portdesc')
		logging.info("portfolio name: " + portname)
		newport = Portfolio(key_name=portname, portName=portname, portDesc=portdesc)
		newport.put()
		logging.info("added portfolio " + portname)
		self.response.out.write("Added portfolio: "+portname)
		
app = webapp2.WSGIApplication([
	('/stock/.*', stockhandler),
	('/portfolio/.*', portfoliohandler),
], debug=True)
