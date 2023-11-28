import cv2
import numpy as np
from utils.Detector import detect
from utils.KalmanFilter import KalmanFilter
from plot import plot
import matplotlib.pyplot as plt

def main():

    # Create opencv video capture object
    VideoCap = cv2.VideoCapture('video/randomball.avi')
    
    """   # Get the frame size from the VideoCap object
    frame_width = int(VideoCap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(VideoCap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Frame dimensions: {frame_width}x{frame_height}")

    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Changed codec to MJPG
    out = cv2.VideoWriter('video/output.avi', fourcc, 20.0, (frame_width, frame_height)) """


    #Variable used to control the speed of reading the video
    ControlSpeedVar = 100  #Lowest: 1 - Highest:100

    HiSpeed = 100
    parameter_sets = [
    {'std_acc': std_acc, 'x_std_meas': std_meas, 'y_std_meas': std_meas}
    for std_acc in np.linspace(0.1, 0.5, num=5)
    for std_meas in np.linspace(0.0001, 0.001, num=10)
    ]
    scores=[]
    
    #Create KalmanFilter object KF
    #KalmanFilter(dt, u_x, u_y, std_acc, x_std_meas, y_std_meas)
    for params in parameter_sets:
        # Reinitialize the video capture for each set of parameters
        VideoCap.release()
        VideoCap = cv2.VideoCapture('video/randomball.avi')

        KF = KalmanFilter(0.1, 1, 1, params['std_acc'], params['x_std_meas'], params['y_std_meas'])
    



        debugMode=1
        measured_positions = []
        predicted_positions = []
        updated_positions = []

        while(True):
            # Read frame
            ret, frame = VideoCap.read()
            if not ret:
                print("No more frames to read or error reading a frame.")
                break

            # Detect object
            centers = detect(frame,debugMode)

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
        
                measured_positions.append((cx,cy))
                predicted_positions.append((x, y)) # Where x and y are scalar values
                updated_positions.append((x1, y1)) # Similarly, x1 and y1 should be scalars


                # Draw a rectangle as the estimated object position
                cv2.rectangle(frame, (int(x1 - 15), int(y1 - 15)), (int(x1 + 15), int(y1 + 15)), (0, 0, 255), 2)

                
                cv2.putText(frame, "Estimated Position", (int(x1 + 15), int(y1 + 10)), 0, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, "Predicted Position", (int(x + 15), int(y)), 0, 0.5, (255, 0, 0), 2)
                cv2.putText(frame, "Measured Position", (int(cx + 15), int(cy - 15)), 0, 0.5, (0,191,255), 2)
                
            cv2.imshow('image', frame)

            if cv2.waitKey(2) & 0xFF == ord('q'):
                VideoCap.release()
                #out.release()
                cv2.destroyAllWindows()
                break
        

            cv2.waitKey(HiSpeed-ControlSpeedVar+1)

        # Before calling claculate_score
        if not measured_positions:
            print("No measured positions recorded. Skipping score calculation.")
            continue 

      
        
        np.save(f"output/measured_positions_{params['std_acc']}_{params['x_std_meas']}_{params['y_std_meas']}.npy", measured_positions)
        np.save(f"output/predicted_positions_{params['std_acc']}_{params['x_std_meas']}_{params['y_std_meas']}.npy", predicted_positions)
        np.save(f"output/updated_positions_{params['std_acc']}_{params['x_std_meas']}_{params['y_std_meas']}.npy", updated_positions)
        
        RMSE_Predicted,RMSE_Updated=  plot(measured_positions,updated_positions,predicted_positions,f"{params['std_acc']}_{params['x_std_meas']}_{params['y_std_meas']}")
        print(f"Params: {params}, RMSE_Predicted: {RMSE_Predicted}, RMSE_Updated: {RMSE_Updated}")
        scores.append((RMSE_Predicted,RMSE_Updated))
        

    RMSE_Predicted, RMSE_Updated = zip(*scores)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(RMSE_Predicted, label='RMSE Predicted')
    plt.plot(RMSE_Updated, label='RMSE Updated')
    plt.xlabel('Iteration')
    plt.ylabel('RMSE')
    plt.title('RMSE Scores Over Iterations')
    plt.legend()
    plt.grid(True)

    # Saving the figure
    plt.savefig('rmse_scores.png')

    # Optionally, show the plot
    plt.show()
    
if __name__ == "__main__":
    main()
     