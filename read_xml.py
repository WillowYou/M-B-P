#-*-coding:utf8-*-

dataexoportbids_f=open("datas/ProsperDataExportBids.xml","r")
less_dataexportbids_f=open("less_dataexportbids.txt",'w')
n=0
while n <500:
    line=dataexoportbids_f.readline()
    less_dataexportbids_f.write(line+"\n")
    n+=1

