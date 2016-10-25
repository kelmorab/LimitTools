import sys
import math


allSysts=["lumi_13TeV","QCDscale_ttH","QCDscale_ttbar","QCDscale_singlet","pdf_gg_ttH","pdf_gg","pdf_qqbar","pdf_qg","QCDscale_V","QCDscale_VV","CMS_ttH_Q2scale_ttbarOther","CMS_ttH_Q2scale_ttbarPlusB","CMS_ttH_Q2scale_ttbarPlus2B","CMS_ttH_Q2scale_ttbarPlusBBbar","CMS_ttH_Q2scale_ttbarPlusCCbar","CMS_ttH_CSVLF","CMS_ttH_CSVHF","CMS_ttH_CSVHFStats1","CMS_ttH_CSVLFStats1","CMS_ttH_CSVHFStats2","CMS_ttH_CSVLFStats2","CMS_ttH_CSVCErr1","CMS_ttH_CSVCErr2","CMS_scale_j","CMS_ttH_QCDscale_ttbarPlusB","CMS_ttH_QCDscale_ttbarPlus2B","CMS_ttH_QCDscale_ttbarPlusBBbar","CMS_ttH_QCDscale_ttbarPlusCCbar","CMS_ttH_PU","CMS_res_j","CMS_ttH_eff_leptonLJ","CMS_ttH_ljets_Trig","CMS_ttH_PSscale_ttbarOther","CMS_ttH_PSscale_ttbarPlusB","CMS_ttH_PSscale_ttbarPlus2B","CMS_ttH_PSscale_ttbarPlusBBbar","CMS_ttH_PSscale_ttbarPlusCCbar","CMS_ttH_dl_Trig","CMS_ttH_eff_lepton"]

statSysts=["CMS_ttH_CSVHFStats1","CMS_ttH_CSVLFStats1","CMS_ttH_CSVHFStats2","CMS_ttH_CSVLFStats2","lumi_13TeV","CMS_ttH_eff_leptonLJ","CMS_ttH_eff_lepton","CMS_scale_j","CMS_ttH_CSVLF","CMS_ttH_CSVHF","CMS_ttH_CSVCErr1","CMS_ttH_CSVCErr2","CMS_res_j","BinByBin"]
statSystsMinimum=[0.01,0.01,0.01,0.01,0.015,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]
assert(len(statSysts)==len(statSystsMinimum))
		  
theoSysts=["QCDscale_ttH","QCDscale_ttbar","QCDscale_singlet","pdf_gg_ttH","pdf_gg","pdf_qqbar","pdf_qg","QCDscale_V","QCDscale_VV","CMS_ttH_QCDscale_ttbarPlusB","CMS_ttH_QCDscale_ttbarPlus2B","CMS_ttH_QCDscale_ttbarPlusBBbar","CMS_ttH_QCDscale_ttbarPlusCCbar","CMS_ttH_Q2scale_ttbarOther","CMS_ttH_Q2scale_ttbarPlusB","CMS_ttH_Q2scale_ttbarPlus2B","CMS_ttH_Q2scale_ttbarPlusBBbar","CMS_ttH_Q2scale_ttbarPlusCCbar","CMS_ttH_PSscale_ttbarOther","CMS_ttH_PSscale_ttbarPlusB","CMS_ttH_PSscale_ttbarPlus2B","CMS_ttH_PSscale_ttbarPlusBBbar","CMS_ttH_PSscale_ttbarPlusCCbar"]


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def scaleRates(infilename,outfilename, scale, scaleFactorTheoSysts=1.0, scaleStatSysts=False):
  infile=open(infilename,"r")
  inlist=list(infile)
  newlines=[]
  
  for line in inlist:
    #print line
    if ("observation" in line or "rate" in line):
      splitline=line.replace("\n","").replace("\t"," ").split(" ")
      #print line
      #print splitline
      futureline=""
      for word in splitline:
	#print word
	if (is_number(word) and word!="-1"):
	  fl=float(word)
	  nfl=fl*scale
	  nw=str(nfl)
	  futureline+=nw+" "
	else:
	  futureline+=word+" "
      futureline=futureline.rstrip(" ")+"\n"
	  #print word, nw
      #print futureline
      newlines.append(futureline)
      #print newlines[-1]
    
    elif (scaleStatSysts==True and ( line.replace("\n","").replace("\t"," ").split(" ")[0] in statSysts or ("BDTbin" in line and "BinByBin" in statSysts))):
      print "stat syst", line.replace("\n","").replace("\t"," ").split(" ")[0]
      splitline=line.replace("\n","").replace("\t"," ").split(" ")
      futureline=""
      for word in splitline:
	#print word
	# get min scale
	minscale=0.0
	for sS, sSM in zip(statSysts,statSystsMinimum):
	  if line.replace("\n","").replace("\t"," ").split(" ")[0] == sS:
	    minscale=sSM
	#print "minimum ", line.replace("\n","").replace("\t"," ").split(" ")[0], minscale
	if (is_number(word) and word!="-1"):
	  fl=float(word)
	  nfl=max(fl/math.sqrt(float(scale)),minscale)
	  nw=str(nfl)
	  futureline+=nw+" "
	  #print word, nw
	else:
	  futureline+=word+" "
      futureline=futureline.rstrip(" ")+"\n"
      #print futureline
      newlines.append(futureline)
            
    elif (scaleFactorTheoSysts!=1.0 and line.replace("\n","").replace("\t"," ").split(" ")[0] in theoSysts):
      print "theo syst", line.replace("\n","").replace("\t"," ").split(" ")[0]
      splitline=line.replace("\n","").replace("\t"," ").split(" ")
      futureline=""
      for word in splitline:
	#print word
	if (is_number(word) and word!="-1"):
	  fl=float(word)
	  #print fl
	  nfl=(fl-1.0)*float(scaleFactorTheoSysts)+1.0
	  #print nfl
	  nw=str(nfl)
	  futureline+=nw+" "
	  #print word, nw
	elif ("/" in word):
	  if (is_number(word.split("/")[0]) and is_number(word.split("/")[1]) ):
	    fl1=float(word.split("/")[0])
	    nfl1=1.0-(1.0-fl1)*float(scaleFactorTheoSysts)
	    nw1=str(nfl1)
	    futureline+=nw1+"/"
	    fl2=float(word.split("/")[1])
	    nfl2=(fl2-1.0)*float(scaleFactorTheoSysts)+1.0
	    nw2=str(nfl2)
	    futureline+=nw2+" "
	  #print word, nw
	else:
	  futureline+=word+" "
      futureline=futureline.rstrip(" ")+"\n"
      #print futureline
      newlines.append(futureline)
      
    
    else:
      newlines.append(line)
      #print line
    
  outfile=open(outfilename,"w")
  for line in newlines:
    outfile.write(line)
  outfile.close()
  
  
  
  
infilename=sys.argv[1]
outfilename=sys.argv[2]
scalestring=sys.argv[3]
scaleFactorTheoSysts=1.0
if len(sys.argv)>=5:
  scaleFactorTheoSysts=sys.argv[4]
  
scaleStatSysts=False
if len(sys.argv)==6:
  if sys.argv[5]=="scaleStatSysts":
    scaleStatSysts=True
  

scale=float(scalestring)
scale=scale/2.7

print "scaling lumi by ", str(scale)

scaleRates(infilename,outfilename,scale,scaleFactorTheoSysts,scaleStatSysts)


