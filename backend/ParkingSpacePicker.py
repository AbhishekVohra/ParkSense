#
#
import cv2
import pickle


width, height = 70, 150
# width, height = 100, 100
posList = []

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []
#
#
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN: # to add a rectangle
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN: # to delete a rectangle
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('CarParkPos', 'wb') as f: # to save the posList in a file called CarParkPos
        pickle.dump(posList, f)
#
#
while True:
#     cv2.rectangle(img, (100,100), (200,150), (255,0,255), 2)
    img = cv2.imread('carParking1.png')
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)