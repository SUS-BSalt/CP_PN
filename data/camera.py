from . import global_environment as GE
from . import setting
import pygame

class Camera:
    def __init__(self):
        self.loc = [0,0]
        self.size = [1280,720]
        self.cameraShot = pygame.Surface(self.size)
        self.white = pygame.Surface(self.size)
        self.white.fill((255,255,255))
        self.black = pygame.Surface(self.size)
        self.black.fill((0,0,0))


        self.draw_List_Creating = []
        """正在创建中的绘制任务"""
        self.draw_List_Ready = []
        """创建好的绘制任务"""
        self.draw_List_Drawing = []
        """执行中的绘制任务"""
        #如果可以的话，应该把这三个列表各自对齐内存块头部，以提高cache命中率

        self.cameraLocRectify = [0,0]
        self.cameraScaleIndex = setting.windowsize[0] / setting.org_windowsize[0]
        """windowSize / org_windowsize"""
        self.mousePos = (0,0)

    def focalOn(self,focalPointLoc):
        self.loc = [(focalPointLoc[0]-(self.size[0])/2), (focalPointLoc[1]-(self.size[1]/2))]

    def updateCameraLoc(self,rectify):
        self.loc = [self.loc[0]+rectify[0],self.loc[1]+rectify[1]]

    def draw(self,vision,objLocOnPlayGround):
        self.draw_List_Creating.append((vision,(objLocOnPlayGround[0] - self.loc[0],objLocOnPlayGround[1] - self.loc[1])))

    def draw_UI(self,vision,loc):
        self.draw_List_Creating.append((vision,loc))

    def executeDrawQuest(self):
        """执行绘制任务"""
        self.draw_List_Drawing = self.draw_List_Ready
        self.cameraShot.blits(self.draw_List_Drawing,False)


    def createDrawQuest(self):
        """创建绘制任务的同时，将现有的绘制任务状态切换为预备中"""
        self.draw_List_Ready = self.draw_List_Creating
        self.draw_List_Creating = []

    def getMousePos(self):
        mousePosX = (pygame.mouse.get_pos()[0] - self.cameraLocRectify[0])/self.cameraScaleIndex + self.loc[0]
        mousePosY = (pygame.mouse.get_pos()[1] - self.cameraLocRectify[1])/self.cameraScaleIndex + self.loc[1]
        self.mousePos = (mousePosX, mousePosY)
        return(mousePosX, mousePosY)
    
    def mousePosCheck(self,rect):
        if  self.mousePos[0] > rect[0] and \
            self.mousePos[1] > rect[1] and \
            self.mousePos[0] < rect[0]+rect[2] and \
            self.mousePos[1] < rect[1]+rect[3]:
            return True
        else:
            return False
    def mousePosCheck_UI(self,rect):
        if  self.mousePos[0] - self.loc[0] > rect[0] and \
            self.mousePos[1] - self.loc[1] > rect[1] and \
            self.mousePos[0] - self.loc[0] < rect[0]+rect[2] and \
            self.mousePos[1] - self.loc[1] < rect[1]+rect[3]:
            return True
        else:
            return False
        
    def resetWindow(self,event):
        if event.x/event.y > setting.org_windowsize[0]/setting.org_windowsize[1]:
            setting.windowsize = ((setting.org_windowsize[0]/setting.org_windowsize[1])*event.y,event.y)
            self.cameraScaleIndex = event.y / setting.org_windowsize[1]
        else:
            setting.windowsize = (event.x,event.x/(setting.org_windowsize[0]/setting.org_windowsize[1]))
            self.cameraScaleIndex = event.x / setting.org_windowsize[0]
        #更新摄像机修正位置
        self.cameraLocRectify = [(event.x-setting.windowsize[0])/2,(event.y-setting.windowsize[1])/2]
        GE.screen.fill((0,0,0))