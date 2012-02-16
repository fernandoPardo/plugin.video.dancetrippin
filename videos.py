'''
Created on Feb 14, 2012

@author: fpardo
'''

from remoteservices import VimeoClient

class Video(object):
    
    '''Base Video Class'''    
    
    _caption = None
    _thumbnail = None
    _path = None
    '''
        the url that contains the video & webvideoplayer.
        since "http://www.dancetrippin.tv/video/dj-set-episode-1-bart-thimbles" is not playable 
        we have to get the actual playable videoUrl : "http://hwcdn.net/k7w9n4n5/cds/episodes400/1.flv?rs=710"             
    '''
    #TODO Come up with a better naming first or solve this in a more elegant way 
    _snapUrl = None
    
    def __init__(self,snapUrl):       
        self._snapUrl = snapUrl    
    
    def getCaption(self):
        return self._caption
    
    def getThumbnail(self):
        return self._thumbnail    
    
    def getPath(self):
        return self._path
    
    def getSnapUrl(self):
        return self._snapUrl        
    
    def setCaption(self, caption):
        self._caption = caption
    
    def setThumbnail(self, thumbnail):
        self._thumbnail = thumbnail
    
    def setPath(self, path):
        self._path = path  
    
    def fetchVideoData(self):
        raise NotImplementedError    

class AcudeoVideo(Video):
    #TODO Implement AcudeoVideo
    '''Acudeo Video Implementation'''
    
    def fetchVideoData(self):
        self.setCaption("caption")
        self.setThumbnail("thumbnail")
        self.setPath("path")

class VimeoVideo(Video):
    videoData = None
    '''Vimeo Video Implementation'''  
    
    def __init__(self,snapUrl):        
        Video.__init__(self, snapUrl)

    #TODO populate videoObjects here and like this ? what about doing it in a lazy manner ?
            
    def fetchVideoData(self):        
        snapUrl = self.getSnapUrl()
        vimeoClient = VimeoClient()
        videoId = vimeoClient.getVideoId(snapUrl)
        videoData = vimeoClient.getVideoData(videoId)        
        self.setCaption(videoData['caption'])
        self.setThumbnail(videoData['thumbnail'])
        self.setPath(videoData['streamUrl'])
