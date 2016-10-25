import ROOT
import subprocess
import sys
from glob import glob
from array import array
ROOT.gROOT.SetBatch(True)
ROOT.gDirectory.cd('PyROOT:/')

infile=sys.argv[1]
inf=ROOT.TFile(infile,"READ")
outfolder=sys.argv[2]
doPrePost=sys.argv[3]

FitType="prefit"
if doPrePost=="postfit":
  FitType="postfit"


samples=["ttbarOther","ttbarPlusCCbar","ttbarPlusB","ttbarPlus2B","ttbarPlusBBbar"]
colors=[ROOT.kRed,ROOT.kGreen,ROOT.kMagenta,ROOT.kCyan,ROOT.kAzure]
names=["t#bar{t}+lf","t#bar{t}+c#bar{c}","t#bar{t}+b","t#bar{t}+2b","t#bar{t}+b#bar{b}"]
#cats=["ljets_j4_t3","ljets_j4_t4_low","ljets_j4_t4_high","ljets_j5_t3","ljets_j5_tge4_low","ljets_j5_tge4_high","ljets_jge6_t2","ljets_jge6_t3","ljets_jge6_tge4_low","ljets_jge6_tge4_high"]
cats=["sl_boost","sl_gej6get4_high","sl_gej6get4_low","sl_gej6t2","sl_gej6t3","sl_j4t3","sl_j4t4_high","sl_j4t4_low","sl_j5get4_high","sl_j5get4_low","sl_j5t3"]

for cat in cats:
  print cat
  histos=[]
  for s,c,n in zip(samples,colors,names):
    thish=inf.Get(cat+"_"+FitType+"/"+s)
    thisclone=thish.Clone()
    thisclone.SetTitle(n)
    thisclone.SetFillColor(c)
    thisclone.SetLineColor(c)
    histos.append(thisclone)
  
  c=ROOT.TCanvas("_"+cat,"_"+cat,1024,768)  
  for ih, h in enumerate(histos):
    if ih==0:
      h.Draw("histoE")
    else:
      h.Draw("histoEsame")
  c.SaveAs(outfolder+"/"+FitType+"_"+cat+".png")
  c.SaveAs(outfolder+"/"+FitType+"_"+cat+".pdf")
  c.SaveAs(outfolder+"/"+FitType+"_"+cat+".root")

inf.Close()
    