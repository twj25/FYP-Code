
%%
%%%% code to demonstrate how to convert an airglow image to a regular
%%%% distance grid, and find the new lat and lon or this regular grid.

%%%% ASSUMPTIONS
% Our input data is an MxN pixel image.
% We're going to assume that:
% 1. the image is YxX, where X is in the west->east direction and Y is in
% the north->south direction. If this is wrong we can just flip the image
% using the ' operator. ***This is something we'll need to check first***
% 2. The edges of the image are at zenith angles of 90 degrees (i.e.
% directed towards the horizon) and the centre is pointing straight up at
% the zenith.
% 3. The pixels of the image lie at uniform steps in zenith angle, i.e.
% starting from one horizon and smoothly stepping up the the zenith and
% down to the opposite horizon. This assumes the lens is a perfect half
% sphere I think. Without having the exact specifications of the camera's
% lens from the manufacturer, we have no idea if this is true.
% So let's assume it is :)


%%%% SCRIPT SECTION:

filepath = '/Users/tomjo/OneDrive/Documents/50 University/Year 5/Individual Proj/Code/mcdonald_5577_10_Apr_2019_T053317A100_.gif';
% change this for each file

% height of the airglow layer above the ground
h = 90; % km (TOM CHECK THIS)

% Camera Lat/Lon (I don't know this, so I chose my house!)
cameralat = 30;
cameralon = -104;


% define a new regular distance  grid:
dx = 1; % spacing between points on new grid (km). Use a finer grid spacing if you want, but it'll take longer.
gridlim = 500; % km, I assume we want another square...
[newgridX,newgridY] = ndgrid(-gridlim:dx:gridlim,-gridlim:dx:gridlim);

% apply my function below:
[regridded_image,x_in,y_in,Lat,Lon] = regridairglowimage(filepath,cameralat,cameralon,h,newgridX,newgridY);



%%%% Make some figs to check our working

figure; set(gcf,'color','w');

Z = double(flip(imread(filepath),1));

%%%% First the input image
subplot(1,4,1); pcolor(Z); shading flat; axis square; set(gca,'tickdir','out')
title('input image')
colormap('gray')
xlabel('px');
ylabel('px');

%%%% now the image on a distance grid
subplot(1,4,2); pcolor(x_in,y_in,Z); shading flat; axis square; set(gca,'tickdir','out')
title('image on the current "pixel" distance grid (km)')
xlabel('km');
ylabel('km');
xlim(x_in(floor(size(Z,1)/2),[1 end]))
ylim(y_in([1 end],floor(size(Z,2)/2)))
colormap('gray')
% add a boundary:
boundary = 100;
bx = boundary.*[-1 1 1 -1 -1];
by = boundary.*[-1 -1 1 1 -1];
hold on; plot(bx,by,'m');

%%%% now the new regridded image on the new regular distance grid
subplot(1,4,3); pcolor(newgridX,newgridY,regridded_image); shading flat; axis square; set(gca,'tickdir','out')
title('image on new regular distance grid (zoomed in)')
xlim(2.*[-boundary boundary])
ylim(2.*[-boundary boundary])
xlabel('km');
ylabel('km'); 
colormap('gray')
% add that same boundary:
hold on; plot(bx,by,'m');

%%%% and finally the regridded image on a new lat lon grid
subplot(1,4,4); pcolor(Lon,Lat,regridded_image); shading flat; axis square; set(gca,'tickdir','out')
title('image data on new lat lon grid (zoomed out)')
xlabel('lon');
ylabel('lat'); 
colormap('gray')
% add that same boundary again but in lat lon:
[blat,blon] = reckon(cameralat,cameralon,km2deg(sqrt(bx.^2+by.^2)),atan2d(bx,by));
hold on; plot(blon,blat,'m');
xlim(cameralon + [-10 10])
ylim(cameralat + [-10 10])
% and plot a coastline because why not
C = load('coast');
hold on; plot(C.long,C.lat,'color','w','linewi',2.5)
hold on; plot(C.long,C.lat,'k')








%%%% FUNCTION SECTION
% here's where the magic happens

function [regridded_image,x_in,y_in,Lat,Lon] = regridairglowimage(filepath,cameralat,cameralon,h,newgridX,newgridY)

%%%% INPUTS
% filepath              = filepath to airglow image
% cameralat,cameralon   = the lat lon of the camera
% h                     = altitude of the airglow layer in KM
% newgridX,newgridY     = new regular output grid in KM created by ndgrid or meshgrid etc.

%%%% OUTPUTS
% regridded_image   = the image on the new regular grid (newgridX,newgridY)
% Lat,Lon           = the lats and lons of this new regular grid.

% input image
Z = double(flip(imread(filepath),1));
% we flip this so that the first dimension is ascending from south to
% north. type "figure; pcolor(Z); shading flat;" to check this.
% If you're using imshow() or imagesc(), the image will be PLOTTED the
% correct way but the values in the array will still be upside down.
sz = size(Z);

% Radius of the earth
Re = 6371; % km

% radius of the airglow layer
r = Re + h;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 1. Find the zenith angle and azimuth of every location in the image

% try a different method:
[V1,V2] = meshgrid(linspace(-1,1,sz(1)),linspace(-1,1,sz(2)));
zen     = 90.*sqrt(V1.^2+V2.^2);
az      = atan2d(V1,V2);

% % (optional) remove anywhere where zenith angle > 90 (below the horizon)
% zen(zen >= 90) = 90;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 2. convert zenith angle values of the airglow layer at height h above
% the ground to arc length along that airglow layer (see diagram for
% method)
theta = zen;

% first find the angle alpha: (use projection to PQ axis method)
alpha = 90 - theta;

% find the angle phi
phi = acosd(Re.*sind(theta)./r);

% now find the angle beta (the arc angle):
beta = phi - alpha;
arclen = beta; % in DEGREES

% convert to arcdist and project into x,y distance:
arcdist = (2.*pi.*r) .* (arclen ./ 360);
x_in       = arcdist.*sind(az);
y_in       = arcdist.*cosd(az);

% great! we've now got the X,Y distance locations of every point on the image.
% Now let's put this on a regular distance grid centre on the camera.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 3. Create a new regular distance grid and project onto this

% define a new grid:
dx = 1; % spacing between points on new grid, km. Choose a better value if you like
gridlim = 500; % km, I assume we want another square...
[D1,D2] = ndgrid(-gridlim:dx:gridlim,-gridlim:dx:gridlim);

% interpolate on to this new grid:
F = scatteredInterpolant(x_in(:),y_in(:),Z(:),'linear','none');
regridded_image = F(D1,D2);
% there is probably a better way to do this interpolation step but this is
% simple and effective

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 4. Find new lat lons of this new regular grid

% this is a little sticky - easiest way is to use reckon, but with an
% increased earth radius for the airglow layer
RS = referenceSphere('earth');
RS.Radius = RS.Radius + h;

[Lat,Lon] = reckon(cameralat,cameralon,km2deg(sqrt(D1.^2+D2.^2)),atan2d(D1,D2));


end

