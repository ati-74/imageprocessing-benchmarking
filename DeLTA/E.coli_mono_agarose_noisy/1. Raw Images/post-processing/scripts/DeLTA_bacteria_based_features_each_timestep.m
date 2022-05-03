
load('../../2. results/Position000000.mat','res');

cellNumber=length(res{1}.lineage);

TimeStep=[];
cell_lable=[];
Orientation=[];
Center_X=[];
Center_Y=[];
major_axis = [];
minor_axis = [];
width = [];
height = [];


for i=1:cellNumber
    lifeHistoryValue=length(res{1}.lineage{i}.frames);
    for j=1:lifeHistoryValue
        TimeStep(end+1) = res{1}.lineage{i}.frames(j);
        cell_lable(end+1)=i;
        Orientation(end+1)=res{1}.lineage{i}.orientation(j);
        Center_X(end+1)=res{1}.lineage{i}.x_center(j);
        Center_Y(end+1)=res{1}.lineage{i}.y_center(j);
        major_axis(end+1)=res{1}.lineage{i}.length(j);
        minor_axis(end+1)=res{1}.lineage{i}.width(j);
        width(end+1)=res{1}.lineage{i}.absolute_width(j);
        height(end+1)=res{1}.lineage{i}.absolute_height(j);
    end   
end

%add to table
T = sortrows(table(transpose(TimeStep),transpose(cell_lable),transpose(Orientation),transpose(Center_X),transpose(Center_Y),transpose(major_axis),transpose(minor_axis),transpose(width),transpose(height)));
%add column name
T.Properties.VariableNames={'TimeStep','Cell_lable','Orientation','Center_X','Center_Y','Major_axis','Minor_axis','width','height'};

% write to csv
writetable(T,'../results/DeLTA_bacteria_feature_analysis.csv','Delimiter',',','QuoteStrings',true)
