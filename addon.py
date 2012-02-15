'''
Created on Feb 14, 2012

@author: fpardo
'''

import urllib2, re, sys, xbmcplugin, xbmcgui
from xml.sax.saxutils import unescape
from BeautifulSoup import BeautifulSoup

USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"

def VIDEOLINKS():        
        """TODO generate a fixed length list and add a "more videos button" """
        pathsToVideos = getPathsToVideos()        
        for pathToVideo in pathsToVideos[0:10]:              
                videoId = getVideoId(pathToVideo) 
                if videoId:                                                                 
                    videoData = getVideoData(str(videoId[0]))                         
                    addLink(videoData['caption'],videoData['streamUrl'],videoData['thumbnail'])        

def addLink(name, url, iconimage):
        ok = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name })
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)        
        return ok
    
def getVideoData(videoId):     
    requestUrl = "http://vimeo.com/moogaloop/load/clip:%s/local" % (videoId)
    req = urllib2.Request(requestUrl)
    req.add_header('User-Agent', USERAGENT)    
    print req.get_full_url()
    con = urllib2.urlopen(req)
    response = con.read()
    video = BeautifulSoup(response)    
    videoCaption = unescape(video.findChild("video").findChild("caption").getText())
    videoThumbnailUrl = video.findChild("video").findChild("thumbnail").getText()
    videoRequestSignature = video.findChild("request_signature").getText()
    videoRequestSignatureExpires = video.findChild("request_signature_expires").getText()
    videoStreamUrl = generateStreamUrl(videoId,videoRequestSignature,videoRequestSignatureExpires)        
    con.close()
    return {'caption':videoCaption,'thumbnail':videoThumbnailUrl,"streamUrl":videoStreamUrl}

def generateStreamUrl(videoId,videoRequestSignature,videoRequestSignatureExpires):        
    requestUrl = "http://player.vimeo.com/play_redirect?clip_id=%s&sig=%s&time=%s&quality=hd&codecs=H264,VP8,VP6&type=moogaloop_local&embed_location=" % ( videoId, videoRequestSignature, videoRequestSignatureExpires)    
    req = urllib2.Request(requestUrl)
    req.add_header('User-Agent', USERAGENT);
    con = urllib2.urlopen(req);   
    streamUrl = con.geturl()  
    con.close()   
    return streamUrl 

def getVideoId(videoUrl):    
    req = urllib2.Request(videoUrl)
    req.add_header('User-Agent', USERAGENT)
    con = urllib2.urlopen(req)
    link = con.read()
    con.close()    
    """TODO make re for every videohost & avoid playlist videoids
    eg : vimeoVideoExpr = 'http://www.vimeo.com/moogaloop.swf\?clip_id=(.+?)&'
    """     
    expression ='http://www.vimeo.com/moogaloop.swf\?clip_id=(.+?)&'
    match = re.compile(expression).findall(link)    
    return match 

def getPathsToVideos():
    requestUrl = "http://www.dancetrippin.tv/media-library/all"
    req = urllib2.Request(requestUrl)
    req.add_header('User-Agent', USERAGENT)
    con = urllib2.urlopen(req)
    link = con.read()
    con.close()      
    """TODO write a more strict re     
    """  
    expression ='<a href="(.+?)" class="imagecache imagecache-media_thumb_small'
    match = re.compile(expression).findall(link)
    videosPath = []
    for videopath in match: 
        videosPath.append("http://www.dancetrippin.tv"+videopath)    
    return videosPath

url = "http://www.dancetrippin.tv/media-library/all"
VIDEOLINKS()        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
