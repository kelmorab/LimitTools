import ROOT
import sys
import os
from subprocess import call
ROOT.gROOT.SetBatch(True)

datacards=sys.argv[1]

params=sys.argv[2:]
print params
params2=['r']+['CMS_res_j', 'CMS_scale_j', 'CMS_ttH_CSVCErr1', 'CMS_ttH_CSVCErr2', 'CMS_ttH_CSVHF', 'CMS_ttH_CSVHFStats1', 'CMS_ttH_CSVHFStats2', 'CMS_ttH_CSVLF', 'CMS_ttH_CSVLFStats1', 'CMS_ttH_CSVLFStats2', 'CMS_ttH_PSscale_ttbarOther', 'CMS_ttH_PSscale_ttbarPlus2B', 'CMS_ttH_PSscale_ttbarPlusB', 'CMS_ttH_PSscale_ttbarPlusBBbar', 'CMS_ttH_PSscale_ttbarPlusCCbar', 'CMS_ttH_PU', 'CMS_ttH_Q2scale_ttbarOther', 'CMS_ttH_Q2scale_ttbarPlus2B', 'CMS_ttH_Q2scale_ttbarPlusB', 'CMS_ttH_Q2scale_ttbarPlusBBbar', 'CMS_ttH_Q2scale_ttbarPlusCCbar', 'CMS_ttH_QCDscale_ttbarPlus2B', 'CMS_ttH_QCDscale_ttbarPlusB', 'CMS_ttH_QCDscale_ttbarPlusBBbar', 'CMS_ttH_QCDscale_ttbarPlusCCbar',
	       #'CMS_ttH_dl_Trig', 'CMS_ttH_dl_eff_lepton', 
	       'CMS_ttH_eff_el', 'CMS_ttH_eff_mu', 'CMS_ttH_ljets_Trig_el', 'CMS_ttH_ljets_Trig_mu', 
	       'QCDscale_V', 'QCDscale_VV', 'QCDscale_singlet', 'QCDscale_ttH', 'QCDscale_ttbar', 'lumi_13TeV', 'pdf_gg', 'pdf_gg_ttH', 'pdf_qg', 'pdf_qqbar']


if not os.path.exists("nllscans"):
    os.makedirs("nllscans")

#floatmode="--floatOtherPOI=1"
floatR=True
doBonlyAsimov=True

counter=0

for p in params:
  counter+=1
  if p=="r":
    if "dl" in datacards:
      minpoi=-10
      maxpoi=10
      minr=-10
      maxr=10
    else:
      minpoi=-5
      maxpoi=5
      minr=-5
      maxr=5
  else:
    minpoi=-5
    maxpoi=5
    minr=-5
    maxr=5
  
  npoints=10
  
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
  print stringOfOtherNuis
  
  pp=p.replace(" ","")

  if floatR:
    cmd="combine -M MultiDimFit"
    if doBonlyAsimov:
      cmd+=" -t -1 --expectSignal 0 "
      
    cmd+=" --algo=grid --points="+str(npoints)+ " --minimizerStrategy 0 --minimizerTolerance 0.01 --floatOtherPOI 1 --redefineSignalPOIs r -P "+pp+" --setPhysicsModelParameterRanges "+pp+"="+str(minpoi)+","+str(maxpoi)+" --rMin="+str(minr)+" --rMax="+str(maxr)+" --saveInactivePOI 1 --saveSpecifiedNuis "+stringOfOtherNuis+" "+datacards
    
    call(cmd,shell=True)

    #call(["combine","-M","MultiDimFit","--algo=grid","--points="+str(npoints),"--floatOtherPOI","1","--redefineSignalPOIs","r","-P",pp,"--setPhysicsModelParameterRanges",pp+"="+str(minpoi)+","+str(maxpoi),"--rMin",str(minr),"--rMax",str(maxr),"--saveInactivePOI","1","--saveSpecifiedNuis",stringOfOtherNuis,datacards])

  else:
    print "currently not supported"
  
  outfilename="higgsCombineTest.MultiDimFit.mH120.root"
  print outfilename
    
  resfilename="nllscans/"+pp+"_"+outfilename
  call(["cp",outfilename, resfilename])
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
