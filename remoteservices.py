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

import urllib2, re
from xml.sax.saxutils import unescape
from BeautifulSoup import BeautifulSoup

class VimeoClient():
    
    '''Vimeo Api Client Implementation'''            
        
    def getVideoData(self, videoId):     
            requestUrl = "http://vimeo.com/moogaloop/load/clip:%s/local" % (videoId)
            req = urllib2.Request(requestUrl)
            req.add_header('User-Agent', "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8")    
            print req.get_full_url()
            con = urllib2.urlopen(req)
            response = con.read()
            video = BeautifulSoup(response)    
            videoCaption = unescape(video.findChild("video").findChild("caption").getText())
            videoThumbnailUrl = video.findChild("video").findChild("thumbnail").getText()
            videoRequestSignature = video.findChild("request_signature").getText()
            videoRequestSignatureExpires = video.findChild("request_signature_expires").getText()
            videoStreamUrl = self.getStreamPath(videoId, videoRequestSignature, videoRequestSignatureExpires)        
            con.close()
            return {'caption':videoCaption, 'thumbnail':videoThumbnailUrl, "streamUrl":videoStreamUrl}

    def getStreamPath(self, videoId, videoRequestSignature, videoRequestSignatureExpires):        
            requestUrl = "http://player.vimeo.com/play_redirect?clip_id=%s&sig=%s&time=%s&quality=hd&codecs=H264,VP8,VP6&type=moogaloop_local&embed_location=" % (videoId, videoRequestSignature, videoRequestSignatureExpires)    
            req = urllib2.Request(requestUrl)
            req.add_header('User-Agent', "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8");
            con = urllib2.urlopen(req);   
            streamUrl = con.geturl()  
            con.close()   
            return streamUrl 
    
    def getVideoId(self, videoUrl):    
            req = urllib2.Request(videoUrl)
            req.add_header('User-Agent', "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8")
            con = urllib2.urlopen(req)
            html = BeautifulSoup(con.read())
            con.close()            
            embeddedVideo = html.find(name="div", attrs={"class" : re.compile('emvideo-vimeo')})                        
            expression = 'http://www.vimeo.com/moogaloop.swf\?clip_id=(.+?)&'
            match = re.compile(expression).findall(embeddedVideo.object["data"])    
            return match[0]