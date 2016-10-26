import ROOT
import sys
import os
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

incardname=sys.argv[1]
mlfitfile=sys.argv[2]
outputDir=sys.argv[3]

infprocs=[]
channels=[]
catnames=[]

procs="ttbarOther ttbarPlusB ttbarPlus2B ttbarPlusBBbar ttbarPlusCCbar singlet wjets zjets ttbarW ttbarZ diboson".split(" ")
colors=[ROOT.kRed-7,ROOT.kRed-2,ROOT.kRed+2,ROOT.kRed+3,ROOT.kRed+1,ROOT.kMagenta,ROOT.kGreen-7,ROOT.kGreen-3,ROOT.kBlue-10,ROOT.kBlue-6,ROOT.kAzure+2]
infl=open(incardname,"r")
inlist=list(infl)
for line in inlist:
  if "process " in line and infprocs==[]:
    print "found process line"
    sl=line.replace("\n","").replace("\t","").replace("  "," ").split(" ")
    print sl
    for pl in sl[1:]:
      if "ttH" in pl:
	continue
      infprocs.append(pl)
  if "Combination of" in line:
    sl=line.replace("\n","").replace("\t"," ").replace("  "," ").split(" ")
    print sl
    for icat, cat in enumerate(sl[2:]):
      channels.append("ch"+str(icat+1))
      catnames.append(cat.replace("ttH_hbb_13TeV_","").replace(".txt",""))

#print infprocs
print catnames
print channels

infl.close()

f=ROOT.TFile(mlfitfile,"READ")



if not os.path.exists(outputDir):
    os.makedirs(outputDir)

buff=ROOT.TCanvas("buff","buff",800,600)
buff.SaveAs(outputDir+"/plots.pdf[")

for cn, ch in zip(catnames,channels):
  	canvas=ROOT.TCanvas("c","c",800,600)
        canvas.SetGridy()
	
        legend=ROOT.TLegend()
	legend.SetX1NDC(0.6)
	legend.SetX2NDC(0.95)
	legend.SetY1NDC(0.4)
	legend.SetY2NDC(0.88)
	legend.SetBorderSize(0);
	legend.SetLineStyle(0);
	legend.SetTextFont(42);
	legend.SetTextSize(0.03);
	legend.SetFillStyle(0);	
	
	histos=[]
        stack=ROOT.THStack(cn+"_prefit",cn+"_prefit")
        for p,col in zip(procs,colors):
	  print "shapes_prefit/"+ch+"/"+p
	  if f.Get("shapes_prefit/"+ch+"/"+p)!=None:
	    histos.append(f.Get("shapes_prefit/"+ch+"/"+p).Clone())
	  
	  histos[-1].SetLineColor(ROOT.kBlack)
	  histos[-1].SetFillColor(col)
	  stack.Add(histos[-1],"hist")
	  integ=histos[-1].Integral()
	  legend.AddEntry(histos[-1], p+" %.1f" % integ, "F")
	canvas.cd()
	stack.Draw()
	legend.Draw()
	canvas.SaveAs(outputDir+"/plots.pdf")
	
	#psotfit b
	
	canvas=ROOT.TCanvas("c","c",800,600)
	canvas.SetGridy()
	

        legend=ROOT.TLegend()
	legend.SetX1NDC(0.6)
	legend.SetX2NDC(0.95)
	legend.SetY1NDC(0.4)
	legend.SetY2NDC(0.88)
	legend.SetBorderSize(0);
	legend.SetLineStyle(0);
	legend.SetTextFont(42);
	legend.SetTextSize(0.03);
	legend.SetFillStyle(0);	
	
	histos=[]
        stack=ROOT.THStack(cn+"shapes_fit_b",cn+"shapes_fit_b")
        for p,col in zip(procs,colors):
	  print "shapes_fit_b/"+ch+"/"+p
	  if f.Get("shapes_fit_b/"+ch+"/"+p)!=None:
	    histos.append(f.Get("shapes_fit_b/"+ch+"/"+p).Clone())
	  
	  histos[-1].SetLineColor(ROOT.kBlack)
	  histos[-1].SetFillColor(col)
	  stack.Add(histos[-1],"hist")
	  integ=histos[-1].Integral()
	  legend.AddEntry(histos[-1], p+" %.1f" % integ, "F")
	canvas.cd()
	stack.Draw()
	legend.Draw()
	canvas.SaveAs(outputDir+"/plots.pdf")
	
buff.SaveAs(outputDir+"/plots.pdf]") 



