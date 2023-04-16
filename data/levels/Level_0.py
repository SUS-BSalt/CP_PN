from data import global_environment as GE



class Manage_Level_0:
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
        print(GE.moduleList)

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
    module_AVG = AVGObjects.AVGModule(open('books/level_0.txt','r',encoding='UTF-8'))
    GE.controller = module_AVG.controller
    module_AVG.clickArea = [0,470,800,300]
    module_AVG.activeSituation = True
    module_AVG.workingSituation = True
    #（创建模块）
    #（创建textBox）
    module_AVG.textBox = AVGObjects.TextBox(loc=[0,470], size=[800,300])
    module_AVG.textBox.frameList.append(pygame.image.load('source/test/testarea_02.png'))
    module_AVG.textBox.init()
    #（创建textBox）
    #(创建logsBox)
    module_AVG.logsBox = AVGObjects.LogsBox(loc=[0,0], size=[800,770], textBoxHeight=300)
    module_AVG.logsBox.backGroundVision = pygame.image.load('source/UI/logs.png')
    #(创建logsBox)
    #（人物）
    satmic = AVGObjects.Character(size=[150,200],loc=[600,70],color = (200,200,200))
    #（表情1）
    expressions = AVGObjects.Expression()

    expressions.body = pygame.image.load('Source/character/Satmic/body.png')

    expressions.eyes = AVGObjects.Eye(loc=[72,51])
    appendFrame(expressions.eyes,3,"Source/character/Satmic/eye/")

    expressions.mouth = AVGObjects.Mouth(loc=[88,89])
    appendFrame(expressions.mouth,4,"Source/character/Satmic/mouth/")

    satmic.expressionList.append(expressions)
    #（表情1）
    satmic.init()
    satmic.setExpression(0)

    module_AVG.characterDict["Satmic"] = satmic
    #（人物）

    #（人物）
    Azure = AVGObjects.Character(size=[150,200],loc=[700,270],color = (200,200,200))
    #（表情1）
    expressions = AVGObjects.Expression()

    expressions.body = pygame.image.load('Source/character/Azure/blank/body.jpg')

    expressions.eyes = AVGObjects.Eye(loc=[72,51])
    expressions.eyes.frameList.append(pygame.image.load("./Source/test/transparent.png"))
    expressions.eyes.frameList.append(pygame.image.load("Source/test/transparent.png"))
    expressions.eyes.frameList.append(pygame.image.load("Source/test/transparent.png"))

    expressions.mouth = AVGObjects.Mouth(loc=[88,89])
    expressions.mouth.frameList.append(pygame.image.load("Source/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("Source/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("Source/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("Source/test/transparent.png"))

    Azure.expressionList.append(expressions)
    #（表情1）
    #（表情2）
    expressions = AVGObjects.Expression()

    expressions.body = pygame.image.load('Source/character/Azure/angry/body.jpg')

    expressions.eyes = AVGObjects.Eye(loc=[72,51])
    expressions.eyes.frameList.append(pygame.image.load("Source/test/transparent.png"))
    expressions.eyes.frameList.append(pygame.image.load("Source/test/transparent.png"))
    expressions.eyes.frameList.append(pygame.image.load("Source/test/transparent.png"))

    expressions.mouth = AVGObjects.Mouth(loc=[88,89])
    expressions.mouth.frameList.append(pygame.image.load("Source/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("Source/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("Source/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("Source/test/transparent.png"))

    Azure.expressionList.append(expressions)
    #（表情2）
    #（表情3）
    expressions = AVGObjects.Expression()

    expressions.body = pygame.image.load('Source/character/Azure/cute/body.jpg')

    expressions.eyes = AVGObjects.Eye(loc=[72,51])
    expressions.eyes.frameList.append(pygame.image.load("Source/test/transparent.png"))
    expressions.eyes.frameList.append(pygame.image.load("Source/test/transparent.png"))
    expressions.eyes.frameList.append(pygame.image.load("Source/test/transparent.png"))

    expressions.mouth = AVGObjects.Mouth(loc=[88,89])
    expressions.mouth.frameList.append(pygame.image.load("Source/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("Source/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("Source/test/transparent.png"))
    expressions.mouth.frameList.append(pygame.image.load("Source/test/transparent.png"))

    Azure.expressionList.append(expressions)
    #（表情3）
    Azure.init()
    Azure.setExpression(0)

    module_AVG.characterDict["Azure"] = Azure
    #（人物）

    GE.moduleList.append(module_AVG)

    return module_AVG