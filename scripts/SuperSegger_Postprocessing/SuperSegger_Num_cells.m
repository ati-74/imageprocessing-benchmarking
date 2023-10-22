function [] = SuperSegger_Num_cells(T, write_directory)
%SuperSegger_Num_cells Counts the number of cells in each time step and saves to CSV.
%
%   SuperSegger_Num_cells(T, write_directory) analyzes the input table T 
%   (bacteria properties - output of SuperSegger_bacteria_based_features_each_timestep function) 
%   to count the number of cells present in each time step and then writes the result to 
%   a CSV file in the specified directory.
%
%   INPUTS:
%   T - A table containing cell data. It must contain a 'TimeStep' variable.
%   write_directory - The directory path where the output CSV file will be stored.
%
%   OUTPUTS:
%   None. The function writes the output directly to a CSV file.

% Determine the maximum time step in the table
Number_of_timesteps =  max(T.TimeStep);
% Initialize an array to store the number of cells for each time step
number_of_cells_in_each_timesteps = zeros(1, Number_of_timesteps);

% Loop through each time step to count the number of cells
for j = 1 : Number_of_timesteps
    number_of_cells_in_each_timesteps(j) = size(T(T.TimeStep == j, :), 1);
end  

% Convert the results to a table for easier CSV writing
T2 = table(transpose(1:length(number_of_cells_in_each_timesteps)), ...
           transpose(number_of_cells_in_each_timesteps));
% Rename columns for clarity
T2.Properties.VariableNames = {'StepNumber', 'NumberOfCells'};

% Write the table to a CSV file in the specified directory
writetable(T2, strcat(write_directory, '/SuperSegger_Num_cells_in_each_timeStep.csv'), ...
           'Delimiter', ',' ,'QuoteStrings', true);
end
