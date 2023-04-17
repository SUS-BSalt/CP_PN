import pygame
from data import global_environment as GE , setting
import random


class AVGModule:
    """AVG模块，该类只负责逻辑处理，
    你需要在创建该模块后自行添加人物对象、文本框对象，转交当前控制器，设置点击的检测区域（或许该将其写成按钮），
    其中人物对象应该以字典的语法添加在characterDict下，
    文本框通过直接赋值的方式添加
    """
    def __init__(self, book):
        self.activeSituation = True
        """整个OBJ活跃与否的标志,是相对于其他平等地位的模块而言的"""
        self.workingSituation = False
        """模块内的活跃标志，是用于指示是否该输出文本的标志"""
        self.sleepSwitch = False
        """等待的标志"""
        self.autoPlaySwitch =False
        """自动播放的标志"""
        self.clickSwitch = False
        """鼠标点击的标志"""
        self.skipSwitch = False
        """快进的标志"""

        self.eventList = []

        self.clickArea = [0,0,0,0]

        self.characterDict = {}

        self.book = book

        self.textBox = None

        self.logsBox = None

        self.reader = Reader(self)

        self.printSpeed = setting.printSpeed*setting.logicLoopFps
        """打印速度"""
        
        self.timer = 0
        self.sleepTime = 0


    def init(self):
        pass


    def controller(self):
        """为了方便理清逻辑，这里面只运行改变运行的状态标签，不允许直接执行方法！！！"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                match pygame.key.name(event.key):
                    case setting.skip:
                        #开始skip
                        self.skipSwitch = True
                    case "escape":
                        GE.controller = GE.escMenu.controller
                        GE.manager = GE.escMenu                   

            elif event.type == pygame.KEYUP:
                match pygame.key.name(event.key):
                    case setting.skip:
                        #停止skip
                        self.skipSwitch = False
                        pass

                    case 'space':
                        self.clickSwitch = True
                        pass

                    case setting.autoPlay:
                        if self.autoPlaySwitch:
                            self.autoPlaySwitch = False
                        else:
                            self.autoPlaySwitch = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                GE.camera.getMousePos()
                #print(GE.camera.getMousePos(),self.clickArea)
                if self.logsBox.activeSituation == True:
                    GE.camera.mousePosCheck(self.logsBox.rect)
                    match event.button:
                        case 1 :
                            self.logsBox.init()
                            #隐藏logs菜单
                        case 3:
                            self.logsBox.init()
                            #隐藏logs菜单
                        case 4:
                            self.logsBox.slideY += 100
                            self.logsBox.animateSym = True
                            #更新logs菜单
                        case 5:
                            self.logsBox.slideY -= 100
                            self.logsBox.animateSym = True
                            #更新logs菜单
                        
                elif GE.camera.mousePosCheck(self.clickArea):
                    match event.button:
                        case 1:
                            self.clickSwitch = True
                        case 3:
                            pass
                            
                        case 4:
                            self.logsBox.activeSituation = True
                            self.logsBox.animateSym = True
                            #打开logs菜单
                        
                    return
                #如果鼠标不在检测区域内，停止函数
            elif event.type == pygame.QUIT:
                GE.GV.set('gameRun',False)

            elif event.type == pygame.WINDOWRESIZED:
                #变化windowsize
                GE.camera.resetWindow(event)

                
    def printCurrentSentenceImmediately(self):
        while self.workingSituation == True:
            self.reader.act()
            for character in self.characterDict:
                self.characterDict[character].act()

    def act(self):
        """接下来是很长的一串判定树，别急，我会在每一层都进行说明"""
        if self.logsBox.activeSituation == True:
            #logs界面开启时
            if self.workingSituation == True:
                ##logs界面开启时，活跃
                self.printCurrentSentenceImmediately()

        elif self.skipSwitch == True:
            #（快进的方法）
            self.timer += 1
            if self.timer >= 10:
                self.workingSituation = True
                self.textBox.init()
                self.printCurrentSentenceImmediately()
                self.timer = 0
            #（快进的方法）
        
        elif self.clickSwitch == False:
            #没有点击
            if self.workingSituation == True :
                #没有点击，自身活跃
                if self.sleepSwitch == True :
                    #（睡眠的方法）没有点击，自身活跃，有睡眠开关
                    self.timer += 1
                    if self.timer >= self.sleepTime:
                        self.sleepSwitch = False
                        self.timer = 0
                    #（睡眠的方法）
                else:
                    #（常规输出的方法）没有点击，自身活跃，无睡眠开关
                    self.timer += 1
                    if self.timer >= self.printSpeed:
                        self.reader.act()
                        for character in self.characterDict:
                            if self.characterDict[character].activeSituation == True:
                                self.characterDict[character].currentExpression.mouthAct()
                        self.timer = 0
                    #（常规输出的方法）
            else:
                #没有点击，自身不活跃
                if self.autoPlaySwitch == True:
                    #（自动播放的方法）没有点击，自身不活跃，自动播放开启
                    self.timer += 1
                    if self.sleepSwitch == False:
                        self.sleepSwitch = True
                        self.sleepTime = 150
                    elif self.timer >= self.sleepTime:
                        self.timer = 0
                        self.sleepSwitch = False

                        self.workingSituation = True
                        self.textBox.init()
                        #下一句
                    #（自动播放的方法）
        else:
            #有点击
            if self.workingSituation == True:
                #有点击，活跃
                self.printCurrentSentenceImmediately()
            else:
                #有点击，不活跃
                self.workingSituation = True
                self.textBox.init()
                self.timer += 1
                if self.timer >= self.printSpeed:
                    self.reader.act()
                    for character in self.characterDict:
                        if self.characterDict[character].activeSituation == True:
                                self.characterDict[character].currentExpression.mouthAct()
                    self.timer = 0

            self.autoPlaySwitch = False
            self.clickSwitch = False
            self.sleepSwitch = False


                    
    def draw(self):
        GE.camera.cameraShot.fill((255,255,255))
        GE.camera.draw(self.textBox.vision, self.textBox.loc)
        for character in self.characterDict:
            if self.characterDict[character].onStage == True:
                self.characterDict[character].currentExpression.vision.blit(self.characterDict[character].currentExpression.mouth.vision, self.characterDict[character].currentExpression.mouth.loc)
                self.characterDict[character].currentExpression.vision.blit(self.characterDict[character].currentExpression.eyes.vision, self.characterDict[character].currentExpression.eyes.loc)
                GE.camera.draw(self.characterDict[character].currentExpression.vision, self.characterDict[character].loc)
        if self.logsBox.activeSituation == True:
            GE.camera.draw(self.logsBox.vision, self.logsBox.loc)
        

        

    def animate(self):
        for character in self.characterDict:
            self.characterDict[character].animate()            
        if self.logsBox.activeSituation == True:
            self.logsBox.animate()