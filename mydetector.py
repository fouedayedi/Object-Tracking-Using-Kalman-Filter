import cv2
from utils.KalmanFilter import KalmanFilter
import numpy as np
from utils.detectRed import detect_red_object

def detect_and_track():
    # Initialisation de la caméra
    cap = cv2.VideoCapture(0)

    KF = KalmanFilter(0.1, 1, 1, 0.2, 0.0006, 0.0006)
    debugMode= 1

    while True:
        # Capture frame par frame
        ret, frame = cap.read()
        if not ret:
            break

        centers= detect_red_object(frame,debugMode)

        # Mise à jour du filtre de Kalman et suivi de l'objet
        # If centroids are detected then track them
        if (len(centers) > 0):

                # Draw the detected circle
                cv2.circle(frame, (int(centers[0][0]), int(centers[0][1])), 10, (0, 191, 255), 2)

                # Predict
                (x, y) = KF.predict()
            
                
                # Draw a rectangle as the predicted object position
                cv2.rectangle(frame, (int(x - 15), int(y - 15)), (int(x + 15), int(y + 15)), (255, 0, 0), 2)

                # Update
                (x1, y1) = KF.update(centers[0])
            
                
                cx, cy = centers[0][0], centers[0][1]
        
        
                # Draw a rectangle as the estimated object position
                cv2.rectangle(frame, (int(x1 - 15), int(y1 - 15)), (int(x1 + 15), int(y1 + 15)), (0, 0, 255), 2)

                
                cv2.putText(frame, "Estimated Position", (int(x1 + 15), int(y1 + 10)), 0, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, "Predicted Position", (int(x + 15), int(y)), 0, 0.5, (255, 0, 0), 2)
                cv2.putText(frame, "Measured Position", (int(cx + 15), int(cy - 15)), 0, 0.5, (0,191,255), 2)
                
        cv2.imshow('image', frame)

        # Quitter si 'q' est appuyé
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libération de la capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_and_track()

