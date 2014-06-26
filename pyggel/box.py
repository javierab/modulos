#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Requisitos SW:
# pygame  
# pyggel
# pyopengl
# python

import sys
import pygame
from OpenGL import *
import pyggel
from pyggel import *
import math
from Module import *

################################
########## Clase Draw ##########
# Genera camara, luz, espacios, lee el input, crea modulos y renderiza.
# Permite movimientos de la camara con el mouse
################################


class Draw:
    def __init__(self):
        self.initialise()
        self.setupValues()
        self.loadModels()
        

    def initialise(self):
        #generar pantalla
        pyggel.init(screen_size=(1600,1200))
        #crear escena
        self.scene = pyggel.scene.Scene()
        #titulo de la ventana
        pyggel.view.set_title("Cubos")
        #crear la luz
        self.light = pyggel.light.Light((0,10,10),
                          (0.5,0.5,0.5,1),#ambient color
                          (1,1,1,1),#diffuse color
                          (50,50,50,10),#specular
                          (0,0,0),#spot position
                          True) #directional, not a spot light                          
        self.scene.add_light(self.light)
        #crear camara
        self.camera = pyggel.camera.LookAtCamera((0,0,0),distance=7, rotation=(-17,237,0))
        #pygel handler
        self.event_handler = pyggel.event.Handler()


    def setupValues(self):
	#por si extendemos la funcionalidades
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
        self.cubes = []


    #la clase importante que hace los modelos.
    def loadModels(self):

	self.texture_sky = pyggel.data.Texture("data/sky.jpg")
	self.texture_ground = pyggel.data.Texture("data/ground.jpg")
	#cubo que se comporta como la tierra.
	plane = pyggel.geometry.Cube(100, pos=(3.0,-50.0,0.0), rotation=(0,0,0), texture = self.texture_ground, colorize=(0.5,0.5,0.5))
	self.scene.add_3d(plane)
	#cielo celeste.
        self.skyball = pyggel.geometry.Skyball(self.texture_sky)
        self.scene.add_skyDraw(self.skyball)
        #cubos desde el archivo.
	f = file("test.txt", 'r')
	#leo el archivo linea a linea
	self.b = True
	for line in f:
		#lo parseo y creo el nuevo módulo
		self.splitInput = line.split("\t")
		print "nuevito:"
		print self.splitInput
		if self.b:
			self.module = Module(self.splitInput, percentage = 100, state="disponible", visible=True)
			self.b = False
		else:
			self.module = Module(self.splitInput, percentage = 100, state="ocupado", visible=True)
			self.b = True
		self.scene.add_3d(self.module)
	f.close


    def rotateCamera(self,rotation):
        x,y = rotation
        self.camera.rotx += x
        self.camera.roty += y
	print "rotation:"
	print self.camera.rotx
	print self.camera.roty
	print "distance:"
	print self.camera.distance


    def processInput(self):
        #rotar con el boton izquierdo
        rotx=0; roty=0
        if self.mousebutton == self.leftmousebutton and self.mousedown and self.mouseMoveX:
            roty = -0.5*self.mouseMoveX;
        if self.mousebutton == self.leftmousebutton and self.mousedown and self.mouseMoveY:
            rotx = -0.5*self.mouseMoveY;
        self.rotateCamera((rotx,roty))
        #mover la distancia con dos botones del mouse
        if self.twomousebuttons and self.mouseMoveY:
            self.camera.distance += 0.05*self.mouseMoveY                      
        

    def getInput(self):
        self.mousemoveX=None; self.mouseMoveY = None
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        self.mouseMoveX, self.mouseMoveY = pygame.mouse.get_rel()
        self.events.update()
        if self.events.quit or K_ESCAPE in self.events.keyboard.hit: 
           pyggel.quit() 
           sys.exit(0)
        #1 boton apretado
        if len(self.events.mouse.held)==2:
            self.mousebutton = self.events.mouse.held[0]
            self.mousedown = True
        else:
            self.mousebutton = None
            self.mousedown = False
        #2 botones apretados
        if len(self.events.mouse.held)==4:
            self.twomousebuttons = True
        else:
            self.twomousebuttons = False
        

    def run(self):
        while 1:
 
            self.clock.tick(60)
            self.getInput()
            self.processInput()
            pyggel.view.clear_screen()
	    #renderizar la imagen
            self.mouse_over_object = self.scene.render(self.camera)
            #intercambiar buffer
            pyggel.view.refresh_screen()


########################################main
if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except:
        pass
    Draw = Draw()
    Draw.run()



########################################clase para los modulos


