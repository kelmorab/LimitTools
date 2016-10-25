import ROOT
import sys
from subprocess import call
ROOT.gROOT.SetBatch(True)

datacards=sys.argv[1]

mode=sys.argv[2]
#print params

allstring="CMS_ttH_singlet_ljets_boosted_13TeV_BDTbin4=-0.0259883,CMS_ttH_singlet_ljets_boosted_13TeV_BDTbin9=-0.084844,CMS_ttH_ttbarOther_ljets_boosted_13TeV_BDTbin4=-0.0420465,CMS_ttH_ttbarOther_ljets_boosted_13TeV_BDTbin5=-0.027657,CMS_ttH_ttbarOther_ljets_boosted_13TeV_BDTbin7=-0.0558301,CMS_ttH_ttbarOther_ljets_j4_t3_13TeV_BDTbin17=-0.00591694,CMS_ttH_ttbarOther_ljets_j4_t3_13TeV_BDTbin18=-0.154335,CMS_ttH_ttbarOther_ljets_j4_t3_13TeV_BDTbin19=-0.184037,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin13=0.0334328,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin14=0.0990168,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin16=-0.197932,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin17=0.00814102,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin19=-0.0630185,CMS_ttH_ttbarOther_ljets_jge6_t2_13TeV_BDTbin18=-0.124051,CMS_ttH_ttbarOther_ljets_jge6_t2_13TeV_BDTbin19=-0.129905,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin10=-0.0739002,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin11=0.137417,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin12=0.00559844,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin13=0.0117721,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin14=-0.0294919,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin15=-0.23401,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin16=-0.0426022,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin17=0.0546186,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin9=-0.147111,CMS_ttH_ttbarPlus2B_ljets_boosted_13TeV_BDTbin4=-0.0279141,CMS_ttH_ttbarPlus2B_ljets_boosted_13TeV_BDTbin5=-0.0209351,CMS_ttH_ttbarPlus2B_ljets_boosted_13TeV_BDTbin7=-0.0350362,CMS_ttH_ttbarPlus2B_ljets_j4_t3_13TeV_BDTbin17=-0.00668465,CMS_ttH_ttbarPlus2B_ljets_j4_t3_13TeV_BDTbin19=-0.0829358,CMS_ttH_ttbarPlus2B_ljets_j5_t3_13TeV_BDTbin19=-0.0320143,CMS_ttH_ttbarPlus2B_ljets_jge6_t3_13TeV_BDTbin15=-0.123258,CMS_ttH_ttbarPlus2B_ljets_jge6_t3_13TeV_BDTbin16=-0.0259627,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin4=-0.0402349,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin5=-0.0310345,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin7=-0.060811,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin9=-0.136605,CMS_ttH_ttbarPlusBBbar_ljets_j4_t3_13TeV_BDTbin18=-0.0898747,CMS_ttH_ttbarPlusBBbar_ljets_j5_t3_13TeV_BDTbin16=-0.0990353,CMS_ttH_ttbarPlusBBbar_ljets_j5_t3_13TeV_BDTbin17=0.0132683,CMS_ttH_ttbarPlusBBbar_ljets_j5_t3_13TeV_BDTbin19=-0.0460457,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t2_13TeV_BDTbin18=-0.0720566,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t2_13TeV_BDTbin19=-0.0693223,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin10=-0.0447048,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin11=0.0995946,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin12=0.00557894,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin13=0.0107058,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin14=-0.0237478,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin15=-0.201803,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin16=-0.0479436,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin17=0.070391,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin9=-0.0887399,CMS_ttH_ttbarPlusB_ljets_boosted_13TeV_BDTbin4=-0.0562869,CMS_ttH_ttbarPlusB_ljets_boosted_13TeV_BDTbin7=-0.0704347,CMS_ttH_ttbarPlusB_ljets_boosted_13TeV_BDTbin9=-0.128386,CMS_ttH_ttbarPlusB_ljets_j4_t3_13TeV_BDTbin17=-0.0153786,CMS_ttH_ttbarPlusB_ljets_j4_t3_13TeV_BDTbin18=-0.165202,CMS_ttH_ttbarPlusB_ljets_j4_t3_13TeV_BDTbin19=-0.187247,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin13=0.0273315,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin14=0.0861494,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin16=-0.194436,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin17=0.0223082,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin19=-0.0768489,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin10=-0.0574396,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin11=0.141048,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin12=0.012651,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin13=0.0182717,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin14=-0.0262472,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin15=-0.249971,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin16=-0.0536,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin17=0.0804241,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin9=-0.127742,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin4=-0.0387131,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin5=-0.0336641,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin7=-0.045285,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin9=-0.0629306,CMS_ttH_ttbarPlusCCbar_ljets_j4_t3_13TeV_BDTbin17=-0.0060003,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin13=0.0188383,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin14=0.0502553,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin16=-0.0958603,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin17=0.0113205,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin19=-0.0344164,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t2_13TeV_BDTbin18=-0.0984638,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t2_13TeV_BDTbin19=-0.0958199,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin10=-0.0462414,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin11=0.0949093,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin12=0.00476141,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin13=0.00892194,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin14=-0.0188602,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin15=-0.161637,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin16=-0.0369916,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin17=0.0462262,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin9=-0.0946357,CMS_res_j=-0.132915,CMS_scale_j=-0.793014,CMS_ttH_CSVCErr1=0.520719,CMS_ttH_CSVCErr2=0.0767695,CMS_ttH_CSVHF=-0.977386,CMS_ttH_CSVHFStats1=0.217849,CMS_ttH_CSVHFStats2=-0.82241,CMS_ttH_CSVLF=0.573358,CMS_ttH_CSVLFStats1=-0.465628,CMS_ttH_CSVLFStats2=0.251019,CMS_ttH_PSscale_ttbarOther=0.596612,CMS_ttH_PSscale_ttbarPlus2B=0.112759,CMS_ttH_PSscale_ttbarPlusB=0.677711,CMS_ttH_PSscale_ttbarPlusBBbar=-0.0350131,CMS_ttH_PSscale_ttbarPlusCCbar=0.560753,CMS_ttH_PU=0.568687,CMS_ttH_Q2scale_ttbarOther=0.321372,CMS_ttH_Q2scale_ttbarPlus2B=0.120594,CMS_ttH_Q2scale_ttbarPlusB=0.131629,CMS_ttH_Q2scale_ttbarPlusBBbar=0.258675,CMS_ttH_Q2scale_ttbarPlusCCbar=0.303783,CMS_ttH_QCDscale_ttbarPlus2B=-0.234065,CMS_ttH_QCDscale_ttbarPlusB=1.63555,CMS_ttH_QCDscale_ttbarPlusBBbar=0.306941,CMS_ttH_QCDscale_ttbarPlusCCbar=0.00995502,CMS_ttH_dl_Trig=0.278483,CMS_ttH_eff_lepton=0.474658,CMS_ttH_eff_leptonLJ=-0.739221,CMS_ttH_ljets_Trig=-0.705747,QCDscale_V=-0.0169929,QCDscale_VV=-0.00166042,QCDscale_singlet=-0.0220484,QCDscale_ttH=0.00142652,QCDscale_ttbar=-0.509768,lumi_13TeV=-0.417273,pdf_gg=-0.397036,pdf_gg_ttH=0.000713935,pdf_qg=-0.0257369,pdf_qqbar=-0.0662019"

alwaysstring="CMS_ttH_singlet_ljets_boosted_13TeV_BDTbin4=-0.0259883,CMS_ttH_singlet_ljets_boosted_13TeV_BDTbin9=-0.084844,CMS_ttH_ttbarOther_ljets_boosted_13TeV_BDTbin4=-0.0420465,CMS_ttH_ttbarOther_ljets_boosted_13TeV_BDTbin5=-0.027657,CMS_ttH_ttbarOther_ljets_boosted_13TeV_BDTbin7=-0.0558301,CMS_ttH_ttbarOther_ljets_j4_t3_13TeV_BDTbin17=-0.00591694,CMS_ttH_ttbarOther_ljets_j4_t3_13TeV_BDTbin18=-0.154335,CMS_ttH_ttbarOther_ljets_j4_t3_13TeV_BDTbin19=-0.184037,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin13=0.0334328,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin14=0.0990168,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin16=-0.197932,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin17=0.00814102,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin19=-0.0630185,CMS_ttH_ttbarOther_ljets_jge6_t2_13TeV_BDTbin18=-0.124051,CMS_ttH_ttbarOther_ljets_jge6_t2_13TeV_BDTbin19=-0.129905,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin10=-0.0739002,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin11=0.137417,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin12=0.00559844,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin13=0.0117721,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin14=-0.0294919,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin15=-0.23401,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin16=-0.0426022,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin17=0.0546186,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin9=-0.147111,CMS_ttH_ttbarPlus2B_ljets_boosted_13TeV_BDTbin4=-0.0279141,CMS_ttH_ttbarPlus2B_ljets_boosted_13TeV_BDTbin5=-0.0209351,CMS_ttH_ttbarPlus2B_ljets_boosted_13TeV_BDTbin7=-0.0350362,CMS_ttH_ttbarPlus2B_ljets_j4_t3_13TeV_BDTbin17=-0.00668465,CMS_ttH_ttbarPlus2B_ljets_j4_t3_13TeV_BDTbin19=-0.0829358,CMS_ttH_ttbarPlus2B_ljets_j5_t3_13TeV_BDTbin19=-0.0320143,CMS_ttH_ttbarPlus2B_ljets_jge6_t3_13TeV_BDTbin15=-0.123258,CMS_ttH_ttbarPlus2B_ljets_jge6_t3_13TeV_BDTbin16=-0.0259627,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin4=-0.0402349,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin5=-0.0310345,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin7=-0.060811,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin9=-0.136605,CMS_ttH_ttbarPlusBBbar_ljets_j4_t3_13TeV_BDTbin18=-0.0898747,CMS_ttH_ttbarPlusBBbar_ljets_j5_t3_13TeV_BDTbin16=-0.0990353,CMS_ttH_ttbarPlusBBbar_ljets_j5_t3_13TeV_BDTbin17=0.0132683,CMS_ttH_ttbarPlusBBbar_ljets_j5_t3_13TeV_BDTbin19=-0.0460457,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t2_13TeV_BDTbin18=-0.0720566,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t2_13TeV_BDTbin19=-0.0693223,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin10=-0.0447048,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin11=0.0995946,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin12=0.00557894,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin13=0.0107058,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin14=-0.0237478,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin15=-0.201803,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin16=-0.0479436,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin17=0.070391,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin9=-0.0887399,CMS_ttH_ttbarPlusB_ljets_boosted_13TeV_BDTbin4=-0.0562869,CMS_ttH_ttbarPlusB_ljets_boosted_13TeV_BDTbin7=-0.0704347,CMS_ttH_ttbarPlusB_ljets_boosted_13TeV_BDTbin9=-0.128386,CMS_ttH_ttbarPlusB_ljets_j4_t3_13TeV_BDTbin17=-0.0153786,CMS_ttH_ttbarPlusB_ljets_j4_t3_13TeV_BDTbin18=-0.165202,CMS_ttH_ttbarPlusB_ljets_j4_t3_13TeV_BDTbin19=-0.187247,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin13=0.0273315,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin14=0.0861494,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin16=-0.194436,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin17=0.0223082,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin19=-0.0768489,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin10=-0.0574396,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin11=0.141048,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin12=0.012651,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin13=0.0182717,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin14=-0.0262472,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin15=-0.249971,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin16=-0.0536,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin17=0.0804241,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin9=-0.127742,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin4=-0.0387131,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin5=-0.0336641,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin7=-0.045285,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin9=-0.0629306,CMS_ttH_ttbarPlusCCbar_ljets_j4_t3_13TeV_BDTbin17=-0.0060003,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin13=0.0188383,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin14=0.0502553,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin16=-0.0958603,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin17=0.0113205,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin19=-0.0344164,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t2_13TeV_BDTbin18=-0.0984638,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t2_13TeV_BDTbin19=-0.0958199,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin10=-0.0462414,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin11=0.0949093,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin12=0.00476141,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin13=0.00892194,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin14=-0.0188602,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin15=-0.161637,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin16=-0.0369916,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin17=0.0462262,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin9=-0.0946357,CMS_res_j=-0.132915,CMS_scale_j=-0.793014,CMS_ttH_CSVCErr1=0.520719,CMS_ttH_CSVCErr2=0.0767695,CMS_ttH_CSVHF=-0.977386,CMS_ttH_CSVHFStats1=0.217849,CMS_ttH_CSVHFStats2=-0.82241,CMS_ttH_CSVLF=0.573358,CMS_ttH_CSVLFStats1=-0.465628,CMS_ttH_CSVLFStats2=0.251019,CMS_ttH_PSscale_ttbarOther=0.596612,CMS_ttH_PSscale_ttbarPlus2B=0.112759,CMS_ttH_PSscale_ttbarPlusB=0.677711,CMS_ttH_PSscale_ttbarPlusBBbar=-0.0350131,CMS_ttH_PSscale_ttbarPlusCCbar=0.560753,CMS_ttH_PU=0.568687,CMS_ttH_Q2scale_ttbarOther=0.321372,CMS_ttH_Q2scale_ttbarPlus2B=0.120594,CMS_ttH_Q2scale_ttbarPlusB=0.131629,CMS_ttH_Q2scale_ttbarPlusBBbar=0.258675,CMS_ttH_Q2scale_ttbarPlusCCbar=0.303783,CMS_ttH_QCDscale_ttbarPlus2B=-0.234065,CMS_ttH_QCDscale_ttbarPlusB=1.63555,CMS_ttH_QCDscale_ttbarPlusBBbar=0.306941,CMS_ttH_QCDscale_ttbarPlusCCbar=0.00995502,CMS_ttH_dl_Trig=0.278483,CMS_ttH_eff_lepton=0.474658,CMS_ttH_eff_leptonLJ=-0.739221,CMS_ttH_ljets_Trig=-0.705747,QCDscale_V=-0.0169929,QCDscale_VV=-0.00166042,QCDscale_singlet=-0.0220484,QCDscale_ttH=0.00142652,QCDscale_ttbar=-0.509768,lumi_13TeV=-0.417273,pdf_gg=-0.397036,pdf_gg_ttH=0.000713935,pdf_qg=-0.0257369,pdf_qqbar=-0.0662019"

neverfreezestring="CMS_res_j=-0.132915,CMS_scale_j=-0.793014,CMS_ttH_CSVCErr1=0.520719,CMS_ttH_CSVCErr2=0.0767695,CMS_ttH_CSVHF=-0.977386,CMS_ttH_CSVHFStats1=0.217849,CMS_ttH_CSVHFStats2=-0.82241,CMS_ttH_CSVLF=0.573358,CMS_ttH_CSVLFStats1=-0.465628,CMS_ttH_CSVLFStats2=0.251019,CMS_ttH_PSscale_ttbarOther=0.596612,CMS_ttH_PSscale_ttbarPlus2B=0.112759,CMS_ttH_PSscale_ttbarPlusB=0.677711,CMS_ttH_PSscale_ttbarPlusBBbar=-0.0350131,CMS_ttH_PSscale_ttbarPlusCCbar=0.560753,CMS_ttH_PU=0.568687,CMS_ttH_Q2scale_ttbarOther=0.321372,CMS_ttH_Q2scale_ttbarPlus2B=0.120594,CMS_ttH_Q2scale_ttbarPlusB=0.131629,CMS_ttH_Q2scale_ttbarPlusBBbar=0.258675,CMS_ttH_Q2scale_ttbarPlusCCbar=0.303783,CMS_ttH_QCDscale_ttbarPlus2B=-0.234065,CMS_ttH_QCDscale_ttbarPlusB=1.63555,CMS_ttH_QCDscale_ttbarPlusBBbar=0.306941,CMS_ttH_QCDscale_ttbarPlusCCbar=0.00995502,CMS_ttH_dl_Trig=0.278483,CMS_ttH_eff_lepton=0.474658,CMS_ttH_eff_leptonLJ=-0.739221,CMS_ttH_ljets_Trig=-0.705747,QCDscale_V=-0.0169929,QCDscale_VV=-0.00166042,QCDscale_singlet=-0.0220484,QCDscale_ttH=0.00142652,QCDscale_ttbar=-0.509768,lumi_13TeV=-0.417273,pdf_gg=-0.397036,pdf_gg_ttH=0.000713935,pdf_qg=-0.0257369,pdf_qqbar=-0.0662019"

paramstringSplusB="CMS_res_j=-0.132915,CMS_scale_j=-0.793014,CMS_ttH_CSVCErr1=0.520719,CMS_ttH_CSVCErr2=0.0767695,CMS_ttH_CSVHF=-0.977386,CMS_ttH_CSVHFStats1=0.217849,CMS_ttH_CSVHFStats2=-0.82241,CMS_ttH_CSVLF=0.573358,CMS_ttH_CSVLFStats1=-0.465628,CMS_ttH_CSVLFStats2=0.251019,CMS_ttH_PSscale_ttbarOther=0.596612,CMS_ttH_PSscale_ttbarPlus2B=0.112759,CMS_ttH_PSscale_ttbarPlusB=0.677711,CMS_ttH_PSscale_ttbarPlusBBbar=-0.0350131,CMS_ttH_PSscale_ttbarPlusCCbar=0.560753,CMS_ttH_PU=0.568687,CMS_ttH_Q2scale_ttbarOther=0.321372,CMS_ttH_Q2scale_ttbarPlus2B=0.120594,CMS_ttH_Q2scale_ttbarPlusB=0.131629,CMS_ttH_Q2scale_ttbarPlusBBbar=0.258675,CMS_ttH_Q2scale_ttbarPlusCCbar=0.303783,CMS_ttH_QCDscale_ttbarPlus2B=-0.234065,CMS_ttH_QCDscale_ttbarPlusB=1.63555,CMS_ttH_QCDscale_ttbarPlusBBbar=0.306941,CMS_ttH_QCDscale_ttbarPlusCCbar=0.00995502,CMS_ttH_dl_Trig=0.278483,CMS_ttH_eff_lepton=0.474658,CMS_ttH_eff_leptonLJ=-0.739221,CMS_ttH_ljets_Trig=-0.705747,QCDscale_V=-0.0169929,QCDscale_VV=-0.00166042,QCDscale_singlet=-0.0220484,QCDscale_ttH=0.00142652,QCDscale_ttbar=-0.509768,lumi_13TeV=-0.417273,pdf_gg=-0.397036,pdf_gg_ttH=0.000713935,pdf_qg=-0.0257369,pdf_qqbar=-0.0662019"

paramNamelist=[]
paramListSplusB=[]

paramListAlways=[]
paramNamesAlways=[]

paramListNever=[]
paramNamesNever=[]

prl=[]
if alwaysstring!="":
  prl=alwaysstring.split(",")
for p in prl:
  n=p.split("=")[0]
  v=p.split("=")[1]
  if mode=="dl" and ("ljets" in n or "LJ" in n):
    continue
  if mode=="sl" and ("dl" in n or "dl" in n or n=="CMS_ttH_eff_lepton"):
    continue
  paramNamesAlways.append(n)
  paramListAlways.append(v)

if neverfreezestring!="":
  prl=neverfreezestring.split(",")
  for p in prl:
    n=p.split("=")[0]
    v=p.split("=")[1]
    if mode=="dl" and ("ljets" in n or "LJ" in n):
      continue
    if mode=="sl" and ("dl" in n or "DL" in n or n=="CMS_ttH_eff_lepton"):
      continue
    paramNamesNever.append(n)
    paramListNever.append(v)
print paramNamesNever

prl=paramstringSplusB.split(",")
for p in prl:
  v=p.split("=")[1]
  n=p.split("=")[0]
  if mode=="dl" and ("ljets" in n or "LJ" in n):
    continue
  if mode=="sl" and ("dl" in n or "DL" in n or n=="CMS_ttH_eff_lepton"):
      continue
  paramListSplusB.append(v)
  paramNamelist.append(n)

print paramNamelist
print paramListSplusB
#floatmode="--floatOtherPOI=1"
floatR=True
doPlots=False

counter=0

if mode=="dl":
  minr=-7.5
  maxr=6
else:
  minr=-6
  maxr=6
for p,pv in zip(paramNamelist,paramListSplusB):
  print p,pv
  #if p!="CMS_ttH_QCDscale_ttbarPlusB":
    #continue
  counter+=1
   
  npoints=60
  
  stringOfOtherNuis=""
  listOfOtherNuis=[]
  #for op in paramNamelist:
    #listOfOtherNuis.append(op)
  #stringOfOtherNuis=",".join(listOfOtherNuis)
  #print stringOfOtherNuis
  
  #pp=p.replace(" ","")
  #cmd="combine -M MultiDimFit --algo=grid --points=10 --rMin -5 --rMax 5 "+floatmode+" -P "+pp+" ttH_hbb_13TeV_sl_noMC.txt -n _nllScan_"+pp
  #print cmd
  
  freezestring="--freezeNuisances"
  setstring="--setPhysicsModelParameters"
  freezeParams=""
  setParams=""
  for an,ap in zip(paramNamesAlways,paramListAlways):
    if (an not in paramNamesNever) and (an!=p):
      freezeParams+=an+","
      setParams+=an+"="+ap+","
    else:
      listOfOtherNuis.append(an)
  
  stringOfOtherNuis=",".join(listOfOtherNuis)
  print stringOfOtherNuis
  print freezeParams
  print setParams

  if floatR:
    call(["combine","-M","MultiDimFit","--algo=grid","--points="+str(npoints),"--rMin",str(minr),"--rMax",str(maxr),"--redefineSignalPOIs","r","-P","r","--setPhysicsModelParameterRanges","r"+"="+str(minr)+","+str(maxr),"--saveInactivePOI","1","--robustFit=1","--minimizerTolerance=0.001",freezestring,freezeParams,setstring,setParams,datacards,"--saveSpecifiedNuis",stringOfOtherNuis])

    #call(["combine","-M","MultiDimFit","--algo=grid","--points="+str(npoints),"--floatOtherPOI","1","--redefineSignalPOIs","r","-P",pp,"--setPhysicsModelParameterRanges",pp+"="+str(minpoi)+","+str(maxpoi),"--rMin",str(minr),"--rMax",str(maxr),"--saveInactivePOI","1","--saveSpecifiedNuis",stringOfOtherNuis,datacards])
    #call(["combine","-M","MultiDimFit","--algo=grid","--points="+str(npoints),floatmode,"-P",pp,"--redefineSignalPOIs",pp,"--setPhysicsModelParameterRanges",pp+"="+str(minr)+","+str(maxr),"--saveInactivePOI","--saveSpecifiedNuis",stringOfOtherNuis,datacards])

  else:
    print "currently not supported"
    #call(["combine","-M","MultiDimFit","--algo=grid","--points=100",floatmode,"-P",pp,"--redefineSignalPOIs","r,"+pp,"--setPhysicsModelParameterRanges","r=-"+str(minr)*","+str(maxr)+":"+pp+"=-5,5" ,datacards])
  
  outfilename="higgsCombineTest.MultiDimFit.mH120.root"
  print outfilename

    
  resfilename="nllscans/"+p+"_frozen_"+outfilename
  call(["cp",outfilename, resfilename])
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
