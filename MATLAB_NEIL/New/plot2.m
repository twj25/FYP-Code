%direc = '/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/Clear/';
%direc = '/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Final System Data/mcdonald/5577/2018/Jul/Sorted By CNN/Almost_Clear';
direc = '/Users/tomjo/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Final System Data/mercedes/5577/2020/Aug/Hand Picked';
folder_details = dir(direc);
%file_names = string([folder_details.name]);
file_names = extractfield(folder_details,'name');

dates_completed = zeros(1,30);

%% Do the first file in the folder
file = string(file_names{3});
date = split(file,'_');
date = str2num(date(3));
disp(file)
file_path = string(direc) + '/' + file;
[X,Y,ST] = run_2DST(file_path);
flat_amps = reshape(ST.A,[],1);
flat_amps_matrix = double(flat_amps);
date_log = date;

%% Loop over the rest of the files
%skip_num = round(numel(file_names)/10);
skip_num = 1;

for i = 4:skip_num:numel(file_names)
    
    % Get the file name
    file = string(file_names{i});
    % Get the date
    date = split(file,'_');
    date = str2num(date(3));
    disp(file)
    
    % If the date has been done before then skip
    if dates_completed(date) == 0
        file_path = string(direc) + '/' + file;
        [X,Y,ST] = run_2DST(file_path);
        
        flat_amps = reshape(ST.A,[],1);
        flat_amps = double(flat_amps);
        
        flat_amps_matrix = cat(2,flat_amps_matrix,flat_amps);
        
        date_log = [date_log;date];
        dates_completed(date) = 1;
    end
end

[~,id]=sort(date_log);
C=flat_amps_matrix(id,:);

%% To order days

% 1. Prime matrix to swap rows and colums
% 2. Add dates as first column
% 3. Use sortrows(matrix, 1)
% 4. Unprime matrix

figure(); boxplot(flat_amps_matrix);
