__name__ = "全局环境"
import pygame as PG
from data import setting,tools
from data.camera import Camera
import json

#载入音频
SFX = tools.load_all_sfx("resources/SFX")

screen = PG.display.set_mode(setting.windowsize,setting.windowflags,8)
"""游戏窗口"""
PG.display.set_caption("CP_P")
PG.display.set_icon(tools.getImage("UI","ONE.ico"))

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



eventList = []
"""全局事件"""

controller = tools.controller_noMode
"""控制器"""

camera = Camera()
"""摄像机，包括了绘制任务的创建与执行，获取鼠标位置，跟随窗口大小调整画面等功能"""

UIfont_01 = PG.font.Font(setting.charType,50)
UIfont_02 = PG.font.Font(setting.charType,40)
UIfont_03 = PG.font.Font(setting.charType,30)
UIfont_04 = PG.font.Font(setting.charType,25)
UIfont_05 = PG.font.Font(setting.charType,10)
"""一些预设字体"""

manager = None
"""当前程序的管理者"""

level_manager = None
"""关卡的管理者"""

escMenu = None
"""按esc会跳出来的菜单"""

scence = None
"""场景"""