function plot_mags(mags)
    X = -127:127;
    X = repmat(X,255,1);
    X = reshape(X,[],1);

    Y = -127:127;
    Y = Y * -1;
    Y = reshape(Y,[],1);
    Y = repmat(Y,1,255);
    Y = reshape(Y,[],1);

    mags = reshape(mags,[],1);
    
    M = cat(2,X,Y,mags);
    
    scatter(M(:,1), M(:,2), 50, M(:,3), 'Filled')

end