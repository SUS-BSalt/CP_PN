__name__ = "全局环境"
import pygame as PG
from . import setting
from .camera import Camera
import json

GFX = json.load(open('resources/asset.json','r',encoding='UTF-8'))["GFX"]

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

PG.display.set_caption("CP_P")
PG.display.set_icon(PG.image.load(GFX["icon"]))
screen = PG.display.set_mode(setting.windowsize,setting.windowflags)


moduleList = []
"""模组列表"""

controller = 0
"""控制器"""

camera = Camera()
"""摄像机，包括了绘制任务的创建与执行，获取鼠标位置，跟随窗口大小调整画面等功能"""
