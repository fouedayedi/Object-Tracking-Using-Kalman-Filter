import cv2

# Path to the video file
video_path = 'video/output.avi'

# Create a VideoCapture object
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print(f"Error: Could not open the video file {video_path}. Please check the file path and format.")
    exit()

# Try to get the first frame
ret, frame = cap.read()
if not ret:
    print("Error: Can't read video data. The file may be corrupted or in an unsupported format.")
    exit()

# Read and display the video frame by frame
while True:
    ret, frame = cap.read()
    
    if ret:
        cv2.imshow('Video Playback', frame)

        # Press 'q' to exit the video window
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

# Release the VideoCapture object and close windows
cap.release()
cv2.destroyAllWindows()

