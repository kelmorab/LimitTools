# Originally written by Darren Puigh?
# Updated by Michael Wassmer

#include "TFile.h"
#include "TChain.h"
#include "THStack.h"
#include "TF1.h"
#include "TH1.h"
#include "TH3.h"
#include "TH2F.h"
#include "TProfile.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TStyle.h"
#include "TPaveStats.h"
#include "TGaxis.h"
#include "TAxis.h"
#include "TList.h"
#include "TLatex.h"
#include "TLine.h"
#include "TObject.h"
#include "TDirectory.h"
#include "TGraphAsymmErrors.h"
#include "TEfficiency.h"
#include "TKey.h"
#include <iostream>
#include <algorithm>
#include <vector>
#include <exception>
#include <cmath> 
#include <iomanip>
#include <fstream>
#include <string>
#include <sys/stat.h>
#include <sstream>
#include <map>
#include "TMath.h"

//*****************************************************************************

//*****************************************************************************

// Set Poisson errors for histogram
// works only for histograms with INTEGER bin content and no weights
void replaceWithCopyWithPoissonErrors(TH1* &hOrig, const bool useArray=false) {
  // need to make a copy (not clone!) of the histogram without
  // the sum-of-weights array (sumw2)
  // https://root.cern.ch/doc/v606/TH1_8cxx_source.html#l08442
  const TString nameOrig = hOrig->GetName();
  hOrig->SetName("tmp");
  TH1* hNew = 0;
  if( useArray ) {
    hNew = new TH1D(nameOrig,"",
    		    hOrig->GetNbinsX(),
    		    hOrig->GetXaxis()->GetXbins()->GetArray());
  } else {
    hNew = new TH1D(nameOrig,"",
		    hOrig->GetNbinsX(),
		    hOrig->GetXaxis()->GetBinLowEdge(1),
		    hOrig->GetXaxis()->GetBinUpEdge(hOrig->GetNbinsX()));
  }

  hNew->SetDirectory(0);
  hNew->SetMarkerStyle(hOrig->GetMarkerStyle());
  hNew->SetMarkerSize(hOrig->GetMarkerSize());
  hNew->SetMarkerColor(hOrig->GetMarkerColor());
  hNew->SetLineStyle(hOrig->GetLineStyle());
  hNew->SetLineWidth(hOrig->GetLineWidth());
  hNew->SetLineColor(hOrig->GetLineColor());
  for(int bin = 1; bin <= hNew->GetNbinsX(); ++bin) {
    const double x = hOrig->GetBinCenter(bin);
    const int n = hOrig->GetBinContent(bin);
    for(int i = 0; i < n; ++i) {
      hNew->Fill(x);
    }
  }
  delete hOrig;

  // Add support for Poisson errors in data hist:
  // https://twiki.cern.ch/twiki/bin/viewauth/CMS/PoissonErrorBars
  hNew->SetBinErrorOption(TH1::kPoisson);

  hOrig = hNew;
}


// return h1/h2
// consider h2 to have no errors
TGraphAsymmErrors* createDataMCRatio(const TH1* h1, const TH1* h2) {
  std::vector<double> x;
  std::vector<double> y;
  std::vector<double> xe;
  std::vector<double> yeup;
  std::vector<double> yedn;
  for(int bin = 1; bin <= h1->GetNbinsX(); ++bin) {
    x.push_back( h1->GetBinCenter(bin) );
    xe.push_back(0.);
    const double y1 = h1->GetBinContent(bin);
    const double y2 = h2->GetBinContent(bin);
    if( y2 > 0 ) {
      y.push_back( y1/y2 );
      yeup.push_back( h1->GetBinErrorUp(bin)/y2 );
      yedn.push_back( h1->GetBinErrorLow(bin)/y2 );
    } else {
      y.push_back( 0. );
      yeup.push_back( 0. );
      yedn.push_back( 0. );
    }    
  }

  TGraphAsymmErrors* g = new TGraphAsymmErrors(x.size(),
					       &(x.front()),&(y.front()),
					       &(xe.front()),&(xe.front()),
					       &(yedn.front()),&(yeup.front()));
  g->SetMarkerStyle( h1->GetMarkerStyle() );
  g->SetMarkerColor( h1->GetMarkerColor() );
  g->SetLineStyle( h1->GetLineStyle() );
  g->SetLineColor( h1->GetLineColor() );
  g->SetLineWidth( h1->GetLineWidth() );

  return g;
}


void setRatioYRange(TH1* h) {
  double min =  99999.;
  double max = -99999.;
  for(int bin = 1; bin <= h->GetNbinsX(); ++bin) {
    const double y = h->GetBinContent(bin);
    if( y > 0 ) {
      if( y < min ) min = y;
      if( y > max ) max = y;
    }
  }

  const double yMax = 1.7;
  const double yMin = 0.3;
  const double yMaxExtreme = 2.6;
  const double yMinExtreme = 0.2;
  if( min > yMin && max < yMax ) {
    h->GetYaxis()->SetRangeUser(yMin,yMax);
  } else {
    h->GetYaxis()->SetRangeUser(yMinExtreme,yMaxExtreme);
  }
}


void makePlots_PostFitShapes_ttH_hbb_13TeV_new( TString inputFile_ = "shapes_ttH_hbb_13TeV_2016_03_10.root", bool printPDF_ = true, TString dirpostfix_ = "final" ){

  //TH1::SetDefaultSumw2(); interferes with SetBinErrorOption(kPoisson)!!

  gStyle->SetEndErrorSize(0);

  TFile* file = new TFile(inputFile_);


  std::vector<TString> categories;
  categories.push_back("dl_j3t2");
  categories.push_back("dl_j3t3");
  categories.push_back("dl_gej4t2");
  categories.push_back("dl_gej4t3");
  categories.push_back("dl_gej4get4");

  categories.push_back("sl_gej6t2");
  categories.push_back("sl_j4t3");
  categories.push_back("sl_j5t3");
  categories.push_back("sl_gej6t3");
  categories.push_back("sl_j4t4_low");
  categories.push_back("sl_j4t4_high");
  categories.push_back("sl_j5get4_low");
  categories.push_back("sl_j5get4_high");
  categories.push_back("sl_gej6get4_low");
  categories.push_back("sl_gej6get4_high");
  categories.push_back("sl_boost");

  int Ncategories = int(categories.size());

  std::vector<TString> category_names_new;
  category_names_new.push_back("dilepton, 3 jets, 2 b-tags");
  category_names_new.push_back("dilepton, 3 jets, 3 b-tags");
  category_names_new.push_back("dilepton, #geq4 jets, 2 b-tags");
  category_names_new.push_back("dilepton, #geq4 jets, 3 b-tags");
  category_names_new.push_back("dilepton, #geq4 jets, #geq4 b-tags");

  category_names_new.push_back("1 lepton, #geq6 jets, 2 b-tags");
  category_names_new.push_back("1 lepton, 4 jets, 3 b-tags");
  category_names_new.push_back("1 lepton, 5 jets, 3 b-tags");
  category_names_new.push_back("1 lepton, #geq6 jets, 3 b-tags");
  category_names_new.push_back("1 lepton, 4 jets, 4 b-tags");
  category_names_new.push_back("1 lepton, 4 jets, 4 b-tags");
  category_names_new.push_back("1 lepton, 5 jets, #geq4 b-tags");
  category_names_new.push_back("1 lepton, 5 jets, #geq4 b-tags");
  category_names_new.push_back("1 lepton, #geq6 jets, #geq4 b-tags");
  category_names_new.push_back("1 lepton, #geq6 jets, #geq4 b-tags");
  category_names_new.push_back("1 lepton, boosted");


  std::vector<TString> category_names;
  category_names.push_back("DL,3j,2b");
  category_names.push_back("DL,3j,3b");
  category_names.push_back("DL,#geq4j,2b");
  category_names.push_back("DL,#geq4j,3b");
  category_names.push_back("DL,#geq4j,#geq4b");

  category_names.push_back("SL,#geq6j,2b");
  category_names.push_back("SL,4j,3b");
  category_names.push_back("SL,5j,3b");
  category_names.push_back("SL,#geq6j,3b");
  category_names.push_back("SL,4j,4b,L");
  category_names.push_back("SL,4j,4b,H");
  category_names.push_back("SL,5j,#geq4b,L");
  category_names.push_back("SL,5j,#geq4b,H");
  category_names.push_back("SL,#geq6j,#geq4b,L");
  category_names.push_back("SL,#geq6j,#geq4b,H");
  category_names.push_back("SL,boost");

  std::vector<TString> fits;
  fits.push_back("prefit");
  fits.push_back("postfit");

  int Nfits = int( fits.size() );
  

  std::vector<TString> samples;
  samples.push_back("data_obs");
  samples.push_back("ttbarOther");
  samples.push_back("ttbarPlusCCbar");
  samples.push_back("ttbarPlusB");
  samples.push_back("ttbarPlus2B");
  samples.push_back("ttbarPlusBBbar");
  samples.push_back("singlet");
  samples.push_back("wjets");
  samples.push_back("zjets");
  samples.push_back("ttbarW");
  samples.push_back("ttbarZ");
  samples.push_back("diboson");
  samples.push_back("TotalSig");
  samples.push_back("TotalBkg");

  int Nsamples = int( samples.size() );

  


  std::vector<TString> histLabels(Nsamples);
  histLabels[0] = "Data    ";
  histLabels[1] = "t#bar{t}+lf";
  histLabels[2] = "t#bar{t}+c#bar{c}";
  histLabels[3] = "t#bar{t}+b";
  histLabels[4] = "t#bar{t}+2b";
  histLabels[5] = "t#bar{t}+b#bar{b}";
  histLabels[6] = "Single Top";
  histLabels[7] = "V+jets";
  histLabels[8] = "V+jets";
  histLabels[9] = "t#bar{t}V";
  histLabels[10] = "t#bar{t}V";
  histLabels[11] = "Diboson";
  histLabels[12] = "t#bar{t}H";
  histLabels[13] = "Tot. unc.";


  Color_t color[Nsamples];
  color[0] = kBlack;
  color[1] = kRed-7;
  color[2] = kRed+1;
  color[3] = kRed-2;
  color[4] = kRed+2;
  color[5] = kRed+3;
  color[6] = kMagenta;
  color[7] = kGreen-3;
  color[8] = kGreen-3;
  color[9] = kBlue-10;
  color[10]= kBlue-10;
  color[11]= kAzure+2;
  color[12]= kBlue;
  color[13]= kBlack;

  std::map <TString, TString> optional_argument;
  optional_argument["SL,4j,4b,L"] = "BDT < 0.2";
  optional_argument["SL,4j,4b,H"] = "BDT > 0.2";
  optional_argument["SL,5j,#geq4b,L"] = "BDT < 0.2";
  optional_argument["SL,5j,#geq4b,H"] = "BDT > 0.2";
  optional_argument["SL,#geq6j,#geq4b,L"] = "BDT < 0.1";
  optional_argument["SL,#geq6j,#geq4b,H"] = "BDT > 0.1";

  TString dirprefix = "Images_2016_03_12_ttH_hbb_PostFitShapes" + dirpostfix_ + "/";

  struct stat st;
  if( stat(dirprefix.Data(),&st) != 0 )  mkdir(dirprefix.Data(),0777);


 /////////////////////////////////////////////////////////////////////////////////////////////////////////////

 /////////////////////////////////////////////////////////////////////////////////////////////////////////////

  TGaxis::SetMaxDigits(4);

  const double scale_ttH = 15.;


  TString plotname;


  TCanvas* myC1 = new TCanvas("myC1", "myC1", 600,700);
  gStyle->SetPadBorderMode(0);
  gStyle->SetFrameBorderMode(0);
  gStyle->SetLegendBorderSize(0);

  //gStyle->SetPadTickX(1)
  //gStyle->SetPadTickY(1)
  //gStyle->SetErrorX(0.);
  Float_t small = 1.e-5;
  myC1->Divide(1,2,small,0.01);
  const float padding=1e-5; const float ydivide=0.3;
  myC1->GetPad(1)->SetPad( padding, ydivide + padding , 1-padding, 1-padding);
  myC1->GetPad(2)->SetPad( padding, padding, 1-padding, ydivide-padding);
  // myC1->GetPad(1)->SetLeftMargin(.11);
  // myC1->GetPad(2)->SetLeftMargin(.11);
  myC1->GetPad(1)->SetLeftMargin(.12);
  myC1->GetPad(2)->SetLeftMargin(.12);
  myC1->GetPad(1)->SetRightMargin(.05);
  myC1->GetPad(2)->SetRightMargin(.05);
  myC1->GetPad(1)->SetBottomMargin(.3);
  myC1->GetPad(2)->SetBottomMargin(.3);
  myC1->GetPad(1)->SetTickx();
  myC1->GetPad(1)->SetTicky();
  myC1->GetPad(1)->Modified();
  myC1->GetPad(2)->Modified();
  myC1->cd(1);
  gPad->SetBottomMargin(small);
  gPad->Modified();


  const double infoYMin = 1. - myC1->GetPad(1)->GetTopMargin() + 0.02;

  TString lumiinfo = "2.7 fb^{-1} (13 TeV)";
  TLatex LumiInfoLatex(0.715, infoYMin, lumiinfo);
  LumiInfoLatex.SetNDC();
  LumiInfoLatex.SetTextFont(42);
  LumiInfoLatex.SetTextSize(0.045);

  TString cmsinfo =   "CMS";
  TLatex CMSInfoLatex(myC1->GetPad(1)->GetLeftMargin(), infoYMin, cmsinfo);
  CMSInfoLatex.SetNDC();
  CMSInfoLatex.SetTextFont(42);
  CMSInfoLatex.SetTextFont(61);
  CMSInfoLatex.SetTextSize(0.06); //SBOUTLE

  TString publishinfo =   "Preliminary"; //DPUIGH
  TLatex PublishInfoLatex(myC1->GetPad(1)->GetLeftMargin()+0.11, infoYMin, publishinfo); //SBOUTLE
  PublishInfoLatex.SetNDC();
  PublishInfoLatex.SetTextFont(52);
  PublishInfoLatex.SetTextSize(0.045); //SBOUTLE


  for( int iFit=0; iFit<Nfits; iFit++ ){

    TH1* hist_sl_cat[Nsamples];
    TH1* hist_dl_cat[Nsamples];
    for( int iSample=0; iSample<Nsamples; iSample++ ){
      TString hist_name_sl = "h_category_yield_sl_" + fits[iFit] + "_" + samples[iSample];
      TString hist_name_dl = "h_category_yield_dl_" + fits[iFit] + "_" + samples[iSample];

      hist_sl_cat[iSample] = new TH1D(hist_name_sl, ";;Number of events per category", 11, 0, 11 );
      hist_dl_cat[iSample] = new TH1D(hist_name_dl, ";;Number of events per category", 5, 0, 5 );
    }
	  
    for( int iCat=0; iCat<Ncategories; iCat++ ){

      const bool useArray = ( categories.at(iCat) == "dl_gej4t2" );

      // //// Original vertical legend
      // TLegend *legend = new TLegend(0.76,0.50,0.84,0.89);

      // legend->SetFillColor(kWhite);
      // legend->SetLineColor(kWhite);
      // legend->SetShadowColor(kWhite);
      // legend->SetTextFont(42);
      // legend->SetTextSize(0.035);

      // //// horizontal legend
      // TLegend *legend = new TLegend(0.16,0.75,0.89,0.89);

      // legend->SetFillColor(kWhite);
      // legend->SetLineColor(kWhite);
      // legend->SetShadowColor(kWhite);
      // legend->SetTextFont(42);
      // legend->SetTextSize(0.035);

      // legend->SetNColumns(5);

      
      //TLegend *legend = new TLegend(0.46,0.65,0.89,0.89);
      TLegend *legend = new TLegend(0.59,0.65,0.94,0.87);

      legend->SetFillColor(kWhite);
      legend->SetLineColor(kBlack);
      legend->SetShadowColor(kWhite);
      legend->SetTextFont(42);
      legend->SetTextSize(0.035);
      legend->SetLineWidth(2);
      legend->SetNColumns(2);
      



      TH1* hist[Nsamples];
      for( int iSample=0; iSample<Nsamples; iSample++ ){
	TString hist_name = categories[iCat] + "_" + fits[iFit] + "/" + samples[iSample];
	std::cout << category_names[iCat] << endl; 
	hist[iSample] = 0;
	file->GetObject(hist_name,hist[iSample]);
	if( hist[iSample] == 0 ) {
	  std::cerr << "ERROR reading histogram '" << hist_name << "'" << std::endl;
	  exit(1);
	}
	hist[iSample]->SetDirectory(0);

	//printf(" HistoName = %30s, integral = %5.1f \n", hist_name.Data(), hist[iSample]->Integral());

	if( iSample==0 ) {
	  replaceWithCopyWithPoissonErrors(hist[iSample],useArray);
	}

	if( iSample>0 ){
	  hist[iSample]->SetLineColor(kBlack/*color[iSample]*/);
	  hist[iSample]->SetLineWidth(2);
	  if( iSample<Nsamples-2 ) hist[iSample]->SetFillColor(color[iSample]);
	  else if( iSample<Nsamples-1 ) {
                hist[iSample]->SetLineWidth(2);
		hist[iSample]->SetLineColor(color[iSample]);
   		hist[iSample]->SetFillStyle(0);
	  }		
	}
	else {
	  hist[iSample]->SetMarkerStyle(20);
          hist[iSample]->SetLineColor(kBlack/*color[iSample]*/);
	  hist[iSample]->SetLineWidth(2);
	}
      }


      
      int Nbins = hist[0]->GetNbinsX();

      double xmin = hist[0]->GetBinLowEdge(1);
      double xmax = hist[0]->GetBinLowEdge(Nbins) + hist[0]->GetBinWidth(Nbins);

      for( int iSample=0; iSample<Nsamples; iSample++ ){
	double sum=0;
	double sum_err=0;
	for( int iBin=0; iBin<Nbins; iBin++ ){
	  sum += hist[iSample]->GetBinContent(iBin+1);
	  sum_err += hist[iSample]->GetBinError(iBin+1);
	}
	//if( iSample==0 ) printf(" %20s: data_obs = %4.1f \n", categories[iCat].Data(), sum);
	if( categories[iCat].BeginsWith("sl_") ){
	  hist_sl_cat[iSample]->SetBinContent(iCat-5+1, sum);
	  hist_sl_cat[iSample]->SetBinError(iCat-5+1, sum_err);
	}
	else{
	  std::cout << "Setting DL bin " << iCat+1 << ": " << sum << std::endl;
	  hist_dl_cat[iSample]->SetBinContent(iCat+1, sum);
	  hist_dl_cat[iSample]->SetBinError(iCat+1, sum_err);
	}


	if( iSample>0 ){
	  hist_sl_cat[iSample]->SetLineColor(kBlack/*color[iSample]*/);
	  hist_dl_cat[iSample]->SetLineColor(kBlack/*color[iSample]*/);
	  hist_sl_cat[iSample]->SetLineWidth(2);
	  hist_dl_cat[iSample]->SetLineWidth(2);

	  if( iSample<Nsamples-2 ){
	    hist_sl_cat[iSample]->SetFillColor(color[iSample]);
	    hist_dl_cat[iSample]->SetFillColor(color[iSample]);

	  }
	  else if( iSample==Nsamples-2 ){
	    hist_sl_cat[iSample]->SetLineWidth(3);
	    hist_dl_cat[iSample]->SetLineWidth(3);
            hist_sl_cat[iSample]->SetLineColor(color[iSample]);
	    hist_dl_cat[iSample]->SetLineColor(color[iSample]);

	  }
	  else if( iSample==Nsamples-1 ){
	    hist_sl_cat[iSample]->SetFillStyle(3354);
	    hist_sl_cat[iSample]->SetFillColor(kBlack);
	    hist_sl_cat[iSample]->SetLineColor(kBlack);
	    hist_sl_cat[iSample]->SetMarkerSize(0);

	    hist_dl_cat[iSample]->SetFillStyle(3354);
	    hist_dl_cat[iSample]->SetFillColor(kBlack);
	    hist_dl_cat[iSample]->SetMarkerSize(0);
	  }
	}
	else {
	  hist_sl_cat[iSample]->SetMarkerStyle(20);
	  hist_dl_cat[iSample]->SetMarkerStyle(20);
	  hist_sl_cat[iSample]->SetLineColor(kBlack);
	  hist_dl_cat[iSample]->SetLineColor(kBlack);
	  hist_sl_cat[iSample]->SetLineWidth(2);
	  hist_dl_cat[iSample]->SetLineWidth(2);
	}
      }

      TH1* hist_bkg = (TH1*)hist[Nsamples-1]->Clone(Form("%s_%s_TotBkg",fits[iFit].Data(),categories[iCat].Data()));

      //double data_integral = hist[0]->Integral();
      //double bkg_integral = hist_bkg->Integral();
      //double integral_ratio = data_integral / bkg_integral;

      //double sig_integral = hist[Nsamples-2]->Integral();
      //scale_ttH = (sig_integral>0.) ? bkg_integral / sig_integral : 1.;
      hist[Nsamples-2]->Scale(scale_ttH);

      
      legend->AddEntry(hist[0],histLabels[0],"pe1");
      legend->AddEntry(hist[Nsamples-2],histLabels[Nsamples-2]+Form(" (x%d)",int(scale_ttH+0.0001)),"l");
      for( int iSample=1; iSample<Nsamples; iSample++ ){
	if( samples[iSample]=="zjets" || samples[iSample]=="ttbarZ" ) continue;
	if( iSample<Nsamples-2 )  legend->AddEntry(hist[iSample],histLabels[iSample],"f");
      }

      hist_bkg->SetFillStyle(3354);
      hist_bkg->SetFillColor(kBlack);
      hist_bkg->SetMarkerSize(0);

      legend->AddEntry(hist_bkg,histLabels[Nsamples-1],"f");



      THStack *hs = new THStack("hs","");
      for( int iSample=Nsamples-1; iSample>-1; iSample-- ){
	if( iSample>0 && iSample<Nsamples-2 ) hs->Add(hist[iSample]);
      }

      
      TH1* myRatio = 0;
      TH1* myRatio_1sig = 0;

      if( useArray ) {
	myRatio = new TH1D("ratio", "",
			   hist[0]->GetNbinsX(),
			   hist[0]->GetXaxis()->GetXbins()->GetArray());
	myRatio_1sig = new TH1D("ratio_1sig", "",
				hist[0]->GetNbinsX(),
				hist[0]->GetXaxis()->GetXbins()->GetArray());
      } else {
	myRatio = new TH1D("ratio", "", hist[0]->GetNbinsX(), xmin, xmax);
	myRatio_1sig = new TH1D("ratio_1sig", "",hist[0]->GetNbinsX(), xmin, xmax);
      }

      myRatio->SetStats(0);
      myRatio->Sumw2();
      myRatio->SetLineColor(kBlack);
      myRatio->SetMarkerColor(kBlack);
      myRatio->SetLineWidth(2);
      myRatio->Divide(hist[0],hist_bkg);
      myRatio->SetMarkerStyle(0);
      TGraphAsymmErrors* myRatio_asymmerr = createDataMCRatio(hist[0],hist_bkg);


      for( int iBin=0; iBin<Nbins; iBin++ ){
	double bkg  = hist_bkg->GetBinContent(iBin+1);
	double bkg_1sig  = hist_bkg->GetBinError(iBin+1);
	double data = hist[0]->GetBinContent(iBin+1);
	double ratio = ( bkg>0. ) ? data/bkg : 0.;
	double ratio_err = ( bkg>0. ) ? sqrt(data)/bkg : 0.;

	double bkg_noshift  = hist_bkg->GetBinContent(iBin+1);
	if( bkg_noshift>0. ) ratio = data/bkg_noshift;
	if( bkg_noshift>0. ) ratio_err = ( bkg>0. ) ? sqrt(data)/bkg_noshift : 0.;

	double up_err = bkg + bkg_1sig;
	double down_err = bkg - bkg_1sig;

	if( bkg>0. && bkg_noshift>0. ){
	  myRatio->SetBinContent(iBin+1,ratio);
	  myRatio->SetBinError(iBin+1,ratio_err);

	  up_err *= 1./bkg_noshift;
	  down_err *= 1./bkg_noshift;

	  double new_ave = 0.5 * ( up_err + down_err );

	  myRatio_1sig->SetBinContent(iBin+1,new_ave);
	  myRatio_1sig->SetBinError(iBin+1,up_err - new_ave);

	  //std::cout << " hist = " << temp << ", bin = " << bin << ", new_ave = " << new_ave << ", up_err = " << up_err << ", down_err = " << down_err << std::endl;
	}

	myRatio->SetBinError(iBin+1,0); // we'll use the TGraph to draw the errors
      }

      setRatioYRange(myRatio);
      myRatio->GetYaxis()->SetNdivisions(50000+204);
      myRatio->GetYaxis()->SetLabelSize(0.1); //make y label bigger
      myRatio->GetXaxis()->SetLabelSize(0.12*0.9); //make y label bigger
      //myRatio->GetXaxis()->SetTitleOffset(1.1);
      myRatio->GetXaxis()->SetTitleOffset(1.3);
      myRatio->GetXaxis()->SetTitle(hist[0]->GetXaxis()->GetTitle()); //make y label bigger
      myRatio->GetXaxis()->SetLabelSize(0.12*0.9);
      myRatio->GetXaxis()->SetLabelOffset(0.04);
      myRatio->GetXaxis()->SetTitleSize(0.12*0.9);
      myRatio->GetYaxis()->SetTitle("data/MC");
      myRatio->GetYaxis()->SetTitleSize(0.11);
      myRatio->GetYaxis()->SetTitleOffset(.55*1);
      //myRatio->GetXaxis()->SetTickLength((myRatio->GetXaxis()->GetTickLength())*2);
      myRatio->GetYaxis()->SetTickLength((myRatio->GetYaxis()->GetTickLength())*1.5);
      myC1->cd(2);
      gPad->SetTopMargin(small);
      gPad->SetTickx();
      //gStyle->SetPadTickX(1)
      gPad->SetTicky();
      //gStyle->SetPadTickY(1)
      gPad->Modified();

      myRatio->GetYaxis()->CenterTitle(kTRUE);

      hist[0]->SetTitle("");
      hist[0]->SetStats(0);
      hist[0]->SetLineWidth(2);
      hist[0]->GetYaxis()->SetTitleOffset(1.2*1);
      hist[0]->GetYaxis()->SetTitleSize(0.05);
      hist[0]->GetYaxis()->SetTitle("Number of Events");
      hist[0]->GetYaxis()->SetLabelSize(((hist[0]->GetYaxis())->GetLabelSize())*1.25);


      int max_bin_data = hist[0]->GetMaximumBin();
      double max_data = hist[0]->GetBinContent(max_bin_data) + hist[0]->GetBinError(max_bin_data);

      int max_bin_mc = hist_bkg->GetMaximumBin();
      double max_mc = hist_bkg->GetBinContent(max_bin_mc) + hist_bkg->GetBinError(max_bin_mc);

      double max_content = std::max(max_data, max_mc);

      hist[0]->GetYaxis()->SetRangeUser(0.,1.5 * max_content);
      //hist[0]->GetYaxis()->SetRangeUser(1E-4,1.5 * max_content);


      // Optionally, adjust x-axis range to only include bins with non-zero bkg or sig
      const bool adjustXRange = true;
      double xminUser = xmin;
      double xmaxUser = xmax;
      if( adjustXRange ) {
	std::cout << "Finding x-range for " << categories[iCat] << std::endl;
	int firstBinWithBkgOrSig = -1;
	int lastBinWithBkgOrSig = -1;
	bool previousBinHadContent = false;

	for(int bin = 1; bin <= hist_bkg->GetNbinsX(); ++bin) {
	  const double yBkg = hist_bkg->GetBinContent(bin);
	  const double ySig = hist[Nsamples-2]->GetBinContent(bin);
	  const bool hasBinContent = yBkg>0. || ySig>0.;
	  if( firstBinWithBkgOrSig==-1 && hasBinContent ) {
	    firstBinWithBkgOrSig = bin;
	    previousBinHadContent = true;
	  } else if( previousBinHadContent && !hasBinContent ) {
	    lastBinWithBkgOrSig = bin-1;
	    break;
	  }
	}
	if( lastBinWithBkgOrSig == -1 ) {
	  lastBinWithBkgOrSig = hist_bkg->GetNbinsX();
	}
	std::cout << "  found bins " << firstBinWithBkgOrSig << " - " << lastBinWithBkgOrSig << std::endl;

	if( firstBinWithBkgOrSig > -1 && lastBinWithBkgOrSig > -1 && firstBinWithBkgOrSig != lastBinWithBkgOrSig ) {
	  if( firstBinWithBkgOrSig > 1 || lastBinWithBkgOrSig < hist_bkg->GetNbinsX() ) {
	    xminUser = hist[0]->GetXaxis()->GetBinLowEdge(firstBinWithBkgOrSig);
	    xmaxUser = hist[0]->GetXaxis()->GetBinUpEdge(lastBinWithBkgOrSig);
	    
	    hist[0]->GetXaxis()->SetRange(firstBinWithBkgOrSig,lastBinWithBkgOrSig);
	    std::cout << "    1" << std::endl;
	    std::cout << "    2" << std::endl;
	    hist_bkg->GetXaxis()->SetRange(firstBinWithBkgOrSig,lastBinWithBkgOrSig);
	    std::cout << "    3" << std::endl;
	    
	    hist[Nsamples-2]->GetXaxis()->SetRange(firstBinWithBkgOrSig,lastBinWithBkgOrSig);
	    std::cout << "    4" << std::endl;

	    myRatio->GetXaxis()->SetRange(firstBinWithBkgOrSig,lastBinWithBkgOrSig);
	    std::cout << "    5" << std::endl;

	    myRatio_1sig->GetXaxis()->SetRange(firstBinWithBkgOrSig,lastBinWithBkgOrSig);
	    std::cout << "    6" << std::endl;

	  }
	}
      }


      if( categories[iCat].BeginsWith("sl_") ){
	if( categories[iCat].Contains("j4t3") ) myRatio->GetXaxis()->SetTitle("BDT (incl. MEM) discriminant");
	if( categories[iCat].Contains("j4t4_high") ) myRatio->GetXaxis()->SetTitle("MEM discriminant");
	if( categories[iCat].Contains("j4t4_low") ) myRatio->GetXaxis()->SetTitle("MEM discriminant");
	if( categories[iCat].Contains("j5t3") ) myRatio->GetXaxis()->SetTitle("BDT (incl. MEM) discriminant");
	if( categories[iCat].Contains("j5get4_high") ) myRatio->GetXaxis()->SetTitle("MEM discriminant");
	if( categories[iCat].Contains("j5get4_low") ) myRatio->GetXaxis()->SetTitle("MEM discriminant");
	if( categories[iCat].Contains("boost") ) myRatio->GetXaxis()->SetTitle("BDT (incl. MEM) discriminant");
	if( categories[iCat].Contains("gej6t2") ) myRatio->GetXaxis()->SetTitle("BDT discriminant");
	if( categories[iCat].Contains("gej6t3") ) myRatio->GetXaxis()->SetTitle("BDT (incl. MEM) discriminant");
	if( categories[iCat].Contains("gej6get4_high") ) myRatio->GetXaxis()->SetTitle("MEM discriminant");
	if( categories[iCat].Contains("gej6get4_low") ) myRatio->GetXaxis()->SetTitle("MEM discriminant");
      } else {
	myRatio->GetXaxis()->SetTitle("BDT discriminant");
      }
      myRatio_1sig->SetFillStyle(3354);
      myRatio_1sig->SetFillColor(kBlack);




      TLine* myLine;
      myLine = new TLine(xminUser, 1, xmaxUser, 1);
      


      // Plot
      myC1->cd(1);
      hist[0]->Draw("p0ex0");
      hs->Draw("histsame");
      hist_bkg->Draw("e2same");
      hist[Nsamples-2]->Draw("histsame");
      hist[0]->Draw("p0ex0same");

      legend->Draw();
      TString optional_label;
      LumiInfoLatex.Draw();
      CMSInfoLatex.Draw();
      PublishInfoLatex.Draw();
      for (std::map<TString,TString>::iterator it=optional_argument.begin(); it!=optional_argument.end(); ++it){
           std::cout << "test " << it->first << "   " << it->second << "   " << category_names[iCat] << "   " << category_names[iCat].Contains(it->first) << std::endl;
           if(!category_names[iCat].CompareTo(it->first)) {
                 std::cout << "jaaa" << std::endl;
                 optional_label=it->second;
		 std::cout << optional_label << std::endl;
		 break;
                 }
	   else {optional_label="";}
      }
      TString label = "#splitline{"+category_names_new[iCat]+"}{"+optional_label+"}";
      TLatex cat_label(0.16, 0.80, label);
      cat_label.SetNDC();
      cat_label.SetTextFont(42);
      cat_label.SetTextSize(0.045);
      cat_label.Draw();

      TLatex prefit_label(0.16,(optional_label=="" ? 0.75 : 0.70),"pre-fit expectation");
      prefit_label.SetNDC();
      prefit_label.SetTextFont(42);
      prefit_label.SetTextSize(0.045);
      if( fits[iFit] == "prefit" ) prefit_label.Draw();

      

      myC1->cd(2);
      myRatio->SetLineWidth(2);
      myRatio->Draw("pex0");
      myRatio_1sig->Draw("e2same");
      myRatio_asymmerr->Draw("pesame");

      myLine->Draw();

      myC1->GetPad(1)->SetLogy(0);

      myC1->GetPad(1)->RedrawAxis();
      myC1->GetPad(2)->RedrawAxis();

      myC1->cd(1);
      // want to hide the 0 label of the y axis
      // setting ymin to sth small > 0 works, but omits data points = 0 to be drawn....
      const double cover_x_min = xminUser - 0.005;
      const double cover_y_max = 0.05*(hist[0]->GetMaximum());
      TBox* cover = new TBox(cover_x_min-0.1,0.,cover_x_min,cover_y_max);
      cover->SetLineColor(kWhite);
      cover->SetFillColor(kWhite);
      cover->Draw("same");

      plotname = dirprefix + categories[iCat] + "_" + fits[iFit] + ".png";
      myC1->Print(plotname);

      plotname = dirprefix + categories[iCat] + "_" + fits[iFit] + ".pdf";
      if( printPDF_ ) myC1->Print(plotname);


      delete myRatio;
      delete myRatio_asymmerr;
      delete myRatio_1sig;
      delete myLine;
      delete legend;
      delete cover;
    }
    std::cout << "\n\n==========1111===========\n";
    for(int bin = 1; bin <=     hist_dl_cat[0]->GetNbinsX(); ++bin) {
      std::cout << "  bin" << bin << ": " <<     hist_dl_cat[0]->GetBinContent(bin) << std::endl;
    }

    // now fix data errors in inclusive yield plots
    // (have been added linearly per BDT bin, but are fully uncorrelated)
    // also, use Poisson errors
    replaceWithCopyWithPoissonErrors(hist_sl_cat[0]);
    replaceWithCopyWithPoissonErrors(hist_dl_cat[0]);

    std::cout << "\n\n==========2222===========\n";
    for(int bin = 1; bin <=     hist_dl_cat[0]->GetNbinsX(); ++bin) {
      std::cout << "  bin" << bin << ": " <<     hist_dl_cat[0]->GetBinContent(bin) << std::endl;
    }


    double ratioMax = 1.6;
    double ratioMin = 0.5;


    ///////////////////
    ///
    /// sl
    ///
    ///////////////////
     
    TLegend *legend_sl = new TLegend(0.59,0.65,0.94,0.87);

    legend_sl->SetFillColor(kWhite);
    legend_sl->SetLineColor(kBlack/*kWhite*/);
    legend_sl->SetShadowColor(kWhite);
    legend_sl->SetTextFont(42);
    legend_sl->SetTextSize(0.035);

    legend_sl->SetNColumns(2);

    
    int Nbins_sl = hist_sl_cat[0]->GetNbinsX();

    double xmin_sl = hist_sl_cat[0]->GetBinLowEdge(1);
    double xmax_sl = hist_sl_cat[0]->GetBinLowEdge(Nbins_sl) + hist_sl_cat[0]->GetBinWidth(Nbins_sl);

    TH1* hist_sl_cat_bkg = (TH1*)hist_sl_cat[Nsamples-1]->Clone(Form("%s_sl_category_TotBkg",fits[iFit].Data()));

    THStack *hs_sl = new THStack("hs_sl","");
    for( int iSample=Nsamples-1; iSample>-1; iSample-- ){
      if( iSample>0 && iSample<Nsamples-2 ) hs_sl->Add(hist_sl_cat[iSample]);
    }

    // double ratioMax = 2.3;
    // double ratioMin = 0.0;

    TH1* myRatio_sl = new TH1D("ratio_sl", "", Nbins_sl, xmin_sl, xmax_sl );
    TH1* myRatio_sl_1sig = new TH1D("ratio_sl_1sig", "", Nbins_sl, xmin_sl, xmax_sl );

    myRatio_sl->SetStats(0);
    myRatio_sl->Sumw2();
    myRatio_sl->SetLineColor(kBlack);
    myRatio_sl->SetMarkerColor(kBlack);
    myRatio_sl->Divide(hist_sl_cat[0],hist_sl_cat_bkg);
    myRatio_sl->SetMarkerStyle(0);


    for( int iBin=0; iBin<Nbins_sl; iBin++ ){
      double bkg  = hist_sl_cat_bkg->GetBinContent(iBin+1);
      double bkg_1sig  = hist_sl_cat_bkg->GetBinError(iBin+1);
      double data = hist_sl_cat[0]->GetBinContent(iBin+1);
      double ratio = ( bkg>0. ) ? data/bkg : 0.;
      double ratio_err = ( bkg>0. ) ? sqrt(data)/bkg : 0.;

      double bkg_noshift  = hist_sl_cat_bkg->GetBinContent(iBin+1);
      if( bkg_noshift>0. ) ratio = data/bkg_noshift;
      if( bkg_noshift>0. ) ratio_err = ( bkg>0. ) ? sqrt(data)/bkg_noshift : 0.;

      double up_err = bkg + bkg_1sig;
      double down_err = bkg - bkg_1sig;

      if( bkg>0. && bkg_noshift>0. ){
    	myRatio_sl->SetBinContent(iBin+1,ratio);
    	myRatio_sl->SetBinError(iBin+1,ratio_err);

    	up_err *= 1./bkg_noshift;
    	down_err *= 1./bkg_noshift;

    	double new_ave = 0.5 * ( up_err + down_err );

    	myRatio_sl_1sig->SetBinContent(iBin+1,new_ave);
    	myRatio_sl_1sig->SetBinError(iBin+1,up_err - new_ave);
      }

      myRatio_sl->SetBinError(iBin+1,0); // we'll draw a TGraph for the errors
    }

    // data/MC ratio with asym errors
    TGraphAsymmErrors* myRatio_sl_asymmerr = createDataMCRatio(hist_sl_cat[0],hist_sl_cat_bkg);



    myRatio_sl->SetMinimum(ratioMin);
    myRatio_sl->SetMaximum(ratioMax);
    // double ratioMax = 2.3;
    // double ratioMin = 0.0;
    //myRatio_sl->GetYaxis()->SetNdivisions(50000+404);
    // double ratioMax = 1.6;
    // double ratioMin = 0.5;
    myRatio_sl->GetYaxis()->SetNdivisions(50000+204);
    myRatio_sl->GetYaxis()->SetLabelSize(0.1); //make y label bigger
    myRatio_sl->GetXaxis()->SetLabelSize(0.12*0.9); //make y label bigger
    myRatio_sl->GetXaxis()->SetTitleOffset(1.1);
    myRatio_sl->GetXaxis()->SetTitle(hist_sl_cat[0]->GetXaxis()->GetTitle()); //make y label bigger
    myRatio_sl->GetXaxis()->SetLabelSize(0.12*0.9);
    myRatio_sl->GetXaxis()->SetLabelOffset(0.04);
    myRatio_sl->GetXaxis()->SetTitleSize(0.12*0.9);
    myRatio_sl->GetYaxis()->SetTitle("data/MC");
    myRatio_sl->GetYaxis()->SetTitleSize(0.11);
    myRatio_sl->GetYaxis()->SetTitleOffset(.55*1);
    //myRatio_sl->GetXaxis()->SetTickLength((myRatio_sl->GetXaxis()->GetTickLength())*2);
    myRatio_sl->GetYaxis()->SetTickLength((myRatio_sl->GetYaxis()->GetTickLength())*1.5);
    myC1->cd(2);
    gPad->SetTopMargin(small);
    gPad->SetTickx();
    //gStyle->SetPadTickX(1)
    gPad->SetTicky();
    //gStyle->SetPadTickY(1)
    gPad->Modified();

    myRatio_sl->GetYaxis()->CenterTitle(kTRUE);


    for( int iBin=0; iBin<Nbins_sl; iBin++ ){
      myRatio_sl->GetXaxis()->SetBinLabel(iBin+1,category_names[iBin+5]);
    }
    
    hist_sl_cat[0]->SetTitle("");
    hist_sl_cat[0]->SetStats(0);

    hist_sl_cat[0]->GetYaxis()->SetTitleOffset(1.2*1);
    hist_sl_cat[0]->GetYaxis()->SetTitleSize(0.05);
    hist_sl_cat[0]->GetYaxis()->SetLabelSize(((hist_sl_cat[0]->GetYaxis())->GetLabelSize())*1.25);
    hist_sl_cat[0]->GetYaxis()->SetTitle("Number of Events");


    int max_bin_data_sl = hist_sl_cat[0]->GetMaximumBin();
    double max_data_sl = hist_sl_cat[0]->GetBinContent(max_bin_data_sl) + hist_sl_cat[0]->GetBinError(max_bin_data_sl);

    hist_sl_cat[0]->GetYaxis()->SetRangeUser(0.5,15 * max_data_sl);

    
    hist_sl_cat_bkg->SetFillStyle(3354);
    hist_sl_cat_bkg->SetFillColor(kBlack);
    hist_sl_cat_bkg->SetMarkerSize(0);

    myRatio_sl_1sig->SetFillStyle(3354);
    myRatio_sl_1sig->SetFillColor(kBlack);
    myRatio_sl_1sig->SetMarkerSize(0);



    
    // double bkg_integral_sl = hist_sl_cat_bkg->Integral();

    // double sig_integral_sl = hist_sl_cat[Nsamples-2]->Integral();
    hist_sl_cat[Nsamples-2]->Scale(scale_ttH);

    
    legend_sl->AddEntry(hist_sl_cat[0],histLabels[0],"pe1");
    legend_sl->AddEntry(hist_sl_cat[Nsamples-2],histLabels[Nsamples-2]+Form(" (x%d)",int(scale_ttH+0.0001)),"l");
    for( int iSample=1; iSample<Nsamples; iSample++ ){
      if( samples[iSample]=="zjets" || samples[iSample]=="ttbarZ" ) continue;
      if( iSample<Nsamples-2 )  legend_sl->AddEntry(hist_sl_cat[iSample],histLabels[iSample],"f");
    }

    legend_sl->AddEntry(hist_sl_cat_bkg,histLabels[Nsamples-1],"f");
    
    TLine* myLine_sl;
    myLine_sl = new TLine(xmin_sl, 1, xmax_sl, 1);

    hist_sl_cat[0]->SetLineWidth(2);
    hist_sl_cat[0]->SetLineColor(kBlack);
    // Plot
    myC1->cd(1);
    hist_sl_cat[0]->Draw("pex0");
    hs_sl->Draw("histsame");
    hist_sl_cat_bkg->Draw("e2same");
    hist_sl_cat[Nsamples-2]->Draw("histsame");
    hist_sl_cat[0]->Draw("pex0same");

    if( 1 ) {
      std::cout << "\n\nSL per-category relative errors: " << fits[iFit] << std::endl;
      for(int bin = 1; bin <= hist_sl_cat_bkg->GetNbinsX(); ++bin) {
	const double y = hist_sl_cat_bkg->GetBinContent(bin);
	const double e = hist_sl_cat_bkg->GetBinError(bin);
	const TString label = myRatio_sl->GetXaxis()->GetBinLabel(bin);
	std::cout << "  bin" << bin << "(" << label << "): " << y << " +/- " << e << " --> rel err = " << e/y << std::endl;
      }
    }

    legend_sl->Draw();

    LumiInfoLatex.Draw();
    CMSInfoLatex.Draw();
    PublishInfoLatex.Draw();

    TLatex prefit_label(0.16,0.82,"pre-fit expectation");
    prefit_label.SetNDC();
    prefit_label.SetTextFont(42);
    prefit_label.SetTextSize(0.045);
    if( fits[iFit] == "prefit" ) prefit_label.Draw();


    myC1->cd(2);
    myRatio_sl->SetLineWidth(2);
    myRatio_sl->Draw("pex0");
    myRatio_sl_1sig->Draw("e2same");
    myRatio_sl_asymmerr->Draw("pesame");

    myLine_sl->Draw();

    myC1->GetPad(1)->SetLogy(1);

    myC1->GetPad(1)->RedrawAxis();
    myC1->GetPad(2)->RedrawAxis();

    plotname = dirprefix + "category_yield_sl_" + fits[iFit] + ".png";
    myC1->Print(plotname);

    plotname = dirprefix + "category_yield_sl_" + fits[iFit] + ".pdf";
    if( printPDF_ ) myC1->Print(plotname);


    delete myRatio_sl;
    delete myRatio_sl_asymmerr;
    delete myRatio_sl_1sig;
    delete myLine_sl;
    delete legend_sl;

    for(int iCat=0; iCat<int(category_names.size()); ++iCat) {
      std::cout << category_names[iCat] << std::endl;
      if( iCat > 4 ) {
	for(int iSample=0; iSample<Nsamples; ++iSample) {
	  printf("%s \t %.1f $\\pm$ %.1f \n",samples[iSample].Data(),hist_sl_cat[iSample]->GetBinContent(iCat+1-5),0.1);
	}
      }
    }


    
    ///////////////////
    ///
    /// dl
    ///
    ///////////////////
    

    TLegend *legend_dl = new TLegend(0.59,0.65,0.94,0.87);

    legend_dl->SetFillColor(kWhite);
    legend_dl->SetLineColor(kBlack/*kWhite*/);
    legend_dl->SetShadowColor(kWhite);
    legend_dl->SetTextFont(42);
    legend_dl->SetTextSize(0.035);

    legend_dl->SetNColumns(2);

    
    int Nbins_dl = hist_dl_cat[0]->GetNbinsX();

    double xmin_dl = hist_dl_cat[0]->GetBinLowEdge(1);
    double xmax_dl = hist_dl_cat[0]->GetBinLowEdge(Nbins_dl) + hist_dl_cat[0]->GetBinWidth(Nbins_dl);

    TH1* hist_dl_cat_bkg = (TH1*)hist_dl_cat[Nsamples-1]->Clone(Form("%s_dl_category_TotBkg",fits[iFit].Data()));


    THStack *hs_dl = new THStack("hs_dl","");
    for( int iSample=Nsamples-1; iSample>-1; iSample-- ){
      if( iSample>0 && iSample<Nsamples-2 ) hs_dl->Add(hist_dl_cat[iSample]);
    }

    // double ratioMax = 2.3;
    // double ratioMin = 0.0;

    TH1* myRatio_dl = new TH1D("ratio_dl", "", Nbins_dl, xmin_dl, xmax_dl );
    TH1* myRatio_dl_1sig = new TH1D("ratio_dl_1sig", "", Nbins_dl, xmin_dl, xmax_dl );

    myRatio_dl->SetStats(0);
    myRatio_dl->Sumw2();
    myRatio_dl->SetLineColor(kBlack);
    myRatio_dl->SetMarkerColor(kBlack);
    myRatio_dl->Divide(hist_dl_cat[0],hist_dl_cat_bkg);
    myRatio_dl->SetMarkerStyle(0);


    for( int iBin=0; iBin<Nbins_dl; iBin++ ){
      double bkg  = hist_dl_cat_bkg->GetBinContent(iBin+1);
      double bkg_1sig  = hist_dl_cat_bkg->GetBinError(iBin+1);
      double data = hist_dl_cat[0]->GetBinContent(iBin+1);
      double ratio = ( bkg>0. ) ? data/bkg : 0.;
      double ratio_err = ( bkg>0. ) ? sqrt(data)/bkg : 0.;

      double bkg_noshift  = hist_dl_cat_bkg->GetBinContent(iBin+1);
      if( bkg_noshift>0. ) ratio = data/bkg_noshift;
      if( bkg_noshift>0. ) ratio_err = ( bkg>0. ) ? sqrt(data)/bkg_noshift : 0.;

      double up_err = bkg + bkg_1sig;
      double down_err = bkg - bkg_1sig;

      if( bkg>0. && bkg_noshift>0. ){
    	myRatio_dl->SetBinContent(iBin+1,ratio);
    	myRatio_dl->SetBinError(iBin+1,ratio_err);

    	up_err *= 1./bkg_noshift;
    	down_err *= 1./bkg_noshift;

    	double new_ave = 0.5 * ( up_err + down_err );

    	myRatio_dl_1sig->SetBinContent(iBin+1,new_ave);
    	myRatio_dl_1sig->SetBinError(iBin+1,up_err - new_ave);

    	//std::cout << " hist = " << temp << ", bin = " << bin << ", new_ave = " << new_ave << ", up_err = " << up_err << ", down_err = " << down_err << std::endl;
      }
      myRatio_dl->SetBinError(iBin+1,0); // we'll draw a TGraph for the errors
    }

    // data/MC ratio with asym errors
    TGraphAsymmErrors* myRatio_dl_asymmerr = createDataMCRatio(hist_dl_cat[0],hist_dl_cat_bkg);


    myRatio_dl->SetMinimum(ratioMin);
    myRatio_dl->SetMaximum(ratioMax);
    // double ratioMax = 2.3;
    // double ratioMin = 0.0;
    //myRatio_dl->GetYaxis()->SetNdivisions(50000+404);
    // double ratioMax = 1.6;
    // double ratioMin = 0.5;
    myRatio_dl->GetYaxis()->SetNdivisions(50000+204);
    myRatio_dl->GetYaxis()->SetLabelSize(0.1); //make y label bigger
    myRatio_dl->GetXaxis()->SetLabelSize(0.12*0.9); //make y label bigger
    myRatio_dl->GetXaxis()->SetTitleOffset(1.1);
    myRatio_dl->GetXaxis()->SetTitle(hist_dl_cat[0]->GetXaxis()->GetTitle()); //make y label bigger
    myRatio_dl->GetXaxis()->SetLabelSize(0.12*0.9);
    myRatio_dl->GetXaxis()->SetLabelOffset(0.04);
    myRatio_dl->GetXaxis()->SetTitleSize(0.12*0.9);
    myRatio_dl->GetYaxis()->SetTitle("data/MC");
    myRatio_dl->GetYaxis()->SetTitleSize(0.11);
    myRatio_dl->GetYaxis()->SetTitleOffset(.55*1);
    //myRatio_dl->GetXaxis()->SetTickLength((myRatio_dl->GetXaxis()->GetTickLength())*2);
    myRatio_dl->GetYaxis()->SetTickLength((myRatio_dl->GetYaxis()->GetTickLength())*1.5);
    myC1->cd(2);
    gPad->SetTopMargin(small);
    gPad->SetTickx();
    //gStyle->SetPadTickX(1)
    gPad->SetTicky();
    //gStyle->SetPadTickY(1)
    gPad->Modified();

    myRatio_dl->GetYaxis()->CenterTitle(kTRUE);


    for( int iBin=0; iBin<Nbins_dl; iBin++ ){
      myRatio_dl->GetXaxis()->SetBinLabel(iBin+1,category_names[iBin]);
    }
    
    hist_dl_cat[0]->SetTitle("");
    hist_dl_cat[0]->SetStats(0);

    hist_dl_cat[0]->GetYaxis()->SetTitleOffset(1.2*1);
    hist_dl_cat[0]->GetYaxis()->SetTitleSize(0.05);
    hist_dl_cat[0]->GetYaxis()->SetLabelSize(((hist_dl_cat[0]->GetYaxis())->GetLabelSize())*1.25);
    hist_dl_cat[0]->GetYaxis()->SetTitle("Number of Events");


    int max_bin_data_dl = hist_dl_cat[0]->GetMaximumBin();
    double max_data_dl = hist_dl_cat[0]->GetBinContent(max_bin_data_dl) + hist_dl_cat[0]->GetBinError(max_bin_data_dl);

    hist_dl_cat[0]->GetYaxis()->SetRangeUser(0.5,40 * max_data_dl);

    
    hist_dl_cat_bkg->SetFillStyle(3354);
    hist_dl_cat_bkg->SetFillColor(kBlack);
    hist_dl_cat_bkg->SetMarkerSize(0);

    myRatio_dl_1sig->SetFillStyle(3354);
    myRatio_dl_1sig->SetFillColor(kBlack);
    myRatio_dl_1sig->SetMarkerSize(0);



    
    // double bkg_integral_dl = hist_dl_cat_bkg->Integral();

    // double sig_integral_dl = hist_dl_cat[Nsamples-2]->Integral();
    hist_dl_cat[Nsamples-2]->Scale(scale_ttH);

    
    legend_dl->AddEntry(hist_dl_cat[0],histLabels[0],"pe1");
    legend_dl->AddEntry(hist_dl_cat[Nsamples-2],histLabels[Nsamples-2]+Form(" (x%d)",int(scale_ttH+0.0001)),"l");
    for( int iSample=1; iSample<Nsamples; iSample++ ){
      if( samples[iSample]=="zjets" || samples[iSample]=="ttbarZ" ) continue;
      if( iSample<Nsamples-2 )  legend_dl->AddEntry(hist_dl_cat[iSample],histLabels[iSample],"f");
    }

    legend_dl->AddEntry(hist_dl_cat_bkg,histLabels[Nsamples-1],"f");


    
    TLine* myLine_dl;
    myLine_dl = new TLine(xmin_dl, 1, xmax_dl, 1);


    std::cout << "\n\n=====================\n";
    for(int bin = 1; bin <=     hist_dl_cat[0]->GetNbinsX(); ++bin) {
      std::cout << "  bin" << bin << ": " <<     hist_dl_cat[0]->GetBinContent(bin) << std::endl;
    }

    // Plot
    myC1->cd(1);
    hist_dl_cat[0]->SetLineWidth(2);
    hist_dl_cat[0]->SetLineColor(kBlack);
    hist_dl_cat[0]->Draw("pex0");
    hs_dl->Draw("histsame");
    hist_dl_cat_bkg->Draw("e2same");
    hist_dl_cat[Nsamples-2]->Draw("histsame");
    hist_dl_cat[0]->Draw("pex0same");

    if( 1 ) {
      std::cout << "\n\nDL per-category relative errors: " << fits[iFit] << std::endl;
      for(int bin = 1; bin <= hist_dl_cat_bkg->GetNbinsX(); ++bin) {
	const double y = hist_dl_cat_bkg->GetBinContent(bin);
	const double e = hist_dl_cat_bkg->GetBinError(bin);
	const TString label = myRatio_dl->GetXaxis()->GetBinLabel(bin);
	std::cout << "  bin" << bin << "(" << label << "): " << y << " +/- " << e << " --> rel err = " << e/y << std::endl;
      }
    }

    legend_dl->Draw();

    LumiInfoLatex.Draw();
    CMSInfoLatex.Draw();
    PublishInfoLatex.Draw();
    if( fits[iFit] == "prefit" ) prefit_label.Draw();


    myC1->cd(2);
    myRatio_dl->SetLineWidth(2);
    myRatio_dl->Draw("pex0");
    myRatio_dl_1sig->Draw("e2same");
    myRatio_dl_asymmerr->Draw("pesame");

    myLine_dl->Draw();

    myC1->GetPad(1)->SetLogy(1);

    myC1->GetPad(1)->RedrawAxis();
    myC1->GetPad(2)->RedrawAxis();

    plotname = dirprefix + "category_yield_dl_" + fits[iFit] + ".png";
    myC1->Print(plotname);

    plotname = dirprefix + "category_yield_dl_" + fits[iFit] + ".pdf";
    if( printPDF_ ) myC1->Print(plotname);



    delete myRatio_dl;
    delete myRatio_dl_asymmerr;
    delete myRatio_dl_1sig;
    delete myLine_dl;
    delete legend_dl;


	
  }


  // Close the files
  std::cout << " Closing file..." << std::endl;
  file->Close();
  std::cout << " Done! " << std::endl;
}




// void setErrorsInYieldPlots(TH1* h, const bool isPrefit, const TString& channel, const bool isRatio) {
//   std::vector<double> dlUncPrefit;
//   std::vector<double> dlUncPostfit;
//   std::vector<double> slUncPrefit;
//   std::vector<double> slUncPostfit;
  
//   std::vector<double>* usedUnc = 0;
//   if( isPrefit  && channel=="DL" ) usedUnc = &dlUncPrefit;
//   if( isPostfit && channel=="DL" ) usedUnc = &dlUncPostfit;
//   if( isPrefit  && channel=="SL" ) usedUnc = &slUncPrefit;
//   if( isPostfit && channel=="SL" ) usedUnc = &slUncPostfit;
//   for(int bin = 1; bin <= h->GetNbinsX(); ++bin) {
//     double unc = usedUnc->at(bin-1);
//     if( !isRatio ) {
//       unc *= h->GetBinContent(bin);
//     }
//     h->SetBinError(bin,unc);
//   }
// }

