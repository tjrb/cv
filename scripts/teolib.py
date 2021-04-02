"""
    This file is part of vision.

    teolib is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    teolib is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with teolib.  If not, see <https://www.gnu.org/licenses/>6.
"""

import cv2
import numpy as np
class sets():

    def __init__(self,cam=None,net=None,classnames=None,classcolors=None,layers=None):
        #self.cam=cv2.VideoCapture(0)
        self.cam=cam
        self.net=net
        self.classnames=classnames
        #with open(classfile, "r") as f:
        #    self.classnames= [line.strip() for line in f.readlines()]
        if(classnames is None):
            self.clacolors=classcolors
        else:
            self.classcolors=np.random.uniform(0, 255, size=(len(self.classnames), 3))
        self.layers=layers
    
    def setcam(self,index):
        self.cam=cv2.VideoCapture(index)

    def setclassnames(self,path):
        with open(path, "r") as f:
            self.classnames= [line.strip() for line in f.readlines()]
        self.classcolors=np.random.uniform(0, 255, size=(len(self.classnames), 3))
    
    def setlayers(self):
        layernames = self.net.getLayerNames()
        self.layers = [layernames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]


class infer:
    def __init__(self,outs=None,class_ids=None,confidences=None):
        self.outs=outs
        self.class_ids=class_ids
        self.confidences=confidences
