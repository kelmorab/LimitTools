Use these tools to study likelihoods

lnnScanner.py scans likelihoods for r and different nuisances parameters
call like
python nllScanner.py [bAsimov|sPlusbAsimov|data] nPoints outputDir workspace paramsToScan
python nllScanner.py bAsimov 20 myOutPutDirectory workspace.root r CMS_ttH_CSVHF

It will do multidim fits and save all the parameters.
The stepsize is determined by nPoints
The range is taken from initial MaxLikelihoodFits
For r all nuisances are freely floating
For other parameters, the poi will be redefined to the parameter. And r will be kepts as r (not treated as nuisance)


To plot the results use NllPlotter.py
python NllPlotter.py [WithCorr|AnyOtherString] outputDir workspace paramsToPlot

In the outputDir you will find all kinds of plots
scans_nll.pdf contains them all
First likelihood curves for r.
Then the fitted nuisance values as function of r
Then similar things for the other scanned parameters.
The red line always indicates the value the parameters take on at the best fit of r.

If you do "WithCorr" you will also get plots of each nuisances vs each other nuiance.
