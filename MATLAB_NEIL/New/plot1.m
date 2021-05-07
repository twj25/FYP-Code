%direc = '/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/Clear/';
direc = '/Users/tomjo/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Final System Data/mercedes/5577/2018/Sep/Sorted By CNN/Almost_Clear/';
folder_details = dir(direc);
%file_names = string([folder_details.name]);
file_names = extractfield(folder_details,'name');

file = string(file_names{3});
disp(file)
file_path = string(direc) + '/' + file;
[X,Y,ST] = run_2DST(file_path);
amp_matrix = ST.A;
max_amps(date) = max(max(ST.A));


plot = 1;
skip_num = round(numel(file_names)/10);
%skip_num = 1;
for i = 4:skip_num:numel(file_names)
    file = string(file_names{i});
    disp(file)
    file_path = string(direc) + '/' + file;
    [X,Y,ST] = run_2DST(file_path);
    
    amp_matrix = cat(3, amp_matrix, ST.A);
%     figure(1)
%     subplot(2,5,plot); pcolor(X,Y,ST.IN); shading flat; axis square; set(gca,'tickdir','out')
%     title('Input')
%     colormap('gray')
%     xlabel('px');
%     ylabel('px');
%     
%     figure(2)
%     subplot(2,5,plot); pcolor(X,Y,ST.A); shading flat; axis square; set(gca,'tickdir','out')
%     title('ST amplitude')
%     set(gca,'clim',[0 10]);
%     %colorbar('location','southoutside')
%     xlabel('km');
%     ylabel('km');
%     plot = plot+1;
end

mean_amp = mean(amp_matrix,3);
median_amp = median(amp_matrix,3);
figure(3)
pcolor(X,Y,mean_amp); shading flat; axis square; set(gca,'tickdir','out')
title('Mean Amplitude')
set(gca,'clim',[0 10]);
colorbar('location','southoutside')
xlabel('km');
ylabel('km');
figure(4)
pcolor(X,Y,median_amp); shading flat; axis square; set(gca,'tickdir','out')
title('Median Amplitude')
set(gca,'clim',[0 10]);
colorbar('location','southoutside')
xlabel('km');
ylabel('km');
