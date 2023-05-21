import pygame
from data import global_environment as GE , setting

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

        self.cursor = pygame.Surface((5,30))
        self.cursor.fill((255,255,255))
        self.cursor_timer = 0

        self.clickArea = [0,0,0,0]

        self.characterDict = {}

        self.onStageCharacterList = []

        self.book = book

        self.logsBox = None

        self.reader = Reader(self)

        self.printSpeed = setting.printSpeed*setting.logicLoopFps
        """打印速度"""
        
        self.timer = 0
        self.sleepTime = 0

    def setTextBox(self, loc, size, vision):
        self.textBox = TextBox(loc, size)
        self.textBox.frameList.append(vision)
        self.textBox.init()

    def setLogsBox(self, loc, size,textBoxHeight, vision):
        self.logsBox = LogsBox(loc, size, textBoxHeight)
        self.logsBox.backGroundVision = vision


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

                    case "escape":
                        GE.controller = GE.escMenu.controller
                        GE.manager = GE.escMenu
                        #print(GE.level_manager.moduleList)
                        print("camera.loc",GE.camera.loc)
                        for obj in GE.scence.objList:
                            print(obj.loc)



            elif event.type == pygame.MOUSEBUTTONDOWN:
                GE.camera.getMousePos()
                #print(GE.camera.getMousePos(),self.clickArea)
                if self.logsBox.activeSituation == True:
                    GE.camera.mousePosCheck_UI(self.logsBox.rect)
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
                        
                elif GE.camera.mousePosCheck_UI(self.clickArea):
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
                GE.GV.set('game_run',False)

            elif event.type == pygame.WINDOWRESIZED:
                #变化windowsize
                GE.camera.resetWindow(event)

                
    def printCurrentSentenceImmediately(self):
        while self.workingSituation == True:
            self.reader.update()
            for character in self.onStageCharacterList:
                character.update()

    def update(self):
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
                        self.reader.update()
                        for character in self.onStageCharacterList:
                            if character.activeSituation == True:
                                character.currentExpression.mouthAct()
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
                    self.reader.update()
                    for character in self.onStageCharacterList:
                            if character.activeSituation == True:
                                character.currentExpression.mouthAct()
                    self.timer = 0

            self.autoPlaySwitch = False
            self.clickSwitch = False
            self.sleepSwitch = False

        #GE.camera.draw_UI(GE.camera.black,(0,0))
        GE.camera.draw_UI(self.textBox.vision, self.textBox.loc)
        for character in self.onStageCharacterList:
            character.draw()
        if self.logsBox.activeSituation == True:
            GE.camera.draw_UI(self.logsBox.vision, self.logsBox.loc)
        if self.workingSituation == False:
            #光标
            GE.camera.draw_UI(self.cursor, (self.textBox.loc[0] + self.textBox.currentWordLoc[0]+10,self.textBox.loc[1] + self.textBox.currentWordLoc[1]))
        

        
        
    def animate(self):
        for character in self.onStageCharacterList:
            if character.activeSituation == True:
                character.currentExpression.mouthAct()       
        if self.logsBox.activeSituation == True:
            self.logsBox.animate()
        
        self.cursor_timer += 1  
        if self.cursor_timer == 25:   
            self.cursor.fill((0,0,0))
        elif self.cursor_timer == 50:
            self.cursor.fill((255,255,255))
            self.cursor_timer = 0

class Reader:
    def __init__(self,AVGModule):
        
        self.master = AVGModule
        self.currentSentence = self.master.book.readline()
        self.currentWord = 0
        
        self.textEffectSwitch = False

        
    def update(self):
        try:
            match self.currentSentence[self.currentWord]:
                #匹配特殊字符，否则直接输出
                case "$":
                    #输出下一个字符
                    self.currentWord += 1
                    self.master.textBox.printer(self.currentSentence[self.currentWord])
                    self.currentWord += 1
                case "《":
                    self.textEffectSwitch = True
                    self.textEffectMatcher()
                case '[':
                    self.textEffectSwitch = True
                    self.identifyCharacters()
                case _:
                    self.master.textBox.printer(self.currentSentence[self.currentWord])
                    self.currentWord += 1


        except:
            self.currentSentence = self.master.book.readline()
            self.currentWord = 0
            self.master.workingSituation = False
            self.master.logsBox.textVisionList.insert(0,self.master.textBox.vision)
            for character in self.master.characterDict:
                self.master.characterDict[character].init()
            #读取下一句并初始化
    
    def identifyCharacters(self):
        characterName = ""
        while self.textEffectSwitch:
            self.currentWord += 1
            if self.currentSentence[self.currentWord] == "]":
                self.currentWord += 1
                self.textEffectSwitch = False
                break
            characterName += self.currentSentence[self.currentWord]
        #将人物名字读取进来

        self.master.textBox.printer(characterName, self.master.characterDict[characterName].color)
        self.master.textBox.printer(": ")
        self.master.characterDict[characterName].activeSituation = True


    def textEffectMatcher(self):
        self.textEffect = ""
        while self.textEffectSwitch:
            self.currentWord += 1
            if self.currentSentence[self.currentWord] == "》":
                self.currentWord += 1
                self.textEffectSwitch = False
                break
            self.textEffect += self.currentSentence[self.currentWord]
        #将文本特殊样式读取进来

        match self.textEffect:
            #颜色
            case _ if self.textEffect[0] == 'c':
                if self.textEffect[1:] == 'red':
                    self.master.textBox.textColor = (255,20,20)
                else:
                    self.textEffect = self.textEffect[1:].split(',')
                    self.master.textBox.textColor = tuple(int(n) for n in self.textEffect)
            case '/c':
                self.master.textBox.textColor = setting.textColor
            #加粗
            case 'b' :

                self.master.textBox.textSize = setting.textBlodSize
                self.master.textBox.font = pygame.font.Font(setting.charBlodType,self.master.textBox.textSize)
                self.master.textBox.currentWordLoc[1] -= 5
            case '/b':
                self.master.textBox.textSize = setting.textSize
                self.master.textBox.font = pygame.font.Font(setting.charType,self.master.textBox.textSize)
                self.master.textBox.currentWordLoc[1] += 5
            
            #停顿
            case _ if self.textEffect[:4] == 'wait':
                self.master.sleepSwitch = True
                self.master.sleepTime = float(self.textEffect[4:])*setting.logicLoopFps
                
            #换行
            case '/n':
                self.master.textBox.wrapText()

            case _ if self.textEffect[:4] == 'face':
                self.textEffect = self.textEffect.split("|")
                self.master.characterDict[self.textEffect[1]].setExpression(self.textEffect[2])
            case _ if self.textEffect[:6] == 'appear':
                self.textEffect = self.textEffect.split("|")
                self.master.onStageCharacterList.append(self.master.characterDict[self.textEffect[1]])
                print(self.master.onStageCharacterList)
            case _ if self.textEffect[:5] == 'leave':
                self.textEffect = self.textEffect.split("|")
                self.master.onStageCharacterList.remove(self.master.characterDict[self.textEffect[1]])
            case "NEXT":
                GE.eventList.append("NEXT")
            case 'END':
                GE.eventList.append("AVGMODULE_END")
            case _ :
                print("未知效果"+self.textEffect)

class TextBox:
    """文本框，
    存了文本大小颜色等设置，以及打印与换行，
    记得给frameList添加图片，执行初始化方法"""
    def __init__(self, loc,size):
        self.loc = loc
        self.size = size
        self.rect = self.loc + self.size

        self.vision = None
        self.frameList = []

        self.textColor = setting.textColor
        """文字颜色"""
        self.textSize = setting.textSize
        """文字大小"""
        self.textLineGap = setting.textLineGap
        """#行间距"""
        self.margins = setting.margins
        """#页边距"""
        self.textLineCutLineLoc = self.size[0] - self.margins*2
        """#换行的边线坐标"""

        self.charType = setting.charType
        self.font = pygame.font.Font(self.charType,self.textSize)
        """字体"""

        self.currentWordLoc = [self.margins, self.margins]

        self.textLineCutLineLoc = self.size[0] - self.margins*2
        """换行的位置"""

    def init(self):
        self.vision = self.frameList[0].copy()
        self.currentWordLoc = [self.margins, self.margins]

    def wrapText(self):
        self.currentWordLoc[0] = self.margins
        self.currentWordLoc[1] += self.textLineGap + self.textSize
        #换行的判断及执行

    def printer(self,msg, color = None):
        if color == None:
            self.color = self.textColor
        else:
            self.color = color
        #设置颜色

        self.msgImg = self.font.render(msg,False,self.color)
        #生成文字图像
        
        self.vision.blit(self.msgImg,self.currentWordLoc)
        #将文字图像绘上画板
        
        self.currentWordLoc[0] += self.msgImg.get_size()[0]
        #决定下一个字符位置
        if self.currentWordLoc[0] >= self.textLineCutLineLoc:
            self.wrapText()

class LogsBox:
    """在每次刷新textBox的vision之前，将其copy一份扔到textVisionList里"""
    def __init__(self,loc = [0,0], size = [10,10], textBoxHeight = 0 ):
        self.activeSituation = False
        self.animateSym = False
        self.loc = loc.copy()
        self.size = size.copy()
        self.rect = loc+size
        self.vision = pygame.Surface(size)
        self.tempVision = pygame.Surface(size)

        self.backGroundVision = pygame.Surface(size)
        self.textVisionList = []
        """新的语句应该插入到队列头部"""

        self.textBoxHeight = textBoxHeight
        #每个文本的高度
        self.slideY = 0
        """#记录滚轮滑动的距离，因为该功能只许玩家向上看之前的记录，故，滚轮向上该值增大，滚轮向下该值减小，
        并且不允许小于0,不允许大于 (len(self.textVisionList)-1) * self.textBoxHeight """
    def init(self):
        self.activeSituation = False
        self.slideY = 0

    def animate(self):
        """每次滚动滑轮时调用该方法,更新画面用"""
        #画上背景
        if self.animateSym == True:
            if self.slideY > (len(self.textVisionList)-1) * self.textBoxHeight:
                self.slideY -= 10
            elif self.slideY < 0:
                self.slideY += 10
            else:
                self.animateSym = False

            self.tempVision.blit(self.backGroundVision,self.loc)
            
            index = 0
            for textVision in self.textVisionList:
                index += 1
                currentTextLoc  = self.size[1] - self.textBoxHeight*index + self.slideY
                if currentTextLoc > self.size[1]:
                    continue

                elif currentTextLoc > -self.textBoxHeight :
                    self.tempVision.blit(textVision,[0,currentTextLoc])

                elif currentTextLoc < -self.textBoxHeight :
                    break
            self.vision = self.tempVision.copy()

class Character:
    """你需要先创建表情Expression，并添加进expressionList里"""
    def __init__(self, loc = [0,0], size = [0,0], color = (255,255,255)):
        self.activeSituation = False

        self.loc = loc.copy()
        self.size = size.copy()
        
        self.color = color

        self.expressionDict = {}
        self.currentExpression = None
        #表情列表与当前的表情

    
    def init(self):
        self.activeSituation = False
        for expression in self.expressionDict:
            self.expressionDict[expression].init()

    def setExpression(self, expression):
        self.currentExpression = self.expressionDict[expression]

    def update(self):
        pass
        
    def draw(self):
        GE.camera.draw_UI(self.currentExpression.vision,self.loc)
        GE.camera.draw_UI(self.currentExpression.mouth.vision,self.returnPartsAbsLoc(self.currentExpression.mouth.loc))
        GE.camera.draw_UI(self.currentExpression.eyes.vision,self.returnPartsAbsLoc(self.currentExpression.eyes.loc))
        pass
    def returnPartsAbsLoc(self,partsLoc):
        return (self.loc[0]+partsLoc[0],self.loc[1]+partsLoc[1])


    def animate(self):
        #可能一个是否眨眼的判断
        #self.vision = self.frameList[0].copy()
        self.currentExpression.eyes.animate()
        if self.activeSituation:
            self.currentExpression.mouthAct()

class Expression:
    """你需要给body给予一张图片，并赋予eyes与mouth对象"""
    def __init__(self,body):
        self.vision = None
        self.body = body

    def eyeSetting(self,loc = [0,0], eyesBlinkGap = 3, frameList = [], framePlayList = [0,1,2,1], timeStampList = [40,41,44,46]):
        self.eyes = Eye(loc, eyesBlinkGap, frameList, framePlayList, timeStampList)
    def mouthSetting(self,loc = [0,0], frameList = [], framePlayList = []):
        self.mouth = Mouth(loc, frameList, framePlayList)

    def init(self):
        self.mouth.init()
        self.eyes.init()
        self.vision = self.body
    def mouthAct(self):
        self.mouth.animate()

    def animate(self):
        #可能一个是否眨眼的判断
        #self.vision = self.frameList[0].copy()
        self.eyes.animate()

class Eye:
    def __init__(self, loc, eyesBlinkGap, frameList, framePlayList, timeStampList):
        self.loc = loc
        self.currentEye = 0

        self.BlinkGap = eyesBlinkGap * setting.animateLoopFps
        self.BlinkGapTimer = 0
        self.blinkTimer = 0

        self.vision = None
        self.frameList = frameList
        self.timeStampList = timeStampList
        self.framePlayList = framePlayList
    def init(self):
        self.blinkTimer = 0
        self.currentFrame = 0
        self.vision = self.frameList[self.framePlayList[0]]
        self.activeSituation = False
        pass
    
    def animate(self):
        self.eyesBlinkTimer += 1

        if self.eyesBlinkTimer >= self.BlinkGap:
            self.eyesBlinkTimer = 0
            self.blink()

    def blink(self):
        self.blinkTimer += 1
        #timer每动画帧自加一
        if self.blinkTimer >= self.timeStampList[-1]:
            self.init()
        #如果timer等于动画周期，重置自身
        if self.blinkTimer >= self.timeStampList[self.currentFrame]:
            self.currentFrame += 1
            self.vision = self.frameList[self.framePlayList[self.currentFrame]]
        #如果timer等于当前帧对应的时间戳，则将当前帧记号加一,更新obj的vision

class Mouth:
    def __init__(self, loc, frameList, framePlayList):
        self.loc = loc

        self.currentMouth = 0

        self.mouthActTimer = 0

        self.vision = pygame.Surface((10,10))
        self.frameList = frameList
        self.framePlayList = framePlayList
        pass

    def init(self):
        self.currentMouth = 0
        self.vision = self.frameList[0]

    def animate(self):
        self.vision = self.frameList[self.framePlayList[self.currentMouth]]
        self.currentMouth += 1

        if self.currentMouth >= len(self.frameList):
            self.currentMouth = self.framePlayList[0]