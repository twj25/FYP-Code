function xy_matrix = f_Step1(size)
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
    
    for y = 1:y_size
       for x = 1:x_size
           this_x = Y(x,y);
           this_y = X(x,y);


           %disp(this_x)
           xy_matrix(x,y) = [num2str(this_x),',', num2str(this_y)];

       end
    end
end