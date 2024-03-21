import cv2
import pickle
import cvzone
import numpy as np
 
# Video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

# width, height = 107, 48
width, height = 70, 150

refX, refY = 450, 100  # Example reference point (entrance coordinates)

def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def checkParkingSpace(imgPro):
    spaceCounter = 0
    nearestSpot = None
    nearestSpotIndex = None
    minDistance = float('inf')
    
    for index, pos in enumerate(posList):
        x, y = pos
        distance = calculate_distance(refX, refY, x, y)
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)
        
        if count < 800:  # Spot is empty
            color = (0, 255, 0)
            spaceCounter += 1

            if distance < minDistance:
                minDistance = distance
                nearestSpot = pos
                nearestSpotIndex = index

        else:
            color = (0, 0, 255)  # Red for occupied

        # Draw the rectangle for the parking spot
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 2)
        # Overlay the parking spot number
        spot_number = str(index + 1)  # Adding 1 for user-friendly numbering
        cvzone.putTextRect(img, spot_number, (x + 5, y + 20), scale=1, thickness=2, offset=0, colorR=color)

    # Highlight the nearest spot in blue
    if nearestSpot:
        cvzone.putTextRect(img, "Nearest: " + str(nearestSpotIndex + 1), (800, 50), scale=2, thickness=3, offset=10, colorR=(0, 0, 255))
        x, y = nearestSpot
        cv2.rectangle(img, (x, y), (x + width, y + height), (255, 0, 0), 5)  # Blue rectangle for nearest spot

    # Mark the entry point
    cv2.arrowedLine(img, (refX, refY), (refX, refY - 50), (0, 255, 255), 5)  # Yellow arrow for entry point
    cvzone.putTextRect(img, "Entry", (refX - 40, refY - 60), scale=2, thickness=1, offset=0, colorR=(45, 106, 196))

    # cvzone.putTextRect(img, f'Free: 6/20', (550, 50), scale=2, thickness=3, offset=10, colorR=(0,200,0))

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)

    cv2.imwrite('parking_status.jpg', img)
    cv2.imshow("Image", img)
    cv2.waitKey(10)
