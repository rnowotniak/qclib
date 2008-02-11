#!/usr/bin/python

from visual import *
import math


#
# Re and Im axes
#
aRe1 = arrow(axis=(  0,    0,  1.5), shaftwidth = 0.02, fixedwidth = 1)
aRe2 = arrow(axis=(  0,    0, -1.5), shaftwidth = 0.02, fixedwidth = 1)
aIm1 = arrow(axis=(  0,  1.5,    0), shaftwidth = 0.02, fixedwidth = 1)
aIm2 = arrow(axis=(  0, -1.5,    0), shaftwidth = 0.02, fixedwidth = 1)

#
# n axis
#
a3 = arrow(axis=(  5,   0,   0), shaftwidth = 0.02, fixedwidth = 1)

#
# axes labels
#
Relabel = label(pos=(0, 0, 1), text = 'Re')
Imlabel = label(pos=(0, 1, 0), text = 'Im')
nlabel = label(pos=(1, 0, 0), text = 'n')

#
# circle in Re-Im plane
#
r = ring(axis=(1,0,0), radius=1, thickness=0.02, color=color.red)


dt = 0.033333

rotate = False
rotate_angle = 0
drag = None

# amplitudes
amps = []
for n in xrange(16):
    amp = [None, None, None]
    amp[0] = sphere(pos=(1.0*n/4, sqrt(2)/2, sqrt(2)/2), radius = 0.02, color=color.yellow)
    amp[1] = arrow(pos=(1.0*n/4, 0, 0), color = color.yellow, axis = (0, sqrt(2)/2, sqrt(2)/2), shaftwidth = 0.04, fixedwidth = 1)
    amp[0].rotate(angle = math.pi / 10 * n, axis = (1, 0, 0), origin = (0, 0, 0))
    amp[1].rotate(angle = math.pi / 10 * n, axis = (1, 0, 0), origin = (0, 0, 0))
    amp[2] = label(pos = amp[0].pos, text = 'alpha', xoffset = 20, yoffset = 20)
    amps.append(amp)

while true:
    rate(25)

    if scene.kb.keys:
        s = scene.kb.getkey()
        if s == 'r':
            rotate = not rotate
        if s == 'l':
            for a in amps:
                a[2].visible = not a[2].visible

#    if scene.mouse.events:
#        e = scene.mouse.getevent()
#        if drag and (e.drop or e.click):
#            dp = scene.mouse.project(normal = (1, 0, 0))
#            if dp:
#                if mag(dp) > 1:
#                    dp = dp / mag(dp)
#                drag.pos = (0, dp.y, dp.z)
#                amp1.axis = drag.pos
#                lab1.pos = amp1.axis
#                lab1.text = 'alpha: %+0.3f %+0.3f*i' % (drag.pos.z, drag.pos.y)
#            drag = None
#            # scene.cursor.visible = True
#        elif e.pick:
#            drag = e.pick
#            # scene.cursor.visible = False
#    if drag:
#        dp = scene.mouse.project(normal = (1, 0, 0))
#        if dp:
#            if mag(dp) > 1:
#                dp = dp / mag(dp)
#            drag.pos = (0, dp.y, dp.z)
#            amp1.axis = drag.pos
#            lab1.pos = amp1.axis
#            lab1.text = 'alpha: %+0.3f %+0.3f*i' % (drag.pos.z, drag.pos.y)

    for a in amps:
        a[0].rotate(angle = 0.1 * math.pi * dt, axis = (1, 0, 0), origin = (0, 0, 0))
        a[1].rotate(angle = 0.1 * math.pi * dt, axis = (1, 0, 0), origin = (0, 0, 0))
        a[2].pos = a[0].pos

    if rotate:
        rotate_angle = rotate_angle + 0.1 * math.pi * dt;
        scene.forward = (-1.0 * sin(rotate_angle), -1, -1.0 * cos(rotate_angle))


