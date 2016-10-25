import ROOT
import sys
from subprocess import call
from array import array
ROOT.gROOT.SetBatch(True)
ROOT.gDirectory.cd('PyROOT:/')

datacard=sys.argv[1]

alwaysstring="CMS_ttH_singlet_ljets_boosted_13TeV_BDTbin4=-0.0259883,CMS_ttH_singlet_ljets_boosted_13TeV_BDTbin9=-0.084844,CMS_ttH_ttbarOther_ljets_boosted_13TeV_BDTbin4=-0.0420465,CMS_ttH_ttbarOther_ljets_boosted_13TeV_BDTbin5=-0.027657,CMS_ttH_ttbarOther_ljets_boosted_13TeV_BDTbin7=-0.0558301,CMS_ttH_ttbarOther_ljets_j4_t3_13TeV_BDTbin17=-0.00591694,CMS_ttH_ttbarOther_ljets_j4_t3_13TeV_BDTbin18=-0.154335,CMS_ttH_ttbarOther_ljets_j4_t3_13TeV_BDTbin19=-0.184037,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin13=0.0334328,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin14=0.0990168,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin16=-0.197932,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin17=0.00814102,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin19=-0.0630185,CMS_ttH_ttbarOther_ljets_jge6_t2_13TeV_BDTbin18=-0.124051,CMS_ttH_ttbarOther_ljets_jge6_t2_13TeV_BDTbin19=-0.129905,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin10=-0.0739002,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin11=0.137417,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin12=0.00559844,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin13=0.0117721,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin14=-0.0294919,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin15=-0.23401,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin16=-0.0426022,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin17=0.0546186,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin9=-0.147111,CMS_ttH_ttbarPlus2B_ljets_boosted_13TeV_BDTbin4=-0.0279141,CMS_ttH_ttbarPlus2B_ljets_boosted_13TeV_BDTbin5=-0.0209351,CMS_ttH_ttbarPlus2B_ljets_boosted_13TeV_BDTbin7=-0.0350362,CMS_ttH_ttbarPlus2B_ljets_j4_t3_13TeV_BDTbin17=-0.00668465,CMS_ttH_ttbarPlus2B_ljets_j4_t3_13TeV_BDTbin19=-0.0829358,CMS_ttH_ttbarPlus2B_ljets_j5_t3_13TeV_BDTbin19=-0.0320143,CMS_ttH_ttbarPlus2B_ljets_jge6_t3_13TeV_BDTbin15=-0.123258,CMS_ttH_ttbarPlus2B_ljets_jge6_t3_13TeV_BDTbin16=-0.0259627,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin4=-0.0402349,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin5=-0.0310345,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin7=-0.060811,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin9=-0.136605,CMS_ttH_ttbarPlusBBbar_ljets_j4_t3_13TeV_BDTbin18=-0.0898747,CMS_ttH_ttbarPlusBBbar_ljets_j5_t3_13TeV_BDTbin16=-0.0990353,CMS_ttH_ttbarPlusBBbar_ljets_j5_t3_13TeV_BDTbin17=0.0132683,CMS_ttH_ttbarPlusBBbar_ljets_j5_t3_13TeV_BDTbin19=-0.0460457,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t2_13TeV_BDTbin18=-0.0720566,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t2_13TeV_BDTbin19=-0.0693223,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin10=-0.0447048,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin11=0.0995946,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin12=0.00557894,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin13=0.0107058,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin14=-0.0237478,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin15=-0.201803,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin16=-0.0479436,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin17=0.070391,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin9=-0.0887399,CMS_ttH_ttbarPlusB_ljets_boosted_13TeV_BDTbin4=-0.0562869,CMS_ttH_ttbarPlusB_ljets_boosted_13TeV_BDTbin7=-0.0704347,CMS_ttH_ttbarPlusB_ljets_boosted_13TeV_BDTbin9=-0.128386,CMS_ttH_ttbarPlusB_ljets_j4_t3_13TeV_BDTbin17=-0.0153786,CMS_ttH_ttbarPlusB_ljets_j4_t3_13TeV_BDTbin18=-0.165202,CMS_ttH_ttbarPlusB_ljets_j4_t3_13TeV_BDTbin19=-0.187247,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin13=0.0273315,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin14=0.0861494,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin16=-0.194436,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin17=0.0223082,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin19=-0.0768489,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin10=-0.0574396,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin11=0.141048,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin12=0.012651,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin13=0.0182717,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin14=-0.0262472,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin15=-0.249971,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin16=-0.0536,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin17=0.0804241,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin9=-0.127742,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin4=-0.0387131,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin5=-0.0336641,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin7=-0.045285,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin9=-0.0629306,CMS_ttH_ttbarPlusCCbar_ljets_j4_t3_13TeV_BDTbin17=-0.0060003,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin13=0.0188383,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin14=0.0502553,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin16=-0.0958603,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin17=0.0113205,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin19=-0.0344164,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t2_13TeV_BDTbin18=-0.0984638,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t2_13TeV_BDTbin19=-0.0958199,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin10=-0.0462414,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin11=0.0949093,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin12=0.00476141,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin13=0.00892194,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin14=-0.0188602,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin15=-0.161637,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin16=-0.0369916,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin17=0.0462262,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin9=-0.0946357,CMS_res_j=-0.132915,CMS_scale_j=-0.793014,CMS_ttH_CSVCErr2=0.0767695,CMS_ttH_CSVHF=-0.977386,CMS_ttH_CSVHFStats1=0.217849,CMS_ttH_CSVHFStats2=-0.82241,CMS_ttH_CSVLF=0.573358,CMS_ttH_CSVLFStats1=-0.465628,CMS_ttH_CSVLFStats2=0.251019,CMS_ttH_PSscale_ttbarOther=0.596612,CMS_ttH_PSscale_ttbarPlus2B=0.112759,CMS_ttH_PSscale_ttbarPlusB=0.677711,CMS_ttH_PSscale_ttbarPlusBBbar=-0.0350131,CMS_ttH_PSscale_ttbarPlusCCbar=0.560753,CMS_ttH_PU=0.568687,CMS_ttH_Q2scale_ttbarOther=0.321372,CMS_ttH_Q2scale_ttbarPlus2B=0.120594,CMS_ttH_Q2scale_ttbarPlusB=0.131629,CMS_ttH_Q2scale_ttbarPlusBBbar=0.258675,CMS_ttH_Q2scale_ttbarPlusCCbar=0.303783,CMS_ttH_QCDscale_ttbarPlus2B=-0.234065,CMS_ttH_QCDscale_ttbarPlusBBbar=0.306941,CMS_ttH_QCDscale_ttbarPlusCCbar=0.00995502,CMS_ttH_dl_Trig=0.278483,CMS_ttH_eff_lepton=0.474658,CMS_ttH_eff_leptonLJ=-0.739221,CMS_ttH_ljets_Trig=-0.705747,QCDscale_V=-0.0169929,QCDscale_VV=-0.00166042,QCDscale_singlet=-0.0220484,QCDscale_ttH=0.00142652,QCDscale_ttbar=-0.509768,lumi_13TeV=-0.417273,pdf_gg=-0.397036,pdf_gg_ttH=0.000713935,pdf_qg=-0.0257369,pdf_qqbar=-0.0662019"

#paramstringBonly="CMS_res_j=-0.12192,CMS_scale_j=-0.780764,CMS_ttH_CSVCErr1=0.520029,CMS_ttH_CSVCErr2=0.132348,CMS_ttH_CSVHF=-1.00802,CMS_ttH_CSVHFStats1=0.169279,CMS_ttH_CSVHFStats2=-0.87024,CMS_ttH_CSVLF=0.56031,CMS_ttH_CSVLFStats1=-0.478382,CMS_ttH_CSVLFStats2=0.322799,CMS_ttH_PSscale_ttbarOther=0.609084,CMS_ttH_PSscale_ttbarPlus2B=0.113844,CMS_ttH_PSscale_ttbarPlusB=0.710773,CMS_ttH_PSscale_ttbarPlusBBbar=-0.0298604,CMS_ttH_PSscale_ttbarPlusCCbar=0.551773,CMS_ttH_PU=0.537874,CMS_ttH_Q2scale_ttbarOther=0.352201,CMS_ttH_Q2scale_ttbarPlus2B=0.139296,CMS_ttH_Q2scale_ttbarPlusB=0.173773,CMS_ttH_Q2scale_ttbarPlusBBbar=0.300737,CMS_ttH_Q2scale_ttbarPlusCCbar=0.300152,CMS_ttH_QCDscale_ttbarPlus2B=-0.304735,CMS_ttH_QCDscale_ttbarPlusB=1.50701,CMS_ttH_QCDscale_ttbarPlusBBbar=-0.0856282,CMS_ttH_QCDscale_ttbarPlusCCbar=0.094877,CMS_ttH_dl_Trig=0.256853,CMS_ttH_eff_lepton=0.486129,CMS_ttH_eff_leptonLJ=-0.772931,CMS_ttH_ljets_Trig=-0.731674,QCDscale_V=-0.0170848,QCDscale_VV=-0.00172523,QCDscale_singlet=-0.0188946,QCDscale_ttH=0,QCDscale_ttbar=-0.573976,lumi_13TeV=-0.437948,pdf_gg=-0.416657,pdf_gg_ttH=0,pdf_qg=-0.0211118,pdf_qqbar=-0.0664578"

#paramstringSplusB="CMS_res_j=-0.132915,CMS_scale_j=-0.793014,CMS_ttH_CSVCErr1=0.520719,CMS_ttH_CSVCErr2=0.0767695,CMS_ttH_CSVHF=-0.977386,CMS_ttH_CSVHFStats1=0.217849,CMS_ttH_CSVHFStats2=-0.82241,CMS_ttH_CSVLF=0.573358,CMS_ttH_CSVLFStats1=-0.465628,CMS_ttH_CSVLFStats2=0.251019,CMS_ttH_PSscale_ttbarOther=0.596612,CMS_ttH_PSscale_ttbarPlus2B=0.112759,CMS_ttH_PSscale_ttbarPlusB=0.677711,CMS_ttH_PSscale_ttbarPlusBBbar=-0.0350131,CMS_ttH_PSscale_ttbarPlusCCbar=0.560753,CMS_ttH_PU=0.568687,CMS_ttH_Q2scale_ttbarOther=0.321372,CMS_ttH_Q2scale_ttbarPlus2B=0.120594,CMS_ttH_Q2scale_ttbarPlusB=0.131629,CMS_ttH_Q2scale_ttbarPlusBBbar=0.258675,CMS_ttH_Q2scale_ttbarPlusCCbar=0.303783,CMS_ttH_QCDscale_ttbarPlus2B=-0.234065,CMS_ttH_QCDscale_ttbarPlusB=1.63555,CMS_ttH_QCDscale_ttbarPlusBBbar=0.306941,CMS_ttH_QCDscale_ttbarPlusCCbar=0.00995502,CMS_ttH_dl_Trig=0.278483,CMS_ttH_eff_lepton=0.474658,CMS_ttH_eff_leptonLJ=-0.739221,CMS_ttH_ljets_Trig=-0.705747,QCDscale_V=-0.0169929,QCDscale_VV=-0.00166042,QCDscale_singlet=-0.0220484,QCDscale_ttH=0.00142652,QCDscale_ttbar=-0.509768,lumi_13TeV=-0.417273,pdf_gg=-0.397036,pdf_gg_ttH=0.000713935,pdf_qg=-0.0257369,pdf_qqbar=-0.0662019"

paramstringBonly="CMS_res_j=-0.12192,CMS_scale_j=-0.780764,CMS_ttH_CSVCErr1=0.520029,CMS_ttH_CSVCErr2=0.132348,CMS_ttH_CSVHF=-1.00802,CMS_ttH_CSVHFStats1=0.169279,CMS_ttH_CSVHFStats2=-0.87024,CMS_ttH_CSVLF=0.56031,CMS_ttH_CSVLFStats1=-0.478382,CMS_ttH_CSVLFStats2=0.322799,CMS_ttH_PSscale_ttbarOther=0.609084,CMS_ttH_PSscale_ttbarPlus2B=0.113844,CMS_ttH_PSscale_ttbarPlusB=0.710773,CMS_ttH_PSscale_ttbarPlusBBbar=-0.0298604,CMS_ttH_PSscale_ttbarPlusCCbar=0.551773,CMS_ttH_PU=0.537874,CMS_ttH_Q2scale_ttbarOther=0.352201,CMS_ttH_Q2scale_ttbarPlus2B=0.139296,CMS_ttH_Q2scale_ttbarPlusB=0.173773,CMS_ttH_Q2scale_ttbarPlusBBbar=0.300737,CMS_ttH_Q2scale_ttbarPlusCCbar=0.300152,CMS_ttH_QCDscale_ttbarPlus2B=-0.304735,CMS_ttH_QCDscale_ttbarPlusB=1.50701,CMS_ttH_QCDscale_ttbarPlusBBbar=-0.0856282,CMS_ttH_QCDscale_ttbarPlusCCbar=0.094877,CMS_ttH_dl_Trig=0.256853,CMS_ttH_eff_lepton=0.486129,CMS_ttH_eff_leptonLJ=-0.772931,CMS_ttH_ljets_Trig=-0.731674,CMS_ttH_singlet_ljets_boosted_13TeV_BDTbin4=-0.0255903,CMS_ttH_singlet_ljets_boosted_13TeV_BDTbin9=-0.084933,CMS_ttH_ttbarOther_ljets_boosted_13TeV_BDTbin4=-0.0413116,CMS_ttH_ttbarOther_ljets_boosted_13TeV_BDTbin5=-0.02687,CMS_ttH_ttbarOther_ljets_boosted_13TeV_BDTbin7=-0.0588039,CMS_ttH_ttbarOther_ljets_j4_t3_13TeV_BDTbin17=-0.0015874,CMS_ttH_ttbarOther_ljets_j4_t3_13TeV_BDTbin18=-0.157676,CMS_ttH_ttbarOther_ljets_j4_t3_13TeV_BDTbin19=-0.188468,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin13=0.0339859,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin14=0.0992196,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin16=-0.203361,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin17=0.00456622,CMS_ttH_ttbarOther_ljets_j5_t3_13TeV_BDTbin19=-0.073102,CMS_ttH_ttbarOther_ljets_jge6_t2_13TeV_BDTbin18=-0.130012,CMS_ttH_ttbarOther_ljets_jge6_t2_13TeV_BDTbin19=-0.132655,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin10=-0.0720403,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin11=0.14338,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin12=0.0032806,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin13=0.00859142,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin14=-0.0349413,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin15=-0.23844,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin16=-0.0501638,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin17=0.0473514,CMS_ttH_ttbarOther_ljets_jge6_t3_13TeV_BDTbin9=-0.142946,CMS_ttH_ttbarPlus2B_ljets_boosted_13TeV_BDTbin4=-0.0267915,CMS_ttH_ttbarPlus2B_ljets_boosted_13TeV_BDTbin5=-0.0199275,CMS_ttH_ttbarPlus2B_ljets_boosted_13TeV_BDTbin7=-0.0356872,CMS_ttH_ttbarPlus2B_ljets_j4_t3_13TeV_BDTbin17=-0.00492667,CMS_ttH_ttbarPlus2B_ljets_j4_t3_13TeV_BDTbin19=-0.0816491,CMS_ttH_ttbarPlus2B_ljets_j5_t3_13TeV_BDTbin19=-0.035938,CMS_ttH_ttbarPlus2B_ljets_jge6_t3_13TeV_BDTbin15=-0.120443,CMS_ttH_ttbarPlus2B_ljets_jge6_t3_13TeV_BDTbin16=-0.0283894,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin4=-0.0338696,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin5=-0.0259278,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin7=-0.0540521,CMS_ttH_ttbarPlusBBbar_ljets_boosted_13TeV_BDTbin9=-0.115322,CMS_ttH_ttbarPlusBBbar_ljets_j4_t3_13TeV_BDTbin18=-0.077493,CMS_ttH_ttbarPlusBBbar_ljets_j5_t3_13TeV_BDTbin16=-0.0854748,CMS_ttH_ttbarPlusBBbar_ljets_j5_t3_13TeV_BDTbin17=0.00940076,CMS_ttH_ttbarPlusBBbar_ljets_j5_t3_13TeV_BDTbin19=-0.0455702,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t2_13TeV_BDTbin18=-0.0639391,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t2_13TeV_BDTbin19=-0.0599297,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin10=-0.0363453,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin11=0.0877113,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin12=0.00347783,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin13=0.00717051,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin14=-0.0243904,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin15=-0.173238,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin16=-0.0459035,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin17=0.0520415,CMS_ttH_ttbarPlusBBbar_ljets_jge6_t3_13TeV_BDTbin9=-0.0724581,CMS_ttH_ttbarPlusB_ljets_boosted_13TeV_BDTbin4=-0.0515323,CMS_ttH_ttbarPlusB_ljets_boosted_13TeV_BDTbin7=-0.0693287,CMS_ttH_ttbarPlusB_ljets_boosted_13TeV_BDTbin9=-0.120632,CMS_ttH_ttbarPlusB_ljets_j4_t3_13TeV_BDTbin17=-0.00985324,CMS_ttH_ttbarPlusB_ljets_j4_t3_13TeV_BDTbin18=-0.158503,CMS_ttH_ttbarPlusB_ljets_j4_t3_13TeV_BDTbin19=-0.180257,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin13=0.0258757,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin14=0.0805931,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin16=-0.187953,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin17=0.0184709,CMS_ttH_ttbarPlusB_ljets_j5_t3_13TeV_BDTbin19=-0.0846037,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin10=-0.0526234,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin11=0.138132,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin12=0.00997436,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin13=0.0138391,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin14=-0.0298665,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin15=-0.238412,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin16=-0.0577779,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin17=0.0666748,CMS_ttH_ttbarPlusB_ljets_jge6_t3_13TeV_BDTbin9=-0.116427,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin4=-0.0400415,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin5=-0.0346941,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin7=-0.049695,CMS_ttH_ttbarPlusCCbar_ljets_boosted_13TeV_BDTbin9=-0.0651207,CMS_ttH_ttbarPlusCCbar_ljets_j4_t3_13TeV_BDTbin17=-0.00478271,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin13=0.0195029,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin14=0.0518101,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin16=-0.101336,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin17=0.0098231,CMS_ttH_ttbarPlusCCbar_ljets_j5_t3_13TeV_BDTbin19=-0.0411734,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t2_13TeV_BDTbin18=-0.10665,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t2_13TeV_BDTbin19=-0.10147,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin10=-0.0465736,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin11=0.101731,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin12=0.00277109,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin13=0.00695126,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin14=-0.023101,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin15=-0.170171,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin16=-0.044416,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin17=0.0415513,CMS_ttH_ttbarPlusCCbar_ljets_jge6_t3_13TeV_BDTbin9=-0.0949821,QCDscale_V=-0.0170848,QCDscale_VV=-0.00172523,QCDscale_singlet=-0.0188946,QCDscale_ttH=0,QCDscale_ttbar=-0.573976,lumi_13TeV=-0.437948,pdf_gg=-0.416657,pdf_gg_ttH=0,pdf_qg=-0.0211118,pdf_qqbar=-0.0664578"

paramstringSplusB="CMS_res_j=-0.132915,CMS_scale_j=-0.793014,CMS_ttH_CSVCErr1=0.520719,CMS_ttH_CSVCErr2=0.0767695,CMS_ttH_CSVHF=-0.977386,CMS_ttH_CSVHFStats1=0.217849,CMS_ttH_CSVHFStats2=-0.82241,CMS_ttH_CSVLF=0.573358,CMS_ttH_CSVLFStats1=-0.465628,CMS_ttH_CSVLFStats2=0.251019,CMS_ttH_PSscale_ttbarOther=0.596612,CMS_ttH_PSscale_ttbarPlus2B=0.112759,CMS_ttH_PSscale_ttbarPlusB=0.677711,CMS_ttH_PSscale_ttbarPlusBBbar=-0.0350131,CMS_ttH_PSscale_ttbarPlusCCbar=0.560753,CMS_ttH_PU=0.568687,CMS_ttH_Q2scale_ttbarOther=0.321372,CMS_ttH_Q2scale_ttbarPlus2B=0.120594,CMS_ttH_Q2scale_ttbarPlusB=0.131629,CMS_ttH_Q2scale_ttbarPlusBBbar=0.258675,CMS_ttH_Q2scale_ttbarPlusCCbar=0.303783,CMS_ttH_QCDscale_ttbarPlus2B=-0.234065,CMS_ttH_QCDscale_ttbarPlusB=1.63555,CMS_ttH_QCDscale_ttbarPlusBBbar=0.306941,CMS_ttH_QCDscale_ttbarPlusCCbar=0.00995502,CMS_ttH_dl_Trig=0.278483,CMS_ttH_eff_lepton=0.474658,CMS_ttH_eff_leptonLJ=-0.739221,CMS_ttH_ljets_Trig=-0.705747,QCDscale_V=-0.0169929,QCDscale_VV=-0.00166042,QCDscale_singlet=-0.0220484,QCDscale_ttH=0.00142652,QCDscale_ttbar=-0.509768,lumi_13TeV=-0.417273,pdf_gg=-0.397036,pdf_gg_ttH=0.000713935,pdf_qg=-0.0257369,pdf_qqbar=-0.0662019"



paramNamelist=[""]
paramListSplusB=[""]
paramListBonly=[""]

paramListAlways=[]
paramNamesAlways=[]

prl=[]
if alwaysstring!="":
  prl=alwaysstring.split(",")
for p in prl:
  n=p.split("=")[0]
  v=p.split("=")[1]
  paramNamesAlways.append(n)
  paramListAlways.append(v)

prl=paramstringBonly.split(",")
for p in prl:
  v=p.split("=")[1]
  paramListBonly.append(v)

prl=paramstringSplusB.split(",")
for p in prl:
  v=p.split("=")[1]
  n=p.split("=")[0]
  paramListSplusB.append(v)
  paramNamelist.append(n)

#for n,s,b in zip(paramNamelist,paramListSplusB,paramListBonly):
  #same=0
  #if s==b:
    #same=1
  #print n,s,b,same
  
resultFreezes=[]
resultsValues=[]

print paramNamelist

for n,v in zip( paramNamelist,paramListSplusB):
  resfile=open("result.temp","w")
  freezestring="--freezeNuisances"
  setstring="--setPhysicsModelParameters"
  freezeParams=""
  setParams=""
  for an,ap in zip(paramNamesAlways,paramListAlways):
    freezeParams+=an+","
    setParams+=an+"="+ap+","
  if n not in paramNamesAlways:
    freezeParams+=n
    setParams+=n+"="+v
  call(["combine","-M","MaxLikelihoodFit","--minos","all","--rMin","-6","--rMax","6","--robustFit=1","--minimizerTolerance=0.001",freezestring,freezeParams,setstring,setParams,datacard],stdout=resfile)
  resfile.close()
  resfile=open("result.temp","r")
  rl=list(resfile)
  bestfitvalue=0
  for l in rl:
    if "Best fit" in l:
      #print l.split(":")[1].split(" ")[0]
      bestfitvalue=float(l.split(":")[1].split()[0])
  print n,bestfitvalue
  resultFreezes.append(setParams)
  resultsValues.append(bestfitvalue)
  resfile.close()
  
for rf,rv in zip(resultFreezes,resultsValues):
  print rv








