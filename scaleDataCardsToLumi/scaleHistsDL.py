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
directorylist=inf.GetListOfKeys()
print len(directorylist), " directories in file"

for di in directorylist:
  thisdir=inf.Get(di.GetName())
  #print thisdir.GetName(), " current DIR"
  thisdirhistlist=thisdir.GetListOfKeys()
  outf.cd()
  outf.mkdir(di.GetName())
  inf.cd()
  #inf.ls()
  for ih in range(len(thisdirhistlist)):
    inf.cd()
    #inf.cd(thisdir.GetName())
    #thisdir.ls()
    thishist=inf.Get(thisdir.GetName()+"/"+thisdirhistlist.At(ih).GetName())
    #print thisdirhistlist.At(ih).GetName()
    if not isinstance(thishist, ROOT.TH1):
      #print "skipping ", thisdirhistlist.At(ih).GetName()
      continue
    #print thishist.Integral()
    thishist.Scale(scaleFactor)
    #print thishist.Integral()
    thishist.SetName(thisdirhistlist.At(ih).GetName())
    outf.cd()
    outf.cd(thisdir.GetName())
    thishist.Write()
  
inf.Close()
outf.Close()
