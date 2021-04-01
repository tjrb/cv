
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