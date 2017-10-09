#!/usr/bin/python
#
# Qubit Visualisation
# Copyright (C) 2006   Robert Nowotniak <rnowotniak@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from visual import *
from visual.controls import *
import sys, math
from math import pi, sin, cos


class StateArrow(arrow):

    def __init__(self, **args):
        super(StateArrow, self).__init__(**args)
        self.__lines = curve()
        if 'pos' not in args:
            self.pos = (0, 0, 0)
        if 'shaftwidth' not in args:
            self.shaftwidth = 0.04
        if 'theta' not in args:
            object.__setattr__(self, 'theta', 0)
        if 'phi' not in args:
            object.__setattr__(self, 'phi', 0)
        self.theta = self.theta
        self.label = label(pos=self.axis, xoffset=15, yoffset=5, border = 6, text='|x>', height = labelHeights)
        self.__drawlines()

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name in ('theta', 'phi'):
            self.X = sin(2*self.theta) * cos(self.phi)
            self.Y = sin(2*self.theta) * sin(self.phi)
            self.Z = cos(2*self.theta)
            self.__redraw()

    def __getlabel(self):
        a = cos(self.theta)
        b = (cos(self.phi) + 1j * sin(self.phi)) * sin(self.theta)
        return '|x> = %.3g|0>+(%.3g+%.3gi)|1>' % \
                (a, b.real, b.imag)

    def __drawlines(self):
        self.__lines.visible = False
        if hasattr(self, 'arcs'):
            self.arcs[0].visible = False
            self.arcs[1].visible = False
        self.__lines = curve(pos=[(0,0,0), (self.X, 0, self.Y), (self.X, 0, 0),
            (self.X, 0, self.Y), (self.X, self.Z, self.Y), (0, self.Z, 0)])
        arc1 = curve(color=color.red)
        prec = 0.05
        end = self.phi
        i = 0.0
        while i < end:
            arc1.append((0.3*cos(i), 0.0, 0.3*sin(i)))
            i += prec
        arc2 = curve()
        self.arcs = (arc1, arc2)

    def __redraw(self):
        self.axis = (self.X, self.Z, self.Y)
        self.__drawlines()
        if hasattr(self, 'label'):
            self.label.pos = self.axis
            self.label.text = self.__getlabel()



scene = display(title="Qubit Bloch sphere. Robert Nowotniak (C) 2006", width=790, height=650)
scene.ambient = 0.4

c = controls(x=0, y=0, width = 400, height = 100, range = 100, title = 'Angles controls')
s1 = slider(pos=(-90,  10), min=0, max=pi/2, length = 180, action=lambda: setangles())
s2 = slider(pos=(-90, -10), min=0, max=2*pi, length = 180, action=lambda: setangles())

def setangles():
    qubit.theta = s1.value
    qubit.phi = s2.value

torusesThickness = 0.018
labelHeights = 25

ring(color = color.red, pos=(0,0,0), radius=1, thickness=torusesThickness, axis=(0,0,1))
ring(color = color.green, pos=(0,0,0), radius=1, thickness=torusesThickness, axis=(0,1,0))
ring(color = color.blue, pos=(0,0,0), radius=1, thickness=torusesThickness, axis=(1,0,0))

curve(pos=[(-1,0,0), (1,0,0)], color=color.red)
curve(pos=[(0,-1,0), (0,1,0)], color=color.blue)
curve(pos=[(0,0,-1), (0,0,1)], color=color.green)

label(pos=(0,1,0) , xoffset=15, yoffset=5, order=6, text='|0>', height = labelHeights)
label(pos=(0,-1,0), xoffset=15, yoffset=5, order=6, text='|1>', height = labelHeights)

qubit = StateArrow()

rotate = False
rotate_angle = 0

dt = 0.001


while True:
    rate(100)
    c.interact()
    if scene.kb.keys:
        s = scene.kb.getkey()
        if s == 'q':
            sys.exit()
        elif s == ' ':
            rotate = not rotate

    if rotate:
        rotate_angle = rotate_angle + 1.0 * math.pi * dt;
        scene.forward = (-1.0 * sin(rotate_angle), scene.forward.y, -1.0 * cos(rotate_angle))
        


