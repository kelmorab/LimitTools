import ROOT
import sys
from subprocess import call
ROOT.gROOT.SetBatch(True)

datacards=sys.argv[1]

params=sys.argv[2:]
print params
params2=['r', 'CMS_res_j', 'CMS_scale_j', 'CMS_ttH_CSVCErr1', 'CMS_ttH_CSVCErr2', 'CMS_ttH_CSVHF', 'CMS_ttH_CSVHFStats1', 'CMS_ttH_CSVHFStats2', 'CMS_ttH_CSVLF', 'CMS_ttH_CSVLFStats1', 'CMS_ttH_CSVLFStats2', 'CMS_ttH_PSscale_ttbarOther', 'CMS_ttH_PSscale_ttbarPlus2B', 'CMS_ttH_PSscale_ttbarPlusB', 'CMS_ttH_PSscale_ttbarPlusBBbar', 'CMS_ttH_PSscale_ttbarPlusCCbar', 'CMS_ttH_PU', 'CMS_ttH_Q2scale_ttbarOther', 'CMS_ttH_Q2scale_ttbarPlus2B', 'CMS_ttH_Q2scale_ttbarPlusB', 'CMS_ttH_Q2scale_ttbarPlusBBbar', 'CMS_ttH_Q2scale_ttbarPlusCCbar', 'CMS_ttH_QCDscale_ttbarPlus2B', 'CMS_ttH_QCDscale_ttbarPlusB', 'CMS_ttH_QCDscale_ttbarPlusBBbar', 'CMS_ttH_QCDscale_ttbarPlusCCbar',
	 #'CMS_ttH_dl_Trig', 
	 'CMS_ttH_eff_lepton',
	 #'CMS_ttH_ljets_Trig', 
	 'QCDscale_V', 'QCDscale_VV', 'QCDscale_singlet', 'QCDscale_ttH', 'QCDscale_ttbar', 'lumi_13TeV', 'pdf_gg', 'pdf_gg_ttH', 'pdf_qg', 'pdf_qqbar']


#floatmode="--floatOtherPOI=1"
floatR=True
doPlots=False

counter=0

for p in params:
  #if p!="CMS_ttH_QCDscale_ttbarPlusB":
    #continue
  counter+=1
  if p=="r":
    if "dilepton" in datacards:
      minpoi=-8
      maxpoi=5
      minr=-8
      maxr=5
    else:
      minpoi=-5
      maxpoi=5
      minr=-5
      maxr=5
  else:
    minpoi=-2.5
    maxpoi=2.5
    minr=-5
    maxr=5
  
  npoints=60
  
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
  #cmd="combine -M MultiDimFit --algo=grid --points=10 --rMin -5 --rMax 5 "+floatmode+" -P "+pp+" ttH_hbb_13TeV_sl_noMC.txt -n _nllScan_"+pp
  #print cmd
  if floatR:
    call(["combine","-M","MultiDimFit","--algo=grid","--points="+str(npoints),"--floatOtherPOI","1","--redefineSignalPOIs","r","-P",pp,"--setPhysicsModelParameterRanges",pp+"="+str(minpoi)+","+str(maxpoi),"--rMin",str(minr),"--rMax",str(maxr),"--saveInactivePOI","1","--saveSpecifiedNuis",stringOfOtherNuis,datacards])
    #call(["combine","-M","MultiDimFit","--algo=grid","--points="+str(npoints),floatmode,"-P",pp,"--redefineSignalPOIs",pp,"--setPhysicsModelParameterRanges",pp+"="+str(minr)+","+str(maxr),"--saveInactivePOI","--saveSpecifiedNuis",stringOfOtherNuis,datacards])

  else:
    print "currently not supported"
    #call(["combine","-M","MultiDimFit","--algo=grid","--points=100",floatmode,"-P",pp,"--redefineSignalPOIs","r,"+pp,"--setPhysicsModelParameterRanges","r=-"+str(minr)*","+str(maxr)+":"+pp+"=-5,5" ,datacards])
  
  outfilename="higgsCombineTest.MultiDimFit.mH120.root"
  print outfilename
  if doPlots==True:
    ff=ROOT.TFile(outfilename,"READ")
    print ff
    t=ff.Get("limit")
    print t
    #minvalnll=2.1*t.GetMinimum("deltaNLL")
    minvalnll=-0.5
    maxvalnll=2.1*min(t.GetMaximum("deltaNLL"),100)
    if pp=="r":
      maxvalnll=10
      print "DL r override"

    #minvalnll=-1
    #maxvalnll=30


    h=ROOT.TH2D("h"+pp,"h"+pp,npoints*4,minpoi-0.5,maxpoi+0.5,npoints*4,minvalnll,maxvalnll)
    t.Project("h"+pp,"2*deltaNLL:"+pp,"","COLZ")
    c=ROOT.TCanvas("c","c",1024,768)
    h.GetXaxis().SetTitle(pp)
    h.GetYaxis().SetTitle("2*deltaNLL")
    
    h.Draw("COLZ")
    #raw_input()
    #c.SetLogy()
    c.SetGridy()
    if counter==1:
      c.SaveAs("nllscans/scans_nll.pdf[")
    c.SaveAs("nllscans/scans_nll.pdf")
    c.SaveAs("nllscans/"+pp+"_nll.png")
    c.SaveAs("nllscans/"+pp+"_nll.pdf")
    h.SaveAs("nllscans/"+pp+"_nll.root")
    
    for op in listOfOtherNuis+["r"]:
      thisminval=t.GetMinimum(op)-0.5
      thismaxval=t.GetMaximum(op)+0.5
      
      hcorr=ROOT.TH2D("h"+op+"_vs_"+pp,"h"+op+"_vs_"+pp,npoints*4,minpoi-1,maxpoi+2,npoints*4,thisminval,thismaxval)
      t.Project("h"+op+"_vs_"+pp,op+":"+pp,"","COLZ")
      ccorr=ROOT.TCanvas("ccorr","ccorr",1024,768)
      hcorr.Draw("COLZ")
      hcorr.GetXaxis().SetTitle(pp)
      hcorr.GetYaxis().SetTitle(op)
      
      #raw_input()
      #c.SetLogy()
      ccorr.SetGridy()
      ccorr.SaveAs("nllscans/scans_nll.pdf")
    if counter==len(params):
    #if counter==1:
      c.SaveAs("nllscans/scans_nll.pdf]")
      
    if floatR==False:
      h=ROOT.TH2D("h","h",100,-6,6,100,minvalnll,maxvalnll)
      t.Project("h","2*deltaNLL:r","","COLZ")
      c=ROOT.TCanvas("c","c",1024,768)
      h.Draw("COLZ")
      #raw_input()
      c.SaveAs("nllscans/"+pp+"_r_nll.png")
      c.SaveAs("nllscans/"+pp+"_r_nll.pdf")
    
    ff.Close()
    
  resfilename="nllscans/"+pp+"_"+outfilename
  call(["cp",outfilename, resfilename])
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
