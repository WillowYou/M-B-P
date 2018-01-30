#-*-coding:utf8-*-
import pandas as pd
import numpy as np
import threading
import pickle

#统计每位用户的投标次数(成功、全部）、出借人的投资占比（横向、纵向）
# merge_bid_data=pd.read_csv("processed_datas/merge_data.csv")
# merge_bid_data["listingstatus"]=merge_bid_data["listingstatus_x"]
# merge_bid_data=merge_bid_data.loc[:,["borrowerkey","lenderkey","bidkey","listingkey","listingstatus",\
#                                "bidstatus","participationamount","amountfunded","amountborrowed",\
#                                 "loankey","loanstatus"]]
# merge_bid_data=merge_bid_data[merge_bid_data["listingstatus"]=="Completed"]
# pd.DataFrame.to_csv(merge_bid_data,path_or_buf="processed_datas/to_mark_loan_completed.csv",index=False)
merge_bid_data=pd.read_csv("processed_datas/to_mark_loan_completed.csv")
borrowers_f=open("processed_datas/borrowers.txt","r")
borrowers_l=borrowers_f.readline().split(",")

borrowers_f.close()

# lenders_f=open("processed_datas/lenders.txt","r")
# lenders_l=lenders_f.readline().split(",")
#
# lenders_f.close()
bld = pd.read_csv("processed_datas/marker_borrowers3.csv")
b_l_dic={}

#bld = pd.DataFrame(columns=["borrowerkey","B_loan_num","B_loan_paid", "B_loan_notpaid","defaulted"])
for _,borrower in enumerate(borrowers_l[20000:25000]):
    print "b" + borrower

    b_l_dic["borrowerkey"] = borrower
    b_l_b_data = merge_bid_data[merge_bid_data["borrowerkey"] == borrower]
    b_l_b_loan_data = b_l_b_data.loc[:, ["loankey", "loanstatus"]]
    b_l_b_loan_data = b_l_b_loan_data.drop_duplicates()
    b_l_dic["B_loan_num"] = b_l_b_loan_data.shape[0]

    marks_defaulted=["3 months late","4+ months late","Defaulted (Bankruptcy)","Defaulted (Delinquency)",
           "Defaulted (PaidInFull) ","Defaulted (SettledInFull)"]
    marks_paid=["1 month late","2 months late","Late","Paid","Payoff in progress"]
    num_defaulted = b_l_b_loan_data[b_l_b_loan_data["loanstatus"].isin(marks_defaulted)].shape[0]
    num_paid=b_l_b_loan_data[b_l_b_loan_data["loanstatus"].isin(marks_paid)].shape[0]
    b_l_dic["B_loan_paid"] = num_paid
    b_l_dic["B_loan_notpaid"] = num_defaulted

    if num_defaulted>0:
        b_l_dic["defaulted"] = 1
    elif num_paid>0:
        b_l_dic["defaulted"] = 0
    else:
        b_l_dic["defaulted"] = -1
    bld=bld.append(b_l_dic,ignore_index=True)

pd.DataFrame.to_csv(bld,path_or_buf="processed_datas/marker_borrowers3.csv",index=False)


