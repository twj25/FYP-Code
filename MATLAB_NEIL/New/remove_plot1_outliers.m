test_med_array = median_amp;
outlier_locations = median_amp;
outlier_locations(outlier_locations > 8) = 1;
outlier_locations(outlier_locations > 1) = 0;

% Expand Areas
outlier_locations = movmean(movmean(outlier_locations,3,1),3,2);
outlier_locations(outlier_locations > 0) = 1;
outlier_locations = movmean(movmean(outlier_locations,3,1),3,2);
outlier_locations(outlier_locations > 0) = 1;
outlier_locations = movmean(movmean(outlier_locations,3,1),3,2);
outlier_locations(outlier_locations > 0) = 1;

test_med_array(logical(outlier_locations)) = 4;
%test_med_array = movmean(movmean(test_med_array,3,1),3,2);

pcolor(X,Y,test_med_array); shading flat; axis square; set(gca,'tickdir','out')
title('Median Amplitude')
set(gca,'clim',[0 8]);
colorbar('location','southoutside')
xlabel('km');
ylabel('km');


