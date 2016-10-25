import ROOT
import sys
from subprocess import call
from array import array
from glob import glob
ROOT.gROOT.SetBatch(True)
ROOT.gDirectory.cd('PyROOT:/')

infilelist=glob("*_higgsCombineTest.MultiDimFit.mH120.root")

params=[]
for f in infilelist:
  fn=f.split("_frozen_")[0]
  params.append(fn)
print params

npoints=60

doFullCorrelations=True

counter=0

globalBestR=0.0
globalBestRNLL=9999.0

for p in params:
  globalBestRNLL=9999.0
  paramAtBestFit=0
  counter+=1
  minpoi=-2.5
  maxpoi=2.5
  minr=-8
  maxr=6
   
  outfilename=p+"_frozen_higgsCombineTest.MultiDimFit.mH120.root"
  print outfilename
  ff=ROOT.TFile(outfilename,"READ")
  t=ff.Get("limit")
  #minvalnll=2.1*t.GetMinimum("deltaNLL")
  minvalnll=-0.5
  maxvalnll=2.1*min(t.GetMaximum("deltaNLL"),100)
  minpoi=t.GetMinimum(p)
  maxpoi=t.GetMaximum(p)
  
  #if pp=="r":
    #maxvalnll=10
    #print "DL r override"
  xarray=array("f",[0.0])
  yarray=array("f",[0.0])
  rarray=array("f",[0.0])
  varray=array("f",[0.0])
  
  t.SetBranchAddress(p,varray)
  t.SetBranchAddress("deltaNLL",yarray)
  t.SetBranchAddress("r",rarray)
  for ievt in range(t.GetEntries()):
    t.GetEntry(ievt)
    if yarray[0]<globalBestRNLL:
      globalBestRNLL=yarray[0]
      paramAtBestFit=varray[0]
  
  markerline=ROOT.TLine(paramAtBestFit,minvalnll,paramAtBestFit,maxvalnll)
  markerline.SetLineColor(ROOT.kRed)
  
  h=ROOT.TH2D("h"+p,"h"+p,npoints*4,minpoi,maxpoi,npoints*4,minvalnll,maxvalnll)
  t.Project("h"+p,"2*deltaNLL:"+p,"","COLZ")
  c=ROOT.TCanvas("c","c",1024,768)
  h.GetXaxis().SetTitle(p)
  h.GetYaxis().SetTitle("2*deltaNLL")
  
  h.Draw("COLZ")
  markerline.Draw()
 
  #raw_input()
  #c.SetLogy()
  c.SetGridy()
  if counter==1:
    c.SaveAs("scans_nll.pdf[")
  c.SaveAs("scans_nll.pdf")
  #c.SaveAs(""+pp+"_nll.png")
  #c.SaveAs(""+pp+"_nll.pdf")
  #h.SaveAs(""+pp+"_nll.root")
  
  ##################
  h=ROOT.TH2D("hr_"+p,"hr_"+p,npoints*4,minr-0.5,maxr+0.5,npoints*4,minvalnll,maxvalnll)
  t.Project("hr_"+p,"2*deltaNLL:"+"r","","COLZ")
  c=ROOT.TCanvas("c","c",1024,768)
  h.GetXaxis().SetTitle("r")
  h.GetYaxis().SetTitle("2*deltaNLL")  
  h.Draw("COLZ")
  c.SetGridy()
  c.SaveAs("scans_nll.pdf")  
  
  ####################
  
  h=ROOT.TH2D("hr_vs_"+p,"hr_vs_"+p,npoints*4,minr-0.5,maxr+0.5,npoints*4,minpoi,maxpoi)
  t.Project("hr_vs_"+p,p+":r","","COLZ")
  c=ROOT.TCanvas("c","c",1024,768)
  h.GetXaxis().SetTitle("r")
  h.GetYaxis().SetTitle(p)  
  h.Draw("COLZ")
  c.SetGridy()
  c.SaveAs("scans_nll.pdf")  
  
    
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
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
