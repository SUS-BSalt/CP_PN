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
        GE.camera.draw(self.pic_0,(400,720))
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
        self.rect = pygame.Rect(rect)
        self.draw_loc_0 = (1700,552)
        self.draw_loc_1 = (1700,500)
        self.activeSituation = False
        self.dyingSym = False
        self.timer = 100
    def update(self):
        GE.camera.draw(self.pic_0,self.draw_loc_0)
        if self.activeSituation:
            GE.camera.draw(self.pic_1,self.draw_loc_1)
            if "interact" in GE.eventList:
                self.exec()
                GE.eventList.remove("interact")

    def exec(self):
        print("ccc")
        pass

