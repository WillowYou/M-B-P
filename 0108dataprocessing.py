#-*-coding:utf8-*-
from utility import *
import pandas as pd

#链接数据库，提取bids、listings、loans三个表中初步所需数据，之后另有需要可继续添加
ms = MYSQL(host="localhost", user="root", pwd="960513", db="prosper")

#提取bids表中数据
bids_log = ms.ExecQuery("select bidkey, listingkey, listingstatus, memberkey,"
                        "minimumrate, minimumyield, participationamount,"
                        " bidstatus from bids" )

bids=pd.DataFrame(list(bids_log) ,columns=['bidkey', 'listingkey', 'listingstatus', 'memberkey', \
                                           'minimumrate', 'minimumyield', 'participationamount', 'bidstatus'])
print 1
pd.DataFrame.to_csv(bids,path_or_buf="processed_datas/bids.csv",index=False)


#提取listings表中数据
listings_log = ms.ExecQuery("select amountfunded, amountrequested, bidcount, listingkey, "
                            "memberkey, percentfunded, listingstatus from listings" )
print 2
listings=pd.DataFrame(list(listings_log),columns=['amountfunded', 'amountrequested', 'bidcount', 'listingkey',\
                            'memberkey', 'percentfunded', 'listingstatus'])
pd.DataFrame.to_csv(listings,path_or_buf="processed_datas/listings.csv",index=False)

#提取loans表中数据
loans_log = ms.ExecQuery("select amountborrowed, loankey, listingkey, loanstatus,"
                         "loanterm, ageinmonths from loans" )
print 3
loans=pd.DataFrame(list(loans_log),columns=['amountborrowed', 'loankey', 'listingkey', 'loanstatus',\
                         'loanterm', 'ageinmonths'])
pd.DataFrame.to_csv(loans,path_or_buf="processed_datas/loans.csv",index=False)

bids["lenderkey"]=bids["memberkey"]
print bids.head(1)
del bids["memberkey"]
listings["borrowerkey"]=listings["memberkey"]
print listings.head(1)
del listings["memberkey"]
merge_data=pd.merge(bids,listings,on="listingkey")
merge_data=pd.merge(merge_data,loans,on="listingkey")
print merge_data.head(1)
pd.DataFrame.to_csv(merge_data,path_or_buf="processed_datas/merge_data.csv",index=False)


