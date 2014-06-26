#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Author
#======
#Jess Hill (Jestermon)
#jestermon.weebly.com
#jestermonster@gmail.com

#dependencies:
#=============
#pyopengl ~ http://pyopengl.sourceforge.net
#pyggel   ~ http://code.google.com/p/pyggel  
#pygame   ~ http://www.pygame.org
#psyco    ~ http://psyco.sourceforge.net  (not required, but handy to speed things up)
#python   ~ http://www.python.org

#minimum requirements
#====================
#pygame   ~ python game engine
#pyopengl ~ python opengl libraries
#python   ~ python language interpreter


import sys
import pyggel
from pyggel import *
import math

########################################box
class box:
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self):
        self.initialise()
        self.setupValues()
        self.loadModels()
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def initialise(self):
        #initialize pygel screen
        pyggel.init(screen_size=(800,600))
        #create pygel scene
        self.scene = pyggel.scene.Scene()
        #Set window title
        pyggel.view.set_title("Cubos")
        #create a pygel light
        self.light = pyggel.light.Light((0,10,10),
                          (0.5,0.5,0.5,1),#ambient color
                          (1,1,1,1),#diffuse color
                          (50,50,50,10),#specular
                          (0,0,0),#spot position
                          True) #directional, not a spot light                          
        self.scene.add_light(self.light)
        #create a pygel camera
        self.camera = pyggel.camera.LookAtCamera((0,0,0),distance=5)
        #setup pygel event handler
        self.event_handler = pyggel.event.Handler()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setupValues(self):
        self.scene.pick = True
        self.events = pyggel.event.Handler()
        self.clock = pygame.time.Clock()
        self.M3 = math3d.move_with_rotation
        self.mousedown = None
        self.mousebutton = None
        self.twomousebuttons = False
        self.mouseX = None
        self.mouseY = None
        self.mousemoveX = None
        self.mouseMoveY = None
        self.leftmousebutton = 1
        self.middlemousebutton = 2
        self.rightmousebutton = 3
        self.mousewheelup = 4
        self.mousewheeldown = 5
        self.mouse_over_object = None
        self.object_selected = None
        self.balls = []
        self.points = []
        self.pointerballs = []
        self.activebox = None
        self.prevbox = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def sphere_point(self,i,j,N,M):
        theta=math.pi*i/N
        phi=2*math.pi*j/M
        c=math.cos(math.pi/2-theta)
        return (math.cos(phi)*c, math.sin(phi)*c, math.sin(math.pi/2-theta))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def buildSpherePoints(self,N=5, M=5):
        """N is the number of latitudes, M is the number of longitudes"""
        if len(self.pointerballs): return False
        points= []
        # north pole
        points.append((0,0,1))
        points.append(self.sphere_point(1,0,N,M))
        for j in range(1,M):
            points.append(self.sphere_point(1,j,N,M))
        # middle
        for i in range(2,N):
            points.append(self.sphere_point(i,0,N,M))
            for j in range(1,M):
                    points.append(self.sphere_point(i,j,N,M))
                    l = len(points)
            l = len(points)
        # south pole
        points.append((0,0,-1))
        southpole = len(points)-1
        points.append(self.sphere_point(N-1,0,N,M))
        for j in range(1,M):
            points.append(self.sphere_point(N-1,j,N,M))
        return points

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def moveNodes(self,box):
        if not self.prevbox:return
        bx,by,bz = box.pos
        px,py,pz = self.prevbox.pos
        dx=px-bx; dy=py-by; dz=pz-bz
        for b in self.pointerballs:
            x,y,z = b.pos
            x-=dx; y-=dy; z-=dz
            b.pos = (x,y,z)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setPoints(self):
        result = self.buildSpherePoints(12,12)
        if result:
            #create nodes
            self.points = result
            for p in self.points:
                pointer_ball = pyggel.geometry.Sphere(0.1, pos=(p), texture=self.texture_green,colorize=(1,0,0,1))
                self.scene.add_3d(pointer_ball)
                self.pointerballs.append(pointer_ball)
        else:
            for box in self.balls:
            #move nodes to active box
                if box == self.activebox:
                    self.moveNodes(box)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def loadModels(self):
        self.texture_green = pyggel.data.Texture("data/green.jpg")
	self.texture_red = pyggel.data.Texture("data/red.jpg")
        box1 = pyggel.geometry.Cube(1, pos=(0.00001,0.00001,0.00001), texture=self.texture_green,colorize=(0.5,0.5,0.5))
        self.scene.add_3d(box1)
        self.skyball = pyggel.geometry.Skyball("data/brown.jpg")
        self.scene.add_skybox(self.skyball)
        #add first box into the building balls list
        self.balls.append(box1)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def rotateCamera(self,rotation):
        x,y,z = rotation
        self.camera.rotx += x
        self.camera.roty += y
        self.camera.rotz += z

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def setNodes(self,item):
        self.setPoints()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def killbox(self):
        for b in range(len(self.balls)):
            if self.balls[b] == self.activebox and b>0:
                deadbox = self.prevbox = self.activebox
                self.activebox = self.balls[0]
                self.moveNodes(self.balls[0])
                deadbox.visible=False
                self.balls.remove(deadbox)
                self.prevbox = None
                return

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def addNewbox(self,node):
        box = pyggel.geometry.Cube(1, pos=node.pos, texture=self.texture_green,colorize=(0.7,0.7,0.7))              
        self.scene.add_3d(box)
        self.balls.append(box)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def processInput(self):
        #rotate camera if right mouse button is down, and mouse is moved
        rotx=0; roty=0; rotz=0
        if self.mousebutton == self.rightmousebutton and self.mousedown and self.mouseMoveX:
            roty = -0.5*self.mouseMoveX;
        if self.mousebutton == self.rightmousebutton and self.mousedown and self.mouseMoveY:
            rotx = -0.5*self.mouseMoveY;
        self.rotateCamera((rotx,roty,rotz))
        #Move camera distance, activated by 2 mouse buttons, and mouse move up or down
        if self.twomousebuttons and self.mouseMoveY:
            self.camera.distance += 0.05*self.mouseMoveY                      
        #if an object is selected, make a new sphere
        if self.object_selected:
            for box in self.balls:
                #Move nodes to active box
                if self.object_selected == box:
                    self.setNodes(self.object_selected)
                    self.prevbox = self.activebox
                    self.activebox = box
                    self.object_selected = None
            for node in self.pointerballs:
                #grow boxw on selected node
                if node == self.object_selected:
                    self.addNewbox(self.object_selected)
                    self.object_selected = None
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getInput(self):
        self.mousemoveX=None; self.mouseMoveY = None
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        self.mouseMoveX, self.mouseMoveY = pygame.mouse.get_rel()
        self.events.update()
        if self.events.quit or K_ESCAPE in self.events.keyboard.hit: 
           pyggel.quit() 
           sys.exit(0)
        if K_DELETE in self.events.keyboard.hit:
            self.killbox()
        #if 1 mouse button is held down
        if len(self.events.mouse.held)==2:
            self.mousebutton = self.events.mouse.held[0]
            self.mousedown = True
        else:
            self.mousebutton = None
            self.mousedown = False
        #if 2 mouse buttons are held down
        if len(self.events.mouse.held)==4:
            self.twomousebuttons = True
        else:
            self.twomousebuttons = False
        #if 1 mouse button is pressed
        if len(self.events.mouse.hit)==2 and self.mouse_over_object:
            if self.events.mouse.hit[0] == 1: #if left mouse button
                self.object_selected = self.mouse_over_object
            else:
                self.object_selected = None            
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def run(self):
        while 1:
            #limit frames per second 
            self.clock.tick(60)
            #get user input
            self.getInput()
            #process user input
            self.processInput()
            #clear screen for new drawing
            pyggel.view.clear_screen()
            #render the scene... Also retrieve the picked object
            self.mouse_over_object = self.scene.render(self.camera)
            #flip the display buffer
            pyggel.view.refresh_screen()




########################################main
if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except:
        pass
    box = box()
    box.run()
