function [] = DeLTA_bacteria_based_features_each_timestep(dataset,mode,num_time_steps,bac_lable)

write_directory = strcat('../',dataset,'/',mode,'/post-processing/results/');
load(strcat('../',dataset,'/',mode,'/2. results/Position000000.mat'),'res');

cellNumber=length(res{1}.lineage);

TimeStep=[];
cell_life_id=[];
Orientation=[];
Center_X=[];
Center_Y=[];
major_axis = [];
minor_axis = [];
width = [];
height = [];
bacteria_lable = [];


for i=1:cellNumber
    valid_frames_index = find(res{1}.lineage{i}.frames <=num_time_steps);
    valid_frames = res{1}.lineage{i}.frames(valid_frames_index);
    if isempty(valid_frames)==0    
        lifeHistoryValue=length(valid_frames);
        for j=1:lifeHistoryValue
            TimeStep(end+1) = res{1}.lineage{i}.frames(j);
            cell_life_id(end+1)=i;
            bacteria_lable(end+1) = bac_lable(i);
            Orientation(end+1)=res{1}.lineage{i}.orientation(j);
            Center_X(end+1)=res{1}.lineage{i}.x_center(j);
            Center_Y(end+1)=res{1}.lineage{i}.y_center(j);
            major_axis(end+1)=res{1}.lineage{i}.length(j);
            minor_axis(end+1)=res{1}.lineage{i}.width(j);
            width(end+1)=res{1}.lineage{i}.absolute_width(j);
            height(end+1)=res{1}.lineage{i}.absolute_height(j);
        end   
    end
end

%add to table
T = sortrows(table(transpose(TimeStep),transpose(cell_life_id),transpose(bacteria_lable),transpose(Orientation),transpose(Center_X),transpose(Center_Y),transpose(major_axis),transpose(minor_axis),transpose(width),transpose(height)));
%add column name
T.Properties.VariableNames={'TimeStep','CellLifeId','lable','Orientation','Center_X','Center_Y','Major_axis','Minor_axis','width','height'};

% write to csv
writetable(T,strcat(write_directory,'DeLTA_bacteria_feature_analysis.csv'),'Delimiter',',','QuoteStrings',true)
