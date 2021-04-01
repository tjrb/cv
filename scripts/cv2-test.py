import cv2
import numpy as np
import time
import teolib

def setups():            
    
    #<----------------Test opencl------------------->
    print('OpenCL available:', cv2.ocl.haveOpenCL())
    #<---------------------------------------------->

    #<----------------Start camera------------------>
    data.cam=cv2.VideoCapture(0)
    #<---------------------------------------------->

    #----------------Open Neural Net---------------->
    data.net=cv2.dnn.readNet(
                            './models/darknet/yolov-tiny/yolov3-tiny.weights',
                            './models/darknet/yolov-tiny/yolov3-tiny.cfg'
                            )
    data.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    data.net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)
    #<---------------------------------------------->

    #<----------------read classes------------------>
    data.getclassnames(path="./models/darknet/coco.names")
    
    layernames = data.net.getLayerNames()
    data.layers = [layernames[i[0] - 1] for i in data.net.getUnconnectedOutLayers()]
    #<---------------------------------------------->

    #<--------------Set classes coloors------------->
    data.classcolors = np.random.uniform(0, 255, size=(len(data.classnames), 3))
    #<---------------------------------------------->
    print("setup done")
    return


def runner():#outa,outb,outc,outd):
    cv2.namedWindow("main", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("veicle",cv2.WINDOW_AUTOSIZE)
    net=data.net
    while(True):
        STIME=time.time()
        ret,frame=data.cam.read()
        height, width, _ =frame.shape
        #print("{}x{}".format(width,height))
        #height=800
        #width=800
        #frame=cv2.resize(frame,(width,height))
        #frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        blob=cv2.dnn.blobFromImage(frame, 1 / 255.0, (height, width),swapRB=True, crop=False)


        net.setInput(blob)
        outs=data.net.forward(data.layers)
        
        class_ids=[]
        confidences=[]
        boxes=[]
        veicle_frame=None
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                #print(confidence)
                if confidence > 0.6:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
            
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(data.classnames[class_ids[i]])
                color = data.classcolors[class_ids[i]]
                if class_ids[i] >= 2 or class_ids[i] <=4 and veicle_frame is None:
                    veicle_frame=frame[y:y+h,x:x+w]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y -5),cv2.FONT_HERSHEY_SIMPLEX,
                1/2, color, 2)
        Ttime=time.time()-STIME
        cv2.rectangle(frame,(20,10),(40,60),(0,0,0),-1)
        cv2.putText(frame,"Fps:{fps:.2f}".format(fps=1/Ttime),(20,10),cv2.FONT_HERSHEY_SIMPLEX,1/2,(50,200,50),2)
        #cv2.imshow("main",cv2.resize(frame,(800,600)))
        #cv2.resize(frame,(600,600)
        cv2.imshow("main",frame)
        if veicle_frame is not None:
            cv2.imshow("veicle",veicle_frame)
        #fps.update()
        #cv2.waitKey(0)
            
        #cv2.imshow('frame',frame)
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    data.cam.release ()
    #fps.stop()
    cv2.destroyAllWindows()



if __name__=="__main__":
    data=teolib.sets()
    try:
        setups()
    except cv2.error as e:
        print(e)
        exit(-1)
    runner()
    print("everything done")