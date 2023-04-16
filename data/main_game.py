import pygame
import threading
import time
from data import setting
from data import global_environment as GE

class MainGame:
    def __init__(self):
        GE.GV.set("game_run",True)
        #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓fps相关变量与计时器↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        self.fps_Rectify_Frequency = 50
        """每多少帧修正一次"""
        self.fps_Rectify_TimeCell = self.fps_Rectify_Frequency/setting.logicLoopFps
        """每两次修正之间的理想间隔时长"""
        self.fps_Span = 1/setting.logicLoopFps
        """每帧持续时长"""
        self.fps_Span_Rectify = self.fps_Span
        """每帧持续时长的修正，维持fps用"""
        self.fps_Span_Rectify_var = self.fps_Rectify_TimeCell /self.fps_Rectify_Frequency *0.009
        """每次修正时的修正量"""
        
        self.fps_Rectify_Timer = 0
        """用于修正帧率的计时器"""
        self.beg_FrameTimer = 0
        """每帧执行开始时的计时器"""
        self.end_FrameTimer = 0
        """每帧执行结束时的计时器"""
        self.differ_FrameTimer = 0
        """记录每帧实际运行的时长的计时器"""
        self.fps_Span_Rectify_Timer = 0
        """用于修正帧率用的计时器，记录上一次执行修正时的时间"""
        self.fps_Span_Rectify_TimeGap = 0
        """用于修正帧率用的计时器，记录两次修正之间的时间差"""
        #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑fps相关变量与计时器↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

        #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓update相关变量（开关）↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        self.OBJ_updating = False
        self.OBJ_drawing = False
  

    def update(self):
        while GE.GV.get("game_run"):
            
            #循环本体
            #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓维持FPS的第一块代码↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
            self.beg_FrameTimer = time.perf_counter()
            #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑维持FPS的第一块代码↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
            #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓游戏逻辑↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
            GE.controller()
            #处理输入信号
            GE.camera.createDrawQuest()
            #创建绘制任务队列
            GE.manager.update()
            #更新游戏
            #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑游戏逻辑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
            #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓维持FPS的第二块代码↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
            self.end_FrameTimer = time.perf_counter()
            self.differ_FrameTimer = self.end_FrameTimer - self.beg_FrameTimer
            if self.differ_FrameTimer > self.fps_Span_Rectify:
                print("Low!")
                continue
            self.fps_Rectify()
            time.sleep(self.fps_Span_Rectify - self.differ_FrameTimer)
            #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑维持FPS的第二块代码↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


    def drawLoop(self):
        """#画面循环，基本只负责绘制可见对象"""
        """还有更新场景2023.4.7"""
        self.drawLoopclock = pygame.time.Clock()

        while GE.GV.get("game_run"):
            #0循环本体
            self.drawLoopclock.tick(setting.drawLoopFps)
            #保持循环的fps
            GE.camera.executeDrawQuest()#执行绘制任务
            GE.screen.blit(pygame.transform.scale(GE.camera.cameraShot,setting.windowsize),GE.camera.cameraLocRectify)
            #将画面缩放到窗口大小
            pygame.display.update()
            #更新画面


    def animateLoop(self):
        self.animateLoopclock = pygame.time.Clock()
        while GE.GV.get("game_run"):
            self.animateLoopclock.tick(setting.animateLoopFps)
            GE.manager.animate()


    def fps_Rectify(self):
        """修正每帧休眠的时间，以尽可能的减少fps波动，这个维持fps的方法的前提是，电脑性能比游戏所需性能好。"""
        self.fps_Rectify_Timer += 1
        if  self.fps_Rectify_Timer == self.fps_Rectify_Frequency:
            self.fps_Span_Rectify_TimeGap = self.beg_FrameTimer - self.fps_Span_Rectify_Timer
            if   self.fps_Span_Rectify_TimeGap > (self.fps_Rectify_TimeCell*1.1):
                 self.fps_Span_Rectify -= (self.fps_Span_Rectify_var*10)
                 #print(self.fps_Span_Rectify)

            elif self.fps_Span_Rectify_TimeGap > (self.fps_Rectify_TimeCell*1.01):
                 self.fps_Span_Rectify -= self.fps_Span_Rectify_var
                 #print(self.fps_Span_Rectify)
    
            elif self.fps_Span_Rectify_TimeGap < (self.fps_Rectify_TimeCell*0.9):
                 self.fps_Span_Rectify += (self.fps_Span_Rectify_var*10)
                 #print(self.fps_Span_Rectify)

            elif self.fps_Span_Rectify_TimeGap <  (self.fps_Rectify_TimeCell*0.99):
                 self.fps_Span_Rectify += self.fps_Span_Rectify_var
                 #print(self.fps_Span_Rectify)
            #print(tiemGap)
            print(round(1/(self.fps_Span_Rectify_TimeGap)*self.fps_Rectify_Frequency),"FPS")
            #print(self.differ_FrameTimer)
            self.fps_Span_Rectify_Timer = self.beg_FrameTimer
            self.fps_Rectify_Timer = 0


    def runningStart(self):
        self.thread_drawLoop = threading.Thread(target = self.drawLoop)
        self.thread_drawLoop.start()
        
        self.thread_animateLoop = threading.Thread(target = self.animateLoop)
        self.thread_animateLoop.start()
        
        self.update()