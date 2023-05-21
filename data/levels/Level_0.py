from data import global_environment as GE,tools
from data.objects import AVGOBJ,Scence,ACT_main,ACT_NPC
import pygame

class Manager_Level_0:
    def __init__(self):
        self.activeSituation = True
        self.followingEventList = []
        self.moduleList = []

        self.current_interactive_obj = None
        #当前活跃的交互物体，在check_interactive，每帧执行这玩意的update
        self.player_pre_x_loc = 1000
        #这个值只要不是玩家初始位置就行，但其实就算是也无非是出点小bug
        
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

        GE.camera.loc = [-640,0]
        self.scence =GE.scence = tools.load_scence("data/levels/scence/s-0-0.json","level_0",[2650,1440])#createFirstScence()

        #self.scence = GE.scence
        
        self.ACTModule = createACTModule()


        self.followingEventList.append(self.check_0)
        self.followingEventList.append(self.draw_black_block)
        self.black_block_loc = [0,420]
        self.black_block_loc_2 = [0,-720]
        self.moduleList.append(self.AVGModule)
        #print(self.moduleList)

    def draw_black_block(self):
        GE.camera.draw_UI(GE.camera.black,self.black_block_loc)
        GE.camera.draw_UI(GE.camera.black,self.black_block_loc_2)

    def check_0(self):
        """从开始的黑屏到简笔画方尖碑"""
        if "NEXT" in GE.eventList:
            print("next")
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
        self.black_block_loc[1] += 2
        self.black_block_loc_2[1] += 1
        #print(GE.scence.objList[1].loc[0])
        if self.check_3_timer == 100:
            GE.camera.zoomCamera(1)
            self.followingEventList.remove(self.check_3)
            GE.controller = self.controller = self.ACTModule.controller
            
            self.followingEventList.append(self.check_4)
        
    def check_4(self):
        """玩家做出选择"""
        if "jump_to_01" in GE.eventList:
            self.followingEventList.remove(self.draw_black_block)
            self.moduleList.remove(self.scence)
            self.scence = GE.scence = self.scence_1
            self.moduleList.insert(1,self.scence)
            GE.camera.loc = [0,0]
            self.ACTModule.player.loc = [100,420]
            self.ACTModule.bottomUI.loc[1]=420
            self.ACTModule.interactive_obj_list = pygame.sprite.Group()
            GE.eventList.remove("jump_to_01")


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
    Nacy = AVGOBJ.Character(size=[150,200],loc=[405,0],color = (200,200,200))
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
    expressions = AVGOBJ.Expression(tools.getImage('Character',"Nacy","cute","body.jpg"))
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
    scence.appendPlane([550,-360],[140,676],tools.getImage("Scence","level_0","obelisk.png"),0.6)
    scence.appendPlane([1700,552],(142,528),tools.getImage("Scence","level_0","The-Handed-Man.png"),1)
    scence.appendPerspective([538,700],(461,361),"right",tools.getImage("Scence","level_0","02_2.png"),0.95)
    scence.appendPerspective([1221,700],(188,195),"left",tools.getImage("Scence","level_0","04_0.png"),1)
    
    scence.appendPlane([0,0],[1280,720],tools.getImage("Scence","level_0","talker.png"),0.1)
    scence.appendCollisionObj(-350,0,100,2000)
    scence.appendCollisionObj(1750,0,100,2000)
    return scence

def createSecondScence_0():
    scence = Scence.Scence([3000,420])
    scence.appendPlane([0,0],(1280,720),tools.getImage("Scence","level_0","backGround_0.png"),0)
    scence.appendPlane([180,0],(1280,720),tools.getImage("Scence","level_0","mid_2.png"),0.2)
    scence.appendPlane([600,0],(1280,720),tools.getImage("Scence","level_0","mid_3.png"),0.3)
    scence.appendPlane([500,0],(108,361),tools.getImage("Scence","level_0","02_11.png"),0.55)
    scence.appendPlane([0,0],(538,188),tools.getImage("Scence","level_0","02_1.png"),0.95)
    scence.appendPerspective([538,0],(461,361),[0,0],[1178,0],"right",tools.getImage("Scence","level_0","02_2.png"),0.95)
    scence.appendPerspective([961,115],(188,245),[341,188],[1610,188],"right",tools.getImage("Scence","level_0","01_2.png"),1)
    scence.appendPerspective([1221,166],(118,195),[-158,188],[600,188],"left",tools.getImage("Scence","level_0","04_0.png"),1)
    scence.appendPlane([940,228],(252,133),tools.getImage("Scence","level_0","03_1.png"),0.95)
    scence.appendPlane([0,118],(981,243),tools.getImage("Scence","level_0","01_1.png"),1)
    scence.appendPerspective([1667,-37],(722,397),[1027,0],[2389,0],"right",tools.getImage("Scence","level_0","04_2.png"),1)
    scence.appendPlane([1480,0],(543,361),tools.getImage("Scence","level_0","wall_05.png"),0.31)
    scence.appendPlane([1350,145],(179,215),tools.getImage("Scence","level_0","combine_01.png"),0.7)
    scence.appendPlane([1700,137],(175,224),tools.getImage("Scence","level_0","combine_02.png"),0.5)
    scence.appendPlane([2300,273],(255,87), tools.getImage("Scence","level_0","combine_03.png"),0.8)
    scence.appendPlane([1220,-35],(447,397),tools.getImage("Scence","level_0","04_1.png"),1)

    scence.appendCollisionObj(-100,0,100,2000)
    scence.appendCollisionObj(2300,0,100,2000)
    return scence

def createACTModule():
    module_ACT = ACT_main.ACTModule()
    module_ACT.setPlayer([0,922])
    module_ACT.setBottomUI([0,-1000], [640,720], "data/levels/books/level_0_0.txt")

    module_ACT.interactive_obj_list.add(ACT_NPC.Operation_instructions((500,500,320,1280)))
    module_ACT.interactive_obj_list.add(ACT_NPC.handle_man_choice((1650,500,200,600)))
    return module_ACT


manager = Manager_Level_0()
GE.manager = manager
GE.level_manager = manager
manager.start()