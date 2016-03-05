'''
Abstract base class for interface for all classes
 that can return their own Bounding Box
'''

from abc import ABCMeta, abstractmethod

class IBoundingBoxed:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getBoundingBox(self):
        '''
        :return: the boundingBox for this item
        '''
        raise NotImplementedError
