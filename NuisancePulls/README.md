Producing nuisance pull plots

blinded fit

combine -M MaxLikelihoodFit -t -1 --expectSignal=1 -n NAME datacard.txt 

Usefull:
--minos=all
--rMin=-5 --rMax=5 

for s+b or b-only asimov toy
--expectSignal=1 
or
--expectSignal=0

Make pull plots:
python diffNuisances.py mlfit.root -g OUTNAME

The present script is modified to suppress bin-by-bin nuisances in the plots


