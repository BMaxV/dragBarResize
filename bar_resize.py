
# PM]BMaxV: I think I want another UI element
# [10:14 PM]BMaxV: something like a bar with multiple draggable sliders that calculates the scope of things
# [10:14 PM]BMaxV: so
# [10:14 PM]BMaxV: [---][--][-----] and then you can distribute your points on the fixed length bar
# [10:15 PM]BMaxV: anyone built something like that before?

from direct.gui.DirectGui import DGG

import random
import time

from panda_interface_glue import panda_interface_glue as pig
from panda_interface_glue import drag_main
from panda3d.core import ClockObject
from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.gui.DirectGui import DirectFrame


class Barresize():
    def __init__(self, base):
        a = 1
        self.dragged = None
        self.base = base

        # this is irrelevant.
        frame_size = (-0.125, 0.125, 0, 0.5)

        this = ["A", "B", "C"]
        element_list_length = len(this)
        total_length = 1.5
        length_of_elements = total_length / len(this)

        self.limits = {}

        pos = (-0.5, 0, 0)
        x = -0.5
        self.elements = []
        self.active_frame = None
        c = 0
        while c < element_list_length:

            frame_size = (c*length_of_elements, (c+1)
                          * length_of_elements, 0, 0.5)

            F = DirectFrame(pos=pos, frameSize=frame_size, state=DGG.NORMAL)
            # F.bind(DGG.WITHIN , hover_in, [self,F])
            # F.bind(DGG.WITHOUT, hover_out, [self,F])

            F.setColor(random.random(), 0, random.random())
            F.thisname = "Fred"
            self.elements.append(F)

            self.limits[c] = (c*length_of_elements, (c+1)*length_of_elements)
            c += 1

        c = 1
        while c < element_list_length:
            # pos = (x+0.5*c,0,0.2)
            
            pos = (-0.5+c*length_of_elements, 0, 0.2)
            frame_size = (-0.05, 0.05, 0, 0.5)

            F = DirectFrame(pos=pos, frameSize=frame_size, state=DGG.NORMAL)
            F.bind(DGG.WITHIN, hover_in, [self, F])
            F.bind(DGG.WITHOUT, hover_out, [self, F])
            F.bind(DGG.B1PRESS, drag_start, [self, F])
            F.bind(DGG.B1RELEASE, drag_stop, [self, F])

            F.mover_c = c
            self.elements.append(F)
            c += 1

    def main(self):
        
        if self.base.mouseWatcherNode.has_mouse() and self.dragged != None:
            frame = self.dragged
            mpos = self.base.mouseWatcherNode.get_mouse()
            mpos = aspect2d.getRelativePoint(render2d, (mpos[0], mpos[1], 0))

            frame.mover_c
            # get the frames this is connected to.
            el1 = self.elements[frame.mover_c-1]
            el2 = self.elements[frame.mover_c]

            lim1 = self.limits[frame.mover_c-1]
            lim2 = self.limits[frame.mover_c]
            
            p1=el1.getPos()
            p2=el2.getPos()
            
            offset1 = p1[0]
            offset2 = p2[0]
            
            
            #ok, very good. let's limit it to the other side.
            
            # the 0.5 is because of the positioning... so.
            
            new_lim1 = (lim1[0], mpos[0] - offset1, 0, 0.5)
            new_lim2 = (mpos[0] - offset2, lim2[1], 0, 0.5)

            self.limits[frame.mover_c-1] = new_lim1
            self.limits[frame.mover_c] = new_lim2

            if mpos[0]-offset1 <= lim2[1] and mpos[0]-offset2 >=lim1[0]:
            
                el1["frameSize"] = new_lim1
                el2["frameSize"] = new_lim2

            old_pos = frame.getPos()
            new_x = mpos[0]
            frame.setPos(new_x, 0, old_pos[2])


def drag_start(manager, frame, *args):
    manager.dragged = frame


def drag_stop(manager, frame, *args):
    manager.dragged = None
    # output the stuff to console.
    print(manager.limits)

def hover_in(manager, frame, *args):

    frame["frameSize"] = (-0.15, 0.15, 0, 0.5)
    if manager.active_frame != None:
        manager.active_frame.set_color(0.8, 0.8, 0.8)
    manager.active_frame = frame
    frame.set_color(0, 0, 1)
    frame.active = True


def hover_out(manager, frame, *args):
    frame["frameSize"] = (-0.125, 0.125, 0, 0.5)
    manager.active_frame = None
    frame.set_color(0.8, 0.8, 0.8)
    frame.active = False


class Wrapper:
    def __init__(self):

        # this is required for this demo
        self.b = ShowBase()

        # this is sort of optional allows for easily building and deleting
        # elements

        self.Barresize = Barresize(self.b)


def old():
    W = Wrapper()

    while True:
        W.b.taskMgr.step()
        W.Barresize.main()


if __name__ == "__main__":
    old()
