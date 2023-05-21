import pygame as PG
import os
import json
from data import global_environment as GE
from data.objects import Scence

def getFrames(*path) -> list:
    truePath = "resources/GFX"
    for value in path:
        truePath = truePath + "/" + "%s" % value
    temp = []
    for frame in sorted(os.listdir(truePath)):
        temp.append(PG.image.load(truePath+"/"+frame).convert_alpha())
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
                GE.GV.set('game_run',False)
        elif event.type == PG.WINDOWRESIZED:
            #变化windowsize
            GE.camera.resetWindow(event)

def load_all_sfx(directory, accept=('.wav','.mpe','.ogg','.mdi')):
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = PG.mixer.Sound(os.path.join(directory, fx))
    return effects

def load_scence(jsonpath,gfxpath,scence_size):
    scence = Scence.Scence(scence_size,GE.camera.loc)
    dir = json.load(open(jsonpath))
    for i in dir:
        match dir[i][0]:
            case 0 :
                scence.appendPlane(dir[i][1],dir[i][2],getImage("Scence",gfxpath,i),dir[i][3])
            case 1 :
                scence.appendPerspective(dir[i][1],dir[i][2],dir[i][3],getImage("Scence",gfxpath,i),dir[i][4])
            case 2 :
                scence.appendCollisionObj(dir[i][1],dir[i][2],dir[i][3],dir[i][4])
    return scence