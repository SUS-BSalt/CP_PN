import pygame as PG
import os
import json
from data import global_environment as GE

def getFrames(path) -> list:
    temp = []
    for frame in sorted(os.listdir(path)):
        temp.append(PG.image.load(frame).convert_alpha())
    return temp

def getImage(*path) -> PG.Surface:
    truePath = "resources/GFX"
    for value in path:
        truePath = truePath + "/" + "%s" % value
    return PG.image.load(truePath).convert_alpha()

def returnAbsLoc(masterLoc,servertLoc):
    return (masterLoc[0]+servertLoc[0],masterLoc[1]+servertLoc[1])

def loadAssetData(prePath,*argv):
    order = "json.load(open('resources/asset.json','r',encoding='UTF-8'))"
    for value in argv:
        order = order + "[\"%s\"]" % value
    tempDict = eval(order)
    for loc in tempDict:
        tempDict[loc] = prePath + tempDict[loc]
    return tempDict

def controller_noMode():
    #一个仅限于关闭游戏或调整窗口的控制器
    for event in PG.event.get():
        if event.type == PG.QUIT:
                GE.GV.set('gameRun',False)
        elif event.type == PG.WINDOWRESIZED:
            #变化windowsize
            GE.camera.resetWindow(event)