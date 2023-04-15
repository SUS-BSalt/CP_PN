__name__ = "全局环境"
import pygame as PG
from . import setting
from .camera import Camera

PG.display.set_caption("CP_P")
screen = PG.display.set_mode(setting.windowsize,setting.windowflags)

class GlobalValue:
    #设置全局变量，一共两个方法，set与get
    def __init__(self):
        self.content = {}
    
    def set(self, name, value):
        self.content[name] = value
    
    def get(self, name, default=False):
        try:
            return self.content[name]
        except:
            return default
        
GV = GlobalValue()
"""global value全局变量"""

moduleList = []
"""模组列表"""

controller = 0
"""控制器"""

camera = Camera()
