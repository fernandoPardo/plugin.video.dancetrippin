'''
Created on Feb 14, 2012

@author: Fernando Pardo

Copyright (C) 2012 Fernando Pardo
 
This file is part of XBMC DanceTrippin.tv Plugin.

XBMC DanceTrippin.tv Plugin is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

XBMC DanceTrippin.tv Plugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with XBMC DanceTrippin.tv Plugin.  If not, see <http://www.gnu.org/licenses/>.
'''

from remoteservices import VimeoClient
from BeautifulSoup import BeautifulSoup
import urllib2 ,re

class Video(object):    
    '''Base Video Class'''    
    
    _title = ""
    _thumbnail = ""    
    _url = ""
    _streamUrl = ""
    _genres = []    
    
    def __init__(self,url):       
        self._url = url
        self.fetchVideoData()    
    
    def getTitle(self):
        return self._title
    
    def getThumbnail(self):
        return self._thumbnail    
    
    def getUrl(self):
        return self._url
    
    def getStreamUrl(self):
        return self._streamUrl    
    
    def getGenres(self):
        return self._genres      
    
    def fetchVideoData(self):
        raise NotImplementedError    

class AcudeoVideo(Video):    
    '''Acudeo Video Implementation'''
    
    def __init__(self,url):        
        Video.__init__(self, url)        
    
    def fetchVideoData(self):
        url = self.getUrl()
        req = urllib2.Request(url)
        req.add_header('User-Agent', "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8")            
        con = urllib2.urlopen(req)        
        html = BeautifulSoup(con.read())
        
        title = html.find("title").string.split("|")[0]                        
        thumbnail = "http://www.dancetrippin.tv/sites/all/themes/DanceTrippin/logo.png"
        
        #Getting streamUrl from embedded javascript code
        media = html.find(id="media")
        javascriptCode = "".join(media.script.string.split())        
        expression = 'playlist:\["(.+?)"\]'        
        path = re.compile(expression).findall(javascriptCode)       
        self._title = title                
        self._thumbnail = thumbnail
        self._streamUrl = path[0]

class VimeoVideo(Video):    
    '''Vimeo Video Implementation'''  
    
    def __init__(self,url):        
        Video.__init__(self, url)    
            
    def fetchVideoData(self):        
        url = self.getUrl()
        
        req = urllib2.Request(url)
        req.add_header('User-Agent', "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8")            
        con = urllib2.urlopen(req)        
        html = BeautifulSoup(con.read())        
        title = html.find("title").string.split("|")[0]                      
        
        vimeoClient = VimeoClient()
        videoId = vimeoClient.getVideoId(url)
        videoData = vimeoClient.getVideoData(videoId)        
        self._title = title
        self._thumbnail = videoData['thumbnail']
        self._streamUrl = videoData['streamUrl']