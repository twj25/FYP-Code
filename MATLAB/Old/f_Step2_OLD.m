function [azel_matrix] = f_Step2(xy_matrix)
    [x_size,y_size] = size(xy_matrix);
    % C stores polar coordinates
    azel_matrix = zeros(x_size:y_size);
    azel_matrix = string(azel_matrix);
    
    for y_pos = 1:y_size
       for x_pos = 1:x_size
           
           cell_content = xy_matrix(x_pos,y_pos);
           [this_x,this_y] = read_matlab_cell(cell_content);
           
           % Calculate Az and El 
           if this_x == 0 && this_y ~= 0
               % this line accomodates for stupid negative 0 error
               Az = pi + round(-atan(this_y/this_x),2); 
           elseif this_x <= 0
               Az = pi + round(atan(this_y/this_x),2);
           elseif this_x > 0 && this_y < 0
               Az = 2*pi + round(atan(this_y/this_x),2);
           else
               Az = round(atan(this_y/this_x),2);
           end

           El = pi/2 - round((this_x^2 + this_y^2)^0.5,2);

           % Convert from Radians to Degrees
           Az_D = round(180/pi * Az);
           El_D = round(180/pi * El);

           % This is the step two calculation check
%            az_matrix = [sin(theta);cos(theta)];
%            fg_matrix = az_matrix*r;

           azel_matrix(x_pos,y_pos) = [num2str(Az_D),',',num2str(El_D)];
       end
    end
end