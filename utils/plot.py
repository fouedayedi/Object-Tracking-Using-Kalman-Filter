import matplotlib.pyplot as plt  
import numpy as np 
  
""" measured_positions = np.load('output/measured_positions.npy', allow_pickle=True)
predicted_positions = np.load('output/predicted_positions.npy', allow_pickle=True)
updated_positions = np.load('output/updated_positions.npy', allow_pickle=True)
 """


def plot(measured_positions,updated_positions,predicted_positions,name):
    
    # Plot the results
    mx, my = zip(*measured_positions)
    ux, uy = zip(*updated_positions)
    px, py = zip(*predicted_positions)
    

    # Remove the point (0,0)
    filtered_points = [(x, y) for x, y in zip(px, py) if x>5]

    # Unzip the filtered points back into two separate lists
    filtered_px, filtered_py = zip(*filtered_points) if filtered_points else ([], [])

    # Convert to 1D lists
    mx = [x.item() for x in mx]
    my = [y.item() for y in my]
    ux = [x.item() for x in ux]
    uy = [y.item() for y in uy]
    px = [x.item() for x in filtered_px]
    py = [y.item() for y in filtered_py]
    
    
    
    # Plotting
    plt.figure()
    plt.plot(mx, my, 'ro-', label='Measured')
    plt.plot(ux, uy, 'g^-', label='Updated')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title(f'{name} Object Tracking Positions')
    plt.legend()

    plt.savefig(f'plots/tracking_positions_{name}.png')  
    plt.show() 
    
    RMSE_Predicted = calculate_rmse(predicted_positions, measured_positions)
    RMSE_Updated = calculate_rmse(updated_positions, measured_positions)

    return(RMSE_Predicted,RMSE_Updated)


def calculate_rmse(predicted_positions, measured_positions):
    predicted_array = np.array(predicted_positions)
    measured_array = np.array(measured_positions)

    # Reshape arrays to ensure they have the same dimensions
    predicted_array = predicted_array.reshape(measured_array.shape)

    square_diff = np.square(predicted_array - measured_array)
    mean_square_diff = np.mean(square_diff)
    rmse = np.sqrt(mean_square_diff)
    return rmse

#plot(measured_positions,updated_positions,predicted_positions,"test")