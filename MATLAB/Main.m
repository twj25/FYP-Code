azel_matrix = f_Step1(5);
[latlon_matrix,xyz_matrix] = f_Step2(azel_matrix);

% Plot latitudes and longitudes on 2D axis
plot_coordinates2D(latlon_matrix);

% Plot latitudes, longitude and altitudes on 3D axis
figure(2);
plt_rec = false;
plot_coordinates3D(latlon_matrix,plt_rec);

% Plot x,y and z on 3D axis
figure(3);
plt_rec = true;
plot_coordinates3D(xyz_matrix,plt_rec);