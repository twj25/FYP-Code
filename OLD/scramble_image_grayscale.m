% Demo to use randperm() to scramble the pixel locations in a gray scale image, then undo the scrambling to obtain the original image again.
clc;
clearvars;
close all;
workspace;
fontSize = 16;

% Read in a gray scale demo image.
folder = fileparts(which('cameraman.tif')); % Determine where demo folder is (works with all versions).
baseFileName = 'cameraman.tif';
% Get the full filename, with path prepended.
fullFileName = fullfile(folder, baseFileName);
if ~exist(fullFileName, 'file')
	% Didn't find it there.  Check the search path for it.
	fullFileName = baseFileName; % No path this time.
	if ~exist(fullFileName, 'file')
		% Still didn't find it.  Alert user.
		errorMessage = sprintf('Error: %s does not exist.', fullFileName);
		uiwait(warndlg(errorMessage));
		return;
	end
end
grayImage = imread(fullFileName);
% Get the dimensions of the image.  numberOfColorBands should be = 1.
[rows, columns, numberOfColorBands] = size(grayImage);
if numberOfColorBands > 1
	grayImage = rgb2gray(grayImage); % Convert to gray level.
end
% Display the original gray scale image.
subplot(2, 2, 1);
imshow(grayImage);
title('Original Gray Scale Image', 'FontSize', fontSize);
% Enlarge figure to full screen.
set(gcf, 'units','normalized','outerposition',[0 0 1 1]);
% Give a name to the title bar.
set(gcf, 'Name', 'Demo by ImageAnalyst', 'NumberTitle', 'Off') 

% Get the order to scramble them in 
scrambleOrder = randperm(rows*columns);

% Scramble according to the scrambling order.
grayImage = grayImage(scrambleOrder);

% Reshape into a 2D image
scrambledImage = reshape(grayImage, [rows, columns]);

% Display the scrambled gray scale image.
subplot(2, 2, 2);
imshow(scrambledImage);
title('Scrambled Gray Scale Image', 'FontSize', fontSize);

% Recover the image, knowing the sort order
recoverOrder = zeros([rows*columns], 2);
recoverOrder(:, 1) = 1 : (rows*columns);
recoverOrder(:, 2) = scrambleOrder;
% Sort this to find out where each scrambled location needs to be sent to.
newOrder = sortrows(recoverOrder, 2);
% Extract just column 1, which is the order we need.
newOrder = newOrder(:,1);
% Unscramble according to the recoverOrder order.
grayImage = grayImage(newOrder);
% Reshape into a 2D image
scrambledImage = reshape(grayImage, [rows, columns]);

% Display the original gray scale image.
subplot(2, 2, 3);
imshow(scrambledImage);
title('Unscrambled Gray Scale Image', 'FontSize', fontSize);
