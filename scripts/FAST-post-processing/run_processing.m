% Analyze FAST Output and Extract Bacterial Features
%
% This script processes the FAST outputs for different datasets. For each dataset, it 
% performs lineage-based analysis to label each bacterial family tree. Then, it extracts 
% bacterial features based on each timestep. Lastly, it computes life history-based features.

% Define the input directories for FAST output and corresponding output directories
FAST_output_path_matrix = ["xantho/FAST"];
output_directory_matrix = ["xantho/FAST/results/"];

% Specify the interval time (unit: minute) and number of timesteps for each dataset
interval_time_list_array = [5];

% Get the total number of datasets
num_FAST_output_path = length(FAST_output_path_matrix);

% Loop over each dataset
for i = 1:num_FAST_output_path
    
    % Get the FAST output path, output directory, number of timesteps, and interval time for current dataset
    FAST_output_path = FAST_output_path_matrix(i);
    output_directory = output_directory_matrix(i);
    intervalTime = interval_time_list_array(i);

    % Perform lineage-based analysis to assign labels to each bacterial family tree
    bacteria_label = FAST_Lineaged_based_Analysis(FAST_output_path, output_directory);
    
    % Extract bacterial features based on each timestep for current dataset
    [AverageLength, AverageVelocity, AverageOrientation] = ...
        FAST_bacteria_based_features_each_timestep(FAST_output_path, ...
        output_directory, bacteria_label, intervalTime);
    
    % Calculate the number of cells in each time step for current dataset
    FAST_Num_cells(FAST_output_path, output_directory);
    
    % Compute life history-based features for the current dataset
    FAST_lifeHistory_based_features(FAST_output_path, output_directory, intervalTime, ...
        AverageLength, AverageVelocity, AverageOrientation);
end
