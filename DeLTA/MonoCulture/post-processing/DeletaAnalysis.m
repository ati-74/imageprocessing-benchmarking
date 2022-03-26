
load('../MonoCulture/results/Position000000.mat','res');

cellNumber=length(res{1}.lineage);
timeStep=1.5;
minLife=2;

growth_rate=[];
birthLength=[];
lifeHistory=[];

first_frame=[];
last_frame=[];
number_of_cells_in_each_timesteps=[];

for i=1:cellNumber
    lifeHistoryValue=length(res{1}.lineage{i}.frames);
    Celllength=res{1}.lineage{i}.length;
    birthLengthValue=Celllength(1);
    lastLengthValue=Celllength(end);

    if lifeHistoryValue >= minLife
        growth_rateValue=(log(lastLengthValue)-log(birthLengthValue))/ (lifeHistoryValue * timeStep);
    else
        growth_rateValue=NaN;
    end
    
    firstFrameValue=res{1}.lineage{i}.frames(1);
    lastFrameValue=res{1}.lineage{i}.frames(end);
    %save Results
    growth_rate(end+1)=growth_rateValue;
    birthLength(end+1)=birthLengthValue;
    lifeHistory(end+1)=lifeHistoryValue;
    first_frame(end+1)=firstFrameValue;
    last_frame(end+1)=lastFrameValue;
end

Number_of_timesteps=max(last_frame);
cellLifeHistory=transpose([first_frame;last_frame]);
%number of cell per time steps
for j=1:Number_of_timesteps
    number_of_cells=length(cellLifeHistory(j>=cellLifeHistory(:,1) & j<= cellLifeHistory(:,2)));
    number_of_cells_in_each_timesteps(end+1)=number_of_cells;
end  

%add to table
T = table(transpose(1:length(growth_rate)),transpose(growth_rate),transpose(birthLength),transpose(lifeHistory));
T2=table(transpose(1:length(number_of_cells_in_each_timesteps)),transpose(number_of_cells_in_each_timesteps));
%add column name
T.Properties.VariableNames={'CellNumber','GrowthRate','BirthLength','LifeHistory'};
T2.Properties.VariableNames={'StepNumber','NumberOfCells'};

% write to csv
writetable(T,'results/DeLTAAnalysis.csv','Delimiter',',','QuoteStrings',true)
writetable(T2,'results/DeLTA_TimeSteps_Analysis.csv','Delimiter',',','QuoteStrings',true)


