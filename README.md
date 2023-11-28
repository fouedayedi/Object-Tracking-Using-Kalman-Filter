# 2-D Kalman Filter for Object Tracking

This project applies a 2-D Kalman Filter for tracking a moving object. It includes the experimentation with different parameters and the comparison of Root Mean Square Error (RMSE) for each parameter set. The results of these comparisons can be found in the `plots` folder.

## Getting Started

To set up your environment to run this project, follow these steps:

### Create a Conda Environment
conda create -n your_ENV_NAME python=3.9


### Install Requirements
pip install -r requirements.txt


## Project Structure

- `objTracking.py`: Compiles the tracking using different parameters and plots the results.
- `mydetector.py`: Tracks a red object. Modify the pixel range within the script to track objects of different colors.
- `utils/`: Contains utility functions used across the project.
- `output/`: Contains the output positions saved during object tracking.
- `plots/`: Contains plots generated from parameter testing and RMSE comparison.

## Parameter Sets

The project tests various parameter sets for the Kalman Filter:

```
python
parameter_sets = [
    {'std_acc': std_acc, 'x_std_meas': std_meas, 'y_std_meas': std_meas}
    for std_acc in np.linspace(0.1, 0.5, num=5)
    for std_meas in np.linspace(0.0001, 0.001, num=10)
]
```

Adjust these in objTracking.py as needed for your specific use case.
Acknowledgements

    This project was inspired by the GitHub repository "2-D Kalman Filter for tracking a moving object."
    Additional insights were gained from Machine Learning Space on 2D object tracking using Kalman Filters.

Contribution

Feel free to fork this project, submit pull requests, or suggest improvements.


