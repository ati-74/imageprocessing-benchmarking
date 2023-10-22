function [] = SuperSegger_lifeHistory_based_features(SS_output_path, write_directory, intervalTime, AverageLength, AverageVelocity, AverageOrientation)
%SuperSegger_lifeHistory_based_features Computes life-history based features from SuperSegger's output.
%
%   SuperSegger_lifeHistory_based_features(SS_output_path, write_directory, intervalTime, 
%   AverageLength, AverageVelocity, AverageOrientation) analyzes the clist.mat file 
%   from SuperSegger's output directory to compute life-history based features for 
%   each bacterium. The results are written to a CSV file in the specified directory.
%
%   INPUTS:
%   SS_output_path - Directory path where SuperSegger's clist.mat file is located.
%   write_directory - The directory path where the output CSV file will be stored.
%   intervalTime - Time interval between frames.
%   AverageLength - Average length of the bacteria.
%   AverageVelocity - Average velocity of the bacteria.
%   AverageOrientation - Average orientation of the bacteria.
%
%   OUTPUTS:
%   None. The function writes the output directly to a CSV file.

% Load the clist.mat file from SuperSegger's output directory
load(strcat(SS_output_path, '/xy1/clist.mat'), 'data');

% Extract relevant data from the clist.mat file
cell_life_id_value = data(:, 1);     % Cell IDs
lifeHistory = data(:, 6) + 1;        % Life history of each bacterium (length of life)
birthLength = data(:, 10);           % Birth length of each bacterium
lastLength = data(:, 11);            % Final length of each bacterium

% Calculate growth rate for each bacterium
growth_rate = (log(lastLength) - log(birthLength)) ./ (lifeHistory * intervalTime);

% Create a table to store life-history based features
T = table(cell_life_id_value, growth_rate, birthLength, lifeHistory, transpose(AverageVelocity), ...
          transpose(AverageLength), transpose(AverageOrientation));
          
% Name the columns for clarity
T.Properties.VariableNames = {'CellId', 'GrowthRate', 'birthLength', 'LifeHistory', 'AverageVelocity', ...
                             'AverageLength', 'AverageOrientation'};

% Write the results to a CSV file
writetable(T, strcat(write_directory, '/SuperSegger_LifeHistory_based_Analysis.csv'), ...
           'Delimiter', ',', 'QuoteStrings', true);
end
