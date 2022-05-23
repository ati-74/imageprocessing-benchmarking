
%find .mat files in cell directory
directory='../../xy1/cell/';
files=dir([strcat(directory,'*.mat')]);
%sorted files
sorted_files = natsortfiles(files);
%number of files
Num_files=length(sorted_files);
num_time_steps = 19;

TimeStep = [];
cellNumber_value = [];
orientation=[];
Center_X=[];
Center_Y=[];
major_axis = [];
minor_axis = [];

for i=1:Num_files
    file_name=sorted_files(i).name;
    % load `.mat` file
    load(strcat(directory,file_name));
    life_history=length(CellA);
    
    for j=1:life_history
        if birth+j-1 <= num_time_steps
            TimeStep(end+1)=birth+j-1;
            cellNumber_value(end+1) = i;
            orientation (end+1) = CellA{1,j}.coord.orientation;
            Center_X (end+1) = CellA{1,j}.coord.r_center(1);
            Center_Y (end+1) = CellA{1,j}.coord.r_center(2);
            major_axis (end+1) = CellA{1,j}.cellLength(1);
            minor_axis (end+1) = CellA{1,j}.cellLength(2);
        end
    end
end

%add to sorted table
T = sortrows(table(transpose(TimeStep),transpose(cellNumber_value),transpose(orientation),transpose(Center_X),transpose(Center_Y),transpose(major_axis),transpose(minor_axis)));
%add column name
T.Properties.VariableNames={'TimeStep','CellNumber','Orientation','Center_X','Center_Y','Major_axis','Minor_axis'};

% write to csv
%life history based features
writetable(T,'../results/SuperSegger_bacteria_feature_analysis.csv','Delimiter',',','QuoteStrings',true)

