import cv2
import numpy as np
import sys
import os

OUTPUT_PATH = "./data/"
DISPLAY = True

if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

# sub array: y, x, r, g, b
PRIVACYPIXELS = [[68, 1274,  170, 190], [68, 1035,  170, 190]]


def checkPrivacy(frame):
    for PRIVACY in PRIVACYPIXELS:
        # print(frame[PRIVACY[0], PRIVACY[1], 0], frame[PRIVACY[0],
        #                                              PRIVACY[1], 1], frame[PRIVACY[0], PRIVACY[1], 2])

        if frame[PRIVACY[0], PRIVACY[1], 0] > PRIVACY[2] and frame[PRIVACY[0], PRIVACY[1], 0] < PRIVACY[3] and frame[
            PRIVACY[0], PRIVACY[1], 1] > PRIVACY[2] and frame[PRIVACY[0], PRIVACY[1], 1] < PRIVACY[3] and frame[
                PRIVACY[0], PRIVACY[1], 2] > PRIVACY[2] and frame[PRIVACY[0], PRIVACY[1], 2] < PRIVACY[3]:
            print("oki")
            return True

    return False


cap = cv2.VideoCapture(sys.argv[1])

skipTime = (cap.get(cv2.CAP_PROP_FPS) * 60)  # 1min

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

out = cv2.VideoWriter(sys.argv[2], cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

if (cap.isOpened() == False):
    print("Error opening video stream or file")

length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(length)
counter = 0
cap.set(cv2.CAP_PROP_POS_FRAMES, skipTime)


while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        if checkPrivacy(frame):
            print("private")
            continue
        out.write(frame)
        counter += 1
        if counter % 100 == 0:
            print(f"Progress %d/%d" % (counter, length))
        if DISPLAY:
            cv2.imshow('Frame', frame)
        cv2.imwrite(os.path.join(
            OUTPUT_PATH, f'frame-{str(counter)}.jpg'), frame)

        if DISPLAY and cv2.waitKey(25) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
