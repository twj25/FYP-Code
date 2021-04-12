[x_size,y_size] = deal(5,5);

X = -(x_size-1)/2:(x_size-1)/2;
%X = X * -1;
X = repmat(X,x_size,1);

Y = -(y_size-1)/2:(y_size-1)/2;
Y = Y * -1;
Y = reshape(Y,[],1);
Y = repmat(Y,1,y_size);

% A is a 3D matrix
% A = cat(3,X,Y);
% S = size(A);
% [X,Y,Z] = ndgrid(1:S(1),1:S(2),1:S(3));
% scatter3(X(:),Y(:),Z(:),321,A(:),'filled')

% B is a 2D matrix containing coordinate pairs
B = zeros(x_size:y_size);
B = string(B);
B1 = zeros(x_size:y_size);
B1 = string(B1);
% C stores polar coordinates
C = zeros(x_size:y_size);
C = string(C);
C1 = zeros(x_size:y_size);
C1 = string(C1);
for y = 1:y_size
   for x = 1:x_size
       this_x = Y(x,y);
       this_y = X(x,y);
       
       
       %disp(this_x)
       B(x,y) = [num2str(this_x),',', num2str(this_y)];
       
       cell_content = B(x,y);
       [this_y1,this_x1] = read_matlab_cell(cell_content);
       B1(x,y) = [num2str(this_x1),',', num2str(this_y1)];

%        this_x = this_x1;
%        this_y = this_y1;
       
       % Calculate Az and El      
       if this_x < 1
           Az = pi + round(atan(this_y/this_x),2);
       elseif this_x > 0 && this_y < 0
           Az = 2*pi + round(atan(this_y/this_x),2);
       else
           Az = round(atan(this_y/this_x),2);
       end
       
       El = pi - round((this_x^2 + this_y^2)^0.5,2);
       
       % Convert from Radians to Degrees
       Az_D = round(180/pi * Az);
       El_D = round(180/pi * El);
       
       % This is the step two calculation check
%        az_matrix = [sin(theta);cos(theta)];
%        fg_matrix = az_matrix*r;
       
       C(x,y) = [num2str(Az_D),',',num2str(El_D)];
       
       if this_x1 < 1
           test = atan(this_y/this_x);
           test1 = atan(this_y1/this_x1);
           Az = pi + round(atan(this_y/this_x),2);
           Az1 = pi + round(atan(this_y1/this_x1),2);
       elseif this_x1 > 0 && this_y1 < 0
           Az1 = 2*pi + round(atan(this_y1/this_x1),2);
       else
           Az1 = round(atan(this_y1/this_x1),2);
       end
       
       Az_D1 = round(180/pi * Az1);  
       C1(x,y) = [num2str(Az_D1),',',num2str(El_D)];
   end
end



