from collections import deque
import argparse
import cv2
#import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
    help="max buffer size")
args = vars(ap.parse_args())



bawah = (0, 0, 0)
atas = (0, 0, 255)

pts = deque(maxlen=args["buffer"])

(x,y)	= (0,0)
error	= 9999

if not args.get("video", False):
    camera = cv2.VideoCapture(0)

else:
    camera = cv2.VideoCapture(args["video"])



while True:
#grab camera tiap frame
    (grabbed,resized) = camera.read()
    #image = imutils.resize(resized, width=600)
#    ratio = image.shape[0] / float(resized.shape[0])
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, bawah, atas)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
#    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    resolusi= 600
    img0 = cv2.rectangle(image, (0, 0), (resolusi/3, resolusi/4), (255, 255, 255), 2)
    img1 = cv2.rectangle(image, (0, resolusi/4), (resolusi/3,(resolusi/4)*2 ), (255, 255, 255), 2)
    img2 = cv2.rectangle(image, (0, (resolusi / 4)*2), (resolusi / 3, (resolusi / 4) * 3), (255, 255, 255), 2)
    img3 = cv2.rectangle(image, (resolusi/3, 0), ((resolusi / 3)*2, resolusi / 4), (255, 255, 255), 2)
    img4 = cv2.rectangle(image, (resolusi / 3, (resolusi / 4)), ((resolusi / 3) * 2, (resolusi / 4) * 2),(255, 255, 255), 2)
    img5 = cv2.rectangle(image, (resolusi/3, (resolusi / 4) * 2), ((resolusi / 3)*2, (resolusi / 4) * 3), (255, 255, 255), 2)
    img6 = cv2.rectangle(image, ((resolusi / 3)*2, 0), (resolusi, resolusi / 4), (255, 255, 255), 2)
    img7 = cv2.rectangle(image, ((resolusi / 3) * 2, resolusi/4), (resolusi, (resolusi / 4)*2), (255, 255, 255), 2)
    img8 = cv2.rectangle(image, ((resolusi / 3)*2, (resolusi / 4)*2), (resolusi, (resolusi / 4) * 3),(255, 255, 255), 2)
 
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 3:
            cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(image, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)
            error=0
            data.value = 1
            event.set()

    else :
        (x,y)=(9999,9999)
        error=9999
        data=9999

    if x!=9999 and y!=9999 and error==0:
        if x >= 0 and x <= resolusi/3 and y >= 0 and y <= resolusi/4:
            img0 = cv2.rectangle(image, (0, 0), (resolusi / 3, resolusi / 4), (0, 0, 0), 2)
            data=1
        if x >= 0 and x <= resolusi/3 and y >= resolusi/4 and y <= resolusi/2:
            img1 = cv2.rectangle(image, (0, resolusi / 4), (resolusi / 3, (resolusi / 4) * 2), (0, 0, 0), 2)
            data=4
        if x >= 0 and x <= resolusi/3 and y >= resolusi/2 and y <= (resolusi/4)*3:
            img2 = cv2.rectangle(image, (0, resolusi / 2), (resolusi / 3, (resolusi / 4) * 3), (0, 0, 0),2)
            data=7
        if x >= resolusi/3 and x <= (resolusi/3)*2 and y >= 0 and y <= resolusi/4:
            img3 = cv2.rectangle(image, (resolusi / 3, 0), ((resolusi / 3) * 2, resolusi / 4), (0, 0, 0), 2)
            data=2
        if x >= resolusi/3 and x <= (resolusi/3)*2 and y >= resolusi/4 and y <= resolusi/2:
            img4 = cv2.rectangle(image, (resolusi / 3, (resolusi / 4)), ((resolusi / 3) * 2, (resolusi / 4) * 2),(0, 0, 0), 2)
            data=5 #TURUN
        if x >= resolusi/3 and x <= (resolusi/3)*2 and y >= resolusi/2 and y <= (resolusi/4)*3:
            img5 = cv2.rectangle(image, (resolusi / 3, resolusi / 2), ((resolusi / 3) * 2, (resolusi / 4) * 3),(0, 0, 0), 2)
            data=8
        if x >= (resolusi/3)*2 and x <= resolusi and y >= 0 and y <= resolusi/4:
            img6 = cv2.rectangle(image, ((resolusi / 3) * 2, 0), (resolusi, resolusi / 4), (0, 0, 0), 2)
            data=3
        if x >= (resolusi/3)*2 and x <= resolusi and y >= resolusi/4 and y <= resolusi/2:
            img7 = cv2.rectangle(image, ((resolusi / 3) * 2, resolusi / 4), (resolusi, resolusi/2),(0, 0, 0),2)
            data=6
        if x >= (resolusi/3)*2 and x <= resolusi and y >= resolusi/2 and y <= (resolusi/4)*3:
            img8 = cv2.rectangle(image, ((resolusi / 3) * 2, resolusi / 2), (resolusi, (resolusi/4)*3),(0, 0, 0),2)
            data=9

    cv2.putText(image, "x: {}, y: {}".format(x, y),(10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)
    cv2.putText(image, "ERROR : {}".format(error),(230, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)
    cv2.putText(image, "DATA : {}".format(data),(430, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)
        
#    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

#    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
#    thresh=cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    
#menampilkan frame dari img
    cv2.imshow('img', image)
#menunggu huruf q untuk ditekan sehingga keluar dari loop

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# matiin camera matiin smua window
camera.release()
cv2.destroyAllWindows()
