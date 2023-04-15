import sys
import pygame
pygame.init()
from data.main_game import MainGame

#我将注释写在其描述对象的下一行或，描述代码块的注释在其起始条件语句同缩进的代码块尾，也就是说每行注释描述的都是它上面的代码

cp_pN = MainGame()
import Levels.OpeningMenu

cp_pN.runningStart()
pygame.quit()
sys.exit()