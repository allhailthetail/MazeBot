import cv2, pupil_apriltags as apriltag

detector = apriltag.Detector(families="tag36h11")
cam = cv2.VideoCapture(0) # This is the Pi camera (If I manage to make it work)

def read_id():
    ret, frame = cam.read()
    if not ret: return None
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    res = detector.detect(gray, estimate_tag_pose=False)
    return res[0].tag_id if res else None