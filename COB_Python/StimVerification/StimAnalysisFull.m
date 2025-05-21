% load stimulation recordings captured by tekscan oscilliscope
load("Z:\Shared drives\CNI\COB\XipppyServer\COB_Python\StimVerification\StimVerification_1_1.mat");
WFAll = WF;
load("Z:\Shared drives\CNI\COB\XipppyServer\COB_Python\StimVerification\StimVerification_2_1.mat")
WFAll = [WFAll; WF];
load("Z:\Shared drives\CNI\COB\XipppyServer\COB_Python\StimVerification\StimVerification_3_1.mat")
WFAll = [WFAll; WF];
load("Z:\Shared drives\CNI\COB\XipppyServer\COB_Python\StimVerification\StimVerification_1_2.mat");
WFAll = [WFAll; WF];
load("Z:\Shared drives\CNI\COB\XipppyServer\COB_Python\StimVerification\StimVerification_2_2.mat")
WFAll = [WFAll; WF];
load("Z:\Shared drives\CNI\COB\XipppyServer\COB_Python\StimVerification\StimVerification_3_2.mat")
WFAll = [WFAll; WF];
load("Z:\Shared drives\CNI\COB\XipppyServer\COB_Python\StimVerification\StimVerification_1_3.mat");
WFAll = [WFAll; WF];
load("Z:\Shared drives\CNI\COB\XipppyServer\COB_Python\StimVerification\StimVerification_2_3.mat")
WFAll = [WFAll; WF];
load("Z:\Shared drives\CNI\COB\XipppyServer\COB_Python\StimVerification\StimVerification_3_3.mat")
WFAll = [WFAll; WF];
figure();
for index2 = 0:8 %% will change this to n-1
    for index=1:32
        
%         ylim=([5,0]);
%         plot(abs(WFAll(index,:)));
%         ylim=([5,0]);
%         hold on;
%         plot([50e3 * ((100-index)*10^-6)]*ones(1,2500))
%         ylim=([5,0]);
%         title(index)
%         hold off;
%         
%         pause(0.05);
        diffStimulation(index+(index2*32),:) = abs(WFAll(index+(index2*32),:))- 50e3 * (100-index)*10^-6;
        
    end
end

figure(1);
title("Cathode")
avgAmpDifferenceCathode = mean(diffStimulation(:,650:1050),2)
avgAmpDifferenceAnode = mean(diffStimulation(:,1350:1750),2)
dRecorded = heatmap(avgAmpDifferenceCathode)
dRecorded.XLabel = 'Difference between Expected and Recorded Cathode Values (Micro Amps)';
dRecorded.YLabel = 'Channel #';
dRecorded.Colormap = jet;
XLabels = 1:288;
% Convert each number in the array into a string
CustomXLabels = string(XLabels);
% Replace all but the fifth elements by spaces
CustomXLabels(mod(XLabels,32) ~= 0) = " ";
% Set the 'XDisplayLabels' property of the heatmap 
% object 'h' to the custom x-axis tick labels
dRecorded.YDisplayLabels = CustomXLabels;

figure(2)
title("Anode")
dRecorded = heatmap(avgAmpDifferenceAnode)
dRecorded.XLabel = 'Difference between Expected and Recorded Anode Values (Micro Amps)';
dRecorded.YLabel = 'Channel #';
dRecorded.Colormap = jet;
XLabels = 1:288;
% Convert each number in the array into a string
CustomXLabels = string(XLabels);
% Replace all but the fifth elements by spaces
CustomXLabels(mod(XLabels,32) ~= 0) = " ";
% Set the 'XDisplayLabels' property of the heatmap 
% object 'h' to the custom x-axis tick labels
dRecorded.YDisplayLabels = CustomXLabels;

%% find mean cathode/anode stimulation differences
meanCathodeAnode = mean([avgAmpDifferenceCathode avgAmpDifferenceAnode])
meanOverall = mean([avgAmpDifferenceCathode; avgAmpDifferenceAnode])

%% Find largest deviation from expected stimulation in amps
maxCathodeAnode = max([avgAmpDifferenceCathode avgAmpDifferenceAnode])
maxOverallCathodeAnode = max([avgAmpDifferenceCathode; avgAmpDifferenceAnode])

%% Find electrodes that have the most inbalance between phases
max(avgAmpDifferenceCathode - avgAmpDifferenceAnode)

min(avgAmpDifferenceCathode - avgAmpDifferenceAnode)

%% Find electrodes that are over stimulating
a = [avgAmpDifferenceCathode; avgAmpDifferenceAnode]
find(a > 0) %electrodes that are over stimulating will print in command console




