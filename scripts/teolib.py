"""
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


class sets:
    def __init__(self,cam=None,net=None,classnames=None,classcolors=None,layers=None):
        self.cam=cam
        self.net=net
        self.classnames=classnames
        self.classcolors=classcolors
        self.layers=layers
    
    def getclassnames(self,path):
        with open(path, "r") as f:
            self.classnames= [line.strip() for line in f.readlines()]
        
class infer:
    def __init__(self,outs=None,class_ids=None,confidences=None):
        self.outs=outs
        self.class_ids=class_ids
        self.confidences=confidences