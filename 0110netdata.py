#-*-coding:utf8-*-
import pandas as pd
import numpy as np
import threading

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

lenders_f=open("processed_datas/lenders.txt","r")
lenders_l=lenders_f.readline().split(",")

lenders_f.close()
'''
#分别列出borrower和lender的名单
borrowers_l=list(set(np.array(merge_bid_data["borrowerkey"]).tolist()))
f=open("processed_datas/borrowers.txt",'w')
f.write(borrowers_l[0])
for b in borrowers_l[1:]:
    f.write(","+b)
f.close()
print len(borrowers_l)

lenders_l=list(set(np.array(merge_bid_data["lenderkey"]).tolist()))
f=open("processed_datas/lenders.txt",'w')
f.write(lenders_l[0])
for l in lenders_l[1:]:
    f.write(","+l)
f.close()
print len(lenders_l)
'''
#列出借贷者之间投标次数（成功、全部）、listing个数、投资金额（成功）和投资占比（横向）
borrowers_to_lenders_df=pd.DataFrame(columns=["borrowerkey","lenderkey","success_bid_time",\
                                              "all_bid_time","listing_time","win_listing_time","withdraw_bid_time","success_bid_amount",\
                                              "success_bid_percent_b","B_funded_listing_num","B_loan_num","B_loan_paid","B_loan_notpaid"])
b_l_dic={}

def b_l_1(borrower,lenders_l,borrowers_to_lenders_df,b_l_dic):
    print "b"+borrower
    b_l_dic["borrowerkey"] = borrower
    b_l_b_data = merge_bid_data[merge_bid_data["borrowerkey"] == borrower]
    b_l_dic["B_funded_listing_num"] = b_l_b_data["listingkey"].drop_duplicates().shape[0]
    b_l_b_loan_data=b_l_b_data.loc[:,["loankey","loanstatus"]]
    b_l_b_loan_data=b_l_b_loan_data.drop_duplicates()
    b_l_dic["B_loan_num"]=b_l_b_loan_data.shape[0]
    b_l_dic["B_loan_paid"]=b_l_b_loan_data[b_l_b_loan_data["loanstatus"]=="Paid"].shape[0]
    b_l_dic["B_loan_notpaid"]=b_l_b_loan_data[(b_l_b_loan_data["loanstatus"]=="Defaulted (Bankruptcy)")|(b_l_b_loan_data["loanstatus"]=="Defaulted (Delinquency)")| \
        (b_l_b_loan_data["loanstatus"] == "Defaulted (PaidInFull)")|(b_l_b_loan_data["loanstatus"]=="Defaulted (SettledInFull)")].shape[0]
    borrower_bid_amount = b_l_b_data[b_l_b_data["bidstatus"] == "Winning"].loc[:, "participationamount"].sum()
    for lender in lenders_l:
        b_l_dic["lenderkey"] = lender
        b_l_data = b_l_b_data[b_l_b_data["lenderkey"] == lender]
        if b_l_data.shape[0] != 0:

            b_l_list_data=b_l_data.loc[:,["listingkey","bidstatus"]]
            b_l_list_data=b_l_list_data.drop_duplicates()
            b_l_dic["listing_time"]=b_l_list_data.shape[0]
            b_l_dic["win_listing_time"] = b_l_list_data[b_l_list_data["bidstatus"] == "Winning"].shape[0]
            b_l_dic["success_bid_time"] = b_l_data[b_l_data["bidstatus"] == "Winning"].shape[0]
            b_l_dic["withdraw_bid_time"] = b_l_data[b_l_data["bidstatus"] == "Bid Withdrawn"].shape[0]
            b_l_dic["all_bid_time"] = b_l_data[b_l_data["bidstatus"] != "Bid Withdrawn"].shape[0]
            b_l_dic["success_bid_amount"] = b_l_data[b_l_data["bidstatus"] == "Winning"].loc[:,
                                            "participationamount"].sum()
            b_l_dic["success_bid_percent_b"] = float(b_l_dic["success_bid_amount"] / borrower_bid_amount)
            borrowers_to_lenders_df = borrowers_to_lenders_df.append(b_l_dic, ignore_index=True)

# m=0
# for borrower in borrowers_l:
#     print "b"+str(m)
#     m+=1
#     b_l_dic["borrowerkey"]=borrower
#     b_l_b_data=merge_bid_data[merge_bid_data["borrowerkey"] == borrower]
#     borrower_bid_amount=b_l_b_data[b_l_b_data["bidstatus"]=="Winning"].loc[:,"participationamount"].sum()
#     for lender in lenders_l:
#         b_l_dic["lenderkey"]=lender
#         b_l_data=b_l_b_data[b_l_b_data["lenderkey"]==lender]
#         if b_l_data.shape[0]!=0:
#             b_l_dic["success_bid_time"]=b_l_data[b_l_data["bidstatus"]=="Winning"].shape[0]
#             b_l_dic["withdraw_bid_time"] = b_l_data[b_l_data["bidstatus"] == "Bid Withdrawn"].shape[0]
#             b_l_dic["all_bid_time"]=b_l_data[b_l_data["bidstatus"]!="Bid Withdrawn"].shape[0]
#             b_l_dic["success_bid_amount"]=b_l_data[b_l_data["bidstatus"]=="Winning"].loc[:,"participationamount"].sum()
#             b_l_dic["success_bid_percent_b"]=float(b_l_dic["success_bid_amount"]/borrower_bid_amount)
#             borrowers_to_lenders_df=borrowers_to_lenders_df.append(b_l_dic,ignore_index=True)
# print borrowers_to_lenders_df.head(1)


#计算投资占比（纵向）

def b_l_2(lender,borrowers_l,borrowers_to_lenders_df):
    print "l"+lender
    b_l_l_data = merge_bid_data[merge_bid_data["lenderkey"] == lender]
    b_l_l_list_data = b_l_l_data.loc[:,["listingkey", "bidstatus"]]
    b_l_l_list_data = b_l_l_list_data.drop_duplicates()
    bid_listing_num = b_l_l_list_data.shape[0]
    bid_win_listing_num = b_l_l_list_data[b_l_l_list_data["bidstatus"] == "Winning"].shape[0]
    lender_bid_amount = b_l_l_data[b_l_l_data["bidstatus"] == "Winning"].loc[:, "participationamount"].sum()
    for borrower in borrowers_l:
        if borrowers_to_lenders_df[(borrowers_to_lenders_df["lenderkey"] == lender) & (
                borrowers_to_lenders_df["borrowerkey"] == borrower)].shape[0] != 0:
            b_l_index = borrowers_to_lenders_df[(borrowers_to_lenders_df["lenderkey"] == lender) & (
                    borrowers_to_lenders_df["borrowerkey"] == borrower)].index.tolist()
            borrowers_to_lenders_df["success_bid_percent_l"][b_l_index[0]] = float(borrowers_to_lenders_df[(borrowers_to_lenders_df["lenderkey"]==lender) & (borrowers_to_lenders_df["borrowerkey"]==borrower)]["success_bid_amount"].iloc[0]/lender_bid_amount)
            borrowers_to_lenders_df["L_bid_listing_num"][b_l_index[0]] = bid_listing_num
            borrowers_to_lenders_df["L_bid_win_listing_num"][b_l_index[0]] = bid_win_listing_num


            #
#
# borrowers_to_lenders_df["success_bid_percent_l"]=0.00
#
# n=0
# for lender in lenders_l:
#     print 'l'+str(n)
#     n+=1
#     b_l_l_data=merge_bid_data[merge_bid_data["lenderkey"] ==lender]
#     lender_bid_amount=b_l_l_data[b_l_l_data["bidstatus"]=="Winning"].loc[:,"participationamount"].sum()
#     for borrower in borrowers_l:
#        if borrowers_to_lenders_df[(borrowers_to_lenders_df["lenderkey"]==lender) & (borrowers_to_lenders_df["borrowerkey"]==borrower)].shape[0]!=0:
#            b_l_index=borrowers_to_lenders_df[(borrowers_to_lenders_df["lenderkey"]==lender) & (borrowers_to_lenders_df["borrowerkey"]==borrower)].index.tolist()
#            borrowers_to_lenders_df["success_bid_percent_l"][b_l_index[0]]= float(borrowers_to_lenders_df[(borrowers_to_lenders_df["lenderkey"]==lender) & (borrowers_to_lenders_df["borrowerkey"]==borrower)]["success_bid_amount"].iloc[0]/lender_bid_amount)
# print borrowers_to_lenders_df.head(1)



threads_1=[]
for borrower in borrowers_l[:3000]:
    t=threading.Thread(target=b_l_1,args=(borrower,lenders_l,borrowers_to_lenders_df,b_l_dic))
    threads_1.append(t)

# threads_2=[]
# for lender in lenders_l:
#     t=threading.Thread(target=b_l_2,args=(lender,borrowers_l,borrowers_to_lenders_df))

for t in threads_1:
    t.setDaemon(False)
    t.start()
print "thread1 is over"
pd.DataFrame.to_csv(borrowers_to_lenders_df,path_or_buf="processed_datas/borrowers_to_lenders1.csv",index=False)
#
# borrowers_to_lenders_df["success_bid_percent_l"] = 0.00
# borrowers_to_lenders_df["L_bid_listing_num"] = 0
# borrowers_to_lenders_df["L_bid_win_listing_num"] = 0
# for t in threads_2:
#     t.setDaemon(False)
#     t.start()
# print "thread2 is over"
# pd.DataFrame.to_csv(borrowers_to_lenders_df,path_or_buf="processed_datas/borrowers_to_lenders.csv",index=False)
