import sys
import pygame
from OpenGL import *
import pyggel
from pyggel import *
import math
from Module import *


##################################
########## Clase Module ##########
# Renderiza figura dados lista de vertices, porcentaje, estado y visibilidad.
##################################

class Module(object):
    def __init__(self, vertex, percentage = 100, state="D", visible=True):
        pyggel.view.require_init()
	#componentes de la clase
	self.id = vertex[0]
	self.state = state #vertex[25]
	self.percentage = percentage #vertex[26]

	#TODO: que solo renderice si esta visible. campo editable con setVisibility()
        self.visible = True #vertex[27]

        self.v1 = [float(vertex[1])/100.0,float(vertex[3])/100.0,float(vertex[2])/100.0] #000
	self.v2 = [float(vertex[4])/100.0,float(vertex[6])/100.0,float(vertex[5])/100.0] #100
	self.v3 = [float(vertex[7])/100.0,float(vertex[9])/100.0,float(vertex[8])/100.0] #101
	self.v4 = [float(vertex[10])/100.0,float(vertex[12])/100.0,float(vertex[11])/100.0] #001
	self.v5 = [float(vertex[13])/100.0,float(vertex[15])/100.0,float(vertex[14])/100.0] #010
	self.v6 = [float(vertex[16])/100.0,float(vertex[18])/100.0,float(vertex[17])/100.0] #110
	self.v7 = [float(vertex[19])/100.0,float(vertex[21])/100.0,float(vertex[20])/100.0] #111
	self.v8 = [float(vertex[22])/100.0,float(vertex[24])/100.0,float(vertex[23])/100.0] #011

        if "D" in state:
            texture = pyggel.data.Texture("data/green2.jpg")
        elif "O" in state:
            texture = pyggel.data.Texture("data/red2.jpg")
        else:
            texture = pyggel.data.Texture("data/blue2.jpg")

        self.texture = texture

        self.corners = (self.v1,#topleftfront
                      self.v2,#toprightfront
                      self.v3,#bottomrightfront
                      self.v4,#bottomleftfront
                      self.v5,#topleftback
                      self.v6,#toprightback
                      self.v7,#bottomrightback
                      self.v8)#bottomleftback

        self.sides = ((7,4,0,3, 2, 2, 5),#left
                      (2,1,5,6, 3, 4, 4),#right
                      (7,3,2,6, 5, 0, 3),#top
                      (0,4,5,1, 4, 5, 2),#bottom
                      (3,0,1,2, 0, 1, 0),#front
                      (6,5,4,7, 1, 3, 1))#back
        self.normals = ((0, 0, 1), #front
                        (0, 0, -1), #back
                        (0, -1, 0), #top
                        (0, 1, 0), #bottom
                        (1, 0, 0), #right
                        (-1, 0, 0)) #left

        self.split_coords = ((2,2),#top
                             (0,1),#back
                             (1,1),#left
                             (2,1),#front
                             (3,1),#right
                             (2,0))#bottom


        self.scale = 1

        self.display_list = data.DisplayList()


        self.pickable = True


        self._compile()

    def get_dimensions(self):
        """Return a tuple of the size of the cube - to be used by the quad tree and collision testing"""
        return 0

    def get_pos(self):
        """Return the position of the quad"""
        return v1

    def _compile(self):
        """Compile the cube's rendering into a data.DisplayList"""
        self.display_list.begin()

        ox = .25
        oy = .33
        last_tex = None
        for i in self.sides:
            ix = 0
            x, y = self.split_coords[i[5]]
            x *= ox
            y *= oy
            coords = ((x+ox, y+oy), (x+ox, y), (x, y), (x, y+oy))

            glBegin(GL_QUADS)

            glNormal3f(*self.normals[i[6]])

            for x in i[:4]:
                glTexCoord2fv(coords[ix])
                a, b, c = self.corners[x]
                glVertex3f(a,b,c)
                ix += 1
            glEnd()
        self.display_list.end()

    def render(self, camera=None):
        glPushMatrix()
        self.texture.bind()
        self.display_list.render()
        glPopMatrix()

    def setVisibility(self, v=True):
	self.visible = v


