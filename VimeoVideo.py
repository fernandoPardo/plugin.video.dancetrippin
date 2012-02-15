'''
Created on Feb 14, 2012

@author: fpardo
'''

from Video import Video

class VimeoVideo(Video):
    #TODO Implement AcudeoVideo
    '''
    Vimeo Video Implementation
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def getCaption(self):
        raise NotImplementedError
    
    def getThumbnailPath(self):
        raise NotImplementedError    
    
    def getStreamPath(self):
        raise NotImplementedError
    
    def setCaption(self):
        raise NotImplementedError
    
    def setThumbnailPath(self):
        raise NotImplementedError    
    
    def setStreamPath(self):
        raise NotImplementedError