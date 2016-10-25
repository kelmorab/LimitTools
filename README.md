The purpose is to collect usefull scripts and combine commands

WARNING
a lot of the scripts here were hacked for a specific purpose and are not intended for general use yet.
Always look at them and edit whats necessary before using.

DISCLAIMER
Most scripts were originally written by other people
I will add the relevant authors soon

########################################
Combine commands

blinded expected limit:
combine -M Asymptotic --run="blind" --minosAlgo stepping datacard.txt


####################################
Usefull links

https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideHiggsAnalysisCombinedLimit
https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/SWGuideNonStandardCombineUses#Nuisance_parameter_impacts
https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchool2014HiggsCombPropertiesExercise


####################################
Literature
Asymptotic method http://dx.doi.org/10.1140/epjc/s10052-011-1554-0


#####################################
Other stuff

prebuild workspace if you want to do multiple fits with the same datacards
text2workspace.py datacard.txt
-> datacard.root which can be used instead of the datacard for combine input

remove Bin-by-Bin statistics (or other uncertainties)
grep -v BDTbin datacard.txt > newdatacard.txt
You can also "freeze" the nuisance, see https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/SWGuideNonStandardCombineUses#Nuisance_parameter_impacts

combine various cards with
combineCards.py card1.txt card2.txt > newcard.txt
If you want to remove nuisances from the combined card you also have to change the number of nuisances in line 3 with an asterisk
Or use a script similar to makeCombinedCards.py



