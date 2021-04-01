import cv2
import numpy as np
import time


print('OpenCL available:', cv2.ocl.haveOpenCL())
RawVid=cv2.VideoCapture(0)

NeuralNet=cv2.dnn.readNet('./models/darknet/yolov-tiny/yolov3-tiny.weights','./models/darknet/yolov-tiny/yolov3-tiny.cfg')
NeuralNet.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
NeuralNet.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

#fps=FPS().start()



#time.sleep(1)
classes=[]
with open("./models/darknet/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layernames = NeuralNet.getLayerNames()
outputlayers = [layernames[i[0] - 1] for i in NeuralNet.getUnconnectedOutLayers()]


colors = np.random.uniform(0, 255, size=(len(classes), 3))




def runner():#outa,outb,outc,outd):
    cv2.namedWindow("main", cv2.WINDOW_AUTOSIZE)
    while(True):
        #frame=frameBuffer.get()
        #prevframe=None
        #resp = urllib.request.urlopen(url)
        #img = np.asarray(bytearray(resp.read()), dtype="uint8")
        #frame = cv2.imdecode(img, cv2.IMREAD_COLOR)"""
        ret,frame=RawVid.read()
        #frame1=pyautogui.screenshot(region=(0,0,600,600))
        #print(frame1)    

        #frame=np.array(frame)
        #frame=cv2.resize(frame, None, fx=0.6, fy=0.6)
        height, width, channels=frame.shape
        #print("{}x{}".format(width,height))
        #height=800
        #width=800
        #frame=cv2.resize(frame,(width,height))
        #frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
        blob=cv2.dnn.blobFromImage(frame, 1 / 255.0, (height, width),swapRB=True, crop=False)


        NeuralNet.setInput(blob)
        outs=NeuralNet.forward(outputlayers)

        class_ids=[]
        confidences=[]
        boxes=[]

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                #print(scores)
                #print(class_id)
                #if class_id > 14:
                #   class_id=14
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
        #colors = np.random.uniform(0, 255, size=(len(classes), 3))
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y -5),cv2.FONT_HERSHEY_SIMPLEX,
                1/2, color, 2)
        
        #cv2.imshow("main",cv2.resize(frame,(800,600)))
        #cv2.resize(frame,(600,600)
        cv2.imshow("main",frame)
        #fps.update()
        #cv2.waitKey(0)
            
        #cv2.imshow('frame',frame)
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    RawVid.release ()
    #fps.stop()
    cv2.destroyAllWindows()



if __name__=="__main__":
    runner()
