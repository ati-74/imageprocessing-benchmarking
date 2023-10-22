function [T, AverageLength, AverageVelocity, AverageOrientation] = SuperSegger_bacteria_based_features_each_timestep(ss_output_directory, write_directory, bac_label, intervalTime)
%SuperSegger_bacteria_based_features_each_timestep Extracts features for bacteria based on each timestep.
%
%   [T, AverageLength, AverageVelocity, AverageOrientation] = SuperSegger_bacteria_based_features_each_timestep(ss_output_directory, write_directory, bac_label, intervalTime) 
%   analyzes the provided SuperSegger output directory to extract and compute various 
%   bacterial features per time step. The results are then written to a CSV file in the specified directory.
%
%   INPUTS:
%   ss_output_directory - Directory path where SuperSegger's output files are located.
%   write_directory - Directory path where the resulting CSV file will be stored.
%   bac_label - Vector containing labels for bacteria.
%   intervalTime - Time interval between frames.
%
%   OUTPUTS:
%   T - Table containing extracted bacterial features.
%   AverageLength - Average length of bacteria during its life history.
%   AverageVelocity - Average velocity of the bacteria.
%   AverageOrientation - Average orientation of the bacteria.

% Load clist.mat file from SuperSegger's output directory and the crop box
load(strcat(ss_output_directory,'/xy1/clist.mat'),'data');
directory = strcat(ss_output_directory,'/xy1/cell/');
files = dir([strcat(directory,'*.mat')]);
% crop box
load(strcat(ss_output_directory,'/raw_im/cropbox.mat'),'crop_box_array');


% Initialize parameters
% number of time steps
num_time_steps = max(data(:, 5));

%sorted files
sorted_files = natsortfiles(files);
%number of files
Num_cell_files = length(sorted_files);

TimeStep_of_bacteria = zeros(1, sum(data(:, 6) + 1) );
cell_life_id_value = zeros(1, sum(data(:, 6) + 1) );
orientation =  zeros(1, sum(data(:, 6) + 1) );
Center_X = zeros(1, sum(data(:, 6) + 1) );
Center_Y =  zeros(1, sum(data(:, 6) + 1) );
major_axis = zeros(1, sum(data(:, 6) + 1) );
minor_axis = zeros(1, sum(data(:, 6) + 1) );
% tracking information
parent = zeros(1, sum(data(:, 6) + 1) );
daughter1 = zeros(1, sum(data(:, 6) + 1) );
daughter2 = zeros(1, sum(data(:, 6) + 1) );
bacteria_label = zeros(1, sum(data(:, 6) + 1) );

% average length of bacteria during its life history
AverageLength = NaN(1, Num_cell_files);
% average velocity of bacteria
AverageVelocity = NaN(1, Num_cell_files);
AverageOrientation = NaN(1, Num_cell_files);

% cell index in all matrices
cell_index = 1;

% Loop to compute various bacterial features per timestep
for i = 1:Num_cell_files
    
    file_name=sorted_files(i).name;
    % load `.mat` file
    cell = load(strcat(directory,file_name));
    life_history = length(cell.CellA);
    bacteria_life_history = 0;
    
    for j=1:life_history
        living_time_step = cell.birth + j - 1;
        
        if living_time_step <= num_time_steps && living_time_step <= cell.death ...
            && isnan(cell.CellA{1,j}.coord.r_center(1)) == 0
              
            bacteria_life_history = bacteria_life_history + 1;
            TimeStep_of_bacteria(cell_index)= living_time_step;
            cell_life_id_value(cell_index) = i;
            % each bacteria_label matrix cell shows the label of bacteria corresponding to one cell.mat file 
            bacteria_label(cell_index) = bac_label(i);
            % center coordinate
            Center_X(cell_index) = cell.CellA{1,j}.coord.r_center(1) - crop_box_array{1, 1}(living_time_step, 2);
            Center_Y(cell_index) = cell.CellA{1,j}.coord.r_center(2) - crop_box_array{1, 1}(living_time_step, 1);
            % minor and major axis length
            major_axis(cell_index) = cell.CellA{1,j}.cellLength(1);
            minor_axis(cell_index) = cell.CellA{1,j}.cellLength(2);
            % orientation (radian)
            orientation(cell_index) = cell.CellA{1,j}.coord.orientation * pi / 180;
            % tracking information
            parent(cell_index) = cell.motherID;
            if isempty(cell.daughterID)
                daughter1(cell_index) = 0;
                daughter2(cell_index) = 0;             
            else
                daughter1(cell_index) = cell.daughterID(1);
                daughter2(cell_index) = cell.daughterID(2);                
            end

            
            cell_index = cell_index + 1;
            % cell length of bacteria during its life history
        end
    end
    
    first_frame = cell.birth;
    % last time step of bacterium life
    last_frame = min(min(living_time_step, num_time_steps), cell.death);
    % length of bacterium life history: data(i, 6)
    if bacteria_life_history > 1
        mean_length_of_bacterium = mean(cellfun(@(x) x.cellLength(1), cell.CellA(1, 1: bacteria_life_history)));
        AverageOrientationValue = mean(cellfun(@(x) x.coord.orientation * pi / 180, cell.CellA(1, 1: bacteria_life_history)));
        
        % calculate velocity
        x_x1 = cell.CellA{1,1}.coord.r_center(1) - crop_box_array{1, 1}(first_frame, 2);
        y_x1 = cell.CellA{1,1}.coord.r_center(1) - crop_box_array{1, 1}(first_frame, 1);
        x1 = sqrt(x_x1^2 + y_x1^2);

        x_x2 = cell.CellA{1, bacteria_life_history}.coord.r_center(1) - crop_box_array{1, 1}(last_frame, 2);
        y_x2 = cell.CellA{1, bacteria_life_history}.coord.r_center(2) - crop_box_array{1, 1}(last_frame, 1);
        x2 = sqrt(x_x2^2 + y_x2^2);

        AverageVelocityValue= (x2-x1) / ((bacteria_life_history) * intervalTime);
        
    else
        mean_length_of_bacterium = NaN;
        AverageVelocityValue = NaN;
        AverageOrientationValue = NaN;
    end
    AverageLength(i) = mean_length_of_bacterium;
    AverageVelocity(i) = AverageVelocityValue;
    AverageOrientation(i) = AverageOrientationValue;
end

% Create and sort the results table
T = sortrows(table(transpose(TimeStep_of_bacteria), transpose(cell_life_id_value), transpose(bacteria_label),...
    transpose(orientation), transpose(Center_X), transpose(Center_Y), transpose(major_axis),...
    transpose(minor_axis), transpose(parent),  transpose(daughter1), transpose(daughter2)));
%add column name
T.Properties.VariableNames={'TimeStep', 'CellLifeId', 'label', 'Orientation', 'Center_X', 'Center_Y', ...
    'Major_axis', 'Minor_axis', 'parent', 'daughter1', 'daughter2'};
T(T.TimeStep == 0,:)=[];

% write to csv
%life history based features
writetable(T,strcat(write_directory, '/SuperSegger_bacteria_feature_analysis.csv'), ...
    'Delimiter', ',', 'QuoteStrings', true);


