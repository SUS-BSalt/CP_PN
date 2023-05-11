import pygame
from data.objects import ACT_player,ACT_UI
from data import global_environment as GE,setting

class ACTModule:
    def __init__(self):
        self.activeSituation = True

        
        self.enemyList = []
        
        self.playerBeatSymbol = False
        self.playerBeatAward = False
        self.beatSpeed = 30
        #节奏速度
        self.beatZoneStartPoint = 20
        #判定区间开始的节点
    
    def setPlayer(self,loc):
        self.player = ACT_player.Player(loc)

    def setBottomUI(self,loc, size, book):
        self.bottomUI = ACT_UI.bottomUI(loc, size, self,open(book,'r',encoding='UTF-8'))

    def controller(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                match pygame.key.name(event.key):
                    case setting.left:
                        self.player.leftMoveSymbol = True
                        self.player.inputList.append("left")
                        
                    case setting.right:
                        self.player.rightMoveSymbol = True
                        self.player.inputList.append("right")
                    
                    case setting.shift:
                        self.player.shiftSymbol = True

                    
            if event.type == pygame.KEYUP:
                match pygame.key.name(event.key):
                    case setting.left:
                        self.player.leftMoveSymbol = False

                    case setting.right:
                        self.player.rightMoveSymbol = False
                    
                    case setting.shift:
                        self.player.shiftSymbol = False

                    case "escape":
                        print("coerciveActingSymbol",self.player.coerciveActingSymbol)
                        print("playLoc",self.player.loc)
                        print("playerFaceSide",self.player.faceSide)
                        print("playRect",self.player.rect)
                        print("cameraLoc",GE.camera.loc)
                        print("mousePos",GE.camera.mousePos)
                        
                        #print("word_0",self.bottomUI.wordsList[0].colorGradientSym)
                        #print("word_float",len(self.bottomUI.floatingWordsList))
                        GE.controller = GE.escMenu.controller
                        GE.manager = GE.escMenu
            elif event.type == pygame.MOUSEBUTTONDOWN:
                match event.button:
                    case 1 :
                        self.player.inputList.append("atk")
                    case 3:
                        self.player.defenceSymbol = True
                        self.player.inputList.append("def")
            elif event.type == pygame.MOUSEBUTTONUP:
                match event.button:
                    case 3:
                        self.player.defenceSymbol = False


            elif event.type == pygame.QUIT:
                GE.GV.set('game_run',False)

            elif event.type == pygame.WINDOWRESIZED:
                #变化windowsize
                GE.camera.resetWindow(event)

    def update(self):
        for enemy in self.enemyList:
                enemy.update()
        self.player.update()
        self.bottomUI.update()
        GE.camera.draw(self.player.redPoint, self.player.loc)

    def animate(self):
        self.bottomUI.animate()