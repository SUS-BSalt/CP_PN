import pygame
from data import global_environment as GE,tools,setting


class Player(pygame.sprite.Sprite):
    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self)
        self.inputList = []

        self.eventList = []

        self.loc = loc
        self.rect = pygame.Rect(0,0,0,0)

        self.faceSide = "r"
        self.frontFoot = "l"

        self.cameraMovingSpeed = 3.25
        self.cameraMovingSpeedToLeft = -3.25

        self.beatingSymbol = False
        self.rightMoveSymbol = False
        self.leftMoveSymbol = False
        self.shiftSymbol = False
        self.defenceSymbol = False

        self.coerciveActingSymbol = False
        self.beHitSymbol = False

        self.timer = 0

        self.load_state_machine()
        self.currentAction = self.standing
        self.currentAction.beg_execute()

        self.redPoint = pygame.image.load("resources\\GFX\\test\\redPoint.png")

    def load_state_machine(self):
        #载入各种各样的状态机
        self.standing = Standing(self)
        self.standingToLeft = Standing(self).changeFaceSides()

        self.walking = Walking(self)
        self.walkingToLeft = Walking(self).changeFaceSides()

        self.normalAttack = NormalAttack(self)
        self.normalAttackToLeft = NormalAttack(self).changeFaceSides()


        
    def init(self):
        self.inputList.clear()
        self.picLoc = (self.loc[0] - rectify , self.loc[1] - 200)

    def setRect(self, rect):
        self.rect.update(self.loc[0] - rect[0], self.loc[1] - rect[1], rect[2], rect[3])

    def changePosition(self, x_var, y_var):
        self.rect[0] += x_var
        self.rect[1] += y_var
        #检测碰撞
        collider = GE.scence.collisionDetection(self)
        if collider:
            self.rect[0] -= x_var
            self.rect[1] -= y_var
            print("collider!")
            return 0 
        self.loc[0] += x_var
        self.loc[1] += y_var

    def cameraTracking(self):
        gap = self.loc[0] - GE.camera.loc[0] - 640
        if 1 < gap <= 10:
            GE.camera.updateCameraLoc((1,0))
        elif -10 < gap <= -1:
            GE.camera.updateCameraLoc((-1,0))  
        elif 10 < gap <= 120:
            GE.camera.updateCameraLoc((3,0))
        elif -120 < gap <= -10:
            GE.camera.updateCameraLoc((-3,0))        
        elif 120 < gap :
            GE.camera.updateCameraLoc((10,0))
        elif gap < -120:
            GE.camera.updateCameraLoc((-10,0))

    def faceSideCheck(self):
        if GE.camera.mousePos[0] >= self.loc[0]:
            if self.faceSide == "l":
                self.loc[0] += 25
                self.faceSide = "r"
                return True
        else:
            if self.faceSide == "r":
                self.loc[0] -= 25
                self.faceSide = "l"
                return True
        return False


    def update(self):
        #只认可最新输入的一个指令
        #当其执行攻击或防御时，传递一个打击的事件，让上层的模组去读取。
        #print(self.loc,GE.camera.getMousePos())
        self.cameraTracking()
        if self.beHitSymbol == True:
            #被打中时
            pass

        elif self.coerciveActingSymbol == True:
            #如果在强制行动中，执行当前动作
            self.currentAction.update()
            pass

        elif self.coerciveActingSymbol == False:
            #当玩家不在强制行动中
            self.currentAction.update()
            #执行当前动作
            
            if self.inputList != []:
                self.timer = 0
                self.inputList = self.inputList[-1:]

                self.actionDistributor()
                #print(self.loc[0],GE.getMousePos()[0])
                self.inputList.clear()
            
            GE.camera.getMousePos()
            if self.faceSideCheck():
                self.resetAction()
                pass

            #如果输入列表不为空，执行输入信号，归零计时器，重置动作
        GE.camera.draw(self.currentAction.vision,self.currentAction.picLoc)

    def draw(self):
        GE.camera.draw(self.currentAction.vision,self.currentAction.picLoc)
        pass
        
    def animate(self):
        pass

    def resetAction(self):
        self.timer = 0
        if self.defenceSymbol:
            #进入防御
            pass
        elif self.rightMoveSymbol:
            #向右走
            if self.faceSide == "r":
                #向右走，面向右
                if self.shiftSymbol:
                    #向右走，面向右，奔跑
                    pass
                else:
                    #向右走，面向右，慢走
                    self.walking.beg_execute()
            else:
                #向右走，面向左，后退
                self.faceSide = "l"
                pass
        elif self.leftMoveSymbol:
            #向左走
            if self.faceSide == "r":
                #向左走，面向右，后退
                self.faceSide = "r"
                pass
            else:
                #向左走，面向左
                if self.shiftSymbol == True:
                    #向左走，面向左，奔跑
                    pass
                else:
                    #向左走，面向左，慢走
                    self.walkingToLeft.beg_execute()

        else:
            #站立
            if self.faceSide == "r":
                self.standing.beg_execute()
            else:
                self.standingToLeft.beg_execute()

    def actionDistributor(self):
        if "atk" in self.inputList:
            #攻击
            if self.faceSide == "r":
                #向右攻击
                self.normalAttack.beg_execute()
            else:
                #向左攻击
                self.normalAttackToLeft.beg_execute()

        elif "def" in self.inputList:
                    #好防御
                    if self.faceSide == "r":
                        #向右防御
                        pass
                    else:
                        #向左防御
                        pass

        elif self.defenceSymbol:
            #防御
            if self.faceSide == "r":
                #向右防御
                pass
            else:
                 #向左防御
                 pass
                
        elif "right" in self.inputList:
            #向右走
            if self.faceSide == "r":
                #向右走，面向右
                self.walking.beg_execute()
            else:
                #向右走，面向左，后退
                pass

        elif "left" in self.inputList:
            #向左走
            if self.faceSide == "r":
                #向左走，面向右，后退
                pass
            else:
                #向左走，鼠标在左
                self.walkingToLeft.beg_execute()


class NormalAttack:
    def __init__(self, master):
        self.master = master

        self.picSize = (348,200)
        self.picLoc = (0,0)
        
        self.frames = tools.getFrames("Character","Nacy","act_Attack")
        self.sfxs = ("Hu",)

        self.act0_frame_list = (0,1,2)
        self.act0_gfx_time_stamp = (10,20,40)
        self.act0_pic_loc_rectify = (125,122,122)                
        self.act0_moving_steps = (40,55,0)
        self.act0_rect = ((30,147,40,100),(25,144,35,90),(25,144,35,90))
        self.act0_sfx_list = (0,)
        self.act0_sfx_time_stamp = (20,100)

        self.act1_frame_list = (3,4,5)
        self.act1_gfx_time_stamp = (10,20,40)
        self.act1_pic_loc_rectify = (47,120,120)        
        self.act1_moving_steps = (68,113,0)
        self.act1_rect = ((15,167,30,110),(40,120,45,70),(40,120,45,70))
        self.act1_sfx_list = (0,)
        self.act1_sfx_time_stamp = (20,100)

        self.currentFrame = 0
        self.currentSFXFrame = 0

        self.frame_list = self.act0_frame_list
        self.gfx_time_stamp = self.act0_gfx_time_stamp
        self.pic_loc_rectify = self.act0_pic_loc_rectify
        self.moving_steps = self.act0_moving_steps        
        self.rects = self.act0_rect
        self.sfx_list = self.act0_sfx_list
        self.sfx_time_stamp = self.act0_sfx_time_stamp

        self.vision = self.frames[self.frame_list[0]]

        self.coerciveActingFrame = 25

    def locatedPicLoc(self,rectify):
        self.picLoc = (self.master.loc[0] - rectify , self.master.loc[1] - 200)

    def init(self):
        self.currentFrame = 0
        self.currentSFXFrame = 0

    def changeFaceSides(self):
        self.frames = [pygame.transform.flip(image,True,False) for image in self.frames]

        self.act0_moving_steps = (-40,-55,0)
        self.act0_pic_loc_rectify = (9,76,76)
        self.act0_rect = ((10,147,40,100),(10,144,35,90),(10,144,35,90))

        self.act1_moving_steps = (-68,-113,0)
        self.act1_pic_loc_rectify = (25,52,52)
        self.act1_rect = ((15,167,30,110),(5,120,45,70),(5,120,45,70))
        return self

    def beg_execute(self):
        self.master.coerciveActingSymbol = True
        if self.master.currentAction == self:
            self.frame_list = self.act1_frame_list
            self.gfx_time_stamp = self.act1_gfx_time_stamp
            self.pic_loc_rectify = self.act1_pic_loc_rectify
            self.moving_steps = self.act1_moving_steps
            self.sfx_list = self.act1_sfx_list
            self.sfx_time_stamp = self.act1_sfx_time_stamp                        
        else:
            self.frame_list = self.act0_frame_list
            self.gfx_time_stamp = self.act0_gfx_time_stamp
            self.pic_loc_rectify = self.act0_pic_loc_rectify
            self.moving_steps = self.act0_moving_steps
            self.sfx_list = self.act0_sfx_list
            self.sfx_time_stamp = self.act0_sfx_time_stamp

        self.master.currentAction = self
        self.vision = self.frames[self.frame_list[0]]
        self.master.setRect(self.rects[0])
        self.master.changePosition(self.moving_steps[0],0)
        self.locatedPicLoc(self.pic_loc_rectify[0])
        self.init()
        
    def update(self):
        self.master.timer += 1

        if self.master.coerciveActingSymbol \
            and self.master.timer > self.coerciveActingFrame:
            self.master.coerciveActingSymbol = False

        if self.master.timer >= self.gfx_time_stamp[-1]:
            self.master.resetAction()
            self.init()

        elif self.master.timer >= self.gfx_time_stamp[self.currentFrame]:
            self.currentFrame += 1
            self.master.setRect(self.rects[self.currentFrame])
            self.master.changePosition(self.moving_steps[self.currentFrame],0)
            self.locatedPicLoc(self.pic_loc_rectify[self.currentFrame])
            self.vision = self.frames[self.frame_list[self.currentFrame]]

        if self.master.timer >= self.sfx_time_stamp[self.currentSFXFrame]:
            GE.SFX[self.sfxs[self.sfx_list[self.currentSFXFrame]]].play()
            self.currentSFXFrame += 1

class Attack_0:
    def __init__(self, master):
        self.master = master

        self.picSize = (348,200)
        self.picLoc = (0,0)
    
        self.frames = tools.getFrames("Character","Nacy","act_Attack")[0:3]
        self.sfxs = ("Hu",)

        self.frame_list = (0,1,2)
        self.gfx_time_stamp = (10,20,40)
        self.pic_loc_rectify = (125,122,122)
        self.moving_steps = (40,55,0)
        self.rect = ((30,147,40,100),(25,144,35,90),(25,144,35,90))
        self.sfx_list = (0,)
        self.sfx_time_stamp = (20,100)

        self.currentFrame = 0
        self.currentSFXFrame = 0

    def locatedPicLoc(self,rectify):
        self.picLoc = (self.master.loc[0] - rectify , self.master.loc[1] - 200)

    def changeFaceSides(self):
        self.frames = [pygame.transform.flip(image,True,False) for image in self.frames]

        self.moving_steps = (-40,-55,0)
        self.pic_loc_rectify = (9,76,76)
        self.rect = ((10,147,40,100),(10,144,35,90),(10,144,35,90))

    def beg_execute(self):
        self.master.coerciveActingSymbol = True
        self.master.currentAction = self
        self.master.timer = 0

        self.currentFrame = 0
        self.currentSFXFrame = 0

        self.vision = self.frames[self.frame_list[0]]
        self.master.setRect(self.rects[0])
        self.master.changePosition(self.moving_steps[0],0)
        self.locatedPicLoc(self.pic_loc_rectify[0])


    def resetAction(self):
        if "atk" in self.master.inputList:
            self.master.Attack_1.beg_execute()
        elif pygame.key.get_pressed(setting.right):
            self.master.walking.beg_execute()
        elif pygame.key.get_pressed(setting.left):
            self.master.walkingToLeft.beg_execute()
        elif self.master.timer >= self.gfx_time_stamp[-1]:
            if self.master.faceSide == "r":
                self.master.standing.beg_execute()
            else:
                self.master.standingToLeft.beg_execute()

    def update(self):
        self.master.timer += 1

        #判定是否解除硬直
        if self.master.coerciveActingSymbol \
            and self.master.timer > self.coerciveActingFrame:
            self.master.coerciveActingSymbol = False

        #当不在硬直时，判定是否需要更改玩家状态
        if self.master.coerciveActingSymbol == False:
            self.resetAction()

        if self.master.timer >= self.gfx_time_stamp[self.currentFrame]:
            self.currentFrame += 1
            self.master.setRect(self.rects[self.currentFrame])
            self.master.changePosition(self.moving_steps[self.currentFrame],0)
            self.locatedPicLoc(self.pic_loc_rectify[self.currentFrame])
            self.vision = self.frames[self.frame_list[self.currentFrame]]

        if self.master.timer >= self.sfx_time_stamp[self.currentSFXFrame]:
            GE.SFX[self.sfxs[self.sfx_list[self.currentSFXFrame]]].play()
            self.currentSFXFrame += 1

class Walking:
    def __init__(self, master):
        self.master = master

        self.picSize = (112,200)
        self.picLoc = (0,0)
        self.pic_loc_rectify = (22,200)

        self.frames = tools.getFrames("Character","Nacy","act_Walking")

        self.act0_frame_list = (0,1,2,3)
        self.act0_gfx_time_stamp = (10,20,30,40)
        #self.act0_gfx_time_stamp = [30,60,90,120]
        self.act0_moving_steps = (30,30,30,30)
        self.act0_pic_loc_rectify = (42,37,45,42)
        self.act0_rect = ((20,170,30,100),(20,170,30,100),(20,170,30,100),(20,170,30,100))
        self.cameraMovingSpeed = 3

        self.currentFrame = 0

        self.frame_list = self.act0_frame_list
        self.gfx_time_stamp = self.act0_gfx_time_stamp
        self.moving_steps = self.act0_moving_steps
        self.pic_loc_rectify = self.act0_pic_loc_rectify
        self.rects = self.act0_rect

        self.vision = self.frames[self.frame_list[0]]

        self.coerciveActingFrame = 0

    def locatedPicLoc(self,rectify):
        self.picLoc = (self.master.loc[0] - rectify , self.master.loc[1] - 200)

    def init(self):
        self.vision = self.frames[self.frame_list[0]]
        self.currentFrame = 0
        pass

    def changeFaceSides(self) -> "Walking":
        self.frames = [pygame.transform.flip(image,True,False) for image in self.frames]

        self.act0_pic_loc_rectify = (80,85,77,80)
        self.act0_moving_steps = (-30,-30,-30,-30)
        self.act0_rect = ((10,170,30,100),(10,170,30,100),(10,170,30,100),(10,170,30,100))
    
        self.moving_steps = self.act0_moving_steps
        self.pic_loc_rectify = self.act0_pic_loc_rectify
        self.rects = self.act0_rect

        self.cameraMovingSpeed = -3
        return self
    
    def beg_execute(self):
        self.master.currentAction = self
        self.vision = self.frames[self.frame_list[0]]
        self.master.setRect(self.rects[0])
        self.master.changePosition(self.moving_steps[0],0)
        self.locatedPicLoc(self.pic_loc_rectify[0])
        self.init()

    def update(self):
        if not self.master.rightMoveSymbol and\
           not self.master.leftMoveSymbol:
            self.master.resetAction()
            return 0 
        
        self.master.timer += 1
        
        if self.master.timer >= self.gfx_time_stamp[-1]:
            self.master.timer = 0
            self.currentFrame = 0
            self.vision = self.frames[self.frame_list[0]]
            self.master.setRect(self.rects[0])
            self.master.changePosition(self.moving_steps[0],0)
            self.locatedPicLoc(self.pic_loc_rectify[0])
            
        elif self.master.timer >= self.gfx_time_stamp[self.currentFrame]:
            self.currentFrame += 1
            self.master.setRect(self.rects[self.currentFrame])
            self.master.changePosition(self.moving_steps[self.currentFrame],0)
            self.locatedPicLoc(self.pic_loc_rectify[self.currentFrame])
            self.vision = self.frames[self.frame_list[self.currentFrame]]

class Holding:
    pass

class Standing:
    def __init__(self, master):
        self.master = master

        self.picSize = (70,200)
        self.picLoc = (0,0)
        self.pic_loc_rectify = (64,200)
        
        self.frames = tools.getFrames("Character","Nacy","act_Standing")

        self.act0_frame_list = [0,1]
        self.act0_gfx_time_stamp = [70,140]
        self.act0_pic_loc_rectify = (64,200)

        self.currentFrame = 0

        self.frame_list = self.act0_frame_list
        self.gfx_time_stamp = self.act0_gfx_time_stamp
        self.moving_steps = [0]

        self.vision = self.frames[self.frame_list[0]]

        self.coerciveActingFrame = 0

    def locatedPicLoc(self,rectify):
        self.picLoc = (self.master.loc[0] - rectify[0] , self.master.loc[1] - rectify[1])

    def init(self):
        self.vision = self.frames[self.frame_list[0]]
        self.currentFrame = 0
        pass

    def changeFaceSides(self):
        self.frames = [pygame.transform.flip(image,True,False) for image in self.frames]

        self.act0_pic_loc_rectify = (self.picSize[0] - self.act0_pic_loc_rectify[0],self.act0_pic_loc_rectify[1])
        self.pic_loc_rectify = self.act0_pic_loc_rectify
        return self
        
    def beg_execute(self):
        self.master.currentAction = self
        self.locatedPicLoc(self.pic_loc_rectify)
        #self.master.setRect(self.picLoc[0],self.picLoc[1],self.picSize[0],self.picSize[1])
        
        self.init()

    def update(self):
        self.master.timer += 1

        if self.master.timer >= self.gfx_time_stamp[-1]:
            self.master.timer = 0
            self.init()
        elif self.master.timer >= self.gfx_time_stamp[self.currentFrame]:
            self.currentFrame += 1
            self.vision = self.frames[self.frame_list[self.currentFrame]]