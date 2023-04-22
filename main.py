import sys
import pygame as PG
PG.mixer.pre_init(44100, 16, 2, 4096)
PG.init()
PG.event.set_allowed([PG.QUIT, PG.KEYDOWN, PG.KEYUP, PG.MOUSEBUTTONDOWN, PG.WINDOWRESIZED])
from data.main_game import MainGame

cp_pN = MainGame()
from data.levels import opening_menu

cp_pN.runningStart()
PG.quit()
sys.exit()