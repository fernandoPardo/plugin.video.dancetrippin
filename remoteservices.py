'''
Created on Feb 14, 2012

@author: fpardo
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
            link = con.read()
            con.close()    
            #TODO Come up with a better regex. This actually returns all vimeovideos (also next playlist items). Match should hold only one id            
            expression = 'http://www.vimeo.com/moogaloop.swf\?clip_id=(.+?)&'
            match = re.compile(expression).findall(link)    
            return match[0] 
        
class AcudeoClient():
    
    '''Acudeo Api Client Implementation'''                    
    #TODO Implement this
        
    
