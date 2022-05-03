%find .mat files in cell directory
directory='../4. selected segmentation images/';
files=dir([strcat(directory,'*.tif')]);
%sorted files
sorted_files = natsortfiles(files);
%number of files
Num_files=length(sorted_files);

for i=1:Num_files
    file_name=sorted_files(i).name;
    bw = imread(strcat(directory,file_name));
    num_digit = numel(num2str(i));
    if num_digit ==1
        img_name = strcat('final/Xantamonase_T00', int2str(i),'.tif');
    elseif num_digit ==2
           img_name = strcat('final/Xantamonase_T0', int2str(i),'.tif'); 
    else
        img_name = strcat('final/Xantamonase_T', int2str(i),'.tif'); 
    end
    imwrite(bw,img_name);
end