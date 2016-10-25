import ROOT
import subprocess
import sys
from glob import glob
from array import array
ROOT.gROOT.SetBatch(True)
ROOT.gDirectory.cd('PyROOT:/')
ROOT.gStyle.SetOptTitle(0)
import CMS_lumi

infile=sys.argv[1]
inf=ROOT.TFile(infile,"READ")
outfolder=sys.argv[2]
doPrePost=sys.argv[3]
if len(sys.argv)>4:
  doNorm=sys.argv[4]
  if doNorm!="no":
    doNorm=True


FitType="prefit"
if doPrePost=="postfit":
  FitType="postfit"


samples=["ttbarOther","ttbarPlusCCbar","ttbarPlusB","ttbarPlus2B","ttbarPlusBBbar"]
colors=[ROOT.kRed,ROOT.kGreen,ROOT.kMagenta,ROOT.kCyan,ROOT.kAzure]
names=["t#bar{t}+lf","t#bar{t}+c#bar{c}","t#bar{t}+b","t#bar{t}+2b","t#bar{t}+b#bar{b}"]
#cats=["ljets_j4_t3","ljets_j4_t4_low","ljets_j4_t4_high","ljets_j5_t3","ljets_j5_tge4_low","ljets_j5_tge4_high","ljets_jge6_t2","ljets_jge6_t3","ljets_jge6_tge4_low","ljets_jge6_tge4_high"]
cats=["dl_gej4get4","dl_gej4t2","dl_gej4t3","dl_j3t2","dl_j3t3","sl_boost","sl_gej6get4_high","sl_gej6get4_low","sl_gej6t2","sl_gej6t3","sl_j4t3","sl_j4t4_high","sl_j4t4_low","sl_j5get4_high","sl_j5get4_low","sl_j5t3"]
newnames=['#geq4 j #geq4 t', '#geq4 j 2 t', '#geq4 j 3 t', '3 j 2 t', '3 j 3 t', 'boosted', '#geq6 j #geq4 t high', '#geq6 j #geq4 t low', '#geq6 j 2 t', '#geq6 j 3 t', '4 j 3 t', '4 j 4 t high', '4 j 4 t low', '5 j #geq4 t high', '5 j #geq4 t low', '5 j 3 t']

#for cat in cats:
  #newnames.append(cat.replace("_","").replace("sl","").replace("dl","").replace("gej","#geq").replace("j","").replace("get"," j #geq").replace("t"," j "))
#print newnames


for cat in cats:
  print cat
  histos=[]
  for s,c,n, w in zip(samples,colors,names, newnames):
    thish=inf.Get(cat+"_"+FitType+"/"+s)
    thisclone=thish.Clone()
    thisclone.SetTitle(n)
    #thisclone.SetFillColor(c)
    thisclone.SetLineColor(c)
    thisclone.SetFillStyle(0)
    thisclone.GetXaxis().SetTitle(w+" discriminant "+FitType)
    if doNorm:
      thisclone.Scale(1.0/thisclone.Integral())
    histos.append(thisclone)
  
  c=ROOT.TCanvas("_"+cat,"_"+cat,1024,768)
  yMax=0
  for h in histos:
    if h.GetMaximum()>yMax:
      yMax=h.GetMaximum()
  for ih, h in enumerate(histos):
    if ih==0:
      h.SetStats(0)
      h.GetYaxis().SetRangeUser(0.0,yMax*1.3)
      
      h.GetYaxis().SetTitle("Events")
      if doNorm:
	h.GetYaxis().SetTitle("normalized")
      h.GetYaxis().SetTitleOffset(1.3)
      
      h.Draw("hist")
    else:
      h.Draw("histsame")
  legend=ROOT.TLegend()
  legend.SetX1NDC(0.7)
  legend.SetX2NDC(0.9)
  legend.SetY1NDC(0.6)
  legend.SetY2NDC(0.85)
  legend.SetBorderSize(0);
  legend.SetLineStyle(0);
  legend.SetTextFont(42);
  legend.SetTextSize(0.05);
  legend.SetFillStyle(0);
  for h in histos:
    legend.AddEntry(h,h.GetTitle(),"L")
  legend.Draw()
  c.Update()
  
  CMS_lumi.lumi_13TeV = "2.7 fb^{-1}"
  CMS_lumi.writeExtraText = 1
  CMS_lumi.extraText = "Preliminary"
  CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

  CMS_lumi.cmsTextSize = 0.55
  CMS_lumi.cmsTextOffset = 0.1
  CMS_lumi.lumiTextSize = 0.43
  CMS_lumi.lumiTextOffset = 0.2
  
  CMS_lumi.relPosX = 0.15
  
  CMS_lumi.hOffset = 0.05
  
  iPeriod=4   # 13TeV
  iPos=0     # CMS inside frame
  
  CMS_lumi.CMS_lumi(c, iPeriod, iPos)
  
  normSuffix=""
  if doNorm:
    normSuffix="_normalized"
  c.SaveAs(outfolder+"/"+FitType+"_"+cat+normSuffix+".png")
  c.SaveAs(outfolder+"/"+FitType+"_"+cat+normSuffix+".pdf")
  c.SaveAs(outfolder+"/"+FitType+"_"+cat+normSuffix+".root")

inf.Close()
    