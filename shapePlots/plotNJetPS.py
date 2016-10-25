import ROOT
import sys
from array import array 
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

infname=sys.argv[1]
print "init"

cats=["N_Jets","N_BTagsM",]
#cats=[]
#for c in acats[:4]:
#  cats.append(c+"_high")
#  cats.append(c+"_low")

print "ok"
#procs=["ttH","ttbarOther","ttbarPlusCCbar","ttbarPlusB","ttbarPlus2B","ttbarPlusBBbar",]
#systs=['CMS_ttH_Q2scale_ttbarOther', 'CMS_ttH_Q2scale_ttbarPlusB', 'CMS_ttH_Q2scale_ttbarPlus2B', 'CMS_ttH_Q2scale_ttbarPlusBBbar', 'CMS_ttH_Q2scale_ttbarPlusCCbar', 'CMS_ttH_CSVLF', 'CMS_ttH_CSVHF', 'CMS_ttH_CSVHFStats1', 'CMS_ttH_CSVLFStats1', 'CMS_ttH_CSVHFStats2', 'CMS_ttH_CSVLFStats2', 'CMS_ttH_CSVCErr1', 'CMS_ttH_CSVCErr2', 'CMS_scale_j', 'CMS_ttH_PU', 'CMS_res_j', 'CMS_ttH_eff_mu', 'CMS_ttH_eff_el', 'CMS_ttH_ljets_Trig_mu', 'CMS_ttH_ljets_Trig_el']
systs=["CMS_ttH_PSscale_ttbarOther","CMS_ttH_PSscale_ttbarPlusB","CMS_ttH_PSscale_ttbarPlus2B","CMS_ttH_PSscale_ttbarPlusBBbar","CMS_ttH_PSscale_ttbarPlusCCbar"]


procs="ttbarOther ttbarPlusB ttbarPlus2B ttbarPlusBBbar ttbarPlusCCbar".split(" ")
print procs

inf=ROOT.TFile(infname,"READ")

buff=ROOT.TCanvas("buff","buff",800,600)
buff.Print('PSshapes'+'.pdf[')

ratiobuff=ROOT.TCanvas("ratiobuff","ratiobuff",800,300)
ratiobuff.Print('ratioPSshapes'+'.pdf[')

counter=0
for c in cats:
  print c
  if "ljets" in c:
    discname="finaldiscr"
  else:
    discname="inputVar"
  discname=""
  for p in procs:
    nom=inf.Get(p+"_"+c)
    for s in systs:
      print p+"_"+c+"_"+s
      up=inf.Get(p+"_"+c+"_"+s+"Up")
      down=inf.Get(p+"_"+c+"_"+s+"Down")
      if up!=None and down!=None:
	up.SetLineColor(ROOT.kRed)
	up.SetTitle("up")
	down.SetTitle("down")
	down.SetLineColor(ROOT.kGreen)
	canvas=ROOT.TCanvas(p+"_"+c+"_"+s,p+"_"+discname+"_"+c+"_"+s,800,600)
	maxval=max(nom.GetMaximum(), max(up.GetMaximum(),down.GetMaximum()))
	nom.SetMaximum(1.5*maxval)
	nom.Draw("histoE")
	nom.SetTitle(c+"_"+p)
	up.Draw("histoSameE")
	down.Draw("histoSameE")
	integNom=nom.Integral()
	integDown=down.Integral()
	integUp=up.Integral()
	fracUp=0
	fracDown=0
	if integNom!=0:
	  fracDown=integDown/integNom
	  fracUp=integUp/integNom
		  
	canvas.SetTitle(c+"_"+p)
	#canvas.BuildLegend()
	legend=ROOT.TLegend()
	legend.SetX1NDC(0.15)
	legend.SetX2NDC(0.95)
	legend.SetY1NDC(0.7)
	legend.SetY2NDC(0.88)
	legend.SetBorderSize(0);
	legend.SetLineStyle(0);
	legend.SetTextFont(42);
	legend.SetTextSize(0.03);
	legend.SetFillStyle(0);	
	legend.AddEntry(nom,c+"_"+p+" (%.2f)" % integNom,"l")
	legend.AddEntry(up,c+"_"+p+" Up"+" (%.2f, %.2f" % (integUp,fracUp) +")","l")
	legend.AddEntry(down,c+"_"+p+" Down"+" (%.2f, %.2f" % (integDown,fracDown) +")","l")
	legend.Draw()

        canvas.SetLogy()
        canvas.Print('PSshapes'+'.pdf')
	canvas.SaveAs("PSscaleShapes/"+p+"_"+c+"_"+s+".png")
	canvas.SaveAs("PSscaleShapes/"+p+"_"+c+"_"+s+".pdf")
	ratioc=ROOT.TCanvas(p+"_"+c+"_"+s,p+"_"+discname+"_"+c+"_"+s,800,300)
	nomr=nom.Clone()
	nomr.Divide(nom)
	nomr.GetYaxis().SetRangeUser(0.5,1.5)
	upr=up.Clone()
	upr.Divide(nom)
	downr=down.Clone()
	downr.Divide(nom)
	nomr.Draw("histoE")
	upr.Draw("samehistoE")
	downr.Draw("samehistoE")
	legend.Draw()
	ratioc.SetTitle(nom.GetTitle())
	ratioc.Print('ratioPSshapes'+'.pdf')
	ratioc.SaveAs("PSscaleShapes/Ratio_"+p+"_"+discname+"_"+c+"_"+s+".png")
	ratioc.SaveAs("PSscaleShapes/Ratio_"+p+"_"+discname+"_"+c+"_"+s+".pdf")
	counter+=1
buff.Print('PSshapes'+'.pdf]')
ratiobuff.Print('ratioPSshapes.pdf]')
	#exit(0)
