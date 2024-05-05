import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import json
import requests
from PIL import Image


#dataframe creation

#SQl connection

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data",
                      password="sunitham")

cursor=mydb.cursor()

#aggregated_insurance_df

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

aggregated_insurance=pd.DataFrame(table1,columns=("States","year","Quarter","Transaction_type","Transaction_count","Transaction_amount"))


#aggregated_transaction_df

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()

aggregated_transaction=pd.DataFrame(table2,columns=("States","year","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggregated_user_df

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()

aggregated_user=pd.DataFrame(table3,columns=("States","year","Quarter","Brands","Transaction_count","Percentage"))

#map_insurance_df

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

map_insurance=pd.DataFrame(table4,columns=("States","year","Quarter","Districts","Transaction_count","Transaction_amount"))


#map_transaction_df

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

map_transaction=pd.DataFrame(table5,columns=("States","year","Quarter","Districts","Transaction_count","Transaction_amount"))

#map_user_df

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

map_user=pd.DataFrame(table6,columns=("States","year","Quarter","Districts","RegisteredUsers","AppOpens"))

#top_insurance_df

cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()


top_insurance=pd.DataFrame(table7,columns=("States","year","Quarter","Pincodes","Transaction_count","Transaction_amount"))

#top_transaction_df

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

top_transaction=pd.DataFrame(table8,columns=("States","year","Quarter","Pincodes","Transaction_count","Transaction_amount"))

#top_user_df

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

top_user=pd.DataFrame(table9,columns=("States","year","Quarter","Pincodes","RegisteredUsers"))


#transaction_amount_count_Year

def transaction_amount_count(df,year):
    TACY=df[df["year"]==year]

    TACY.reset_index(drop=True,inplace=True)

    TACYg_states=TACY.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    TACYg_states.reset_index(inplace=True) 
    
    col1,col2=st.columns(2)
    with col1:
        
        fig_amount=px.bar(TACYg_states,x="States",y="Transaction_amount",title=f"{year} transaction amount Vs states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)
        
    with col2:
            
        fig_count=px.bar(TACYg_states,x="States",y="Transaction_count",title=f"{year} transaction count Vs states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_count)
        
        
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
        
    states_name .sort() 
      
    col1,col2=st.columns(2)
    
    with col1:
        

        fig_india_1=px.choropleth(TACYg_states,geojson=data1,locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(TACYg_states["Transaction_amount"].min(),TACYg_states["Transaction_amount"].max()),
                                hover_name="States",title=f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                height=600,width=600)
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
        
    with col2:
            
    
        fig_india_2=px.choropleth(TACYg_states,geojson=data1,locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(TACYg_states["Transaction_count"].min(),TACYg_states["Transaction_count"].max()),
                                hover_name="States",title=f"{year} TRANSACTION COUNT", fitbounds="locations",
                                height=600,width=600)

        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    return TACY
   
#transaction_amount_count__year_quarter
        
def transaction_amount_count_Y_Q(df,quarter):
    TACY=df[df["Quarter"]==quarter]

    TACY.reset_index(drop=True,inplace=True)

    TACYg=TACY.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    TACYg.reset_index(inplace=True) 
    
    col1,col2=st.columns(2)
    
    with col1:
        
    
        fig_amount=px.bar(TACYg,x="States",y="Transaction_amount",title=f"{TACY['year'].min()} YEAR {quarter} QUARTER transaction amount Vs states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)
        
    with col2:
            

        fig_count=px.bar(TACYg,x="States",y="Transaction_count",title=f"{TACY['year'].min()} YEAR {quarter} QUARTER transaction count Vs states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_count)
    
    col1,col2=st.columns(2)
    
    with col1:
        
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name .sort()   

        fig_india_1=px.choropleth(TACYg,geojson=data1,locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(TACYg["Transaction_amount"].min(),TACYg["Transaction_amount"].max()),
                                hover_name="States",title=f"{TACY['year'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds="locations",
                                height=600,width=600)
        
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
        
    with col2:    
        
        fig_india_2=px.choropleth(TACYg,geojson=data1,locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(TACYg["Transaction_count"].min(),TACYg["Transaction_count"].max()),
                                hover_name="States",title=f"{TACY['year'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds="locations",
                                height=600,width=600)

        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)  
    return TACY      
 
#Aggre_Tran_Transaction_type       
        
def Aggre_Tran_Transaction_type(df,state):

    TACY=df[df["States"]==state]

    TACY.reset_index(drop=True,inplace=True)

    TACYg=TACY.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    TACYg.reset_index(inplace=True) 
    
    col1,col2=st.columns(2)
    
    with col1:
        
        fig_pi_1=px.pie(data_frame=TACYg,names="Transaction_type",values="Transaction_amount",width=600,title=f"{state.upper()} :TRANSACTION AMOUNT",hole=0.5)
        st.plotly_chart(fig_pi_1)
        
    with col2:    

        fig_pi_2=px.pie(data_frame=TACYg,names="Transaction_type",values="Transaction_count",width=600,title=f"{state.upper()}: TRANSACTION COUNT",hole=0.5)
        st.plotly_chart(fig_pi_2)
       
               
#aggre user analysis_1

def Aggre_user_plot_1(df,year):
    aguy=df[df['year']==year]
    aguy.reset_index(drop=True,inplace=True)
    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg,x="Brands",y="Transaction_count",title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline,hover_name="Brands")

    st.plotly_chart(fig_bar_1)
    return aguy         
        
      
#aggregated user analysis_2 

def Aggre_user_plot_2(df,quarter):
    
    aguyq=df[df['Quarter']==quarter]
    aguyq.reset_index(drop=True,inplace=True)
    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)
    fig_bar_1=px.bar(aguyqg,x="Brands",y="Transaction_count",title=f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                        width=1000,color_discrete_sequence=px.colors.sequential.Magenta_r,hover_name="Brands")

    st.plotly_chart(fig_bar_1)
    return aguyq

#aggregated user analysis_3

def Agre_user_plot_3(df,state):
    auyqs=df[df["States"]==state]
    auyqs.reset_index(drop=True,inplace=True) 

    fig_line_1=px.line(auyqs,x="Brands",y="Transaction_count",hover_data="Percentage",
                    title=f"{state.upper()}: BRANDS,TANSACTION COUNT,PERCENTAGE",width=1000,markers=True)
    st.plotly_chart(fig_line_1) 
    

#map insurance district

def Map_insur_District(df,state):

    TACY=df[df["States"]==state]

    TACY.reset_index(drop=True,inplace=True)

    TACYg=TACY.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    TACYg.reset_index(inplace=True) 
    col1,col2=st.columns(2)
    with col1:
        
        fig_bar_1=px.bar(TACYg,x="Transaction_amount",y="Districts",height=600,title=f"{state.upper()}:  DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart (fig_bar_1)
        
    with col2:

        fig_bar_2=px.bar(TACYg,x="Transaction_count",y="Districts",height=600, title=f"{state.upper()}:  DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.matter)
        st.plotly_chart(fig_bar_2)
        
        
#map use plot_1

def map_user_plot_1(df,year):
    muy=df[df['year']==year]
    muy.reset_index(drop=True,inplace=True)

    muyg=muy.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyg.reset_index(inplace=True)
    fig_line_1=px.line(muyg,x="States",y=["RegisteredUsers", "AppOpens"],
                    title=f"{year}: REGISTERED USER , APPOPENS",width=1000,height=800, markers=True)
    st.plotly_chart(fig_line_1)
    return muy   

#map use plot_2

def map_user_plot_2(df,quarter):
    muyq=df[df['Quarter']==quarter]
    muyq.reset_index(drop=True,inplace=True)

    muyqg=muyq.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyqg.reset_index(inplace=True)
    fig_line_1=px.line(muyqg,x="States",y=["RegisteredUsers", "AppOpens"],
                    title=f"{df['year'].min()}  YEAR {quarter}: QUARTER REGISTERED USER , APPOPENS",width=1000,height=800, markers=True,
                    color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)
    return muyq     


#map user plot_3

def map_user_plot_3(df,states):
    muyqs=df[df['States']==states]
    muyqs.reset_index(drop=True,inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
    
        fig_map_user_bar_1=px.bar(muyqs,x="RegisteredUsers",y="Districts",title=f"{states.upper()}: REGISTERED USER",height=800,
                                color_discrete_sequence=px.colors.sequential.Aggrnyl)

        st.plotly_chart(fig_map_user_bar_1)
        
    with col2:    

        fig_map_user_bar_2=px.bar(muyqs,x="AppOpens",y="Districts",title=f"{states.upper()}: APPOPENS",height=800,
                                color_discrete_sequence=px.colors.sequential.Aggrnyl_r)

        st.plotly_chart(fig_map_user_bar_2)
        
        
#top insuarnce plot_1

def top_insurance_plot_1(df,state):
    tiy=df[df['States']==state]
    tiy.reset_index(drop=True,inplace=True)
    tiyg=tiy.groupby("Pincodes")[["Transaction_count","Transaction_amount"]].sum()
    tiyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_top_user_bar_1=px.bar(tiy,x="Quarter",y="Transaction_amount",hover_data="Pincodes",height=650,width=600, title="TRANSACTION AMOUNT",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl)

        st.plotly_chart(fig_top_user_bar_1)  
    with col2:
        
    
        fig_top_user_bar_2=px.bar(tiy,x="Quarter",y="Transaction_count",hover_data="Pincodes",height=650,width=600, title="TRANSACTION COUNT",
                                color_discrete_sequence=px.colors.sequential.Agsunset_r)

        st.plotly_chart(fig_top_user_bar_2)     

#top_user_plot_1

def top_user_plot_1(df,year):
    tuy=df[df['year']==year]
    tuy.reset_index(drop=True,inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)
    
    fig_top_plot_1=px.bar(tuyg,x="States",y="RegisteredUsers",color="Quarter",width=900,height=800,
                        color_discrete_sequence=px.colors.cmocean,hover_name="States",
                        title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)
    return tuy


#top user plot 2

def top_user_plot_2(df,state):
    
    tuys=df[df['States']==state]
    tuys.reset_index(drop=True,inplace=True)

    fig_top_plot_2=px.bar(tuys,x="Quarter",y="RegisteredUsers",title="REGISTERED USERS",
                                height=800,width=600,color="RegisteredUsers",hover_data="Pincodes",
                                color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)
    
# top_chart_transaction_amount     
    
def top_chart_transaction_amount(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="sunitham")

    cursor=mydb.cursor()
    #plot 1
    query1=f'''SELECT states,sum(transaction_amount) as transaction_amount
                FROM {table_name}
                GROUP BY states
                order by transaction_amount DESC
                LIMIT 10;'''
                
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()
    df_1=pd.DataFrame(table_1,columns=("States","Transaction_amount"))
    
    col1,col2=st.columns(2)
    
    with col1:
        
        fig_amount_1=px.bar(df_1,x="States",y="Transaction_amount",hover_name="States",title="top 10 of transaction amount",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount_1)
    

    #plot 2
    query2=f'''SELECT states,sum(transaction_amount) as transaction_amount
                FROM {table_name}
                GROUP BY states
                order by transaction_amount 
                LIMIT 10;'''
                
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()
    df_2=pd.DataFrame(table_2,columns=("States","Transaction_amount"))
    
    with col2:
        
        fig_amount_2=px.bar(df_2,x="States",y="Transaction_amount",hover_name="States",title="last 10 of transaction amount",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_amount_2)

    #plot3
    query3=f'''SELECT states,AVG(transaction_amount) as transaction_amount
                FROM {table_name}
                GROUP BY states
                order by transaction_amount;'''
                
    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()
    df_3=pd.DataFrame(table_3,columns=("States","Transaction_amount"))
    

        
    fig_amount_3=px.bar(df_3,x="States",y="Transaction_amount", hover_name="States",title="average of transaction amount",
                color_discrete_sequence=px.colors.sequential.GnBu_r)
    st.plotly_chart(fig_amount_3) 




#top_chart_transaction_count

def top_chart_transaction_count(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="sunitham")

    cursor=mydb.cursor()
    #plot 4
    query4=f'''SELECT states,sum(transaction_count) as transaction_count
                FROM {table_name}
                GROUP BY states
                order by transaction_count DESC
                LIMIT 10;'''
                
    cursor.execute(query4)
    table_4=cursor.fetchall()
    mydb.commit()
    df_4=pd.DataFrame(table_4,columns=("States","Transaction_count"))
    
    col1,col2=st.columns(2)
    
    with col1:
        
        fig_count_4=px.bar(df_4,x="States",y="Transaction_count",hover_name="States",title="top 10 of transaction count",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_count_4)

    #plot 5
    query5=f'''SELECT states,sum(transaction_count) as transaction_count
                FROM {table_name}
                GROUP BY states
                order by transaction_count 
                LIMIT 10;'''
                
    cursor.execute(query5)
    table_5=cursor.fetchall()
    mydb.commit()
    df_5=pd.DataFrame(table_5,columns=("States","Transaction_count"))
    
    col1,col2=st.columns(2)
    
    with col2:
        
        fig_count_5=px.bar(df_5,x="States",y="Transaction_count",hover_name="States",title="last 10 of transaction count",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_count_5)

    #plot6
    query6=f'''SELECT states,AVG(transaction_count) as transaction_count
                FROM {table_name}
                GROUP BY states
                order by transaction_count;'''
                
    cursor.execute(query6)
    table_6=cursor.fetchall()
    mydb.commit()
    df_3=pd.DataFrame(table_6,columns=("States","Transaction_count"))
    fig_count_6=px.bar(df_3,x="States",y="Transaction_count", hover_name="States",title="average of transaction count",
                    color_discrete_sequence=px.colors.sequential.GnBu_r)
    st.plotly_chart(fig_count_6)
    
    


#streamlit 

st.set_page_config(layout="wide")

st.title("PHONEPE DATA VISUALISATION AND EXPLORATION")

with st.sidebar:
    select=option_menu("Main manu",["Home","Data exploration","Top charts"])

if select=="Home":
    
    col1,col2=st.columns(2)
    
    with col1:
        
        st.header("PhonePe")
        st.subheader("Digital Payments & Financial Services")
        st.markdown("Transaction App based on the Unified Payments Interface")
        st.write("***features***")
        st.write("****credit and debit card linking****")
        st.write("****Bank balance check****")
        st.write("****Money storage****")
        st.write("****PIN authourization****")
        st.write("****Easy transactions****")    
        st.write("****Supports all kind of payments****")
        
                
    with col2:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.image(Image.open(r"C:\Users\SUNITHA\OneDrive\Desktop\phone-pay-image1.jpg"),width=500)   
        
        
    col3,col4=st.columns(2)   
     
    with col3:
        st.video("https://www.youtube.com/watch?v=QG6iEwlnPoE")
        
            
    with col4: 
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****multiple payment modes****")
        st.write("****earn rewards****")
        st.write("****QR code****")
        
        st.download_button("DOWNLOAD the APP now", "https://www.phonepe.com/app-download/")
        
        
 
            

elif select=="Data exploration":
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top_Analysis"])

    with tab1:
        method=st.radio("select the method",["Insurance Analysis","Transaction Analysis","User Analysis"])

        if method=="Insurance Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                year=st.slider("select the year",aggregated_insurance["year"].min(),aggregated_insurance["year"].max(),aggregated_insurance["year"].min())
            tac_Y=transaction_amount_count(aggregated_insurance,year) 
            
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("select the quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            transaction_amount_count_Y_Q(tac_Y,quarters)    
        
        elif method=="Transaction Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                year=st.slider("select the year",aggregated_transaction["year"].min(),aggregated_transaction["year"].max(),aggregated_transaction["year"].min())
            Aggre_tran_tac_Y=transaction_amount_count(aggregated_transaction,year) 
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the states", Aggre_tran_tac_Y['States'].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)  
            
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("select the quarter",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quarters)   
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the states_ty", Aggre_tran_tac_Y['States'].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q,states) 
            
            

        elif method=="User Analysis":
            col1,col2=st.columns(2)
            with col1:
                year=st.slider("select the year",aggregated_user["year"].min(),aggregated_user["year"].max(),aggregated_user["year"].min())
            Aggre_user_Y=Aggre_user_plot_1(aggregated_user,year)
 

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("select the quarter",aggregated_user["Quarter"].min(),aggregated_user["Quarter"].max(),aggregated_user["Quarter"].min())
            #Aggre_user_Y=Aggre_user_plot_1(aggregated_user,year)
            Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y,quarters)   
            
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the states", Aggre_user_Y_Q['States'].unique())
            Agre_user_plot_3(Aggre_user_Y_Q,states)  
            
            
    with tab2:
        method2=st.radio("select the method",["Map Insurance","Map Transaction","Map User"])

        if method2=="Map Insurance":
            col1,col2=st.columns(2)
            with col1:
                year=st.slider("select the year_mi",map_insurance["year"].min(),map_insurance["year"].max(),map_insurance["year"].min())
            map_insur_tac_Y=transaction_amount_count(map_insurance,year) 
            col1,col2=st.columns(2)
            with col1: 
                states=st.selectbox("select the states_mi", map_insur_tac_Y['States'].unique())
            Map_insur_District(map_insur_tac_Y,states)  
            
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("select the quarter_mi",map_insur_tac_Y["Quarter"].min(),map_insur_tac_Y["Quarter"].max(),map_insur_tac_Y["Quarter"].min())
            map_insur_tac_Y_Q=transaction_amount_count_Y_Q(map_insur_tac_Y,quarters)   
        
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the states_ty", map_insur_tac_Y_Q['States'].unique())
            Map_insur_District(map_insur_tac_Y_Q,states) 
        
        elif method2=="Map Transaction":
            col1,col2=st.columns(2)
            with col1:
                year=st.slider("select the year_mi",map_transaction["year"].min(),map_transaction["year"].max(),map_transaction["year"].min())
            map_tran_tac_Y=transaction_amount_count(map_transaction,year) 
            col1,col2=st.columns(2)
            with col1: 
                states=st.selectbox("select the states_mi", map_tran_tac_Y['States'].unique())
            Map_insur_District(map_tran_tac_Y,states)  
            
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("select the quarter_mi",map_tran_tac_Y["Quarter"].min(),map_tran_tac_Y["Quarter"].max(),map_tran_tac_Y["Quarter"].min())
            map_tran_tac_Y_Q=transaction_amount_count_Y_Q(map_tran_tac_Y,quarters)   
        
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the states_ty", map_tran_tac_Y_Q['States'].unique())
            Map_insur_District(map_tran_tac_Y_Q,states) 
            
            
        elif method2=="Map User":
            col1,col2=st.columns(2)
            with col1:
                year=st.slider("select the year_mu",map_user["year"].min(),map_user["year"].max(),map_user["year"].min())
            map_user_Y=map_user_plot_1(map_user,year) 
            
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("select the quarter_mu",map_user_Y["Quarter"].min(),map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            map_user_Y_Q=map_user_plot_2(map_user_Y,quarters)   
            
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the states_mu", map_user_Y_Q['States'].unique())
            map_user_plot_3(map_user_Y_Q,states) 

    with tab3:

        method3=st.radio("select the method",["top Insurance","top Transaction","top User"])

        if method3=="top Insurance":
            col1,col2=st.columns(2)
            with col1:
                year=st.slider("select the year_ti",top_insurance["year"].min(),top_insurance["year"].max(),top_insurance["year"].min())
            top_insur_tac_Y=transaction_amount_count(top_insurance,year) 
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the states_ti", top_insur_tac_Y['States'].unique())
            top_insurance_plot_1(top_insur_tac_Y,states) 
            
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("select the quarter_ti",top_insur_tac_Y["Quarter"].min(),top_insur_tac_Y["Quarter"].max(),top_insur_tac_Y["Quarter"].min())
            top_insur_Y_Q=transaction_amount_count_Y_Q(top_insur_tac_Y,quarters)   
            
        elif method3=="top Transaction":
            col1,col2=st.columns(2)
            with col1:
                year=st.slider("select the year_tt",top_transaction["year"].min(),top_transaction["year"].max(),top_transaction["year"].min())
            top_tran_tac_Y=transaction_amount_count(top_transaction,year) 
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the states_tt", top_tran_tac_Y['States'].unique())
            top_insurance_plot_1(top_tran_tac_Y,states) 
            
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("select the quarter_tt",top_tran_tac_Y["Quarter"].min(),top_tran_tac_Y["Quarter"].max(),top_tran_tac_Y["Quarter"].min())
            top_insur_Y_Q=transaction_amount_count_Y_Q(top_tran_tac_Y,quarters)   
        
        elif method3=="top User":
            col1,col2=st.columns(2)
            with col1:
     
                year=st.slider("select the year_tu",top_user["year"].min(),top_user["year"].max(),top_user["year"].min())
            top_use_Y=top_user_plot_1(top_user,year) 
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the states_tt", top_use_Y['States'].unique())
            top_user_plot_2(top_use_Y,states)   
              

elif select=="Top charts": 
    
    
    question=st.selectbox("select the question",["1. Transaction amount and count of aggregated insurance",
                                                  "2. Transaction amount and count of map map_insurance",
                                                  "3. Transaction amount and count of top insurance",
                                                  "4. Transaction amount and count of aggregated transaction",
                                                  "5. Transaction amount and count of map transaction",
                                                  "6. Transaction amount and count of top transaction",
                                                  "7. transaction count of aggregated user"
                                                                 ])                                                                     
    
    
    
    if question=="1. Transaction amount and count of aggregated insurance":
        
        st.subheader("TRANSACTON AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")
        
    
    elif question=="2. Transaction amount and count of map map_insurance":
        
    
        st.subheader("TRANSACTON AMOUNT")
        top_chart_transaction_amount("map_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")    
        
        
    elif question=="3. Transaction amount and count of top insurance":
        
    
        st.subheader("TRANSACTON AMOUNT")
        top_chart_transaction_amount("top_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")  
        
        
    elif question=="4. Transaction amount and count of aggregated transaction":
        
    
        st.subheader("TRANSACTON AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction") 
        
        
    elif question=="5. Transaction amount and count of map transaction":
        
    
        st.subheader("TRANSACTON AMOUNT")
        top_chart_transaction_amount("map_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")     
        
        
    elif question=="6. Transaction amount and count of top transaction":
        
    
        st.subheader("TRANSACTON AMOUNT")
        top_chart_transaction_amount("top_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")       
        
        
    elif question=="7. transaction count of aggregated user":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")  
        
        
# end of the program PhonePe data analysis        
                                                  
         




        



    









