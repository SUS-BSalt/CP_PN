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

        self.attack_0 = Attack_0(self)
        self.attack_0_left = Attack_0(self).changeFaceSides()

        self.attack_1 = Attack_1(self)
        self.attack_1_left = Attack_1(self).changeFaceSides()

        self.attack_2 = Attack_2(self)
        self.attack_2_left = Attack_2(self).changeFaceSides()


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
        gap = (self.loc[0]*0.8 + GE.camera.mousePos[0]*0.2) - GE.camera.loc[0] - 640
        GE.camera.updateCameraLoc((int(gap*0.1),0))
        """if 1 < gap <= 10:
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
            GE.camera.updateCameraLoc((-10,0))"""

    def faceSideCheck(self):
        if GE.camera.mousePos[0] >= self.loc[0]:
            if self.faceSide == "l":
                self.faceSide = "r"
                return True
        else:
            if self.faceSide == "r":
                self.faceSide = "l"
                return True
        return False

    def pushing_input(self,input):
        #只认可最新输入的一个指令，因为我发觉这个游戏又不需要搓招
        #虽然这个函数所做的事简直蠢上天了，但是为了方便理清逻辑还是可以保留。
        #抱歉
        self.inputList.clear()
        self.inputList.append(input)

    def update(self):
        
        #当其执行攻击或防御时，传递一个打击的事件，让上层的模组去读取。
        #print(self.loc,GE.camera.getMousePos())
        GE.camera.getMousePos()
        self.cameraTracking()
        self.faceSideCheck()
        self.currentAction.update()
        if self.beHitSymbol == True:
            #被打中时
            pass

        #如果输入列表不为空，执行输入信号，归零计时器，重置动作
        GE.camera.draw(self.currentAction.vision,self.currentAction.picLoc)
        GE.camera.draw(GE.camera.redPoint,(self.loc[0],self.currentAction.picLoc[1]))

    def draw(self):
        GE.camera.draw(self.currentAction.vision,self.currentAction.picLoc)
        pass
        
    def animate(self):
        pass

class Attack_0:
    def __init__(self, master):
        self.master = master

        self.currentFrame = 0
        self.currentSFXFrame = 0

        self.coerciveActingFrame = 25
        self.load_constant()

    def load_constant(self):
        self.frames = tools.getFrames("Character","Nacy","act_Attack")[0:3]
        self.sfxs = ("Hu",)
        self.picSize = (348,200)
        self.picLoc = (0,0)

        self.frame_list = (0,1,2)
        self.gfx_time_stamp = (10,20,40)
        self.pic_loc_rectify = (125,122,122)
        self.moving_steps = (40,55,0,0)
        self.rects = ((30,147,40,100),(25,144,35,90),(25,144,35,90))
        self.sfx_list = (0,)
        self.sfx_time_stamp = (20,100)

    def locatedPicLoc(self,rectify):
        self.picLoc = (self.master.loc[0] - rectify , self.master.loc[1] - 200)

    def changeFaceSides(self):
        self.frames = [pygame.transform.flip(image,True,False) for image in self.frames]

        self.moving_steps = (-40,-55,0,0)
        self.pic_loc_rectify = (9,76,76)
        self.rects = ((10,147,40,100),(10,144,35,90),(10,144,35,90))

        return self

    def beg_execute(self):
        self.master.coerciveActingSymbol = True
        self.master.currentAction = self
        self.master.timer = 0
        self.master.inputList.clear()

        self.currentFrame = 0
        self.currentSFXFrame = 0

        self.vision = self.frames[self.frame_list[0]]
        self.master.setRect(self.rects[0])
        self.master.changePosition(self.moving_steps[0],0)
        self.locatedPicLoc(self.pic_loc_rectify[0])

    def resetAction(self):
        if "atk" in self.master.inputList:
            if  self.master.faceSide == "r":
                self.master.attack_1.beg_execute()
            else:
                self.master.attack_1_left.beg_execute()
        elif self.master.rightMoveSymbol:
            self.master.walking.beg_execute()
        elif self.master.leftMoveSymbol:
            self.master.walkingToLeft.beg_execute()
        elif self.master.timer >= self.gfx_time_stamp[-1]:
            #如果状态自然结束，那么先修改角色位置，再将状态转换到站立
            self.master.changePosition(self.moving_steps[-1],0)
            if self.master.faceSide == "r":
                self.master.standing.beg_execute()
            else:
                self.master.standingToLeft.beg_execute()
        else:
            return False

        return True

    def update(self):
        self.master.timer += 1

        #判定是否解除硬直
        if self.master.coerciveActingSymbol \
            and self.master.timer > self.coerciveActingFrame:
            self.master.coerciveActingSymbol = False

        #当不在硬直时，判定是否需要更改玩家状态
        if self.master.coerciveActingSymbol == False:
            if self.resetAction():
                return 0


        if self.master.timer >= self.gfx_time_stamp[self.currentFrame]:
            self.currentFrame += 1
            self.master.setRect(self.rects[self.currentFrame])
            self.master.changePosition(self.moving_steps[self.currentFrame],0)
            self.locatedPicLoc(self.pic_loc_rectify[self.currentFrame])
            self.vision = self.frames[self.frame_list[self.currentFrame]]

        if self.master.timer >= self.sfx_time_stamp[self.currentSFXFrame]:
            GE.SFX[self.sfxs[self.sfx_list[self.currentSFXFrame]]].play()
            self.currentSFXFrame += 1

class Attack_1(Attack_0):
    def __init__(self,master):
        self.master = master

        self.currentFrame = 0
        self.currentSFXFrame = 0

        self.coerciveActingFrame = 25
        self.load_constant()
    
    def load_constant(self):
        self.frames = tools.getFrames("Character","Nacy","act_Attack")[3:6]
        self.sfxs = ("Hu",)
        self.picSize = (348,200)
        self.picLoc = (0,0)
    
        self.frame_list = (0,1,2)
        self.gfx_time_stamp = (10,20,40)
        self.pic_loc_rectify = (47,120,120)        
        self.moving_steps = (68,113,0,0)
        self.rects = ((15,167,30,110),(40,120,45,70),(40,120,45,70))
        self.sfx_list = (0,)
        self.sfx_time_stamp = (20,100)

    def resetAction(self):
        if "atk" in self.master.inputList:
            if  self.master.faceSide == "r":
                self.master.attack_2.beg_execute()
            else:
                self.master.attack_2_left.beg_execute()
        elif self.master.rightMoveSymbol:
            self.master.walking.beg_execute()
        elif self.master.leftMoveSymbol:
            self.master.walkingToLeft.beg_execute()
        elif self.master.timer >= self.gfx_time_stamp[-1]:
            #如果状态自然结束，那么先修改角色位置，再将状态转换到站立
            self.master.changePosition(self.moving_steps[-1],0)
            if self.master.faceSide == "r":
                self.master.standing.beg_execute()
            else:
                self.master.standingToLeft.beg_execute()

        else:
            return False
        
        return True

    def changeFaceSides(self):
        self.frames = [pygame.transform.flip(image,True,False) for image in self.frames]

        self.moving_steps = (-68,-113,0,0)
        self.pic_loc_rectify = (25,52,30)
        self.rect = ((27,167,30,110),(5,120,45,70),(5,120,45,70))

        return self

class Attack_2(Attack_0):
    def __init__(self,master):
        self.master = master

        self.currentFrame = 0
        self.currentSFXFrame = 0

        self.coerciveActingFrame = 25
        self.load_constant()
    
    def load_constant(self):
        self.frames = tools.getFrames("Character","Nacy","act_Attack")[6:10]
        self.sfxs = ("Hu",)
        self.picSize = (348,200)
        self.picLoc = (0,0)
    
        self.frame_list = (0,1,2,3)
        self.gfx_time_stamp = (8,12,20,40)
        self.pic_loc_rectify = (74,90,120,120)
        self.moving_steps = (35,15,45,0,50)
        self.rects = ((53,73,60,97),(38,37,15,50),(43,39,20,40),(43,39,20,40))
        self.sfx_list = (0,)
        self.sfx_time_stamp = (20,100)

    def resetAction(self):
        if "atk" in self.master.inputList:
            if  self.master.faceSide == "r":
                self.master.attack_0.beg_execute()
            else:
                self.master.attack_0_left.beg_execute()
        elif self.master.rightMoveSymbol:
            self.master.walking.beg_execute()
        elif self.master.leftMoveSymbol:
            self.master.walkingToLeft.beg_execute()
        elif self.master.timer >= self.gfx_time_stamp[-1]:
            self.master.changePosition(self.moving_steps[-1],0)
            if self.master.faceSide == "r":
                self.master.standing.beg_execute()
            else:
                self.master.standingToLeft.beg_execute()
        else:
            return False

        return True                

    def changeFaceSides(self):
        self.frames = [pygame.transform.flip(image,True,False) for image in self.frames]

        self.moving_steps = (-35,-15,-45,0,-50)
        self.pic_loc_rectify = (64,57,87,87)
        self.rect = ((23,73,60,97),(151,37,15,50),(141,39,20,40),(141,39,20,40))

        return self


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

    def resetAction(self):
        if self.master.inputList:
            if "atk" in self.master.inputList:
                if  self.master.faceSide == "r":
                    self.master.attack_0.beg_execute()
                else:
                    self.master.attack_0_left.beg_execute()

        elif self.master.rightMoveSymbol and self.master.leftMoveSymbol:
            if self.master.faceSide == "r":
                self.master.standing.beg_execute()
            else:
                self.master.standingToLeft.beg_execute()

        elif self.master.rightMoveSymbol:
            if self.master.faceSide == "r":#向右前进
                if self.master.currentAction != self.master.walking:

                    self.master.walking.beg_execute()
                else:
                    return False
                
            """else:#向右后退
                if self.master.currentAction != self.master.retreat:
                    pass"""
        elif self.master.leftMoveSymbol:
            if self.master.faceSide == "l":#向左前进
                if self.master.currentAction != self.master.walkingToLeft:
                    self.master.walkingToLeft.beg_execute()
                else:
                    return False
            """else:#向左后退
                if self.master.currentAction != self.master.retreatToLeft:
                    pass"""
        
        elif self.master.faceSide == "r":
            self.master.standing.beg_execute()
        elif self.master.faceSide == "l":
            self.master.standingToLeft.beg_execute()

        return True

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
        self.master.timer = 0
        self.master.inputList.clear()
        self.master.currentAction = self
        self.vision = self.frames[self.frame_list[0]]
        self.master.setRect(self.rects[0])
        self.master.changePosition(self.moving_steps[0],0)
        self.locatedPicLoc(self.pic_loc_rectify[0])
        self.init()

    def update(self):
        if self.resetAction():
            return 0

        self.master.timer += 1
        
        if self.master.timer >= self.gfx_time_stamp[-1]:
            self.master.timer = 0
            self.currentFrame = 0
            self.vision = self.frames[self.frame_list[0]]
            self.master.changePosition(self.moving_steps[0],0)
            self.master.setRect(self.rects[0])
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

        self.currentFrame = 0

        self.coerciveActingFrame = 0
        self.load_constant()

    def changeFaceSides(self):
        self.frames = [pygame.transform.flip(image,True,False) for image in self.frames]

        self.pic_loc_rectify = (32,)
        self.rects = ((16,28,40,120),)
        return self

    def load_constant(self):
        self.frames = tools.getFrames("Character","Nacy","act_Standing")
        self.sfxs = ()
        self.picSize = (70,200)
        self.picLoc = (0,0)
        
        self.frame_list = (0,1)
        self.gfx_time_stamp = (70,140)
        self.pic_loc_rectify = (38,)
        self.moving_steps = (0,)
        self.rects = ((14,28,40,120),)
        self.sfx_list = ()
        self.sfx_time_stamp = ()

    def locatedPicLoc(self,rectify):
        self.picLoc = (self.master.loc[0] - rectify , self.master.loc[1] - 200)
       
    def beg_execute(self):
        self.master.currentAction = self
        self.master.timer = 0
        self.master.inputList.clear()

        self.currentFrame = 0
        self.currentSFXFrame = 0

        self.vision = self.frames[self.frame_list[0]]
        self.master.setRect(self.rects[0])
        self.locatedPicLoc(self.pic_loc_rectify[0])
        
        #self.master.setRect(self.picLoc[0],self.picLoc[1],self.picSize[0],self.picSize[1])

    def resetAction(self):
        if self.master.inputList:
            if "atk" in self.master.inputList:
                if  self.master.faceSide == "r":
                    self.master.attack_0.beg_execute()
                else:
                    self.master.attack_0_left.beg_execute()

        elif self.master.rightMoveSymbol == self.master.leftMoveSymbol:
            #如果左与右都被按下或者都被放开，执行站立姿势，按鼠标分配左右
            if self.master.currentAction != self.master.standing \
            and self.master.faceSide == "r":
                self.master.standing.beg_execute()
            elif self.master.currentAction == self.master.standing \
            and self.master.faceSide == "l":
                self.master.standingToLeft.beg_execute()

        elif self.master.rightMoveSymbol:
            if self.master.faceSide == "r":#向右前进
                if self.master.currentAction != self.master.walking:

                    self.master.walking.beg_execute()
                else:
                    return False
                
            """else:#向右后退
                if self.master.currentAction != self.master.retreat:
                    pass"""
        
        elif self.master.leftMoveSymbol:
            if self.master.faceSide == "l":#向左前进
                if self.master.currentAction != self.master.walkingToLeft:
                    self.master.walkingToLeft.beg_execute()
                else:
                    return False
            """else:#向左后退
                if self.master.currentAction != self.master.retreatToLeft:
                    pass"""

        else:
            return False

        return True

    def update(self):
        self.master.timer += 1
        if self.resetAction():
            return 0

        elif self.master.timer >= self.gfx_time_stamp[-1]:
            self.master.timer = 0
            self.currentFrame = 0
            self.vision = self.frames[self.frame_list[self.currentFrame]]

        elif self.master.timer >= self.gfx_time_stamp[self.currentFrame]:
            self.currentFrame += 1
            self.vision = self.frames[self.frame_list[self.currentFrame]]