import numpy as np
import pandas as pd
import cv2
import argparse as ap

ap=ap.ArgumentParser()
ap.add_argument('-i','--image',required=True,help='Image path')
args=vars(ap.parse_args())
path=args['image']

img=cv2.imread(path)

clicked=False
r=g=b=xpos=ypos=0

index=["color","color_name","hex","R","G","B"]
ds=pd.read_csv('colors.csv',names=index,header=None)

def colorName(R,G,B):
    min=10000
    for i in range(len(ds)):
        d=abs(R-int(ds.loc[i,"R"]))+abs(G-int(ds.loc[i,"G"]))+abs(B-int(ds.loc[i,"B"]))
        if(d<=min):
            min=d
            cname=ds.loc[i,'color_name']
    return cname

def draw_fun(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos,clicked
        clicked=True
        xpos=x
        ypos=y
        b,g,r=img[y,x]
        b=int(b)
        g=int(g)
        r=int(r)

cv2.namedWindow('color detect')
cv2.setMouseCallback('color detect',draw_fun)


while(1):
    cv2.imshow('color detect',img)
    if(clicked):
        cv2.rectangle(img,(10,10),(650,60),(b,g,r),-1)

        text=colorName(r,g,b)+' R ='+ str(r)+' G= '+str(g)+' B= '+str(b)

        cv2.putText(img,text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        if(r+g+b>=600):
             cv2.putText(img,text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)

        clicked=False
    
    if cv2.waitKey(20)&0xFF==27:
        break
cv2.destroyAllWindows