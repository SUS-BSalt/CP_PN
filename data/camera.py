from . import global_environment as GE
from . import setting
import pygame

class Camera:
    def __init__(self):
        self.loc = [0,0]
        self.size = [1280,720]
        self.cameraShot = pygame.Surface(self.size)
        self.cameraShotScence = pygame.Surface(self.size)
        self.cameraScaleIndex = 1
        """场景的camera,方便进行镜头缩放,同时相机的位置指的也是这玩意的位置"""
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
        self.draw_List_Creating_UI = []
        self.draw_List_Ready_UI = []
        self.draw_List_Drawing_UI = []
        """绘制任务三队列，UI版"""
        #如果可以的话，应该把这三个列表各自对齐内存块头部，以提高cache命中率

        self.windowLocRectify = [0,0]
        self.windowScaleIndex = setting.windowsize[0] / setting.org_windowsize[0]
        """windowSize / org_windowsize"""
        self.mousePos = (0,0)

    def focalOn(self,focalPointLoc):
        self.loc = [(focalPointLoc[0]-(self.size[0])/2), (focalPointLoc[1]-(self.size[1]/2))]

    def updateCameraLoc(self,rectify):
        self.loc = [self.loc[0]+rectify[0],self.loc[1]+rectify[1]]

    def draw(self,vision,objLocOnPlayGround):
        self.draw_List_Creating.append((vision,(objLocOnPlayGround[0] - self.loc[0],objLocOnPlayGround[1] - self.loc[1])))

    def draw_UI(self,vision,loc):
        self.draw_List_Creating_UI.append((vision,loc))

    def zoomCamera(self,index):
        """
        该函数用于缩放场景用的shot，
        index是缩放指数，指的是缩放后画面相对于最开始设定的大小的百分比，而不是相对于现在画面大小的百分比
        """
        self.loc[0] = self.loc[0] - (index - self.cameraScaleIndex)*self.size[0]*0.5
        self.loc[1] = self.loc[1] - (index - self.cameraScaleIndex)*self.size[1]*0.5
        self.cameraScaleIndex = index

    def executeDrawQuest(self):
        """执行绘制任务"""
        self.draw_List_Drawing = self.draw_List_Ready
        self.cameraShotScence.blits(self.draw_List_Drawing,False)
        if self.cameraScaleIndex != 1:
            self.cameraShot.blit(pygame.transform.scale(self.cameraShotScence,self.size),(0,0))
        else:
            self.cameraShot.blit(self.cameraShotScence,(0,0))
        self.draw_List_Drawing_UI = self.draw_List_Ready_UI
        self.cameraShot.blits(self.draw_List_Drawing_UI,False)


    def createDrawQuest(self):
        """创建绘制任务的同时，将现有的绘制任务状态切换为预备中"""
        self.draw_List_Ready = self.draw_List_Creating
        self.draw_List_Creating = []
        self.draw_List_Ready_UI = self.draw_List_Creating_UI
        self.draw_List_Creating_UI = []

    def getMousePos(self):
        mousePosX = (pygame.mouse.get_pos()[0] - self.windowLocRectify[0])/self.windowScaleIndex + self.loc[0]
        mousePosY = (pygame.mouse.get_pos()[1] - self.windowLocRectify[1])/self.windowScaleIndex + self.loc[1]
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
            self.windowScaleIndex = event.y / setting.org_windowsize[1]
        else:
            setting.windowsize = (event.x,event.x/(setting.org_windowsize[0]/setting.org_windowsize[1]))
            self.windowScaleIndex = event.x / setting.org_windowsize[0]
        #更新摄像机修正位置
        self.windowLocRectify = [(event.x-setting.windowsize[0])/2,(event.y-setting.windowsize[1])/2]
        GE.screen.fill((0,0,0))
        print(GE.manager)