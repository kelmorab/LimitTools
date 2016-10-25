from ROOT import *

from tdrStyle import *
setTDRStyle()

gStyle.SetPadTickY(0)
gStyle.SetTickLength(0.0, "Y");
gStyle.SetEndErrorSize(10)

from array import array

from results import results

a_mus = {}; v_mus = {}; g_mus = {};
a_y = {}; v_y = {};

a_zero = array('d',[0])
v_zero = TVectorD(len(a_zero),a_zero)

for lumi in ['scenario1','scenario2']:
  i=5
  for mu in ['10.0','30.0','100.0','300.0','3000.0']:
  #for mu in ['2.7','300.0','3000.0']:

    a_y[lumi+'_'+mu] = array('d',[i])
    v_y[lumi+'_'+mu] = TVectorD(len(a_y[lumi+'_'+mu]),a_y[lumi+'_'+mu])
    print len(a_y[lumi+'_'+mu]),a_y[lumi+'_'+mu]

    a_mus[lumi+'_'+mu] = array('d',[(results[lumi+'_'+mu]['up']/results[lumi+'_'+mu]['central']+
                                    results[lumi+'_'+mu]['dn']/results[lumi+'_'+mu]['central'])/2] )
    print a_mus[lumi+'_'+mu]
    v_mus[lumi+'_'+mu] = TVectorD(len(a_mus[lumi+'_'+mu]),a_mus[lumi+'_'+mu])

    g_mus[lumi+'_'+mu] = TGraphAsymmErrors(v_zero,v_y[lumi+'_'+mu],v_zero,v_mus[lumi+'_'+mu],v_zero,v_zero)

    g_mus[lumi+'_'+mu].SetLineWidth(3)

    if ('scenario2' in lumi): g_mus[lumi+'_'+mu].SetLineColor(kRed)
    else: g_mus[lumi+'_'+mu].SetLineColor(kGreen+2)

    i-=1

for lumi in ['scenario1','scenario2']:

  c1 = TCanvas("c1","c1",1000,800)
  c1.SetRightMargin(0.05)
  c1.SetLeftMargin(0.05)

  if (lumi=='scenario1'): dummy = TH1D("dummy","dummy",1,-0.45,1.2)
  if (lumi=='scenario2'): dummy = TH1D("dummy","dummy",1,-0.45,1.2)

  dummy.SetMinimum(0.0)
  dummy.SetMaximum(7.0)
  dummy.SetLineColor(0)
  dummy.SetMarkerColor(0)
  dummy.SetLineWidth(0)
  dummy.SetMarkerSize(0)
  dummy.GetYaxis().SetTitle("")
  dummy.GetYaxis().SetLabelSize(0)
  dummy.GetXaxis().SetTitle("expected uncertainty")
  dummy.GetXaxis().SetLabelSize(0.04)
  dummy.SetNdivisions(510, "X");
  dummy.Draw()
  
  latex2 = TLatex()
  latex2.SetNDC()
  latex2.SetTextSize(0.8*c1.GetTopMargin())
  latex2.SetTextFont(42)
  latex2.SetTextAlign(11) # align right                                                                                        
  latex2.DrawLatex(0.05, 0.95, "CMS preliminary simulation                    13 TeV")
  
  latex2.SetTextSize(0.55*c1.GetTopMargin())
  latex2.DrawLatex(0.08,0.85, "Expected uncertainties on")
  latex2.DrawLatex(0.08,0.81, "t#bar{t}H signal strength")
  
  latex2.SetTextSize(0.55*c1.GetTopMargin())
  latex2.DrawLatex(0.65,0.60, "H #rightarrow b#bar{b}")
  latex2.DrawLatex(0.65,0.55, "m_{H} = 125.09 GeV")
  
  latex2.SetTextSize(0.55*c1.GetTopMargin())
  
  #for mu in ['2.7','300.0','3000.0']:
  for mu in ['10.0','30.0','100.0','300.0','3000.0']:

    g_mus['scenario1_'+mu].Draw("|same")
    g_mus['scenario2_'+mu].Draw("|same")

    latex2.DrawLatex(0.08,a_y[lumi+'_'+mu][0]/8.7+0.13, mu+' fb^{-1}' )

  line =  TLine(0.0,0.0, 0.0, 5.5)
  line.SetLineWidth(2)
  line.SetLineColor(1)
  line.Draw("same")

  legend = TLegend(.55,.75,.94,.90)
  legend.SetBorderSize(0)
  legend.SetFillStyle(0)
  legend.AddEntry(g_mus['scenario1_'+mu], "ECFA16 S1", "l")
  legend.AddEntry(g_mus['scenario2_'+mu], "ECFA16 S2", "l")
  legend.Draw("same")
  
  c1.SaveAs("muPerProc_"+lumi+".pdf")
  

