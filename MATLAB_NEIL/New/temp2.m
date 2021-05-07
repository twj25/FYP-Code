prc_amps = prctile(working_amps,[18,50,82]);  

figure(); boxplot(prc_amps);
xlabel('Day of the Month');
ylabel('Amplitude');