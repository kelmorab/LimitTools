import sys

infile=sys.argv[1]
inlist=list(open(infile,"r"))

names=[]
ups2=[]
ups1=[]
meds=[]
downs1=[]
downs2=[]


for l in inlist:
  sl=l.replace("\n","").split(" ")
  n=sl[0]
  print n
  dd=sl[10]
  d=sl[9]
  m=sl[8]
  u=sl[7]
  uu=sl[6]
  names.append(n)
  ups2.append(uu)
  ups1.append(u)
  meds.append(m)
  downs1.append(d)
  downs2.append(dd)
  
print names
print ups2
print ups1
print meds
print downs1
print downs2