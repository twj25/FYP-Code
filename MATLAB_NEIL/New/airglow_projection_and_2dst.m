
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

direc = '/Users/tomjo/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/For Neil/Hist/';
%filepath = [direc 'mcdonald_5577_10_Apr_2019_T053317A100_.gif'];
%filepath = [direc 'mercedes_5577_2_Sep_2018_B041551B245_.gif'];
filepath = [direc 'mcdonald_5577_11_Jul_2019_T032419A192_.gif'];
%filepath = [direc 'mcdonald_5577_21_May_2019_T033130A141_.gif'];
% change this for each file

% height of the airglow layer above the ground
h = 90; % km (TOM CHECK THIS)

% Camera Lat/Lon (I don't know this, so I chose my house!)
% McDonald
% cameralat = 30;
% cameralon = -104;
% Mercedes
cameralat = -29;
cameralon = -58;


% define a new regular distance  grid:
dx = 1; % spacing between points on new grid (km). Use a finer grid spacing if you want, but it'll take longer.
gridlim = 500; % km, I assume we want another square...
[newgridX,newgridY] = ndgrid(-gridlim:dx:gridlim,-gridlim:dx:gridlim);

% apply my function below:
[regridded_image,x_in,y_in,Lat,Lon] = regridairglowimage(filepath,cameralat,cameralon,h,newgridX,newgridY);

image_for_hist = regridded_image(300:600,400:700);
imwrite(uint8(image_for_hist), 'moon.png');

%%%% Make some figs to check our working

figure; set(gcf,'color','w');

Z = double(flip(imread(filepath),1));

%%%% First the input image
%subplot(1,4,1);
figure();
pcolor(Z); shading flat; axis square; set(gca,'tickdir','out')
title('input image')
colormap('gray')
xlabel('px');
ylabel('px');

%%%% now the image on a distance grid
%subplot(1,4,2); 
figure();
pcolor(x_in,y_in,Z); shading flat; axis square; set(gca,'tickdir','out')
%title('image on the current "pixel" distance grid (km)')
title('undistorted image')
xlabel('km');
ylabel('km');
xlim(x_in(floor(size(Z,1)/2),[1 end]))
ylim(y_in([1 end],floor(size(Z,2)/2)))
colormap('gray')
% add a boundary:
boundary = 100;
bx = boundary.*[-1 1 1 -1 -1];
by = boundary.*[-1 -1 1 1 -1];
hold on; %plot(bx,by,'m');

%%%% now the new regridded image on the new regular distance grid
%subplot(1,4,3); 
figure();
pcolor(newgridX,newgridY,regridded_image); shading flat; axis square; set(gca,'tickdir','out')
%title('image on new regular distance grid')
title('undistorted image (zoomed in)')
xlim(2.*[-boundary boundary])
ylim(2.*[-boundary boundary])
xlabel('km');
ylabel('km'); 
colormap('gray')
% add that same boundary:
hold on; %plot(bx,by,'m');

%%%% and finally the regridded image on a new lat lon grid
%subplot(1,4,4); 
figure();
pcolor(Lon,Lat,regridded_image); shading flat; axis square; set(gca,'tickdir','out')
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





%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% APPLY THE 2DST TO THE AIRGLOW IMAGE - WITH BACKGROUND REMOVED
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% here we're going to, as the title suggests, apply the 2DST to the
%%%% nicely regridded data and plot some parameters.
%%% you'll need nph_ndst() in the matlab path for this to work, I've
%%% included it in the email.


%%%% BUT FIRST: REMOVE BACKGROUND AIRGLOW FROM THE IMAGE
%%%% we're going to start with the regridded image from before.
im = regridded_image;
X = newgridX; Y = newgridY; % save typing time :)
% figure; pcolor(X,Y,IN); shading flat;

%%%% initially, give the image a little smooth to reduce retrieval noise:
im = movmean(movmean(im,3,1),3,2);

%%%% trim the image to a smaller square, away from any trees or shadows at
%%%% the edges.
newgridlim = 100;
region = {abs(newgridX(:,1)) < newgridlim,abs(newgridY(1,:)) < newgridlim};
X = X(region{:});
Y = Y(region{:});
im = im(region{:});

%%%% we need to establish a "background" sky to remove from the image to
%%%% reveal the perturbations. To make this, we'd normally smooth the data
%%%% then subtract this. But stars make this a problem as they artificially
%%%% boost any smoothing we may apply. So we must remove them first.

% first let's make the stars really prominent by squaring applying a power
% to the image:
im_sq = im;
stargradlim = 5;

%%%% let's try and remove some stars using a gradient method...
%%%% anywhere where the 2-point gradient is greater than some value
diff1 = diff(im_sq([1 1:end],:),[],1);
diff2 = diff(im_sq(:,[1 1:end]),[],2);
diffdiff = max(cat(3,diff1,diff2),[],3);
% figure; pcolor(X,Y,diffdiff); shading flat;
% oooooh we can see the stars, nice

% now remove anywhere where the gradient is above some value, sorry this is
% just gonna hev to be a number for now. There's def a better way of
% working one out but I'll leave to you :D
im_nostars = im;
starlocs = double(diffdiff > stargradlim);
% make the stars a little bit wider:
starlocs = movmean(movmean(starlocs,3,1),3,2);
starlocs(starlocs > 0) = 1;
im_nostars(logical(starlocs)) = NaN;
% figure; pcolor(X,Y,IN); shading flat; % check our working with a figure

%%%% now most stars are removed, we can do a background smoother to get
%%%% an idea of the background sky's airglow. A good smoother to use here
%%%% is movmean(), which can ignore NaNs...

filterwidth = 20 / dx; % try a 50km filter width
bg = movmean(movmean(im_nostars,filterwidth,1,'omitnan'),filterwidth,2,'omitnan');

% figure; pcolor(X,Y,bg); shading flat;
% check your working again. there should be no GWs at all left in our
% background.

% remove this from the input image:
im_perts = im_nostars - bg;
% figure; pcolor(X,Y,im); shading flat; % phwoar this looks great

% set these locations to zero for now.
im_perts(isnan(im_perts)) = 0;


%%%% Make some more figs to check our working
figure; set(gcf,'color','w');

%subplot(2,4,1); 
pcolor(X,Y,im); shading flat; axis square; set(gca,'tickdir','out')
title('regridded image')
colormap(gca,'gray'); set(gca,'clim',[0 250])
colorbar('location','southoutside')
xlabel('km');
ylabel('km');

%subplot(2,4,2); 
figure();
pcolor(X,Y,starlocs); shading flat; axis square; set(gca,'tickdir','out')
title('star locations')
colormap(gca,'gray'); set(gca,'clim',[0 1])
colorbar('location','southoutside')
xlabel('km');
ylabel('km');

%subplot(2,4,3); 
pcolor(X,Y,bg); shading flat; axis square; set(gca,'tickdir','out')
figure();
title('airglow background')
colormap(gca,'gray'); set(gca,'clim',[0 250])
colorbar('location','southoutside')
xlabel('km');
ylabel('km');

%subplot(2,4,4); 
figure();
pcolor(X,Y,im_perts); shading flat; axis square; set(gca,'tickdir','out')
title('perturbations')
set(gca,'clim',[-20 20]);
colorbar('location','southoutside')
xlabel('km');
ylabel('km');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Now we're gonna apply the 2DST. Try these settings below and see how
%%%% you get on.

IN = im_perts;

% number of frequencies to analyse for
scales = 1000;
% spacing of the input data
grid_spacing = [dx dx];
% scale factor (try adjusting this and seeing what happens). This
% represents a trade off between spatial and spectral resolution.
c = [1 1];

% set a threshold for wavelengths to consider. We don't want any of the
% stars in our measurements
minwavelengths = [3 3]; % in km

ST = nph_ndst(IN,scales,grid_spacing,c,'minwavelengths',minwavelengths);
ST.LH = 1./sqrt(ST.F1.^2 + ST.F2.^2);

% %%%% stick the NaNs back in from the stars:
% ST.A(logical(starlocs)) = NaN;
% ST.F1(logical(starlocs)) = NaN;
% ST.F2(logical(starlocs)) = NaN;
% ST.LH(logical(starlocs)) = NaN;

%%%% let's plot the ST results
%subplot(2,4,5); 
figure();
pcolor(X,Y,ST.A); shading flat; axis square; set(gca,'tickdir','out')
title('ST amplitude')
set(gca,'clim',[0 10]);
colorbar('location','southoutside')
xlabel('km');
ylabel('km');

%subplot(2,4,6); 
figure();
pcolor(X,Y,ST.LH); shading flat; axis square; set(gca,'tickdir','out')
title('ST Wavelength (km)')
set(gca,'clim',[0 25]);
colorbar('location','southoutside')
xlabel('km');
ylabel('km');

%subplot(2,4,7); 
figure();
pcolor(X,Y,atand(ST.F2./ST.F1)); shading flat; axis square; set(gca,'tickdir','out')
title('Angle (deg anticlockwise from E)')
set(gca,'clim',[-90 90]);
cbar = colorbar('location','southoutside');
cbar.Ticks = -90:30:90;
xlabel('km');
ylabel('km');

%%%% also stick some arrows on for fun:
locs = {floor(linspace(1,size(im,1),20)),floor(linspace(1,size(im,2),20))};
xcomp = -sind(atand(ST.F1./ST.F2));
ycomp = -cosd(atand(ST.F1./ST.F2));
hold on; quiver(X(locs{:}),Y(locs{:}),xcomp(locs{:}),ycomp(locs{:}),'color','k');












%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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

















