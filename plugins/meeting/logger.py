# -*- coding: UTF-8 -*-
import xml.etree.cElementTree as etree
import os, time, unicodedata, ConfigParser

class log:
	def __init__(self, logsdir):
		#################
		#	Root	#
		#################
		#Creating the root of the tree as "pacbot" should to be: <pacbot></pacbot>
		self.root = etree.Element("pacbot")
		self.createLeaf();
		self.body = etree.Element("body")
		self.protocol = etree.Element("protocol")
		self.root.append(self.leafDeatils)
		self.root.append(self.body)
		self.root.append(self.protocol)
		self.logspath = logsdir
		self.WriteToFile()
	#########################
	#	leafDetails	#
	#########################
	def createLeaf(self):
		# Creating the details leaf. should to be <details></details>
		self.leafDeatils = etree.Element("details")
		# creating the date leaf to append onto details
		
		date = etree.Element("date") # <date></date>
		day = etree.Element("day") # <day></day>
		month = etree.Element("month") # <month></month>
		year = etree.Element("year") # <year></year>
		ttime = etree.Element("time") # <time></time>
		
		# Inserting data to day, month, year, time
		day.text = time.strftime("%d", time.localtime())
		month.text = time.strftime("%m", time.localtime())
		year.text = time.strftime("%Y", time.localtime())
		ttime.text = time.strftime("%H:%M:%S", time.localtime())
		date.append(day)
		date.append(month)
		date.append(year)
		date.append(ttime)
		
		# And do the same for the rest...
		self.operator = etree.Element("operator")
		self.keyword = etree.Element("keywords")
		
		#Appending all fields to leafDetails
		self.leafDeatils.append(date)
		self.leafDeatils.append(self.operator)
		self.leafDeatils.append(self.keyword)
	#########################
	#	addLog		#
	#########################
	def addLog(self, nick, msg):
		logtag = etree.Element("log")
		sender = etree.Element("sender")
		sender.text =  unicode(nick, "UTF-8")
		logtag.append(sender)
		msgtime = etree.Element("time")
		logtag.append(msgtime)
		msgtime.text = time.strftime('%H:%M:%S',time.localtime())
		message = etree.Element("msg")
		message.text = unicode(msg, "UTF-8")
		logtag.append(message)
		self.body.append(logtag)
		self.WriteToFile()
	
	def setKeywords(self, keys):
		self.keyword.text = unicode(keys, "UTF-8")
		self.WriteToFile()
		
	def setOper(self, nick):
		self.operator.text = unicode(nick, "UTF-8")
		self.WriteToFile()
		
	def addTopic(self,title):
		self.topic = etree.Element("topic")
		name = etree.Element("name")
		name.text = unicode(title, "UTF-8")
		self.topic.append(name)
		self.protocol.append(self.topic)
		self.WriteToFile()
		
	def addVote(self, subject, results):
		vote = etree.Element("vote")
		sub = etree.Element("subject")
		sub.text = unicode(subject,"UTF-8")
		vote.append(sub)
		declined = etree.Element("decliend")
		declined.text = str(results['decline'])
		vote.append(declined)
		agree = etree.Element("agree")
		agree.text = str(results['agree'])
		vote.append(agree)
		avoid = etree.Element("avoid")
		avoid.text = str(results['avoid'])
		vote.append(avoid)
		self.topic.append(vote)
		self.WriteToFile()
	def WriteToFile(self):
		logdir=self.logspath+"logs/"
		searchdir=self.logspath+"./"
		self.logsxml = etree.tostring(self.root, "utf-8")
		self.logsfilename = "%s.xml" % time.strftime('%d%m%Y',time.localtime())
		self.logsfile = open(logdir+self.logsfilename,'w')
		self.logsfile.write(self.logsxml)
		self.logsfile.close()
		
		
	#Save details in search.xml for indexing
	def SaveSearch(self,searchpath,logsfilename):
		searchdom = etree.parse(searchpath+'search.xml').getroot()
		searchitem = etree.Element("item")
		searchdom.append(searchitem)
		searchkeywords = etree.Element("keywords")
		searchitem.append(searchkeywords)
		searchkeywords.text = self.keyword.text
		searchdateitem = etree.Element("date")
		searchitem.append(searchdateitem)
		searchdateitem.text = time.strftime('%d/%m/%Y',time.localtime())
		fileitem = etree.Element("file")
		searchitem.append(fileitem)
		fileitem.text = time.strftime('%d%m%Y',time.localtime())
		operatoritem = etree.Element("operator")
		searchitem.append(operatoritem)
		operatoritem.text = self.operator.text
		os.remove(searchpath+'search.xml')
		finalfile = open(searchpath+'search.xml','a')
		finalfile.write(etree.tostring(searchdom, "utf-8"))
		finalfile.close()
		
		
	#Save all when done	
	def done(self):
		logdir=self.logspath+"logs/"
		searchdir=self.logspath+"./"
		self.SaveSearch(searchdir,self.logsfilename.split('.',1)[0])
