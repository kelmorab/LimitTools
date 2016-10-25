import ROOT
ROOT.gROOT.SetBatch(True)
import sys

infile=sys.argv[1]
name=sys.argv[2]

inf=ROOT.TFile(infile,"READ")
cS=ROOT.TCanvas("cS","cS",1024,768)
cB=ROOT.TCanvas("cB","cB",1024,768)

cS.cd()
hS=inf.Get("covariance_fit_s")
hS.GetXaxis().SetLabelSize(0.02)
hS.GetYaxis().SetLabelSize(0.02)
hS.Draw("COLZ")
cS.SaveAs(name+"S.pdf")

cB.cd()
hB=inf.Get("covariance_fit_s")
hB.GetXaxis().SetLabelSize(0.02)
hB.GetYaxis().SetLabelSize(0.02)
hB.Draw("COLZ")
cB.SaveAs(name+"B.pdf")





