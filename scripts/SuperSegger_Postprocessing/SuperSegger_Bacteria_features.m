function [] = SuperSegger_Bacteria_features(SS_output_path, write_directory)
%SuperSegger_Bacteria_features Extracts bacteria features from SuperSegger's output.
%
%   SuperSegger_Bacteria_features(SS_output_path, write_directory) loads the clist.mat 
%   file from SuperSegger's output directory, converts it to a table, and writes 
%   the data to a CSV file in the specified directory.
%
%   INPUTS:
%   SS_output_path - Directory path where SuperSegger's clist.mat file is located.
%   write_directory - The directory path where the output CSV file will be stored.
%
%   OUTPUTS:
%   None. The function writes the output directly to a CSV file.

% Load the clist.mat file from SuperSegger's output directory
load(strcat(SS_output_path, '/xy1/clist.mat'), 'data');
load(strcat(SS_output_path, '/xy1/clist.mat'), 'def');

% Convert the loaded data and definitions to a table
SuperSegger_Results = array2table([def; num2cell(data)]);

% Write the results to a CSV file without variable names
writetable(SuperSegger_Results, strcat(write_directory, '/SuperSegger_Bacteria_features.csv'), ...
           'Delimiter', ',', 'QuoteStrings', true, 'WriteVariableNames', 0);
end
