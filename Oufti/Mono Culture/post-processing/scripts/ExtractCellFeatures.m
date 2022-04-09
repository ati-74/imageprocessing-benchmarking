
load('../../seg.mat','cellList');

%number of time steps
TimeSteps=length(cellList.cellId);

StepNum=[];
CellId=[];
x_center=[];
y_center=[];
Orientation=[];
MajorAxisLength=[];
parent=[];
num_cells=[];
lable = [];

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
            %in degree
            Orientation(end+1) = mod(rad2deg(elFit.phi)+180,180)-90;
            MajorAxisLength(end+1) = elFit.long_axis;
            % X0          - center at the X axis of the non-tilt ellipse
            % Y0          - center at the Y axis of the non-tilt ellipse
            x_center(end+1)=elFit.X0;
            y_center(end+1)=elFit.Y0;
            valid_num_cell=valid_num_cell+1;
        else
           Orientation(end+1)=0;
           MajorAxisLength(end+1)=0;
           x_center(end+1)=0;
           y_center(end+1)=0;
        end
%parent details
        if length(cellList.meshData{1, i}{1, j}.ancestors) == 0
            parent(end+1)=0;  
            %lable
            if isKey(lable_dict,cellId_value) ==1
                lable(end+1) = lable_dict (cellId_value);
            else
                if  MajorAxisLength(end) == 0 %invalid cell
                    lable_dict (cellId_value) = 0;
                    cellId_value
                    lable_dict (cellId_value)
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
T = table(transpose(StepNum),transpose(CellId),transpose(x_center),transpose(y_center),transpose(Orientation),transpose(MajorAxisLength),transpose(lable),transpose(parent));
T2=table(transpose(1:length(transpose(num_cells))),transpose(num_cells));
%add column name
T.Properties.VariableNames={'TimeStep','CellId','Center_X','Center_Y','Orientation','MajorAxisLength','lable','parent'};
T2.Properties.VariableNames={'StepNumber','NumberOfCells'};

% remove unwanted rows (MajorAxisLength = 0)
T(ismember(T.MajorAxisLength,0),:)=[];

% write to csv
writetable(T,'../results/Oufti_bacteria_feature_analysis.csv','Delimiter',',','QuoteStrings',true)
writetable(T2,'../results/Oufti_Num_cells_in_each_timeStep.csv','Delimiter',',','QuoteStrings',true)

