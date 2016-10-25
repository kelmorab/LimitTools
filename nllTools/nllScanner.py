import ROOT
import sys
import os
import math
from subprocess import call, check_output
ROOT.gROOT.SetBatch(True)

VetoBBB=True

if len(sys.argv)<2 or sys.argv[1]=="-h" or sys.argv[1]=="--help":
  print "python nllScanner.py [bAsimov|sPlusbAsimov|data] nPoints outputDir workspace paramsToScan"

fitMode=sys.argv[1]
npointsString=sys.argv[2]
npoints=int(npointsString)
outputDir=sys.argv[3]
datacards=sys.argv[4]
inputparams=sys.argv[5:]

#params2=['r']+['CMS_res_j', 'CMS_scale_j', 'CMS_ttH_CSVCErr1', 'CMS_ttH_CSVCErr2', 'CMS_ttH_CSVHF', 'CMS_ttH_CSVHFStats1', 'CMS_ttH_CSVHFStats2', 'CMS_ttH_CSVLF', 'CMS_ttH_CSVLFStats1', 'CMS_ttH_CSVLFStats2', 'CMS_ttH_PSscale_ttbarOther', 'CMS_ttH_PSscale_ttbarPlus2B', 'CMS_ttH_PSscale_ttbarPlusB', 'CMS_ttH_PSscale_ttbarPlusBBbar', 'CMS_ttH_PSscale_ttbarPlusCCbar', 'CMS_ttH_PU', 'CMS_ttH_Q2scale_ttbarOther', 'CMS_ttH_Q2scale_ttbarPlus2B', 'CMS_ttH_Q2scale_ttbarPlusB', 'CMS_ttH_Q2scale_ttbarPlusBBbar', 'CMS_ttH_Q2scale_ttbarPlusCCbar', 'CMS_ttH_QCDscale_ttbarPlus2B', 'CMS_ttH_QCDscale_ttbarPlusB', 'CMS_ttH_QCDscale_ttbarPlusBBbar', 'CMS_ttH_QCDscale_ttbarPlusCCbar',
	       ##'CMS_ttH_dl_Trig', 'CMS_ttH_dl_eff_lepton', 
	       #'CMS_ttH_eff_el', 'CMS_ttH_eff_mu', 'CMS_ttH_ljets_Trig_el', 'CMS_ttH_ljets_Trig_mu', 
	       #'QCDscale_V', 'QCDscale_VV', 'QCDscale_singlet', 'QCDscale_ttH', 'QCDscale_ttbar', 'lumi_13TeV', 'pdf_gg', 'pdf_gg_ttH', 'pdf_qg', 'pdf_qqbar']

print "reading workspace for nuisances"
params2=[]
# find all nuisances
workspacefile=ROOT.TFile(datacards,"READ")
workspace=workspacefile.Get("w")
setOfNuisances=workspace.set("nuisances")
listOfNuisances=setOfNuisances.contentsString().split(",")
for nuis in listOfNuisances:
  if "BDTbin" in nuis and VetoBBB:
    continue
  params2.append(nuis)
workspacefile.Close()

print "found Nuisances"
print params2 

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

#floatmode="--floatOtherPOI=1"
floatR=True

doBonlyAsimov=True

counter=0
params=[]
if inputparams[0]!="r":
  params+=["r"]
params+=inputparams
print params 

minpoi=-5
maxpoi=5
minr=-5
maxr=5

for p in params:
  print ""
  print "Doing now ", p
  counter+=1
  
  #npoints=50
  
  stringOfOtherNuis=""
  listOfOtherNuis=[]
  for op in params2:
    if op==p:
     continue
    if op=="r":
      continue
    else:
      listOfOtherNuis.append(op)
  stringOfOtherNuis=",".join(listOfOtherNuis)
  #print stringOfOtherNuis
  
  pp=p.replace(" ","")

  if floatR:
    cmd="combine -M MultiDimFit"
    fitstring=""
    if fitMode=="bAsimov":
      print "doing asimov B-only"
      fitstring+=" -t -1 --expectSignal 0 "
    elif fitMode=="sPlusbAsimov":
      print "doing asimov SplusB"
      fitstring+=" -t -1 --expectSignal 1 "
    elif fitMode=="data":
      print "doing fit to data"
      fitstring+=""
    else:
      print "DO NOT KNOW MODE -> doing asimov B-only"
      fitstring+=" -t -1 --expectSignal 0 "
    if fitMode!="data":
      if p!="r":
	fitstring=fitstring.replace("--expectSignal","--setPhysicsModelParameters")
	
    print fitstring
    # do prefit to find range 
    print "Doing prefit to determine range of scan"
    cmd="combine -M MaxLikelihoodFit "+fitstring+" --minimizerStrategy 0 --minimizerTolerance 0.01 --rMin=-100 --rMax=100 -n prefit "+datacards
    if p!="r":
      cmd+=" --redefineSignalPOIs "+p
      
    prefitoutput=check_output(cmd,shell=True)
    preBest=0
    preMin=-5
    preMax=5
    for line in prefitoutput.split("\n"):
      if "Best fit" in line:
	print line
	splitline=line.split(" ")
	bests=splitline[-6]
	bufs=splitline[-4]
	print bufs
	lows,highs=bufs.split("/")
	bestf=float(bests)
	lowf=float(lows)
	highf=float(highs)
	print bestf-2*abs(lowf), bestf+2*abs(highf)
	preMin=math.floor(bestf-2*abs(lowf))-1
	preMax=math.floor(bestf+2*abs(highf))+2
	print preMin, preMax
    if p=="r":
      minr=preMin
      maxr=preMax
    minpoi=preMin
    maxpoi=preMax
    
    print "using for r the range ", minr, maxr
    print "using for "+p+" the range ", minpoi, maxpoi
    
    
    # do actual fits
    cmd="combine -M MultiDimFit"
    cmd+=fitstring
    cmd+=" --algo=grid --points="+str(npoints)+ " --minimizerStrategy 0 --minimizerTolerance 0.0001 --floatOtherPOI 1 --redefineSignalPOIs r -P "+pp+" --setPhysicsModelParameterRanges "+pp+"="+str(minpoi)+","+str(maxpoi)+" --rMin="+str(minr)+" --rMax="+str(maxr)+" --saveInactivePOI 1 --saveSpecifiedNuis "+stringOfOtherNuis+" "+datacards
    
    call(cmd,shell=True)

    #call(["combine","-M","MultiDimFit","--algo=grid","--points="+str(npoints),"--floatOtherPOI","1","--redefineSignalPOIs","r","-P",pp,"--setPhysicsModelParameterRanges",pp+"="+str(minpoi)+","+str(maxpoi),"--rMin",str(minr),"--rMax",str(maxr),"--saveInactivePOI","1","--saveSpecifiedNuis",stringOfOtherNuis,datacards])

  else:
    print "currently not supported"
  
  outfilename="higgsCombineTest.MultiDimFit.mH120.root"
  print outfilename
    
  resfilename=outputDir+"/"+pp+"_"+outfilename
  call(["cp",outfilename, resfilename])
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
