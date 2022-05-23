function [] = ExtractCellFeatures(dataset,mode)

load(strcat('../../',dataset,'/',mode,'/seg.mat'),'cellList');
write_directory = strcat('../../',dataset,'/',mode,'/post-processing/results/');

%number of time steps
TimeSteps=length(cellList.cellId);

StepNum=[];
CellId=[];
x_center=[];
y_center=[];
Orientation=[];
Major_axis=[];
Minor_axis = [];
parent=[];
num_cells=[];
lable = [];
width = [];
height = [];

%lable dictionary
last_lable_value=0;
lable_dict=containers.Map(0,0);


for i=1:TimeSteps
    Num_cells=length(cellList.cellId{1, i});
    valid_num_cell = 0;
    for j=1:Num_cells
        StepNum(end+1)=i;
        % unique id for each cell in its life history
        cellId_value = cellList.cellId{1, i}(j);
        CellId(end+1)= cellId_value;
        
        %fit ellipse
        if cellList.meshData{1, i}{1, j}.mesh(1) >= 5
            x=[cellList.meshData{1, i}{1, j}.mesh(:,1);cellList.meshData{1, i}{1, j}.mesh(:,3)];
            y=[cellList.meshData{1, i}{1, j}.mesh(:,2);cellList.meshData{1, i}{1, j}.mesh(:,4)];
            elFit = fit_ellipse(x,y);
            if  isempty( elFit.long_axis ) ==0
                %in degree
                Orientation(end+1) = mod(rad2deg(elFit.phi)+180,180)-90;
                Major_axis(end+1) = elFit.long_axis;
                Minor_axis(end+1) = elFit.short_axis;
                % X0          - center at the X axis of the non-tilt ellipse
                % Y0          - center at the Y axis of the non-tilt ellipse
                x_center(end+1)=elFit.X0_in;
                y_center(end+1)=elFit.Y0_in;
                valid_num_cell=valid_num_cell+1;
                height(end+1) = elFit.b;
                width(end+1) = elFit.a; 
            else
               Orientation(end+1)=0;
               Major_axis(end+1)=0;
               Minor_axis(end+1)=0;
               x_center(end+1)=0;
               y_center(end+1)=0;
               height(end+1) = 0;
               width(end+1) = 0;                
            end
        else
           Orientation(end+1)=0;
           Major_axis(end+1)=0;
           Minor_axis(end+1)=0;
           x_center(end+1)=0;
           y_center(end+1)=0;
           height(end+1) = 0;
           width(end+1) = 0;
        end
%parent details
        if length(cellList.meshData{1, i}{1, j}.ancestors) == 0
            parent(end+1)=0;  
            %lable
            if isKey(lable_dict,cellId_value) ==1
                lable(end+1) = lable_dict (cellId_value);
            else
                if  Major_axis(end) == 0 %invalid cell
                    lable_dict (cellId_value) = 0;
                    lable(end+1) = 0;
                else
                    last_lable_value = last_lable_value+1;
                    lable_dict (cellId_value) = last_lable_value;
                    lable(end+1) = last_lable_value; 
                end
            end
        else
            parent_id = cellList.meshData{1, i}{1, j}.ancestors(end);
            parent(end+1)= parent_id;
            first_ancestor_id = cellList.meshData{1, i}{1, j}.ancestors(1);
            lable(end+1) = lable_dict (first_ancestor_id);
        end
    end
    num_cells(end+1) = valid_num_cell;
end


%add to table
T = table(transpose(StepNum),transpose(CellId),transpose(x_center),transpose(y_center),transpose(Orientation),transpose(Major_axis),transpose(Minor_axis),transpose(lable),transpose(parent),transpose(height),transpose(width));
T2=table(transpose(1:length(transpose(num_cells))),transpose(num_cells));
%add column name
T.Properties.VariableNames={'TimeStep','CellLifeId','Center_X','Center_Y','Orientation','Major_axis','Minor_axis','lable','parent','height','width'};
T2.Properties.VariableNames={'StepNumber','NumberOfCells'};

% remove unwanted rows (Major_axis = 0)
T(ismember(T.Major_axis,0),:)=[];

% write to csv
writetable(T,strcat(write_directory,'Oufti_bacteria_feature_analysis.csv'),'Delimiter',',','QuoteStrings',true)
writetable(T2,strcat(write_directory,'Oufti_Num_cells_in_each_timeStep.csv'),'Delimiter',',','QuoteStrings',true)

