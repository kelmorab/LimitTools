
import ROOT
import subprocess
import sys
from glob import glob
from array import array
import math
ROOT.gROOT.SetBatch(True)
ROOT.gDirectory.cd('PyROOT:/')

incard=sys.argv[1]
inroot=sys.argv[2]

inf=open(incard,"r")
inlist=list(inf)

binname=""
proclist=[]

outlines=[]
for l in inlist:
  #print l
  splitline=l.replace(" ","").replace("\n","").split("\t")
  #print splitline
  #splitline[-1]=="":
    #splitline=splitline[:-1]
  
  if splitline[0]=="bin":
    binname=splitline[1]
    print binname
  
  if splitline[0]=="process" and "ttH" in splitline[1]:
    proclist=splitline[1:-1]
    print proclist
  outlines.append(l.replace("\n",""))
inf.close()

#get nBins
hf=ROOT.TFile(inroot,"READ")
#h=hf.Get(binname+"_BDT/ttH_hbb")
#nBins=h.GetNbinsX()
#print "nbins = ", nBins


bkgs=['ttbarPlusBBbar', 'ttbarPlusB', 'ttbarPlus2B', 'ttbarPlusCCbar', 'ttbarOther', 'singlet', 'wjets', 'zjets', 'ttbarW', 'ttbarZ', 'diboson']
signals=['ttH_hbb', 'ttH_hcc', 'ttH_hgluglu', 'ttH_hgg', 'ttH_htt', 'ttH_hww', 'ttH_hzz', 'ttH_hzg']

for ip, s in enumerate(proclist):
  #if s not in ["ttbarPlusBBbar",  "ttbarPlusB",     "ttbarPlus2B",     "ttbarPlusCCbar",  "ttbarOther"]:
    #continue
  datahist=hf.Get(binname+"_BDT/data_obs")
  #print datahist
  prochist=hf.Get(binname+"_BDT/"+s)
  #print prochist
  bkg1hist=hf.Get(binname+"_BDT/"+bkgs[0])
  bkgsumhist=bkg1hist.Clone()
  for b in bkgs:
    thish=hf.Get(binname+"_BDT/"+b)
    bkgsumhist.Add(thish)
  bkg1hist=hf.Get(binname+"_BDT/"+bkgs[0])
  bkgsumhist=bkg1hist.Clone()
  #print bkgsumhist.Integral()
  for b in bkgs[1:]:
    thish=hf.Get(binname+"_BDT/"+b)
    bkgsumhist.Add(thish)
    #print bkgsumhist.Integral()
  signal1hist=hf.Get(binname+"_BDT/"+signals[0])
  signalsumhist=signal1hist.Clone()
  for bs in signals[1:]:
    thish=hf.Get(binname+"_BDT/"+s)
    signalsumhist.Add(thish)
    #print bkgsumhist.Integral()
  #print "s ", signalsumhist.Integral()
  
  nBins=prochist.GetNbinsX()

  for ib in range(nBins):
    bbb=ib+1
    data = datahist.GetBinContent(bbb)
    data_err = math.sqrt(datahist.GetBinContent(bbb))

    sig = signalsumhist.GetBinContent(bbb)
    sig_err = signalsumhist.GetBinError(bbb)

    bkg = bkgsumhist.GetBinContent(bbb)
    bkg_err = bkgsumhist.GetBinError(bbb)

    val = prochist.GetBinContent(bbb)
    val_err = prochist.GetBinError(bbb)

    other_frac = math.sqrt(bkg_err**2 - val_err**2)

    pruneBinByBin=True
    if pruneBinByBin:
    #Changed from data_err/3 -> data_err/5 and sig/bkg < 0.02 -> 0.01 - KPL
      #if val < .01 or bkg_err < data_err / 5. or other_frac / bkg_err > .95  or sig / bkg < .01:
      if val < .01 or bkg_err < data_err / 7. or other_frac / bkg_err > .98  or sig / bkg < .005:
	#print "pruned ", bbb, s, "  ", val, bkg_err, "<", data_err / 5. , other_frac / bkg_err , sig / bkg
	continue
    
    print "!!kept ", bbb, s
    newline="CMS_ttH_"+s+"_"+binname+"_13TeV_BDTbin"+str(ib+1)+"\t"+"shape"
    print newline
    for counter in range(len(proclist)):
      newline+="\t"
      if counter==ip:
	newline+="1"
      else:
	newline+="-"
    outlines.append(newline)

outf=open(incard,"w")
for l in outlines:
  outf.write(l+"\n")
outf.close()

hf.Close()