import ROOT
import sys
from subprocess import call
from array import array
ROOT.gROOT.SetBatch(True)
ROOT.gDirectory.cd('PyROOT:/')

if len(sys.argv)<=2 or sys.argv[1]=="-h" or sys.argv[1]=="--help":
  print "python NllPlotter.py [WithCorr|AnyOtherString] [blind|unblind] outputDir workspace paramsToPlot"
  exit(0)

blind=True

DoCorrelationString=sys.argv[1]
blindstring=sys.argv[2]
if blindstring=="unblind":
  blind=False
  
outputDir=sys.argv[3]
datacards=sys.argv[4]
inputparams=sys.argv[5:]




print "reading workspace for nuisances"
VetoBBB=True
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

params=["r"]

for par in inputparams:
  if par !="r" and par in params2:
    params.append(par)
  else:
    print "skipping "+par+" for this datacard"
#params+=inputparams
print params 

doFullCorrelations=False
if DoCorrelationString=="WithCorr":
  doFullCorrelations=True

counter=0

globalBestR=0.0
globalBestRNLL=9999.0
BinningFactor=10 

if params[0]!="r":
  print "r should really be first for full functionality"

for p in params:
  counter+=1

  #npoints=10

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
  #print stringOfOtherNuis
  
  pp=p.replace(" ","")
  
  outfilename=outputDir+"/"+pp+"_higgsCombineTest.MultiDimFit.mH120.root"
  print outfilename
  ff=ROOT.TFile(outfilename,"READ")
  t=ff.Get("limit")
  npoints=t.GetEntries()
  #minvalnll=2.1*t.GetMinimum("deltaNLL")
  minvalnll=-10
  maxvalnll=2.1*min(t.GetMaximum("deltaNLL"),40)
  #if pp=="r":
    #maxvalnll=10
    #print "DL r override"
  xarray=array("f",[0.0])
  yarray=array("f",[0.0])
  rarray=array("f",[0.0])
  varray=array("f",[0.0])
  
  ievtWithGlobalBestR=-1

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
    if ievtWithGlobalBestR>=0:
      thisValueAtGlobalBestR=globalBestR

  else:
    thisValueAtGlobalBestR=0.0
    t.SetBranchAddress(pp,xarray)
    t.SetBranchAddress("r",varray)
    deltaBestVal=9999.0
    bufferbestR=999.0
    for ievt in range(t.GetEntries()):
      t.GetEntry(ievt)
      #print varray[0]
      if abs(varray[0]-globalBestR)<deltaBestVal:
	deltaBestVal=abs(varray[0]-globalBestR)
	bufferbestR=varray[0]
	thisValueAtGlobalBestR=xarray[0]
    print pp, " = ", thisValueAtGlobalBestR,  " at r, closest one ", globalBestR, bufferbestR
    
  minpoi=t.GetMinimum(pp)
  maxpoi=t.GetMaximum(pp)
  markerline=ROOT.TLine(thisValueAtGlobalBestR,minvalnll,thisValueAtGlobalBestR,maxvalnll)
  markerline.SetLineColor(ROOT.kRed)
  
  h=ROOT.TH2D("h"+pp,"h"+pp,npoints*BinningFactor,minpoi-0.5,maxpoi+0.5,npoints*BinningFactor,minvalnll,maxvalnll)
  t.Project("h"+pp,"2*deltaNLL:"+pp,"","COLZ")
  c=ROOT.TCanvas("c","c",1024,768)
  h.GetXaxis().SetTitle(pp)
  h.GetYaxis().SetTitle("2*deltaNLL")
  
  h.Draw("COLZ")
  if not blind:
    markerline.Draw()
  
  #raw_input()
  #c.SetLogy()
  c.SetGridy()
  if counter==1:
    c.SaveAs(outputDir+"/"+"scans_nll.pdf[")
  if not (pp=="r" and blind):    
    c.SaveAs(outputDir+"/"+"scans_nll.pdf")
    #c.SaveAs(outputDir+"/"+""+pp+"_nll.png")
    c.SaveAs(outputDir+"/"+""+pp+"_nll.pdf")
  else:
    print "skipping blinded r"
  #h.SaveAs(outputDir+"/"+""+pp+"_nll.root")
  
  for op in listOfOtherNuis:
    thisminval=t.GetMinimum(op)-0.1
    thismaxval=t.GetMaximum(op)+0.1
    print op, thisminval, thismaxval
    
    markerline=ROOT.TLine(thisValueAtGlobalBestR,thisminval,thisValueAtGlobalBestR,thismaxval)
    markerline.SetLineColor(ROOT.kRed)
    
    hcorr=ROOT.TH2D("h"+op+"_vs_"+pp,"h"+op+"_vs_"+pp,npoints*BinningFactor,minpoi-0.5,maxpoi+0.5,npoints*BinningFactor,thisminval,thismaxval)
    t.Project("h"+op+"_vs_"+pp,op+":"+pp,"","COLZ")
    ccorr=ROOT.TCanvas("ccorr","ccorr",1024,768)
    hcorr.GetXaxis().SetTitle(pp)
    hcorr.GetYaxis().SetTitle(op)
    
    hcorr.Draw("COLZ")
    if not blind:
      markerline.Draw()
    #raw_input()
    #c.SetLogy()
    ccorr.SetGridy()
    ccorr.SaveAs(outputDir+"/"+"scans_nll.pdf")
    #ccorr.SaveAs(outputDir+"/"+"h"+op+"_vs_"+pp+".png")
  
  
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
	  if not blind:
	    if bestXMarker!=None:
	      #print "x"
	      bestXMarker.Draw()
	    if bestYMarker!=None:
	      #print "y"
	      bestYMarker.Draw()
	    #raw_input()
	  cfc.SaveAs(outputDir+"/"+"scans_nll.pdf")
    
  if counter==len(params):
    c.SaveAs(outputDir+"/"+"scans_nll.pdf]")

  
  ff.Close()

  
  
  
  
  
  
  
  
  
  
