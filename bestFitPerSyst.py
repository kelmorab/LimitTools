import sys
from subprocess import call


infilename=sys.argv[1]
infile=open(infilename,"r")
indclist=list(infile)
reflimit=4.29688

systs=["lumi_13TeV","QCDscale_ttH","QCDscale_ttbar","QCDscale_singlet","pdf_gg_ttH","pdf_gg","pdf_qqbar","pdf_qg","QCDscale_V","QCDscale_VV","CMS_ttH_Q2scale_ttbarOther","CMS_ttH_Q2scale_ttbarPlusB","CMS_ttH_Q2scale_ttbarPlus2B","CMS_ttH_Q2scale_ttbarPlusBBbar","CMS_ttH_Q2scale_ttbarPlusCCbar","CMS_ttH_CSVLF","CMS_ttH_CSVHF","CMS_ttH_CSVHFStats1","CMS_ttH_CSVLFStats1","CMS_ttH_CSVHFStats2","CMS_ttH_CSVLFStats2","CMS_ttH_CSVCErr1","CMS_ttH_CSVCErr2","CMS_scale_j","CMS_ttH_QCDscale_ttbarPlusB","CMS_ttH_QCDscale_ttbarPlus2B","CMS_ttH_QCDscale_ttbarPlusBBbar","CMS_ttH_QCDscale_ttbarPlusCCbar","CMS_ttH_PU","CMS_res_j","CMS_ttH_eff_leptonLJ","CMS_ttH_ljets_Trig","CMS_ttH_PSscale_ttbarOther","CMS_ttH_PSscale_ttbarPlusB","CMS_ttH_PSscale_ttbarPlus2B","CMS_ttH_PSscale_ttbarPlusBBbar","CMS_ttH_PSscale_ttbarPlusCCbar","CMS_ttH_dl_Trig","CMS_ttH_eff_lepton","binbybin"]
resultlist=[]
improvementlist=[]

for sys in systs:
  print "doing ", sys
  outfilename=infilename+"_"+sys
  outfile=open(infilename+"_"+sys,"w")
  for line in indclist:
    if sys == line.split(" ")[0]:
      continue
    if sys=="binbybin" and "13TeV_BDTbin" in line:
      continue
    outfile.write(line)
  outfile.close()
  limitfile=open("limit.txt","w")
  call(['combine','-M', 'MaxLikelihoodFit','--expectSignal=1','-t','-1','--rMin=-5','--rMax=5' ,'--robustFit=1','--justFit',outfilename],stdout=limitfile)
  limitfile.close()
#  exit(0)
  limitfile=open("limit.txt","r")
  limitlist=list(limitfile)
  for line in limitlist:
    if "Best fit r:" in line:
      #print line
      #print line.replace("\n","").split(" ")
      thislimitstring=line.replace("\n","").split(" ")[-4]
      #print line.replace("\n","").split(" ")[-1]
      #print line.replace("\n","").split(" ")[-2]
      ##print line.replace("\n","").split(" ")[-3]
      #print line.replace("\n","").split(" ")[-4]
      #print line.replace("\n","").split(" ")[-5]
      
      #print thislimitstring
  uppererror=float(thislimitstring.split("/")[1].replace("+",""))
  lowererror=float(thislimitstring.split("/")[0].replace("-",""))
  symerror=(uppererror+lowererror)/2.0
  print sys,lowererror, uppererror, symerror
  
  limitfile.close()
  resultlist.append([sys,lowererror,uppererror, symerror])
  

print ""

#zippedlist=zip(systs,resultlist,improvementlist)
resultlist.sort(key=lambda x: x[3])
outfile=open("results.txt","w")
for sys in zippedlist:
  print sys[0], sys[1], sys[2], sys[3]

for sys in resultlist:
  outfile.write(str(sys[0])+" "+str(sys[1])+" "+str(sys[2])+" "+str(sys[3])+"\n")
outfile.close()



