function [] = FAST_lifeHistory_based_features(FAST_output_path, write_directory, intervalTime, AverageLength, AverageVelocity, AverageOrientation)
%FAST_lifeHistory_based_features Generates features based on the life history of bacteria.
%
% This function calculates various features based on the life history of bacteria 
% using the FAST output data. It then writes these calculated features to a CSV file.
%
% Inputs:
%   FAST_output_path: Directory path where the FAST output data is located.
%   write_directory: Directory path where the results should be written.
%   intervalTime: Time interval for which the features are calculated.
%   AverageLength: Average length of the bacteria over its lifetime.
%   AverageVelocity: Average velocity of the bacteria over its lifetime.
%   AverageOrientation: Average orientation of the bacteria over its lifetime.

% Load tracking and metadata information
load(strcat(FAST_output_path, '/Tracks.mat'), 'procTracks');
load(strcat(FAST_output_path, '/Metadata.mat'), 'metaStore');

% Determine bacteria IDs
cell_life_id_value = 1:size(procTracks, 2);
% Compute the length of life history for each bacterium
lifeHistory = [procTracks(:).length];
% Initialize variables for birth and last length of bacteria
birthLength = zeros(1, cell_life_id_value(end));
lastLength = zeros(1, cell_life_id_value(end));
% Initialize growth rate variable
growth_rate = NaN(1, cell_life_id_value(end));

% Loop through each bacterium and compute birth, last lengths, and growth rate
for i = 1:cell_life_id_value(end)
    if metaStore.dx ~= 0.5
        birthLength(i) = procTracks(i).majorLen(1) / (metaStore.dx * 2);
        lastLength(i) = procTracks(i).majorLen(end) / (metaStore.dy * 2);
    else
        birthLength(i) = procTracks(i).majorLen(1);
        lastLength(i) = procTracks(i).majorLen(end);
    end
    
    if lifeHistory(i) >= 2
        growth_rate(i) = (lastLength(i) - birthLength(i)) / (lifeHistory(i) * intervalTime);
    end
end

% Organize the computed data into a table
T = table(transpose(cell_life_id_value), transpose(growth_rate), transpose(birthLength),...
    transpose(lifeHistory), transpose(AverageVelocity), transpose(AverageLength), transpose(AverageOrientation));
% Set the table column names
T.Properties.VariableNames={'CellId', 'GrowthRate', 'birthLength', 'LifeHistory', 'AverageVelocity',...
    'AverageLength', 'AverageOrientation'};

% write to csv
%life history based features
writetable(T,strcat(write_directory, '/FAST_LifeHistory_based_Analysis.csv'),...
    'Delimiter', ',' ,'QuoteStrings',true)
