function [OutLat,OutLon] = azel2latlon(StationLat,StationLon,Az,El,InAlt)

% convert data at a given (az,el,height) to the (lat,lon)
%feed in a 2d grid of data and grids the same size of (az, el, alt)
%all angles in degrees, distances in m
%returns 2d grids of (lat,lon)

%convert everything to radians
StationLat = deg2rad(StationLat);
StationLon = deg2rad(StationLon);
Az         = deg2rad(Az);
El         = deg2rad(El);


%geophysical properties
Settings.Geo.Re = 6371e3; %radius of Earth, m

%find CARTESIAN coords of measurement location
Cart = sphcart([Settings.Geo.Re,StationLat,StationLon]);


%then work out the Cartesian coord of each point in (az,el) space
%and convert to lat,lon,alt
Sat = NaN([size(Az),3]); %3 is [x,y,z] in Cartesian coords
LLA = Sat;
for iAz = 1:1:size(Az,1);
  for jAz = 1:1:size(Az,2);
    %find cartesian coords of point on sky
    Sat(iAz,jAz,:) = invelevation(Cart, Az(iAz,jAz), El(iAz,jAz),Settings.Geo.Re+InAlt(iAz,jAz));
    %and convert to spherical coords
    LLA(iAz,jAz,:) = cartsph(Sat(iAz,jAz,:));
  end
end


%pull out the coords we want
OutLat = rad2deg(squeeze(LLA(:,:,2))); 
OutLon = rad2deg(squeeze(LLA(:,:,3)));

end

