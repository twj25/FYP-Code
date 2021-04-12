function [Az,El] = azel2latlonalt(StationLat,StationLon,Field,ObsLat,ObsLon,Alt)

% convert data at a given (lat,lon,height) to (az,el) from a particular point on the ground
%feed in a 2d grid of data and grids the same size of (az, el, alt)
%all angles in degrees, distances in m
%returns 2d grids of (lat,lon)

%convert everything to radians
StationLat = deg2rad(StationLat);
StationLon = deg2rad(StationLon);
ObsLat     = deg2rad(ObsLat);
ObsLon     = deg2rad(ObsLon);


%geophysical properties
Settings.Geo.Re = 6371e3; %radius of Earth, m

%find CARTESIAN coords of measurement location
Cart = sphcart([Settings.Geo.Re,StationLat,StationLon]);

%find Cartesian point of each point in the area scanned
Cart2 = NaN([numel(ObsLat),3]);
for iPoint=1:1:numel(ObsLat);
  Cart2(iPoint,:) = sphcart([Settings.Geo.Re+Alt,ObsLat(iPoint),ObsLon(iPoint)]);
end
Cart2 = reshape(Cart2,size(ObsLat,1),size(ObsLat,2),3);


%then convert to az, el from the observed point
Az = NaN(size(ObsLat));
El = Az;
for iAz = 1:1:size(Cart2,1);
  for jAz = 1:1:size(Cart2,2);
    [E,A] = elevation(squeeze(Cart2(iAz,jAz,:))',Cart);
    Az(iAz,jAz) = A;
    El(iAz,jAz) = E;
  end
end

Az = rad2deg(Az);
El = rad2deg(El);

end

