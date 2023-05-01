from data import global_environment as GE
from data.objects import UIObj
from data import setting,tools
import pygame as PG
import os,sys

class Manager_OpeningMenu:
    def __init__(self):
        self.activeSituation = True
        self.followingEventList = []
        self.moduleList = []
        self.controller = None

        self.cover_mask_yloc = 720
        """#转场黑幕遮罩的y坐标位置"""
        self.cover_mask = tools.getImage("UI","mask_0.png")
        self.cover_mask = PG.transform.rotate(self.cover_mask,180)
        
    
    def update(self):
        for checker in self.followingEventList:
            checker()
        for module in self.moduleList:
                if module.activeSituation == True:
                    module.update()
    def animate(self):
        for module in self.moduleList:
                if module.activeSituation == True:
                    module.animate()
        pass

    def start(self):
        self.openingMenu = create_OpingMenu()
        self.moduleList.append(self.openingMenu)
        self.openingMenu.activeSituation = True
        GE.controller = self.openingMenu.controller
        self.controller = self.openingMenu.controller
        self.followingEventList.append(self.check_jump_to_Level_0)

    def check_jump_to_Level_0(self):
        if "jump_to_Level_0" in GE.eventList:
            GE.eventList.remove("jump_to_Level_0")
            #从事件列表中移除此事件
            self.openingMenu.activeSituation = False
            #关闭UI模组
            GE.controller = tools.controller_noMode
            #切换控制器到空控制器，以此剥夺玩家控制权
            self.followingEventList.append(self.change_stage)
            #添加转场函数进检查队列

    def change_stage(self):
        #转场效果
        self.cover_mask_yloc -= 10
        self.openingMenu.activeMenu.loc[1] -= 10

        GE.camera.draw_UI(self.openingMenu.activeMenu.vision,self.openingMenu.activeMenu.loc)
        for button in self.openingMenu.activeMenu.buttonList:
            GE.camera.draw_UI(button.vision,tools.returnAbsLoc(self.openingMenu.activeMenu.loc,button.loc))
        GE.camera.draw_UI(self.cover_mask,(0,self.cover_mask_yloc-75))
        GE.camera.draw_UI(GE.camera.black,(0,self.cover_mask_yloc))

        if self.cover_mask_yloc <= 0 :
            from data.levels import Level_0
            



def create_OpingMenu():
    openingMenu = UIObj.UIModule()
    #开始菜单
    startMenu = UIObj.Menu(activeSituation=True, loc = [0,0],size=[1280,720])
    startMenu.vision = PG.image.load(GE.GFX_UI['StartMenu'])
    openingMenu.menuList.append(startMenu)
    openingMenu.activeMenu = startMenu

    def startMethod():
        GE.eventList.append("jump_to_Level_0")
        

    startMenu.appendButtonToMenu(startMethod,[100,150],[100,50],
                                    GE.UIfont_01.render(setting.START,False,(0,0,0)),
                                    GE.UIfont_02.render(setting.START,False,(0,0,0))
                                )
    def loadMethod():
        openingMenu.activeMenu = loadMenu
    startMenu.appendButtonToMenu(loadMethod,[100,300],[100,50],
                                        GE.UIfont_01.render(setting.LOAD,False,(0,0,0)),
                                        GE.UIfont_02.render(setting.LOAD,False,(0,0,0))
                                )
    def optionMethod():
        openingMenu.activeMenu = optionMenu
    startMenu.appendButtonToMenu(optionMethod,[100,450],[100,50],
                                        GE.UIfont_01.render(setting.OPTION,False,(0,0,0)),
                                        GE.UIfont_02.render(setting.OPTION,False,(0,0,0)))
    def confirmMenuMethod():
        openingMenu.activeMenu = confirmMenu
    startMenu.appendButtonToMenu(confirmMenuMethod,[100,600],[100,50],
                                        GE.UIfont_01.render(setting.QUIT,False,(0,0,0)),
                                        GE.UIfont_02.render(setting.QUIT,False,(0,0,0)))

    #开始菜单
    def backToStartMenuMethod():
        openingMenu.activeMenu = startMenu

    def exitMethod():
        GE.GV.set('game_run',False)

    def noneMethod():
        return 0
    #确认退出菜单
    confirmMenu = UIObj.Menu(activeSituation=False)
    confirmMenu.vision = PG.image.load(GE.GFX_UI['StartMenu'])
    confirmMenu.masterMenu = startMenu
    openingMenu.menuList.append(confirmMenu)

    confirmMenu.appendButtonToMenu(exitMethod,[500,350],[100,50],
                                        GE.UIfont_01.render("是",False,(0,0,0)),
                                        GE.UIfont_02.render("是",False,(0,0,0))
                                    )

    confirmMenu.appendButtonToMenu(backToStartMenuMethod,[700,350],[100,50],
                                        GE.UIfont_01.render("否",False,(0,0,0)),
                                        GE.UIfont_02.render("否",False,(0,0,0))
                                    )
    confirmMenu.appendButtonToMenu(noneMethod,[400,250],[100,50],
                                        GE.UIfont_01.render("确认退出到桌面？",False,(0,0,0)),
                                        GE.UIfont_01.render("确认退出到桌面？",False,(0,0,0))
                                    )
    #确认退出菜单#

    #载入菜单
    loadMenu = UIObj.Menu(activeSituation=False)
    openingMenu.menuList.append(loadMenu)
    loadMenu.vision = PG.image.load(GE.GFX_UI['StartMenu'])
    loadMenu.masterMenu = startMenu
    loadMenu.appendButtonToMenu(backToStartMenuMethod,[100,600],[100,50],
                                        GE.UIfont_01.render("返回",False,(0,0,0)),
                                        GE.UIfont_02.render("返回",False,(0,0,0)),
                                    )
    #载入菜单#

    #设置菜单
    optionMenu = UIObj.Menu(activeSituation=False)
    openingMenu.menuList.append(loadMenu)
    optionMenu.vision = PG.image.load(GE.GFX_UI['StartMenu'])
    optionMenu.masterMenu = startMenu
    optionMenu.appendButtonToMenu(backToStartMenuMethod,[100,600],[100,50],
                                        GE.UIfont_01.render("返回",False,(0,0,0)),
                                        GE.UIfont_02.render("返回",False,(0,0,0)),
                                    )
    #设置菜单#
    return openingMenu



manager = Manager_OpeningMenu()
GE.manager = manager
GE.level_manager = manager
manager.start()




escMenuModule = UIObj.UIModule()
GE.escMenu = escMenuModule

#esc菜单
escMenu = UIObj.Menu(activeSituation=True,loc=[0,0], size=[1280,720])
escMenu.vision = PG.image.load(GE.GFX_UI['StartMenu'])
escMenuModule.menuList.append(escMenu)
escMenuModule.activeMenu = escMenu
print(escMenuModule.activeMenu.loc)

def backMethod():
    GE.controller = GE.level_manager.controller
    GE.level_manager.activeSituation = True
    GE.manager = GE.level_manager

escMenu.appendButtonToMenu(backMethod,[100,450],[150,80],
                                    GE.UIfont_01.render("返回游戏",False,(0,0,0)),
                                    GE.UIfont_02.render("返回游戏",False,(0,0,0))
                                )

def backToOpeningMenu():
    #@Todo保存游戏
    GE.GV.set("gameRun",False)
    os.execl(sys.executable,sys.executable,"./main.py")
    
escMenu.appendButtonToMenu(backToOpeningMenu,[100,600],[150,80],
                                    GE.UIfont_01.render("返回主菜单",False,(0,0,0)),
                                    GE.UIfont_02.render("返回主菜单",False,(0,0,0))
                                )
    