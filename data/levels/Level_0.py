from data import global_environment as GE
from data.objects import AVGOBJ
import pygame

def appendFrame(obj,num,source):
    for i in range(num):
        address = source+'%d'%(i+1)+'.png'
        obj.frameList.append(pygame.image.load(address).convert_alpha())


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
        #self.ACTModule = createACTModule()
        self.AVGModule = createAVGModule()
        self.followingEventList.append(self.check_0)
        self.moduleList.append(self.AVGModule)
        print(self.moduleList)

    def check_0(self):
        for event in GE.eventList:
            if event == "AVGMODULE_END":
                print("end")
                #self.followingEventList.remove(self.check_0)
                GE.moduleList.remove(self.AVGModule)
                self.ACTModule = createACTModule()
                self.followingEventList.remove(self.check_0)
                self.followingEventList.append(self.check_1)

    def check_1(self):
        if self.ACTModule.player.loc[0] >= 1500:
            for word in self.ACTModule.bottomUI.wordsList:
                if word.label == 1:
                    word.render((240,50,50))
                    word.colorGradientSym = True
                    word.color_org = (240,50,50)
            self.followingEventList.remove(self.check_1)
            self.followingEventList.append(self.check_injured)
            self.followingEventList.append(self.check_recovery)
        pass

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
    GE.controller = module_AVG.controller
    module_AVG.clickArea = [0,470,800,300]
    module_AVG.activeSituation = True
    module_AVG.workingSituation = True
    #（创建模块）
    #（创建textBox）
    module_AVG.textBox = AVGOBJ.TextBox(loc=[0,470], size=[800,300])
    module_AVG.textBox.frameList.append(pygame.image.load('resources/GFX/test/testarea_02.png').convert())
    module_AVG.textBox.init()
    #（创建textBox）
    #(创建logsBox)
    module_AVG.logsBox = AVGOBJ.LogsBox(loc=[0,0], size=[800,770], textBoxHeight=300)
    module_AVG.logsBox.backGroundVision = pygame.image.load(GE.GFX_UI["Logs"]).convert()
    #(创建logsBox)
    #（人物）
    satmic = AVGOBJ.Character(size=[150,200],loc=[600,70],color = (200,200,200))
    #（表情1）
    expressions = AVGOBJ.Expression()

    expressions.body = pygame.image.load('resources/GFX/Character/Satmic/body.png')

    expressions.eyes = AVGOBJ.Eye(loc=[72,51])
    appendFrame(expressions.eyes,3,"resources/GFX/Character/Satmic/eye/")

    expressions.mouth = AVGOBJ.Mouth(loc=[88,89])
    appendFrame(expressions.mouth,4,"resources/GFX/Character/Satmic/mouth/")

    satmic.expressionList.append(expressions)
    #（表情1）
    satmic.init()
    satmic.setExpression(0)

    module_AVG.characterDict["Satmic"] = satmic
    #（人物）

    #（人物）
    Nacy = AVGOBJ.Character(size=[150,200],loc=[700,270],color = (200,200,200))
    #（表情1）
    expressions = AVGOBJ.Expression()

    expressions.body = pygame.image.load('resources/GFX/Character/Nacy/blank/body.jpg')

    expressions.eyes = AVGOBJ.Eye(loc=[72,51])
    expressions.eyes.frameList.append(pygame.image.load("./resources/GFX/test/transparent.png"))
    expressions.eyes.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))
    expressions.eyes.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))

    expressions.mouth = AVGOBJ.Mouth(loc=[88,89])
    expressions.mouth.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))

    Nacy.expressionList.append(expressions)
    #（表情1）
    #（表情2）
    expressions = AVGOBJ.Expression()

    expressions.body = pygame.image.load('resources/GFX/Character/Nacy/angry/body.jpg')

    expressions.eyes = AVGOBJ.Eye(loc=[72,51])
    expressions.eyes.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))
    expressions.eyes.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))
    expressions.eyes.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))

    expressions.mouth = AVGOBJ.Mouth(loc=[88,89])
    expressions.mouth.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))

    Nacy.expressionList.append(expressions)
    #（表情2）
    #（表情3）
    expressions = AVGOBJ.Expression()

    expressions.body = pygame.image.load('resources/GFX/Character/Nacy/cute/body.jpg')

    expressions.eyes = AVGOBJ.Eye(loc=[72,51])
    expressions.eyes.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))
    expressions.eyes.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))
    expressions.eyes.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))

    expressions.mouth = AVGOBJ.Mouth(loc=[88,89])
    expressions.mouth.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("resources/GFX/test/transparent.png"))

    Nacy.expressionList.append(expressions)
    #（表情3）
    Nacy.init()
    Nacy.setExpression(0)

    module_AVG.characterDict["Nacy"] = Nacy
    #（人物）
    return module_AVG

manager = Manager_Level_0()
GE.manager = manager
GE.level_manager = manager
manager.start()