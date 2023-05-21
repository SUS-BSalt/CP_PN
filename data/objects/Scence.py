import pygame
from data import global_environment as GE


class Scence:
    def __init__(self,size):
        self.size = size
        self.objList = []
        self.tempCameraLocContainer = (0,0)
        self.activeSituation = True
        self.collisionObjGroup = pygame.sprite.Group()
        self.interactiveObjGroup = pygame.sprite.Group()
    def init(self,cameraLoc):
        for obj in self.objList:
            obj.init(cameraLoc)

    def appendCollisionObj(self,x, y, width, height):
        self.collisionObjGroup.add(Collider(x, y, width, height))

    def collisionDetection(self,sprite) :
        collider = pygame.sprite.spritecollideany(sprite,self.collisionObjGroup)
        return collider

    
    def appendPlane(self,loc,size,vision,movingSpeed):
        plane = Plane([loc[0],self.size[1] - loc[1] - size[1]],size,vision,movingSpeed)
        print("loc",plane.loc)
        self.objList.append(plane)
    
    def appendPerspective(self,loc,size,flag,vision,movingspeed):
        Perspective = PerspectiveObject([loc[0],self.size[1] - loc[1] - size[1]],size,flag,vision,movingspeed)
        self.objList.append(Perspective)

    def update_vision(self):
        #画面出现跳闪的一个原因便是：只有部分的obj完成更新时，camera的位置改变了，导致之后的obj根据新的loc进行更新
        # 故必须用一个新容器来把传入的loc固定住，因为python语言的特性，传入给函数的值永远是其指针，不能自行控制，真不方便！
        
        #顺带一提，另一个原因是画面没更新完毕时就开始了新的绘制，这个问题可以简单的把两个任务强制拉到一个线程里进行来解决
        #但是我希望能找到一个优雅的方法处理它,2023.3.22
        if self.tempCameraLocContainer != GE.camera.loc:
            self.tempCameraLocContainer = tuple(GE.camera.loc)
            for obj in self.objList:
                obj.update(self.tempCameraLocContainer)
        
    def update(self):
        for obj in self.objList:
            GE.camera.draw(obj.vision,obj.loc)
    def animate(self):
        for obj in self.objList:
            obj.animate()


class Plane:
    def __init__(self,loc,size,vision,movingSpeed):
        self.loc = loc
        self.org_loc = tuple(loc)
        self.size = size
        self.vision = vision
        self.movingSpeed = movingSpeed
        """摄像机每移动x个像素，该物体移动x*movingSpeed个像素"""

    def init(self,cameraLoc):
        pass

    def draw(self):
        GE.camera.draw(self.vision,self.loc)
        
    def animate(self):
        pass
    def update(self,cameraLoc):
        self.loc[0] = (cameraLoc[0]*(1-self.movingSpeed)) + self.org_loc[0]


class PerspectiveObject:
    def __init__(self,loc,size,flag,vision,movingspeed):
        self.loc = loc
        self.org_loc = tuple(loc)
        self.size = size
        self.movingSpeed = movingspeed
     
        self.scaleIndex = 1
        self.vision = vision
        self.org_vision = vision
        self.blitLoc = [0,0]

        #复杂的计算，所需的参数
        self.mut_0 = self.loc[0]+640
        """这里的640指的是摄像机一半的尺寸"""
        self.mut_1 = self.loc[1]+1280

        if flag == "right":
            self.blitLoc = self.loc
            self.update = self.updateMethodForRight
            self.init = self.initRightSide
        elif flag == "left":
            self.blitLoc = (self.loc[0] - self.size[0],self.loc[1] - self.size[1])
            self.update = self.updateMethodForLeft
            self.init = self.initLeftSide
        self.init(GE.camera.loc)

    def init(self,cameraLoc):
        pass
    def initRightSide(self,cameraLoc):
        if cameraLoc[0] < self.loc[0] - 640:
            self.vision = pygame.transform.scale(self.org_vision, (0,self.size[1]))
        elif cameraLoc[0] > self.loc[0] + self.size[0]:
            self.vision = self.org_vision
        else:
            self.updateMethodForRight(cameraLoc)
    def initLeftSide(self,cameraLoc):
        if cameraLoc[0] < self.loc[0] - self.mut_1:
            self.vision = self.org_vision 
        elif cameraLoc[0] > self.loc[0] - 640:
            self.vision = pygame.transform.scale(self.org_vision, (0,self.size[1]))
        else:
            self.updateMethodForLeft(cameraLoc)
    
    
    def draw(self):
        GE.camera.draw(self.vision,self.blitLoc)
    
    def animate(self):
        pass
    
    
    def update(self,cameraLoc):
        pass
    
    def updateMethodForRight(self,cameraLoc):
        #引入一个depth的概念，意义为这个片面垂直于镜头，它最远点到摄像机平面的距离
        #depth实际上与图片宽度无关，图片宽度是假设当片面刚好消失在镜头里时，片面通过透视投影到摄像机平面的宽度
        #当摄像机的焦距等于摄像机屏幕宽度一半时，图片的宽度在数值上等于这个depth
        #为了简化计算，以下所有计算都是基于摄像机的焦距等于摄像机屏幕宽度一半，也就是图片的宽度在数值上等于这个depth的情况下进行的
        #当摄像机位置减去物体位置大于等于depth（图片宽度）时，图像不需要拉伸，缩放比为100%
        #当摄像机位置减去物体位置小于等于摄像机宽度一半的负数，也就是平面中心正好怼在物体位置上时，片面就看不见了，所以缩放比为0%
        #故缩放比为摄像机位置减去物体位置的数值结果在depth到摄像机宽度一半的负数之间的差值
        self.loc[0] = cameraLoc[0]*(1-self.movingSpeed) + self.org_loc[0]
        if cameraLoc[0] < self.loc[0] - 640 or cameraLoc[0] > self.loc[0] + self.size[0]:
            #这里的640指的是摄像机尺寸的一半
            #若摄像机位置在上述条件之内时，物体不可能出现在场景中，所以不用更新它
            return
        self.scaleIndex=(cameraLoc[0]-self.loc[0] + 640)/self.mut_0
        self.vision = pygame.transform.scale(self.org_vision, (self.size[0]*self.scaleIndex,self.size[1]))
        

    def updateMethodForLeft(self,cameraLoc):
        self.loc[0] = cameraLoc[0]*(1-self.movingSpeed) + self.org_loc[0]
        if self.loc[0] - cameraLoc[0] > self.mut_1 or self.loc[0] - cameraLoc[0] < 640:
            return
        self.scaleIndex=(self.loc[0] - cameraLoc[0] - 640)/self.mut_0
        self.vision = pygame.transform.scale(self.org_vision, (self.size[0]*self.scaleIndex,self.size[1]))
        self.blitLoc = (self.loc[0] - self.size[0]*self.scaleIndex,self.loc[1])

class Collider(pygame.sprite.Sprite):
    """Invisible sprites placed overtop background parts
    that can be collided with (pipes, steps, ground, etc."""
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height)).convert()
        #self.image.fill(c.RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


