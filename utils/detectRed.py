import numpy as np
import cv2

def detect_red_object(frame, debugMode):
    # Convert frame from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range for red color and create a mask
    lower_red = np.array([161, 155, 84])
    upper_red = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    if debugMode:
        cv2.imshow('Red Mask', mask)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Set the accepted minimum & maximum radius of a detected object
    min_radius_thresh = 3
    max_radius_thresh = 30

    centers = []
    for c in contours:
        (x, y), radius = cv2.minEnclosingCircle(c)
        radius = int(radius)

        # Take only the valid circle(s)
        if min_radius_thresh < radius < max_radius_thresh:
            centers.append(np.array([[x], [y]]))

    if debugMode:
        cv2.imshow('contours', mask)
    
    return centers
