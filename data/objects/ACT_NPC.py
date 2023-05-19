import pygame
from data import global_environment as GE,tools
class Operation_instructions(pygame.sprite.Sprite):
    """操作教程，提示操作方法的图标，玩家离开提示位置后自动消失"""
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.pic_0 = tools.getImage("UI","A.png")
        self.pic_1 = tools.getImage("UI","D.png")
        self.rect = pygame.Rect(rect)
        self.activeSituation = False
        self.dyingSym = False
        self.timer = 100
    
    def update(self):
        if self.dyingSym:
            self.timer -= 1
            self.pic_0.set_alpha(int(self.timer*2.5))
            self.pic_1.set_alpha(int(self.timer*2.5))
            if self.timer == 0:
                self.kill()
        elif self.activeSituation:
            pass
        else:
            self.dyingSym = True
        GE.camera.draw(self.pic_0,(265,720))
        GE.camera.draw(self.pic_1,(940,720))
    def exec(self):
        pass

class NPC_noMod(pygame.sprite.Sprite):
    """空物体"""
    def __init__(self, rect=(0,0,10,10)):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(rect)
        self.activeSituation = False
        self.dyingSym = False
        self.timer = 100
    
    def update(self):
        pass
    def exec(self):
        pass

class handle_man_choice(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.pic_0 = tools.getImage("Scence","level_0","The-Handed-Man.png")
        self.pic_1 = tools.getImage("UI","E.png")

        self.textBoxSize = [30,30]
        self.textBoxLoc = [630.0,340]
        self.currentWordLoc = [0,0]
        self.textBox = pygame.Surface((self.textBoxSize[0]+30,self.textBoxSize[1]+20))
        self.printingList = []

        self.speakSymbol = False
        self.printingSymbol = False
        
        self.rect = pygame.Rect(rect)
        self.draw_loc_0 = (1700,552)
        self.draw_loc_1 = (615,648)
        self.activeSituation = False
        self.dyingSym = False
        self.timer = 100
        self.step_counter = 0
        self.printing_timer = 0

    def textBoxUpdate(self):
        GE.camera.draw_UI(self.textBox,(self.textBoxLoc[0],self.textBoxLoc[1]))
        if self.printingList:
            self.printing_timer +=1
            if self.printing_timer < 5:
                return
            self.textBoxPrint(self.printingList.pop(0))
            self.printing_timer = 0
            if not self.printingList:
                self.printingSymbol = False
            

    def textBoxPrint(self,msg):
        self.msgImg = GE.UIfont_04.render(msg,False,(255,255,255))
        #生成文字图像
        if self.currentWordLoc[0] >= self.textBoxSize[0]-25:
            if self.textBoxSize[0] <= 200:
                self.textBoxSize[0] += self.msgImg.get_size()[0]
                self.textBoxLoc[0] -= 0.5*self.msgImg.get_size()[0]
            else:
                self.textBoxSize[1] = 100
                self.currentWordLoc = [0,50]
                self.textBoxLoc[1] -= 25
            newbox = pygame.Surface((self.textBoxSize[0]+30,self.textBoxSize[1]+20))
            newbox.blit(self.textBox,(0,0))
            self.textBox = newbox
        self.textBox.blit(self.msgImg,(self.currentWordLoc[0]+15,self.currentWordLoc[1]+10))
        #将文字图像绘上画板
        self.currentWordLoc[0] += self.msgImg.get_size()[0]
        #决定下一个字符位置
 
    def initTextBox(self):
        self.textBoxSize = [30,30]
        self.textBoxLoc = [630.0,340]
        self.textBox = pygame.Surface((self.textBoxSize[0]+30,self.textBoxSize[1]+20))
        self.currentWordLoc = [0,0]

    def update(self):
        GE.camera.draw(self.pic_0,self.draw_loc_0)
        if self.activeSituation:
        #当自身处在与玩家活动的区域
            GE.camera.draw_UI(self.pic_1,self.draw_loc_1)
            if self.speakSymbol:
                self.textBoxUpdate()
            if "interact" in GE.eventList:
                if not self.printingSymbol:
                    self.exec()
                GE.eventList.remove("interact")
        elif self.step_counter != 0 :
        #当自生不在与玩家互动的区域，且步骤计数器不为0时，重置状态
            self.speakSymbol = False
            self.step_counter = 0
            self.initTextBox()
    def exec(self):
        match self.step_counter:
            case 0:
                self.speakSymbol = True
                self.printingSymbol = True
                self.printingList = [i for i in "献身于斗争←"]
            case 1:
                self.initTextBox()
                self.printingSymbol = True
                self.printingList = [i for i in "确定吗？←"]
            case 2:
                GE.eventList.append("jump_to_01")
        self.step_counter += 1

