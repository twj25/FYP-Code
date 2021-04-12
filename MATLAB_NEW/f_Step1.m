function [azel_matrix] = f_Step1(size)
    [x_size,y_size] = deal(size,size);

    X = -(x_size-1)/2:(x_size-1)/2;
    %X = X * -1;
    X = X/((size-1)/2);
    X = repmat(X,x_size,1);

    Y = -(y_size-1)/2:(y_size-1)/2;
    Y = Y * -1;
    Y = Y/((size-1)/2);
    Y = reshape(Y,[],1);
    Y = repmat(Y,1,y_size);
    
    % B is a 2D matrix containing coordinate pairs
    xy_matrix = zeros(x_size:y_size);
    xy_matrix = string(xy_matrix);
    % C stores polar coordinates
    azel_matrix = zeros(size:size);
    azel_matrix = string(azel_matrix);
    
    for y_pos = 1:y_size
       for x_pos = 1:x_size
           
           this_x = Y(x_pos,y_pos);
           this_y = X(x_pos,y_pos);
           %disp(this_x)
           xy_matrix(x_pos,y_pos) = [num2str(this_x),',', num2str(this_y)];
           
           
           if this_x <= 0
               Az = pi + round(atan(this_y/this_x),2);
           elseif this_x > 0 && this_y < 0
               Az = 2*pi + round(atan(this_y/this_x),2);
           else
               Az = round(atan(this_y/this_x),2);
           end

           El = pi/2 - round((this_x^2 + this_y^2)^0.5,2);

           % Convert from Radians to Degrees
           
%            if y_pos < y_size/2 
%                Az_D = 360 - round(180/pi * Az);
%            else
%                Az_D = round(180/pi * Az);
%            end
           
           Az_D = round(180/pi * Az);
           El_D = round(180/pi * El);

           % This is the step two calculation check
%            az_matrix = [sin(theta);cos(theta)];
%            fg_matrix = az_matrix*r;

           azel_matrix(x_pos,y_pos) = [num2str(Az_D),',',num2str(El_D)];
       end
    end
end