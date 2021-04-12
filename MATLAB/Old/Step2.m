select = 3;

% T = readtable('test.csv');
% cell_content = T{254,128};
% [az,el] = read_cell(cell_content);

% B_mag = convert_to_mag(B);
% plot_mags(B_mag);

% x=3;
% y=4;
% cell_content = C(x,y);
% [az,el] = read_matlab_cell(cell_content);
% [x_val,y_val] = solve_equ(az,el,select);
% [az1,el1] = check_solve_ans(x_val,y_val);

% Calculate the reciever cartesian coordinates using the lat and lon
% McDonald Observatory (Texas, US)
% Latitude = 30
% Longitude = -104
lat = 30;
lon = -104;
alt = 0;
[x,y,z] = lla2ecef(lat,lon,alt);
Rec = [x,y,z];
Rsat = 90000;

[x_size, y_size] = size(C);
D = zeros(x_size,y_size);
D = string(D);
for y_pos = 1:y_size
    for x_pos = 1:x_size
        percentage = num2str(((((y_pos-1)*y_size)+x_pos)/(x_size*y_size))*100);
        print_percentage = [percentage,'%'];
        disp(print_percentage)
        cell_content = C(x_pos,y_pos);
        [az,el] = read_matlab_cell(cell_content);
        
        Sat = invelevation(Rec,az,el,Rsat);
        cart_x = real(Sat(1));
        cart_y = real(Sat(2));
        cart_z = real(Sat(3));
        
        [S_lat,S_lon,S_alt] = ecef2lla(cart_x,cart_y,cart_z);
        
        %val = string([num2str(S_lat),',', num2str(S_lon),',', num2str(S_alt)]);
        val = string([num2str(S_lat),',', num2str(S_lon)]);
        %disp(val)
        D(x_pos,y_pos) = val;
    end
end



