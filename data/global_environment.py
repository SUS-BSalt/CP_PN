__name__ = "全局环境"
import pygame as PG
from data import setting
from data.camera import Camera
import json

def loadAssetData(prePath,*argv):
    order = "json.load(open('resources/asset.json','r',encoding='UTF-8'))"
    for value in argv:
        order = order + "[\"%s\"]" % value
    tempDict = eval(order)
    for loc in tempDict:
        tempDict[loc] = prePath + tempDict[loc]
    return tempDict

#载入资产的位置信息，方便需要时直接读取
GFX_UI = loadAssetData("resources/GFX/UI/","GFX","UI")
GFX_test = loadAssetData("resources/GFX/test","GFX","UI")

PG.display.set_caption("CP_P")
PG.display.set_icon(PG.image.load(GFX_UI["icon"]))

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
"""global value全局变量字典"""

screen = PG.display.set_mode(setting.windowsize,setting.windowflags)
"""游戏窗口"""


eventList = []
"""全局事件"""

controller = 0
"""控制器"""

camera = Camera()
"""摄像机，包括了绘制任务的创建与执行，获取鼠标位置，跟随窗口大小调整画面等功能"""

UIfont_01 = PG.font.Font(setting.charType,40)
UIfont_02 = PG.font.Font(setting.charType,50)
UIfont_03 = PG.font.Font(setting.charType,30)
UIfont_04 = PG.font.Font(setting.charType,20)
UIfont_05 = PG.font.Font(setting.charType,40)
"""一些预设字体"""

manager = None
"""当前程序的管理者"""

level_manager = None
"""关卡的管理"""

escMenu = None
"""按esc会跳出来的菜单"""