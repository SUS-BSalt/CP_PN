from data import global_environment as GE,tools
from data.objects import AVGOBJ,Scence
import pygame

def getFrames(num,source):
    temp = []
    for i in range(num):
        address = source+'%d'%(i+1)+'.png'
        temp.append(pygame.image.load(address).convert_alpha())
    return temp


class Manager_Level_0:
    def __init__(self):
        self.activeSituation = True
        self.internalEventList = []
        self.globalEventList = []
        self.followingEventList = []
        self.moduleList = []
        
    def update(self):
        for checker in self.followingEventList:
            checker()
        for module in self.moduleList:
                if module.activeSituation == True:
                    module.update()

    def animate(self):
        for module in self.moduleList:
                if module.activeSituation == True:
                    module.animate()

    def start(self):
        """开始"""
        #self.ACTModule = createACTModule()
        self.AVGModule = createAVGModule()
        GE.controller = self.AVGModule.controller
        self.controller = self.AVGModule.controller

        GE.scence = createFirstScence()
        self.scence = GE.scence

        self.followingEventList.append(self.check_0)
        self.moduleList.append(self.AVGModule)
        print(self.moduleList)

    def check_0(self):
        """从开始的黑屏到简笔画方尖碑"""
        if "NEXT" in GE.eventList:
            print("next")
            print(GE.scence.objList[0].loc)
            self.moduleList.append(self.scence)
            self.followingEventList.remove(self.check_0)
            self.followingEventList.append(self.check_1)
            GE.eventList.remove("NEXT")

    def check_1(self):
        """从简笔画方尖碑到像素款"""
        if "NEXT" in GE.eventList:
            print("next")
            #print(GE.scence.objList[0].loc)
            GE.camera.zoomCamera(2)
            #print(GE.scence.objList[0].loc)
            self.scence.objList.pop()
            self.followingEventList.remove(self.check_1)
            self.followingEventList.append(self.check_2)
            print(GE.scence.objList[0].loc)
            GE.eventList.remove("NEXT")

    def check_2(self):
        """检测何时开始拉伸镜头"""
        if "NEXT" in GE.eventList:
            print("next")
            self.followingEventList.remove(self.check_2)
            self.followingEventList.append(self.check_3)
            self.check_2_timer = 0
            print(GE.scence.objList[0].loc)
            GE.eventList.remove("NEXT")

    def check_3(self):
        """拉伸镜头的方法"""
        self.check_2_timer += 1
        GE.camera.zoomCamera(2-self.check_2_timer*0.01)
        GE.scence.objList[0].loc[1] -= 6
        GE.scence.objList[1].loc[1] -= 1.5
        print(GE.camera.cameraScaleRectify)
        if self.check_2_timer == 100:
            self.followingEventList.remove(self.check_3)
            #self.followingEventList.append(self.check_4)

    def check_4(self):
        GE.camera.zoomCamera(1)
        pass
    
            

    def check_1111(self):
        for event in GE.eventList:
            if event == "AVGMODULE_END":
                print("end")
                #self.followingEventList.remove(self.check_0)
                self.moduleList.remove(self.AVGModule)
                self.scence = GE.scence = createFirstScence()
                self.followingEventList.remove(self.check_0)
                #self.followingEventList.append(self.check_1)

    

    def check_injured(self):
        if self.ACTModule.player.loc[0] >= 1700:
            self.ACTModule.bottomUI.randomPrintSwitch = True
            self.timer = 0
            self.followingEventList.remove(self.check_injured)
            pass
    
    def check_recovery(self):
        if self.ACTModule.player.loc[0] >= 1900:
            self.ACTModule.bottomUI.recoverSwitch = True
            self.timer = 0
            #self.followingEventList.remove(self.check_injured)
            pass

def createAVGModule():
    #（创建模块）
    module_AVG = AVGOBJ.AVGModule(open('data/levels/books/level_0.txt','r',encoding='UTF-8'))
    module_AVG.clickArea = [0,420,1280,300]
    module_AVG.activeSituation = True
    module_AVG.workingSituation = True
    #（创建模块）
    #（创建textBox）
    module_AVG.setTextBox([0,420], [1280,300], tools.getImage("UI","textBox.png"))
    #(创建logsBox)
    module_AVG.setLogsBox([0,0], [1280,720], 300, tools.getImage("UI","Logs.png"))
    #(创建logsBox)
    #（人物）
    satmic = AVGOBJ.Character(size=[150,200],loc=[600,70],color = (200,200,200))
    #（表情1）
    expressions = AVGOBJ.Expression(pygame.image.load('resources/GFX/Character/Satmic/body.png').convert())
    expressions.eyeSetting([72,51],3,getFrames(3,"resources/GFX/Character/Satmic/eye/"))
    expressions.mouthSetting([88,89],getFrames(4,"resources/GFX/Character/Satmic/mouth/"))
    satmic.expressionDict["blank"] = expressions
    #（表情1）
    satmic.init()
    satmic.setExpression("blank")
    module_AVG.characterDict["Satmic"] = satmic
    #（人物）

    #（人物）
    Nacy = AVGOBJ.Character(size=[150,200],loc=[700,270],color = (200,200,200))
    #（表情1）
    expressions = AVGOBJ.Expression(pygame.image.load('resources/GFX/Character/Nacy/blank/body.jpg').convert_alpha())
    expressions.eyeSetting([72,51],3,[pygame.image.load("resources/GFX/test/transparent.png").convert_alpha()],(0,0),(50,100))
    expressions.mouthSetting([88,89],[pygame.image.load("resources/GFX/test/transparent.png").convert_alpha()],[0,0])
    Nacy.expressionDict["blank"] = expressions
    #（表情1）
    #（表情2）
    expressions = AVGOBJ.Expression(pygame.image.load('resources/GFX/Character/Nacy/angry/body.jpg').convert_alpha())
    expressions.eyeSetting([72,51],3,[pygame.image.load("resources/GFX/test/transparent.png").convert_alpha()],(0,0),(50,100))
    expressions.mouthSetting([88,89],[pygame.image.load("resources/GFX/test/transparent.png").convert_alpha()],[0,0])
    Nacy.expressionDict["angry"] = expressions
    #（表情2）
    #（表情3）
    expressions = AVGOBJ.Expression(pygame.image.load('resources/GFX/Character/Nacy/cute/body.jpg'))
    expressions.eyeSetting([72,51],3,[pygame.image.load("resources/GFX/test/transparent.png").convert_alpha()],(0,0),(50,100))
    expressions.mouthSetting([88,89],[pygame.image.load("resources/GFX/test/transparent.png").convert_alpha()],[0,0])
    Nacy.expressionDict["cute"] = expressions
    #（表情3）
    Nacy.init()
    Nacy.setExpression("blank")
    module_AVG.characterDict["Nacy"] = Nacy
    #（人物）
    return module_AVG

def createFirstScence():
    scence = Scence.Scence()
    scence.appendPlane([-640,-360],[2650,1440],tools.getImage("Scence","level_0","light.png"),0)
    scence.appendPlane([600,-360],[93,451],tools.getImage("Scence","level_0","obelisk.png"),0.1)
    scence.appendPlane([0,0],[1280,720],tools.getImage("Scence","level_0","talker.png"),0.1)
    return scence

    

manager = Manager_Level_0()
GE.manager = manager
GE.level_manager = manager
manager.start()