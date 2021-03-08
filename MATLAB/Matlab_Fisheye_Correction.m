images = imageDatastore(fullfile(toolboxdir('vision'),'visiondata','calibration','gopro'));

%Detect the calibration pattern from the images.
[imagePoints,boardSize] = detectCheckerboardPoints(images.Files);

%Generate world coordinates for the corners of the checkerboard squares.
squareSize = 29; % millimeters
worldPoints = generateCheckerboardPoints(boardSize,squareSize);

%Estimate the fisheye camera calibration parameters based on the image and world points. Use the first image to get the image size.
I = readimage(images,1); 
imageSize = [size(I,1) size(I,2)];
params = estimateFisheyeParameters(imagePoints,worldPoints,imageSize);

%Remove lens distortion from the first image I and display the results.
J1 = undistortFisheyeImage(I,params.Intrinsics);
figure
imshowpair(I,J1,'montage')
title('Original Image (left) vs. Corrected Image (right)')

J2 = undistortFisheyeImage(I,params.Intrinsics,'OutputView','full');
figure
imshow(J2)
title('Full Output View')