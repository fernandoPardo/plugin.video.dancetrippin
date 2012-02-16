'''
Created on Feb 14, 2012

@author: fpardo
'''

import urllib2, re, sys, xbmcplugin, xbmcgui
from videofactories import RemoteVideoFactory

def VIDEOLINKS():        
        #TODO generate a fixed length list and add a "more videos button" 
        #pathsToVideos = getPathsToVideos()
        pathsToVideos = ["http://www.dancetrippin.tv/video/marc-maya-and-matthew-hoag-elrow-barcelona-spain","http://www.dancetrippin.tv/video/dj-set-episode-43-audio-bullys"]        
        for pathToVideo in pathsToVideos:  
                video = videoFactory.createVideo(pathToVideo)                
                video.fetchVideoData()             
                addLink(video.getCaption(),video.getPath(),video.getThumbnail())                       

def addLink(name, url, iconimage):
        ok = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name })
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)        
        return ok

def getPathsToVideos():
    requestUrl = "http://www.dancetrippin.tv/media-library/all"
    req = urllib2.Request(requestUrl)
    req.add_header('User-Agent', "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8")
    con = urllib2.urlopen(req)
    link = con.read()
    con.close()      
    #TODO write a more strict regex   
    expression ='<a href="(.+?)" class="imagecache imagecache-media_thumb_small'
    match = re.compile(expression).findall(link)
    videosPath = []
    for videopath in match: 
        videosPath.append("http://www.dancetrippin.tv"+videopath)    
    return videosPath

videoFactory = RemoteVideoFactory()
VIDEOLINKS()        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
