'''
Created on Feb 14, 2012

@author: fpardo
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
        expressions = {                       
                       'http://www.vimeo.com/moogaloop.swf\?clip_id=(.+?)&' : "vimeo",
                       'http://objects.tremormedia.com/embed/swf/acudeoflowplayerplugin32.swf' : "acudeo"
                       }        
        for expression in expressions:   
            match = re.compile(expression).findall(htmlDoc)           
            if len(match)>0 : return expressions[expression]        