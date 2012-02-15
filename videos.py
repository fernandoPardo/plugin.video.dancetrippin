'''
Created on Feb 14, 2012

@author: fpardo
'''

class Video(object):
    
    '''
    Base Video 
    '''
    
    __caption = None
    __thumbnailPath = None
    __streamPath = None
    
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
    
    def fetchCaption(self):
        raise NotImplementedError
    
    def fetchThumbnailPath(self):
        raise NotImplementedError    
    
    def fetchStreamPath(self):
        raise NotImplementedError

class _AcudeoVideo(Video):
    #TODO Implement AcudeoVideo
    '''
    Acudeo Video Implementation
    '''

    def __init__(self):
        '''
        Constructor
        '''

class _VimeoVideo(Video):
    #TODO Implement VimeoVideo
    '''
    Vimeo Video Implementation
    '''

    def __init__(self):
        '''
        Constructor
        '''
    