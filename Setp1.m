[x_size,y_size] = deal(5,5);

X = -(x_size-1)/2:(x_size-1)/2;
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
% C stores polar coordinates
C = zeros(x_size:y_size);
C = string(C);
for y = 1:y_size
   for x = 1:x_size
       this_x = X(x,y);
       this_y = Y(x,y);
       %disp(this_x)
       B(x,y) = [num2str(this_x),',', num2str(this_y)];
       
       r = (this_x^2 + this_y^2)^0.5;
       theta = atan(this_y/this_x);
       
       % This is the step two calculation check
       az_matrix = [sin(theta);cos(theta)];
       fg_matrix = az_matrix*r;
       
       C(x,y) = [num2str(r),',', num2str(theta)];
   end
end



