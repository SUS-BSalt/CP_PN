import sys
import pygame as PG
PG.mixer.pre_init(44100, 16, 2, 4096)
PG.init()
PG.event.set_allowed([PG.QUIT, PG.KEYDOWN, PG.KEYUP, PG.MOUSEBUTTONDOWN, PG.WINDOWRESIZED])
from data.main_game import MainGame

#我将注释写在其描述对象的下一行或，描述代码块的注释在其起始条件语句同缩进的代码块尾，也就是说每行注释描述的都是它上面的代码

cp_pN = MainGame()
from data.levels import opening_menu

cp_pN.runningStart()
PG.quit()
sys.exit()