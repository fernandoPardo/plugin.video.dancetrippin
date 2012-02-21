# -*- coding: utf-8 -*-
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

import videos,re,urllib2

class VideoFactory(object): 
    
    def createVideo(self, resourcePath):
        raise NotImplementedError

class RemoteVideoFactory(VideoFactory):          
    
    def createVideo(self, url):
        videoType = self._getVideoType(url)             
        klass = {
            'vimeo': videos.VimeoVideo ,
            'acudeo': videos.AcudeoVideo ,
        }.get(videoType)
        if not klass:
            raise Exception, 'Url : "%s" either contains no videos or a non supported videoType' % (url)         
        video =  klass(url)                
        return video
        
    def _getVideoType(self, url):        
        req = urllib2.Request(url)
        req.add_header('User-Agent', "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8")
        con = urllib2.urlopen(req) 
        htmlDoc = con.read()
        con.close()
        #TODO come up with better expressions
        #TODO Refactor this to work with BeautifulSoup ???
        expressions = {                       
                       'http://www.vimeo.com/moogaloop.swf\?clip_id=(.+?)&' : "vimeo",
                       'http://objects.tremormedia.com/embed/swf/acudeoflowplayerplugin32.swf' : "acudeo"
                       }        
        for expression in expressions:   
            match = re.compile(expression).findall(htmlDoc)           
            if len(match)>0 : return expressions[expression]        