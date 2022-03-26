
load('../../Tracks.mat','procTracks');

cellNumber=length(procTracks);
intervalTime=1.5;
minLife=2;

growth_rate=[];
birthLength=[];
lifeHistory=[];
velocity=[];
AverageVelocity=[];
number_of_cells_in_each_timesteps=[];

Number_of_timesteps=max(cell2mat({procTracks.end}));
cellLifeHistory=transpose([procTracks.start;procTracks.end]);

for i=1:cellNumber
    %bacteri length
    birthLengthValue= procTracks(i).majorLen(1);
    lastLengthValue= procTracks(i).majorLen(end);
    lifeHistoryValue=procTracks(i).length;

    if lifeHistoryValue >= minLife
        growth_rate_value=(log(lastLengthValue)-log(birthLengthValue))/(lifeHistoryValue*intervalTime);
    else
        growth_rate_value=NaN;
    end

    
    %average velocity
    x1=sqrt(procTracks(i).x(1)^2+procTracks(i).y(1)^2);
    x2=sqrt(procTracks(i).x(end)^2+procTracks(i).y(end)^2);
    AverageVelocityValue=(x2-x1)/(lifeHistoryValue*intervalTime);
    
    %save Results
    %append to list
    growth_rate(end+1)=growth_rate_value;
    birthLength(end+1)=birthLengthValue;
    lifeHistory(end+1)=lifeHistoryValue;
    AverageVelocity(end+1)=AverageVelocityValue;
end


%number of cell per time steps
for j=1:Number_of_timesteps
    number_of_cells=length(cellLifeHistory(j>=cellLifeHistory(:,1) & j<= cellLifeHistory(:,2)));
    number_of_cells_in_each_timesteps(end+1)=number_of_cells;
end    



%add to table
T = table(transpose(1:length(growth_rate)),transpose(growth_rate),transpose(birthLength),transpose(lifeHistory),transpose(AverageVelocity));
T2=table(transpose(1:length(number_of_cells_in_each_timesteps)),transpose(number_of_cells_in_each_timesteps));
%add column name
T.Properties.VariableNames={'CellNumber','GrowthRate','BirthLength','LifeHistory','AverageVelocity'};
T2.Properties.VariableNames={'StepNumber','NumberOfCells'};

% write to csv
writetable(T,'../results/FASTAnalysis.csv','Delimiter',',','QuoteStrings',true)
writetable(T2,'../results/FAST_TimeSteps_Analysis.csv','Delimiter',',','QuoteStrings',true)

