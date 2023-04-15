import pygame as PG
import global_environment as GE

class UIModule:
    def __init__(self):
        self.activeSituation = False
        self.menuList = []
        self.activeMenu = None

    def controller(self):
        GE.GV.set("click",False)
        GE.camera.getMousePos()
        for event in PG.event.get():            
            if event.type == PG.KEYUP:
                if PG.key.name(event.key) == "escape":
                    GE.GV.set("escape",True)

            elif event.type == PG.MOUSEBUTTONUP:
                GE.GV.set("click",True)
            
            elif event.type == PG.QUIT:
                GE.GV.set('gameRun',False)

            elif event.type == PG.WINDOWRESIZED:
                #变化windowsize
                GE.camera.resetWindow(event)

    def update(self):
        self.activeMenu.update()

    def animate(self):
        self.activeMenu.animate()

class Menu:
    def __init__(self,loc = [0,0], size = [0,0], activeSituation = False):
        self.activeSituation = activeSituation
        self.masterMenu = None

        self.loc = loc
        self.size = size
        self.rect = PG.Rect(self.loc,self.size)
        self.vision = None
        self.buttonList = []
        

    def update(self):
        for button in self.buttonList:
            if GE.GV.get('click'):
                if GE.camera.mousePosCheck_UI(button.rect) == True:
                    button.exec()
                    GE.GV.set('click', False)
            GE.camera.draw_UI(button.vision,button.loc)
        GE.camera.draw_UI(self.vision,self.loc)
        

    def animate(self):
        for button in self.buttonList:
            if GE.camera.mousePosCheck_UI(button.rect) == True and button.mouseActive == False:
                button.mouseActiveMethond(True)
            elif GE.camera.mousePosCheck_UI(button.rect) == False and button.mouseActive == True:
                button.mouseActiveMethond(False)

    def appendButtonToMenu(self, method,loc,size, *frameList):
        button= Button(loc=loc,size=size, method = method)
        for frame in frameList:
            button.frameList.append(frame)
        button.vision = button.frameList[0]
        self.buttonList.append(button)
        return button

class Button:
    def __init__(self,loc = [0,0], size = [0,0], method = None):
        self.mouseActive = False
        self.loc = loc
        self.size = size
        self.rect = PG.Rect(self.loc,self.size)
        self.vision = None
        self.frameList = []
        self.animationList = []
        self.method = method


    def exec(self):
        self.method()


    def mouseActiveMethond(self,situation):
        if situation:
            self.vision = self.frameList[1]
        else:
            self.vision = self.frameList[0]
