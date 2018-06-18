# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 15:18:21 2018

@author: D34thPi3c3
"""

#----------------------------------------------------------------------------
#Imports
import re
from robobrowser import RoboBrowser
from logingdata import USERNAME, PASSWORD


#----------------------------------------------------------------------------
#Variable - You are allowed to change this with your own risk
FILE = 'Hawaii Five 0 S01'
UPLOADER = 'SerienJK'
RESOLUTION = '720'

#At the moment it can search on "boerse.to". You will get the filescript in the end. I just tested it with Uploader "SerienJK". This whole script will just work if you have "Robobrowser for Python" installed.
#Variable - Please dont change this variable
SEARCHSTARTBOERSE = '<ol class="searchResultsList">'
SEARCHENDBOERSE = '<div class="sectionFooter searchResultSummary">'
STARTLINKTHEMA = '<a href="thema'
ENDLINKTHEMA = '"><'
STARTLINKFILESCRYPT = 'externalLink" href="'
ENDLINKFILESCRYPT = '" rel'
CONTAINERWEBSITE = "filescript"



br = RoboBrowser(parser = 'lxml')

#----------------------------------------------------------------------------
#Program
class autoFindFile():
    def loginBoerse():
        br.open("https://boerse.to/login")
        form = br.get_form()
        form['login'] = USERNAME
        form['password'] = PASSWORD
        br.submit_form(form)
        #print(br.url)
#----------------------------------------------------------------------------
#Suche
    def searchBoerse(keywords, publisher):
        br.open("https://boerse.to/search")
        form = br.get_form()
        form['keywords'] = keywords
        form['users'] = publisher
        br.submit_form(form)
        return(str(br.parsed()))
        

#----------------------------------------------------------------------------
#get link       
    def getString(ssb, seb, src):
        startsearch = re.search(ssb, src).span()[1]
        endsearch = re.search(seb, src).span()[0]
        return src[startsearch:endsearch]
        
    def getLink(sl, el, ssb, seb, src, resolution):
        try:
            searchresult = autoFindFile.getString(ssb, seb, src)
        except:
            print("Dies ist nicht die Suchwebsite")
            searchresult = src
        x = 300
        while x > 200:
            listart = re.search(sl, searchresult).span()[1]
            searchresult = searchresult[listart:len(searchresult)]
            try:
                x = re.search(resolution, searchresult).span()[0]
            except:
                x = 0;
                 
        if x == 0:
            print("Es es ist nichts mit dieser Vorgabe vorganden")
            return "ERROR"
        else:
            liend = re.search(el, searchresult).span()[0]
            link = searchresult[0:liend]
            return link
    
#Site aufrufen
    def openSite(link):
        br.open(link)
        return(str(br.parsed()))
            
        

autoFindFile.loginBoerse()
src = autoFindFile.searchBoerse(FILE, UPLOADER)
link = autoFindFile.getLink(STARTLINKTHEMA, ENDLINKTHEMA, SEARCHSTARTBOERSE, SEARCHENDBOERSE, src, RESOLUTION)
print(link)
src = autoFindFile.openSite("https://boerse.to/thema"+link)
link = autoFindFile.getLink(STARTLINKFILESCRYPT, ENDLINKFILESCRYPT, None, None, src, 'filecrypt')
print(link)
