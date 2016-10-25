import sys

infilelist=sys.argv[1:]

for f in infilelist:
  print f
  inf=open(f,"r")
  outf=open(f.replace("ljets_","").replace("inputs2DV12_datacard","ttH_hbb_13TeV_sl").replace("_hdecay",""),"w")
#outf=open(f.replace("ljets_","").replace("commonAnaV5plus4252_datacard_","ttH_hbb_13TeV_sl_").replace("_hdecay",""),"w")
  print inf
  print outf
  linelist=list(inf)
  for line in linelist:
    outf.write(line.replace("inputs2DV12/inputs2DV12_limitInput","common/ttH_hbb_13TeV_sl"))

  outf.close()
  inf.close()

