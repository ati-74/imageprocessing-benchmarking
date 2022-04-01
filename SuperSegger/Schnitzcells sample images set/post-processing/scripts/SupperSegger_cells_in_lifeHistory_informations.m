
%find .mat files in cell directory
directory='../../xy1/cell/';
files=dir([strcat(directory,'*.mat')]);
%sorted files
sorted_files = natsortfiles(files);
%number of files
Num_files=length(sorted_files);

AverageVelocity=[];
AverageLength=[];
AverageOrientation=[];

intervalTime=1.5;

for i=1:Num_files
    file_name=sorted_files(i).name;
    % load `.mat` file
    load(strcat(directory,file_name),'CellA');
    life_history=length(CellA);
    
    %store length and orientation of cell
    cell_length=[];
    cell_orientation=[];
    
    for j=1:life_history
    cell_length(end+1)=CellA{1,j}.cellLength(1);
    %degree
    cell_orientation(end+1)=CellA{1,j}.coord.orientation;
    end
    %mean length
    meanLength=mean(cell_length);
    meanOrientation=mean(cell_orientation);
    %average velocity
    x1=sqrt(CellA{1,1}.coord.r_center(1)^2+CellA{1,1}.coord.r_center(2)^2);
    x2=sqrt(CellA{1,end}.coord.r_center(1)^2+CellA{1,end}.coord.r_center(2)^2);
    AverageVelocityValue=(x2-x1)/(life_history*intervalTime);
    AverageVelocity(end+1)=AverageVelocityValue;
    AverageLength(end+1)=meanLength;
    AverageOrientation(end+1)=meanOrientation;
end

%add to table
T = table(transpose(1:length(AverageVelocity)),transpose(AverageVelocity),transpose(AverageLength),transpose(AverageOrientation));
%add column name
T.Properties.VariableNames={'CellNumber','AverageVelocity','AverageLength','AverageOrientation'};

% write to csv
writetable(T,'../results/SuperSegger_lifeHistory_Analysis.csv','Delimiter',',','QuoteStrings',true)



