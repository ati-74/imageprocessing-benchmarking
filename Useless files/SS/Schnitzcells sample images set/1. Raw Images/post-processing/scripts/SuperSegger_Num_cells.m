
load('../../xy1/clist.mat','data');

number_of_cells_in_each_timesteps=[];

Number_of_timesteps=max(data(:,5));
cellLifeHistory=[data(:,4),data(:,5)];

%number of cell per time steps
for j=1:Number_of_timesteps
    number_of_cells=length(cellLifeHistory(j>=cellLifeHistory(:,1) & j<= cellLifeHistory(:,2)));
    number_of_cells_in_each_timesteps(end+1)=number_of_cells;
end  


%add to table
T2=table(transpose(1:length(number_of_cells_in_each_timesteps)),transpose(number_of_cells_in_each_timesteps));
%add column name
T2.Properties.VariableNames={'StepNumber','NumberOfCells'};

% write to csv
writetable(T2,'../results/SuperSegger_Num_cells_in_each_timeStep.csv','Delimiter',',','QuoteStrings',true)
