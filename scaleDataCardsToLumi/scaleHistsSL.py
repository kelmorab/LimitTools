import ROOT
import sys
#ROOT.gDirectory.cd('PyROOT:/')

infile=sys.argv[1]
outfile=sys.argv[2]
scaleFactorString=sys.argv[3]
scaleFactor=float(scaleFactorString)
scaleFactor=scaleFactor/2.7

print "scaling ", infile, " by ", str(scaleFactor), " output: ", outfile

inf=ROOT.TFile(infile,"READ")
outf=ROOT.TFile(outfile,"RECREATE")
histlist=inf.GetListOfKeys()
print len(histlist), " histos in file"

for ih in range(len(histlist)):
  inf.cd()
  thishist=inf.Get(histlist[ih].GetName())
  #print thishist.Integral()
  thishist.Scale(scaleFactor)
  #print thishist.Integral()
  outf.cd()
  thishist.Write()
  
inf.Close()
outf.Close()
