%direc = '/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/Clear/';
direc = '/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Final System Data/mercedes/5577/2018/Sep/Sorted By CNN/Almost_Clear';
folder_details = dir(direc);
%file_names = string([folder_details.name]);
file_names = extractfield(folder_details,'name');

max_amps = zeros(1,30);

file = string(file_names{3});
date = split(file,'_');
date = str2num(date(3));
file_path = string(direc) + '/' + file;
[X,Y,ST] = run_2DST(file_path);
amp_matrix = ST.A;
max_amps(date) = max(max(ST.A));

%skip_num = round(numel(file_names)/10);
skip_num = 1;
for i = 4:skip_num:numel(file_names)
    file = string(file_names{i});
    date = split(file,'_');
    date = str2num(date(3));
    disp(file)
    file_path = string(direc) + '/' + file;
    [X,Y,ST] = run_2DST(file_path);
    max_amp = max(max(ST.A));
    if max_amp > max_amps(date)
        max_amps(date) = max_amp;
    end
end
