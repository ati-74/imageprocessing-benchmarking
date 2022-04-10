
load('../../Tracks.mat','procTracks');

cellNumber=length(procTracks);
intervalTime=1;
minLife=2;

growth_rate=[];
birthLength=[];
lifeHistory=[];
velocity=[];
AverageVelocity=[];
AverageLength=[];

for i=1:cellNumber
    %bacteri length
    birthLengthValue= procTracks(i).majorLen(1);
    lastLengthValue= procTracks(i).majorLen(end);
    lifeHistoryValue=procTracks(i).length;
    meanLength=mean(procTracks(i).majorLen);

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
    AverageLength(end+1)=meanLength;
end


%add to table
T = table(transpose(1:length(growth_rate)),transpose(growth_rate),transpose(birthLength),transpose(lifeHistory),transpose(AverageVelocity),transpose(AverageLength));
%add column name
T.Properties.VariableNames={'CellNumber','GrowthRate','birthLength','LifeHistory','AverageVelocity','AverageLength'};

% write to csv
writetable(T,'../results/FAST_LifeHistory_based_Analysis.csv','Delimiter',',','QuoteStrings',true)
