import ROOT
import sys
from subprocess import call
from array import array
ROOT.gROOT.SetBatch(True)
ROOT.gDirectory.cd('PyROOT:/')


datacards=sys.argv[1]

params=sys.argv[2:]

params2=['r', 'CMS_res_j', 'CMS_scale_j', 'CMS_ttH_CSVCErr1', 'CMS_ttH_CSVCErr2', 'CMS_ttH_CSVHF', 'CMS_ttH_CSVHFStats1', 'CMS_ttH_CSVHFStats2', 'CMS_ttH_CSVLF', 'CMS_ttH_CSVLFStats1', 'CMS_ttH_CSVLFStats2', 'CMS_ttH_PSscale_ttbarOther', 'CMS_ttH_PSscale_ttbarPlus2B', 'CMS_ttH_PSscale_ttbarPlusB', 'CMS_ttH_PSscale_ttbarPlusBBbar', 'CMS_ttH_PSscale_ttbarPlusCCbar', 'CMS_ttH_PU', 'CMS_ttH_Q2scale_ttbarOther', 'CMS_ttH_Q2scale_ttbarPlus2B', 'CMS_ttH_Q2scale_ttbarPlusB', 'CMS_ttH_Q2scale_ttbarPlusBBbar', 'CMS_ttH_Q2scale_ttbarPlusCCbar', 'CMS_ttH_QCDscale_ttbarPlus2B', 'CMS_ttH_QCDscale_ttbarPlusB', 'CMS_ttH_QCDscale_ttbarPlusBBbar', 'CMS_ttH_QCDscale_ttbarPlusCCbar', 
	 #'CMS_ttH_dl_Trig',
	 'CMS_ttH_eff_lepton',
	 #'CMS_ttH_ljets_Trig', 
	 'QCDscale_V', 'QCDscale_VV', 'QCDscale_singlet', 'QCDscale_ttH', 'QCDscale_ttbar', 'lumi_13TeV', 'pdf_gg', 'pdf_gg_ttH', 'pdf_qg', 'pdf_qqbar']

if "dilepton" in datacards:
  params2+=['CMS_ttH_dl_Trig']
elif "singlelepton" in datacards:
  params2+=['CMS_ttH_ljets_Trig']
else:
  params2+=['CMS_ttH_ljets_Trig', 'CMS_ttH_dl_Trig']

floatmode="--floatOtherPOI=1"
floatR=True
doFullCorrelations=True

counter=0

globalBestR=0.0
globalBestRNLL=9999.0

if params[0]!="r":
  print "r should be first for full functionality"

for p in params:
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
    #if op=="r":
      #continue
    else:
      listOfOtherNuis.append(op)
  stringOfOtherNuis=",".join(listOfOtherNuis)
  print stringOfOtherNuis
  
  pp=p.replace(" ","")
  #cmd="combine -M MultiDimFit --algo=grid --points=10 --rMin -5 --rMax 5 "+floatmode+" -P "+pp+" ttH_hbb_13TeV_sl_noMC.txt -n _nllScan_"+pp
  #print cmd
  #if floatR:
    #call(["combine","-M","MultiDimFit","--algo=grid","-m","125","--points="+str(npoints),floatmode,"-P",pp,"--redefineSignalPOIs",pp,"--setPhysicsModelParameterRanges",pp+"="+str(minr)+","+str(maxr),"--saveInactivePOI","1","--saveSpecifiedNuis",stringOfOtherNuis,datacards])
    ##call(["combine","-M","MultiDimFit","--algo=grid","--points="+str(npoints),floatmode,"-P",pp,"--redefineSignalPOIs",pp,"--setPhysicsModelParameterRanges",pp+"="+str(minr)+","+str(maxr),"--saveInactivePOI","--saveSpecifiedNuis",stringOfOtherNuis,datacards])

  #else:
    #print "currently not supported"
    ##call(["combine","-M","MultiDimFit","--algo=grid","--points=100",floatmode,"-P",pp,"--redefineSignalPOIs","r,"+pp,"--setPhysicsModelParameterRanges","r=-"+str(minr)*","+str(maxr)+":"+pp+"=-5,5" ,datacards])
  
  outfilename=pp+"_higgsCombineTest.MultiDimFit.mH120.root"
  print outfilename
  ff=ROOT.TFile(outfilename,"READ")
  t=ff.Get("limit")
  #minvalnll=2.1*t.GetMinimum("deltaNLL")
  minvalnll=-0.5
  maxvalnll=2.1*min(t.GetMaximum("deltaNLL"),100)
  #if pp=="r":
    #maxvalnll=10
    #print "DL r override"
  xarray=array("f",[0.0])
  yarray=array("f",[0.0])
  rarray=array("f",[0.0])
  varray=array("f",[0.0])
  
  ievtWithGlobalBestR=0

  if pp=="r":
    t.SetBranchAddress(pp,rarray)
    t.SetBranchAddress("deltaNLL",yarray)
    for ievt in range(t.GetEntries()):
      t.GetEntry(ievt)
      if yarray[0]<globalBestRNLL:
	globalBestRNLL=yarray[0]
	globalBestR=rarray[0]
	ievtWithGlobalBestR=ievt
    print "best fit r ", globalBestR, " at ", globalBestRNLL, ievtWithGlobalBestR
    thisValueAtGlobalBestR=globalBestR

  else:
    thisValueAtGlobalBestR=0.0
    t.SetBranchAddress(pp,xarray)
    t.SetBranchAddress("r",varray)
    deltaBestVal=9999.0
    bufferbestR=999.0
    for ievt in range(t.GetEntries()):
      t.GetEntry(ievt)
      print varray[0]
      if abs(varray[0]-globalBestR)<deltaBestVal:
	deltaBestVal=abs(varray[0]-globalBestR)
	bufferbestR=varray[0]
	thisValueAtGlobalBestR=xarray[0]
    print pp, " = ", thisValueAtGlobalBestR,  " at r, closest one ", globalBestR, bufferbestR
    
    
  markerline=ROOT.TLine(thisValueAtGlobalBestR,minvalnll,thisValueAtGlobalBestR,maxvalnll)
  markerline.SetLineColor(ROOT.kRed)
  
  h=ROOT.TH2D("h"+pp,"h"+pp,npoints*4,minpoi-0.5,maxpoi+0.5,npoints*4,minvalnll,maxvalnll)
  t.Project("h"+pp,"2*deltaNLL:"+pp,"","COLZ")
  c=ROOT.TCanvas("c","c",1024,768)
  h.GetXaxis().SetTitle(pp)
  h.GetYaxis().SetTitle("2*deltaNLL")
  
  h.Draw("COLZ")
  markerline.Draw()
  
  #raw_input()
  #c.SetLogy()
  c.SetGridy()
  if counter==1:
    c.SaveAs("scans_nll.pdf[")
  c.SaveAs("scans_nll.pdf")
  c.SaveAs(""+pp+"_nll.png")
  c.SaveAs(""+pp+"_nll.pdf")
  h.SaveAs(""+pp+"_nll.root")
  
  for op in listOfOtherNuis:
    thisminval=t.GetMinimum(op)-0.1
    thismaxval=t.GetMaximum(op)+0.1
    
    markerline=ROOT.TLine(thisValueAtGlobalBestR,thisminval,thisValueAtGlobalBestR,thismaxval)
    markerline.SetLineColor(ROOT.kRed)
    
    hcorr=ROOT.TH2D("h"+op+"_vs_"+pp,"h"+op+"_vs_"+pp,npoints*4,minpoi-0.5,maxpoi+0.5,npoints*4,thisminval,thismaxval)
    t.Project("h"+op+"_vs_"+pp,op+":"+pp,"","COLZ")
    ccorr=ROOT.TCanvas("ccorr","ccorr",1024,768)
    hcorr.GetXaxis().SetTitle(pp)
    hcorr.GetYaxis().SetTitle(op)
    
    hcorr.Draw("COLZ")
    markerline.Draw()
    #raw_input()
    #c.SetLogy()
    ccorr.SetGridy()
    ccorr.SaveAs("scans_nll.pdf")
    ccorr.SaveAs("h"+op+"_vs_"+pp+".png")
  
  
  if pp=="r" and doFullCorrelations:
      print "doing full correlations"
      listOfArrays=[]
      for on in listOfOtherNuis:
	listOfArrays.append([on,array("f",[0.0])])
        t.SetBranchAddress(on,listOfArrays[-1][1])
      listOfCorrelationHistos=[]
      for ni in range(len(listOfArrays)):
	for nj in range(len(listOfArrays)):
	  if nj<ni:
	    continue
	  print "doing ", listOfArrays[ni][0]+"_vs_"+listOfArrays[nj][0]+"_atBestR"
	  xvalmin=t.GetMinimum(listOfArrays[ni][0])-0.001
	  xvalmax=t.GetMaximum(listOfArrays[ni][0])+0.001
	  yvalmin=t.GetMinimum(listOfArrays[nj][0])-0.001
	  yvalmax=t.GetMaximum(listOfArrays[nj][0])+0.001
	  print xvalmin,xvalmax,yvalmin,yvalmax
	  
	  listOfCorrelationHistos.append(ROOT.TH2D(listOfArrays[ni][0]+"_vs_"+listOfArrays[nj][0]+"_atBestR",listOfArrays[ni][0]+"_vs_"+listOfArrays[nj][0]+"_atBestR",npoints*4,xvalmin,xvalmax,npoints*4,yvalmin,yvalmax))
	  listOfCorrelationHistos[-1].GetXaxis().SetTitle(listOfArrays[ni][0])
	  listOfCorrelationHistos[-1].GetYaxis().SetTitle(listOfArrays[nj][0])
	  listOfCorrelationHistos[-1].SetStats(0)
	  
	  bestXMarker=None
	  bestYMarker=None
	  for iievt in range(t.GetEntries()):
	    t.GetEntry(iievt)
	    listOfCorrelationHistos[-1].Fill(listOfArrays[ni][1][0],listOfArrays[nj][1][0])
	    #print listOfCorrelationHistos[-1].GetEntries()
	    if iievt==ievtWithGlobalBestR:
	      bestXMarker=ROOT.TLine(listOfArrays[ni][1][0],yvalmin,listOfArrays[ni][1][0],yvalmax)
	      bestYMarker=ROOT.TLine(xvalmin, listOfArrays[nj][1][0],xvalmax,listOfArrays[nj][1][0])
	      bestXMarker.SetLineColor(ROOT.kRed)
	      bestYMarker.SetLineColor(ROOT.kRed)
	  cfc=ROOT.TCanvas("c"+listOfArrays[ni][0]+"_vs_"+listOfArrays[nj][0]+"_atBestR","c"+listOfArrays[ni][0]+"_vs_"+listOfArrays[nj][0]+"_atBestR",1024,768)
	  print listOfCorrelationHistos[-1].GetEntries()
	  listOfCorrelationHistos[-1].Draw("COLZ")
	  if bestXMarker!=None:
	    #print "x"
	    bestXMarker.Draw()
	  if bestYMarker!=None:
	    #print "y"
	    bestYMarker.Draw()
	  #raw_input()
	  cfc.SaveAs("scans_nll.pdf")
    
  if counter==len(params):
    c.SaveAs("scans_nll.pdf]")
  #if floatR==False:
    #h=ROOT.TH2D("h","h",100,-6,6,100,minvalnll,maxvalnll)
    #t.Project("h","2*deltaNLL:r","","COLZ")
    #c=ROOT.TCanvas("c","c",1024,768)
    #h.Draw("COLZ")
    ##raw_input()
    #c.SaveAs(""+pp+"_r_nll.png")
    #c.SaveAs(""+pp+"_r_nll.pdf")
  
  ff.Close()
  
  #resfilename=""+pp+"_"+outfilename
  #call(["cp",outfilename, resfilename])
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
