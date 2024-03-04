import pandas as pd
import streamlit as st
import shioaji as sj
from datetime import datetime

#accountDict={"edward":["6F8MBCti6FzZkc86uut5TLfSRAb1UiQjMREER1TKKmnw","8PA2ZJAzew3pFj2zpi3aUHYMvYZwjQEpXrb3a1GysPar"],
#            "edward_wife":["Gvd6pFwFncAHWZgg5jVNEFVBawS2EVEQPqrnwJQ7Jpeo","6nnNUWxuL66eCPR17MGxvgPB8djXPYjCsAENR1KgUycr"],
#            "ellis":["7U541GzLQqFfLrYrWsMczvKptPRLcRhEJHLGdhqXWE7x","4NB7zM7WGhYmbJeaZyaMGCq73LsNULraEz762bMook2B"],
#            "chun":["2oMvtudzAFkH1JeryThNNLYpGuGdG2QDuwuqrevdpXQz","48PtSPc9uJ3JzobmfqPwMsQxUGCuFzMApEJ3XjTpDWRf"],
#            "big":["3MKdCLdZoEq78zYbbRJziUSrzYdxYYGhqEDwGfbnAF3x","KUqwpdqqydh1BLAp4yo7dJdb9zciZzTRTuRok1KdwXd"]}


accountDict={"edward":["6F8MBCti6FzZkc86uut5TLfSRAb1UiQjMREER1TKKmnw","8PA2ZJAzew3pFj2zpi3aUHYMvYZwjQEpXrb3a1GysPar"],
            "edward_wife":["Gvd6pFwFncAHWZgg5jVNEFVBawS2EVEQPqrnwJQ7Jpeo","6nnNUWxuL66eCPR17MGxvgPB8djXPYjCsAENR1KgUycr"],
            "ellis":["7U541GzLQqFfLrYrWsMczvKptPRLcRhEJHLGdhqXWE7x","4NB7zM7WGhYmbJeaZyaMGCq73LsNULraEz762bMook2B"],
            "big":["3MKdCLdZoEq78zYbbRJziUSrzYdxYYGhqEDwGfbnAF3x","KUqwpdqqydh1BLAp4yo7dJdb9zciZzTRTuRok1KdwXd"]}


def query_last_profit():
    
    api = sj.Shioaji(simulation=False) #模擬模式

    nameList=[]
    commodityList=[]
    quantityList=[]
    pnlList=[]
    
    for key,value in accountDict.items():

        api.login(
            api_key=value[0], 
            secret_key=value[1])
        
        profitloss = api.list_profit_loss(api.futopt_account,"{0}-01-01".format(datetime.now().year),"{0}-12-31".format(datetime.now().year))
        
        for data in profitloss:
            
            if data.id==0:
            
                nameList.append(key)
                commodityList.append(data.code)
                quantityList.append(data.quantity)
                pnlList.append(data.pnl-data.tax-data.fee)
                break
            
            
        api.logout()
        
    df = pd.DataFrame(
        {
            "name": nameList,
            "commodity": commodityList,
            "quantity": quantityList,
            "pnl": pnlList,
            
        }
    )
    
    st.dataframe(
        df,
        column_config={
            "name": "Name",
            "commodity": "Commodity",
            "quantity": "Quantity",
            "pnl": "Last PNL",
        },
        hide_index=True,
    )
    
    #st.write("aabbcc")
    
    
def query_position():



    api = sj.Shioaji(simulation=False) #模擬模式

    nameList=[]
    commodityList=[]
    directionList=[]
    contractList=[]
    priceList=[]
    pnlList=[]
    
    for key,value in accountDict.items():

        api.login(
            api_key=value[0], 
            secret_key=value[1])
        
        #profitloss = api.list_profit_loss(api.futopt_account,'2023-12-01','2024-02-01')
        #print(key)
        #for data in profitloss:
        #    print(data)
        
        positions = api.list_positions(api.futopt_account)
        #print(key,len(positions))
        
        for data in positions:
        
            nameList.append(key)
            commodityList.append(data.code)
            directionList.append(data.direction.value)
            contractList.append(data.quantity)
            priceList.append(data.price)
            pnlList.append(data.pnl)
            
        api.logout()
        
    df = pd.DataFrame(
        {
            "name": nameList,
            "commodity": commodityList,
            "direction": directionList,
            "contract": contractList,
            "price": priceList,
            "pnl": pnlList,
            
        }
    )
    
    st.dataframe(
        df,
        column_config={
            "name": "Name",
            "commodity": "Commodity",
            "direction": "Direction",
            "contract": "Contract",
            "price": "Price",
            "pnl": "PNL",
        },
        hide_index=True,
    )


st.title('客戶期貨查詢')
st.button('Query Position', on_click=query_position)
st.button('Query Last Profit', on_click=query_last_profit)