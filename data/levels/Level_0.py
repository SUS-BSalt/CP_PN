from data import global_environment as GE,tools
from data.objects import AVGOBJ,Scence,ACT_main
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

        self.scence =GE.scence = createFirstScence()
        #self.scence = GE.scence
        
        self.ACTModule = createACTModule()


        self.followingEventList.append(self.check_0)
        self.followingEventList.append(self.draw_black_block)
        self.black_block_loc = [0,420]
        self.moduleList.append(self.AVGModule)
        print(self.moduleList)

    def draw_black_block(self):
        GE.camera.draw_UI(GE.camera.black,self.black_block_loc)

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
            #增删事件触发
            self.check_3_timer = 0
            #设置下一个check所需的计时器
            GE.controller = tools.controller_noMode
            #转交控制器
            self.moduleList.append(self.ACTModule)
            GE.eventList.remove("NEXT")
            #完成事件处理，将其移除

    def check_3(self):
        """拉伸镜头的方法"""
        self.check_3_timer += 1
        GE.camera.zoomCamera(2-self.check_3_timer*0.01)
        GE.camera.updateCameraLoc((0,3))
        GE.scence.objList[1].loc[1] += 2
        self.AVGModule.textBox.loc[1] += 3
        self.black_block_loc[1] += 3
        #print(GE.scence.objList[1].loc[0])
        if self.check_3_timer == 100:
            GE.camera.zoomCamera(1)
            self.followingEventList.remove(self.check_3)
            GE.controller = self.controller = self.ACTModule.controller
            #self.followingEventList.append(self.check_4)

    def check_4(self):
        GE.camera.zoomCamera(1)
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
    scence = Scence.Scence([2650,1440])
    scence.appendPlane([-640,-360],[2650,1440],tools.getImage("Scence","level_0","light.png"),1)
    scence.appendPlane([600,-360],[93,451],tools.getImage("Scence","level_0","obelisk.png"),0.6)
    scence.appendPlane([0,0],[1280,720],tools.getImage("Scence","level_0","talker.png"),0.1)
    scence.appendCollisionObj(-350,0,100,2000)
    scence.appendCollisionObj(1700,0,100,2000)
    return scence

def createACTModule():
    module_ACT = ACT_main.ACTModule()
    module_ACT.setPlayer([680,1020])
    module_ACT.setBottomUI([0,-1000], [640,720], "data/levels/books/level_0_0.txt")
    return module_ACT

    

manager = Manager_Level_0()
GE.manager = manager
GE.level_manager = manager
manager.start()