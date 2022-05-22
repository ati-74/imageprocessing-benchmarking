
load('../../Tracks.mat','procTracks');

cellNumber=length(procTracks);

TimeStep = [];
cellNumber_value = [];
orientation=[];
Center_X=[];
Center_Y=[];
major_axis=[];
minor_axis=[];



for i=1:cellNumber
    Timesteps_num = size(procTracks(i).times);
    for j=1:Timesteps_num(2)
        TimeStep(end+1)=procTracks(i).times(j);
        cellNumber_value(end+1) = i;
        orientation (end+1) = procTracks(i).phi(j); 
        Center_X (end+1) = procTracks(i).x(j); 
        Center_Y (end+1) = procTracks(i).y(j); 
        major_axis (end+1) = procTracks(i).majorLen(j); 
        minor_axis (end+1) = procTracks(i).minorLen(j); 
    end
end


%add to sorted table
T = sortrows(table(transpose(TimeStep),transpose(cellNumber_value),transpose(orientation),transpose(Center_X),transpose(Center_Y),transpose(major_axis),transpose(minor_axis)));
%add column name
T.Properties.VariableNames={'TimeStep','CellNumber','Orientation','Center_X','Center_Y','Major_axis','Minor_axis'};

% write to csv
writetable(T,'../results/FAST_bacteria_feature_analysis.csv','Delimiter',',','QuoteStrings',true)
