# tools/base_tool.py
from abc import ABC, abstractmethod

class ImageProcessingTool(ABC):
    @abstractmethod
    def apply(self, image):
        pass
    
    @abstractmethod
    def get_parameters(self):
        pass
    
    @abstractmethod
    def update_parameters(self, params):
        pass