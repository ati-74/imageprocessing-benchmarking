% Analyze SuperSegger Output and Extract Bacterial Features
%
% This script processes the SuperSegger outputs for different datasets. For each dataset, it 
% performs lineage-based analysis to label each bacterial family tree. Then, it extracts 
% bacterial features based on each timestep. Finally, it computes life history-based features.

% Define the input directories for SuperSegger output and corresponding output directories
SS_output_path_matrix = ["baby20/SuperSegger"];
output_directory_matrix = ["baby20/SuperSegger/results"];

% Specify the interval time for each dataset
interval_time_list_array = [1.5];

% Get the total number of datasets
num_SS_output_path = length(SS_output_path_matrix);

% Loop over each dataset
for i = 1:num_SS_output_path
    
    % Get the SuperSegger output path, output directory, and interval time for current dataset
    SS_output_path = SS_output_path_matrix(i);
    output_directory = output_directory_matrix(i);
    intervalTime = interval_time_list_array(i);

    % Perform lineage-based analysis to assign labels to each bacterial family tree.
    % Bacteria in the same family tree have the same label.
    bacteria_label = SuperSegger_Lineaged_based_Analysis(SS_output_path, output_directory);
    
    % Extract bacterial features based on each timestep for current dataset
    [T, AverageLength, AverageVelocity, AverageOrientation] = ...
        SuperSegger_bacteria_based_features_each_timestep(SS_output_path, ...
        output_directory, bacteria_label, intervalTime);
    
    % Uncomment the below line if you want to extract features calculated by SuperSegger for bacteria
    % SuperSegger_Bacteria_features(SS_output_path, output_directory);
    
    % Calculate the number of cells in each time step for current dataset
    SuperSegger_Num_cells(T, output_directory);
    
    % Compute life history-based features for the current dataset
    SuperSegger_lifeHistory_based_features(SS_output_path, output_directory, intervalTime, ...
        AverageLength, AverageVelocity, AverageOrientation);

end
