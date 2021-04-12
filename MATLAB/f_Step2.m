function [latlon_matrix,xyz_matrix] = f_Step2(azel_matrix)
    % Calculate the reciever cartesian coordinates using the lat and lon
    % McDonald Observatory (Texas, US)
    % Latitude = 30 degrees
    % Longitude = -104 degrees
    lat = 30;
    lon = -104;
    alt = 2085;

    % Convert lat and lon to radians
    lat = lat / (180/pi);
    lon = lon / (180/pi);

    [x,y,z] = lla2ecef(lat,lon,alt);
    Rec = [x,y,z];
    Rsat = 90000;
    disp(sqrt(x^2 + y^2 + z^2))
    

    [x_size, y_size] = size(azel_matrix);
    latlon_matrix = zeros(x_size,y_size);
    latlon_matrix = string(latlon_matrix);
    for y_pos = 1:y_size
        for x_pos = 1:x_size
%             percentage = num2str(((((y_pos-1)*y_size)+x_pos)/(x_size*y_size))*100);
%             print_percentage = [percentage,'%'];
%             disp(print_percentage)
            cell_content = azel_matrix(x_pos,y_pos);
            [az,el] = read_matlab_cell(cell_content);

            az = az/(180/pi);
            el = el/(180/pi);

            Sat = invelevation(Rec,az,el,Rsat);
            if isreal(Sat(1))
                x = 1;
            else
                x = 1;
            end
            cart_x = real(Sat(1));
            cart_y = real(Sat(2));
            cart_z = real(Sat(3));


            [S_lat,S_lon,S_alt] = ecef2lla(cart_x,cart_y,cart_z);

            S_lat = S_lat * (180/pi);
            S_lon = S_lon * (180/pi);

            valxyz = string([num2str(round(cart_x,2)),',', num2str(round(cart_y,2)),',', num2str(round(cart_z,2))]);
            xyz_matrix(x_pos,y_pos) = valxyz;
            
            %val = string([num2str(S_lat),',', num2str(S_lon),',', num2str(S_alt)]);
            val = string([num2str(round(S_lat,2)),',', num2str(round(S_lon,2)),',', num2str(round(S_alt,2))]);
            %val = string([num2str(round(S_lat,2)),',', num2str(round(S_lon,2))]);
            latlon_matrix(x_pos,y_pos) = val;
        end
    end
end