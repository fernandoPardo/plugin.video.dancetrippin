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

import urllib, urllib2, sys, re, xbmc, xbmcgui, xbmcplugin
from BeautifulSoup import BeautifulSoup
from xml.sax.saxutils import unescape
from videofactories import RemoteVideoFactory


# plugin related constants
PLUGIN_URL = 'plugin://video/dancetrippin/'

# XBMC plugin modes
MODE_VIDEOS = 1
MODE_VIDEO_PLAY = 2

# Parameter keys

PARAMETER_KEY_MODE = u'mode'
PARAMETER_KEY_URL = u'url'
PARAMETER_KEY_PERMALINK = u'permalink'

def fetchVideoList():
    '''Fetch complete videoList'''                
    requestUrl = "http://www.dancetrippin.tv/media-library/all"
    req = urllib2.Request(requestUrl)
    req.add_header('User-Agent', "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8")
    con = urllib2.urlopen(req)
    html = BeautifulSoup(con.read())
    videosTable = html.find(name="table", attrs={"class" : re.compile('views-table*')})
    videos = []
    for video in videosTable.find("tbody").findAll("tr"):            
        mediaNumber = video.find(name="td", attrs={"class" : re.compile('media-number')}).text
        artistName = video.find(name="td", attrs={"class" : re.compile('views-field-title')}).text
        partyName = video.find(name="td", attrs={"class" : re.compile('views-field-title-1')}).text
        venueName = video.find(name="td", attrs={"class" : re.compile('views-field-title-2')}).text
        #TODO figure out where to populate this. this depends on how search/filter features will be implemented
        videoGenres = []                  
        videoLink = "http://www.dancetrippin.tv" + video.find("a")["href"]                
        videoTitle = "%s %s @ %s %s" % (mediaNumber, artistName, venueName, partyName)
        videos.append({"title":unescape(videoTitle), "thumbnail":"", "url":videoLink, "genres":videoGenres})                        
    con.close()
    return videos

def addDirectoryItem(name, label2='', infoType="Video", infoLabels={}, isFolder=True, parameters={}):
    ''' Add a list item to the XBMC UI.'''
    li = xbmcgui.ListItem(name, label2)
    if not infoLabels:
        infoLabels = {"Title": name }
    li.setInfo(infoType, infoLabels)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=isFolder)

def showVideos(videos, parameters={}):
    ''' Show a list of videos'''
    xbmcplugin.setContent(handle, "videos")
    for video in videos:
        li = xbmcgui.ListItem(label=video["title"], thumbnailImage=video["thumbnail"])
        li.setInfo("video", { "title": video["title"], "genre": video["genres"] })
        li.setProperty("mimetype", 'video/mpeg')
        li.setProperty("IsPlayable", "true")
        video_parameters = { PARAMETER_KEY_MODE: MODE_VIDEO_PLAY, PARAMETER_KEY_URL: PLUGIN_URL + "videos/" + video["url"], PARAMETER_KEY_PERMALINK: video["url"] }
        url = sys.argv[0] + '?' + urllib.urlencode(video_parameters)
        ok = xbmcplugin.addDirectoryItem(handle, url=url, listitem=li, isFolder=False)    
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def playVideo(permaLink):
    ''' Start to stream the video with the given id. '''    
    video = videoFactory.createVideo(urllib.unquote_plus(permaLink))  
    li = xbmcgui.ListItem(label=video.getTitle(), thumbnailImage=video.getThumbnail(), path=video.getStreamUrl())    
    xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)

def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

def show_root_menu():
    ''' Show the plugin root menu. '''
    addDirectoryItem(name='Videos', parameters={PARAMETER_KEY_URL: PLUGIN_URL + 'video', PARAMETER_KEY_MODE: MODE_VIDEOS}, isFolder=True)    
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

##################################################################


params = parameters_string_to_dict(sys.argv[2])
url = urllib.unquote_plus(params.get(PARAMETER_KEY_URL, ""))
mode = int(params.get(PARAMETER_KEY_MODE, "0"))
handle = int(sys.argv[1])
videoFactory = RemoteVideoFactory()

print "##########################################################"
print("Mode: %s" % mode)
print("URL: %s" % url)
print "##########################################################"

# Depending on the mode, call the appropriate function to build the UI.
if not sys.argv[ 2 ] or not url:
    # new start
    ok = show_root_menu()
elif mode == MODE_VIDEOS:    
    videos = fetchVideoList()
    ok = showVideos(parameters={PARAMETER_KEY_MODE: mode}, videos=videos)
elif mode == MODE_VIDEO_PLAY:
    playVideo(params.get(PARAMETER_KEY_PERMALINK, "1"))