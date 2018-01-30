#-*-coding:utf-8-*-
import pandas as pd
import pickle
import os

# files=os.listdir("processed_datas/b_l")
# print files[310]
path="processed_datas/b_l/"
ff=open(path+"1000.pkl","rb")
b_l=pickle.load(ff)
ff.close()
print b_l
# for file in files[1:500]:
#     f=open(path+file,"rb")
#     df=pickle.load(f)
#     f.close()
#     b_l=b_l.append(df)
# b_l=b_l.reset_index(drop=True)
# marked_borrowers=pd.read_csv("processed_datas/marker_borrowers3.csv")
# b_l_m=pd.merge(b_l,marked_borrowers,how="left",on="borrowerkey")
#
# pd.DataFrame.to_csv(b_l_m,path_or_buf="processed_datas/5000borrowers.csv",index=False)