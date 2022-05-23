%find .mat files in cell directory
directory='../3. Object Classification/';
files=dir([strcat(directory,'*.tif')]);
%sorted files
sorted_files = natsortfiles(files);
%number of files
Num_files=length(sorted_files);

for i=1:Num_files
    file_name=sorted_files(i).name;
    bw = imread(strcat(directory,file_name));
    bw2 = imcomplement(bw);
    imwrite(bw2,file_name);
end