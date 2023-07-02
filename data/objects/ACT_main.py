import pygame
from data.objects import ACT_player,ACT_UI,ACT_NPC
from data import global_environment as GE,setting

class ACTModule:
    def __init__(self):
        self.activeSituation = True
        self.interactive_obj_list = pygame.sprite.Group()
        self.current_interactive_obj = ACT_NPC.NPC_noMod()
        self.npc_list = pygame.sprite.Group()
        self.pre_player_x_loc = 0
    
    def setPlayer(self,loc):
        self.player = ACT_player.Player(loc)
        self.player.setRect((50,100,100,200))

    def setBottomUI(self,loc, size, book):
        self.bottomUI = ACT_UI.bottomUI(loc, size, self,open(book,'r',encoding='UTF-8'))

    def controller(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                match pygame.key.name(event.key):
                    case setting.left:
                        self.player.leftMoveSymbol = True
                        
                    case setting.right:
                        self.player.rightMoveSymbol = True
                    
                    case setting.shift:
                        self.player.shiftSymbol = True

                    case setting.interact:
                        GE.eventList.append("interact")
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
                        print("currentAction",self.player.currentAction)
                        
                        #print("word_0",self.bottomUI.wordsList[0].colorGradientSym)
                        #print("word_float",len(self.bottomUI.floatingWordsList))
                        GE.controller = GE.escMenu.controller
                        GE.manager = GE.escMenu
            elif event.type == pygame.MOUSEBUTTONDOWN:
                match event.button:
                    case 1 :
                        self.player.pushing_input("atk")
                    case 3:
                        self.player.defenceSymbol = True
                        self.player.pushing_input("def")
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
        if self.pre_player_x_loc != self.player.loc[0]:
            self.pre_player_x_loc = self.player.loc[0]
            temp = pygame.sprite.spritecollideany(self.player,self.interactive_obj_list)
            if temp != self.current_interactive_obj:
                self.current_interactive_obj.activeSituation = False
            if temp:
                self.current_interactive_obj = temp
                self.current_interactive_obj.activeSituation = True
        self.interactive_obj_list.update()
        self.npc_list.update()
        self.player.update()
        self.bottomUI.update()
        GE.camera.draw(self.player.redPoint, self.player.loc)
        if "interact" in GE.eventList:
            GE.eventList.remove("interact")

    def animate(self):
        self.bottomUI.animate()


