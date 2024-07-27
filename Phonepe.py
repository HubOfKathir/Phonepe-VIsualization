import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import time

import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

#mysql connector to conect with python
mydb = mysql.connector.connect(host = 'localhost', user = 'root', password = '')
mycursor = mydb.cursor(buffered=True,)

#create an engine to insert data value
engine = create_engine("mysql+mysqlconnector://root:@localhost/phonepe")

#create database and use for table creataion
mycursor.execute('CREATE DATABASE IF NOT EXISTS phonepe')
mycursor.execute('USE phonepe')

#streamlit part

#set up page configuration for streamlit
icon='https://cdn.iconscout.com/icon/free/png-512/free-phonepe-2709167-2249157.png?f=webp&w=256'
st.set_page_config(page_title='PHONEPE PULSE',page_icon=icon,initial_sidebar_state='expanded',
                        layout='wide',menu_items={"about":'Developed by KATHIR'})

title_text = '''<h1 style='font-size:36px;text-align: center;'>
                 <span style='color: green;'>PHONEPE PULSE:</span> 
                 <span style='color: violet;'>India's Digital Revolution</span>
                 </h1>'''
st.markdown(title_text, unsafe_allow_html = True)

#setting up the homepage and optionmenu

select = option_menu('MANI MENU',
                     options=['ABOUT','HOME','GEO VISUALIZATION','INSIGHTS'],
                     icons= ["info-circle",'house','globe','lightbulb'],
                     orientation='horizontal',
                     styles={"container": {"width": "100%","border": "2.5px ridge #000000","background-color":"white"},
                            "icon": {"color": "#F8CD47", "font-size": "20px"}})

#option 'About'
if select == 'ABOUT':
        st.subheader(':violet[Project Title:]')
        st.markdown('''<h5>Phonepe Pulse Data Visualization and Exploration:
                                A User-Friendly Tool Using Streamlit and Plotly''',unsafe_allow_html=True)
        st.markdown('<h5>Github Cloning, Python, Pandas, MySQL,mysql-connector-python, Streamlit, and Plotly.',
                unsafe_allow_html=True)
        st.subheader(':violet[Overview:]')
        st.markdown('''
                <h5>Git: Employed Git for version control and efficient collaboration, enabling seamless cloning of the PhonePe dataset from GitHub.
                <h5>Pandas: Leveraged the powerful Pandas library to transform the dataset from JSON format into a structured dataframe.
                Pandas facilitated data manipulation, cleaning, and preprocessing, ensuring the data was ready for analysis.
                <h5>SQL Alchemy: Utilized SQL Alchemy to establish a connection to a SQL database, enabling seamless integration of the transformed dataset
                and the data was efficiently inserted into relevant tables for storage and retrieval.
                <h5>Streamlit: Developed an interactive web application using Streamlit, a user-friendly framework for data visualization and analysis.
                <h5>Plotly: Integrated Plotly, a versatile plotting library, to generate insightful visualizations from the dataset. Plotly's interactive plots,
                including geospatial plots and other data visualizations, provided users with a comprehensive understanding of the dataset's contents.''',
                unsafe_allow_html=True)

#option 'Home'
if select == 'HOME':
        col1, col2 = st.columns(2)
        with col1:
                st.subheader(':violet[what is phonepe]')
                st.markdown('''<h5>PhonePe is a popular digital payments platform in India, offering a range of financial services through its mobile app.
                        Users can make payments, transfer money, recharge phones, pay bills, invest, shop online, and more.
                        <h5>PhonePe has become a preferred choice for millions of users, contributing to India's digital payments revolution.<h5>''',unsafe_allow_html=True)
                
                st.subheader(':violet[what is Phonepe Pulse?]')
                st.markdown('''<h5>PhonePe Pulse provides real-time insights and trends on digital payments across India.
                Its offers comprehensive analytics including transaction volumes, consumer demographics, popular merchant categories,
                geographic trends, transaction values, payment methods, and seasonal fluctuations.<h5>''',unsafe_allow_html=True)
        with col2:
                st.markdown("![Alt Text](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2Vvb2oyaHBqNHZzdm9ycG5lcDEyczk3dDZtcnplamdpbGJudG8xNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/gSU4qpRY00OOe6v8I8/giphy-downsized-large.gif)")
        col1,col2 = st.columns(2)
        with col1:
                st.image('https://www.phonepe.com/pulsestatic/791/pulse/static/4cb2e7589c30e73dca3d569aea9ca280/1b2a8/pulse-2.webp',use_column_width=True)
        with col2:
                st.write(' ')
                st.subheader(':violet[Discover Insights:]')
                st.markdown('''
                        <h4>Transaction:<h5>Transaction insights involve analyzing customer transaction data to understand behavior and preferences.
                        By examining trends, categorizing transactions,and identifying patterns of india.
                        <h4>User: <h5>User insights refer to analyzing customer demographics, engagement metrics, and feedback.
                        By understanding demographics, tracking engagement of user in India''',unsafe_allow_html=True)
                
                st.link_button('Go to Phonepe Pulse','https://www.phonepe.com/pulse/')

#options 'GEO VIS'
if select == 'GEO VISUALIZATION':
        def ind_geo():
                geo = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson" 
                return geo
        
        geo_type = st.radio('Category Selection',["Transactions","Users"], index = None)
        st.write("You Selected:",f"<span style = 'color:#F8CD47'>{geo_type}</span>", unsafe_allow_html= True)

        if geo_type == "Transactions":
                trans_geo_year_wise = st.toggle('Year-Wise')
                if not trans_geo_year_wise:
                        cat = st.radio('Category Selection',["Transaction Amount","Transaction Count"], index = None)
                        st.write("You Selected",f"<span style = 'color:#F8CD47'>{cat}</span>",unsafe_allow_html=True)
                        if cat == "Transaction Amount":
                                st.title(":violet[Total Transaction Amount for States-Sum of all year]")

                                df = pd.read_sql_query('''SELECT States,SUM(TransactionAmount) as 'Total Transaction Amount',
                                        AVG(TransactionAmount) as 'Average Transaction Amount'
                                        from agg_phonpedata_trans
                                        GROUP by States''',con=engine)
                                
                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                                           locations='States',
                                                           hover_data=['Total Transaction Amount','Average Transaction Amount'],
                                                           color='Total Transaction Amount',
                                                           color_continuous_scale='Plasma', #Plasma,Cividis
                                                           mapbox_style= 'carto-darkmatter',zoom=3.5, #terrain,satellite
                                                           center={'lat':21.7679, 'lon':78.8718})
                                fig.update_geos(fitbounds = 'locations', visible = False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height = 600)
                                st.plotly_chart(fig,use_container_width=True)
                        
                        if cat == "Transaction Count":
                                st.title(":violet[Total Transaction Count for States-Sum of all year]")

                                df = pd.read_sql_query('''SELECT States,SUM(TransactionCount) as 'Total Transaction Count',
                                        AVG(TransactionCount) as 'Average Transaction Count'
                                        from agg_phonpedata_trans
                                        GROUP by States''',con=engine)
                                
                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                                           locations='States',
                                                           hover_data=['Total Transaction Count','Average Transaction Count'],
                                                           color='Total Transaction Count',
                                                           color_continuous_scale='Plasma', #Plasma,Cividis
                                                           mapbox_style= 'carto-darkmatter',zoom=3.5, #terrain,satellite
                                                           center={'lat':21.7679, 'lon':78.8718})
                                fig.update_geos(fitbounds = 'locations', visible = False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height = 600)
                                st.plotly_chart(fig,use_container_width=True)
                
                if trans_geo_year_wise:
                        
                        df_year = pd.read_sql_query('''SELECT DISTINCT Years as 'Year' FROM agg_phonpedata_trans''',
                                                    con = engine)
                        selected_year = st.select_slider("Select Year", options=df_year['Year'].tolist())
                        trans_geo_quater_wise = st.toggle('Quarter-Wise')  

                        if not trans_geo_quater_wise:

                                df = pd.read_sql_query('''SELECT States,SUM(TransactionAmount) as 'Total Transaction Amount',
                                                AVG(TransactionAmount) as 'Average Transaction Amount',
                                                SUM(TransactionCount) as 'Total Transaction Count',
                                                AVG(TransactionCount) as 'Average Transaction Count'
                                                FROM agg_phonpedata_trans WHERE Years=%s
                                                GROUP by States''',con=engine,params=[(selected_year,)])  
                                
                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                        locations='States',
                                        hover_data=['Total Transaction Amount','Average Transaction Amount','Total Transaction Count','Average Transaction Count'],
                                        color='Total Transaction Amount',
                                        color_continuous_scale=px.colors.sequential.Plasma,
                                        mapbox_style="carto-positron",zoom=3.5,
                                        center={"lat": 21.7679, "lon": 78.8718},)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.subheader(f":violet[Total Transaction Amount and Count for States - {selected_year}]")
                                st.plotly_chart(fig,use_container_width = True)
                        
                        if trans_geo_quater_wise:
                                df_quater = pd.read_sql_query('''SELECT DISTINCT Quarter as 'Quarter' FROM agg_phonpedata_trans
                                                              ''',con = engine)
                                selected_quater = st.select_slider("Select Quater",options=df_quater['Quarter'].tolist())

                                df = pd.read_sql_query('''SELECT States,SUM(TransactionAmount) AS 'Total Transaction Amount',
                                                AVG(TransactionAmount) as 'Average Transaction Amount',
                                                SUM(TransactionCount) as 'Total Transaction Count',
                                                AVG(TransactionCount) as 'Average Transaction Count'
                                                FROM agg_phonpedata_trans WHERE Years=%s AND Quarter=%s
                                                GROUP BY States''',con=engine,params=(selected_year, selected_quater))
                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                        locations='States',
                                        hover_data=['Total Transaction Amount','Average Transaction Amount','Total Transaction Count','Average Transaction Count'],
                                        color='Total Transaction Amount',
                                        color_continuous_scale=px.colors.sequential.Viridis_r,
                                        mapbox_style="carto-positron",zoom=3.5,
                                        center={"lat": 21.7679, "lon": 78.8718},)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.subheader(f":violet[Total Transaction Amount and Count for States in {selected_year}-Q{selected_quater}]")
                                st.plotly_chart(fig,use_container_width = True)

        if geo_type == "Users":
                user_geo_year_wise = st.toggle('Year-Wise')

                if not user_geo_year_wise:
                        st.title(':violet[Total Register Users Across States and Sum of all Year]')

                        df = pd.read_sql_query('''SELECT DISTINCT States,SUM(registeredUsers) as 'Total registered users',
                                                       AVG(registeredUsers) as 'Average Registered Users'
                                                       FROM map_user
                                                       GROUP BY States''',con=engine)
                        fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                        locations='States',
                                        hover_data=['Total registered users','Average Registered Users'],
                                        color='Total registered users',
                                        color_continuous_scale='Viridis',
                                        mapbox_style="carto-positron",zoom=3.5,
                                        center={"lat": 21.7679, "lon": 78.8718},)

                        fig.update_geos(fitbounds="locations", visible=False)
                        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                        fig.update_layout(height=600)
                        st.plotly_chart(fig,use_container_width = True)
                
                if user_geo_year_wise:
                        df_year=pd.read_sql_query('''SELECT DISTINCT Years as 'Year' FROM map_user''',con=engine)
                        selected_year = st.select_slider("Select Year",options=df_year['Year'].tolist())
                        user_geo_quater_wise= st.toggle('Quater-Wise')
                         
                        if not user_geo_quater_wise:
                                df_year = pd.read_sql_query('''SELECT DISTINCT States, SUM(registeredUsers) as 'Total registered users',
                                                        AVG(registeredUsers) as 'Average Registered Users'
                                                        FROM map_user WHERE Years = %s
                                                        GROUP BY States''',con = engine,params=[(selected_year,)])
                                
                                fig = px.choropleth_mapbox(df_year,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                                        locations='States',
                                                        hover_data=['Total registered users','Average Registered Users'],
                                                        color = 'Total registered users',
                                                        color_continuous_scale=px.colors.sequential.Plasma,
                                                        mapbox_style='carto-positron',zoom=3.5,
                                                        center = {'lat':21.7679,'lon':78.8718},)
                                
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.subheader(f":violet[Total Registered User for States in {selected_year}]")
                                st.plotly_chart(fig,use_container_width = True)
                        
                        if user_geo_quater_wise:
                                df_quater=pd.read_sql_query('''SELECT DISTINCT Quarter as 'Quarter' from map_user''',con=engine)
                                selected_Quater = st.select_slider("Select Quater",options=df_quater['Quarter'].tolist())

                                df = pd.read_sql_query('''SELECT DISTINCT States, SUM(registeredUsers) as 'Total registered users',
                                                       AVG(registeredUsers) as 'Average Registered Users'
                                                FROM map_user WHERE Years=%s and Quarter=%s
                                                GROUP BY States''',con=engine,params=(selected_year,selected_Quater))
                                
                                fig = px.choropleth_mapbox(df,geojson=ind_geo(),featureidkey='properties.ST_NM',
                                                locations='States',
                                                hover_data=['Total registered users','Average Registered Users'],
                                                color='Total registered users',
                                                color_continuous_scale=px.colors.sequential.matter_r,
                                                mapbox_style="carto-positron",zoom=3.5,
                                                center={"lat": 21.7679, "lon": 78.8718},)
                                fig.update_geos(fitbounds="locations", visible=False)
                                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                                fig.update_layout(height=600)
                                st.subheader(f":violet[Total Registered User for States in {selected_year}-Q{selected_Quater} ]")
                                st.plotly_chart(fig,use_container_width = True)

#option 'INSIGHTS":
if select =="INSIGHTS":
        select_insight=option_menu('',options=["TOP INSIGHTS","FILTER INSIGHTS"],
                                icons=["bar-chart", "toggles"],
                                orientation='horizontal',
                                styles={'container':{'border':'2px ridge #00000'},
                                        'icon':{'color':'#F8CD47','font-size': '20px'}})
        
        if select_insight == 'TOP INSIGHTS':
                question = [  'Top 10 states with highest transaction',
                        'Top 10 states with lowest transaction',
                        'Top 10 states with highest Registered User',
                        'Top 10 District with highest transaction',
                        'Top 10 District with lowest transaction',
                        'Top 10 District with highest Registered User',
                        'Top 10 Brands used for Transaction',
                        'Sum of Transaction by Type or categories',
                        'Top 10 Postal code with highest Transaction',
                        'Top 10 Postal code with highest Registered user'
                        ]
                query = st.selectbox(':red[Random Querries Down]', options=question, index= None)

              


                if query == 'Top 10 states with highest transaction':
                        col1,col2 = st.columns(2)
                        with col1:
                                df = pd.read_sql_query('''SELECT States, SUM(TransactionAmount) as 'Transaction Amount'
                                                       FROM agg_phonpedata_trans
                                                       GROUP BY States
                                                       ORDER BY SUM(TransactionAmount) DESC LIMIT 10;''',con = engine)                                          
                                fig = px.bar(df,x='States',y='Transaction Amount',
                                             color = 'States',
                                             hover_data= ['Transaction Amount'],
                                             title='Top 10 states with highest transaction amount',
                                             color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        with col2:
                                df=pd.read_sql_query('''SELECT States, SUM(TransactionCount) AS 'Transaction Count' FROM agg_phonpedata_trans
                                                WHERE States IN ( SELECT States FROM 
                                                (SELECT States, SUM(TransactionAmount) AS amount FROM agg_phonpedata_trans 
                                                GROUP BY States ORDER BY amount DESC LIMIT 10 )as top_state )
                                                GROUP BY States ORDER by sum(TransactionCount) DESC''',con=engine)
                                fig = px.bar(df,x='States',y='Transaction Count',
                                             color = 'States',
                                             hover_data= ['Transaction Count'],
                                             title='Top 10 states with highest transaction count',
                                             color_discrete_sequence=px.colors.qualitative.Vivid_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                if query=='Top 10 states with lowest transaction':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT States,sum(TransactionAmount) as 'Transaction Amount'
                                        from agg_phonpedata_trans GROUP by States
                                        ORDER BY SUM(TransactionAmount) ASC LIMIT 10''',con=engine)
                                df['States']=df['States'].str.replace('Dadra and Nagar Haveli and Daman and Diu','Dadra')

                                fig=px.bar(df,x='States',y='Transaction Amount',
                                                color='States',
                                                hover_data=['Transaction Amount'],
                                                title='Top 10 states of lowest Transaction Amount',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        with col2:        
                                df=pd.read_sql_query('''SELECT States, SUM(TransactionCount) AS 'Transaction Count' FROM agg_phonpedata_trans
                                                WHERE States IN ( SELECT States FROM 
                                                (SELECT States, SUM(TransactionAmount) AS amount FROM agg_phonpedata_trans 
                                                GROUP BY States ORDER BY amount ASC LIMIT 10 )as top_state )
                                                GROUP BY States order by sum(TransactionCount) ASC''',con=engine)
                                df['States']=df['States'].str.replace('Dadra and Nagar Haveli and Daman and Diu','Dadra')
                
                                fig=px.bar(df,x='States',y='Transaction Count',
                                                color='Transaction Count',
                                                hover_data=['Transaction Count'],
                                                title='Top 10 states of lowest Transaction Count',
                                                color_continuous_scale=px.colors.carto.Emrld_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)   

                if query == 'Top 10 states with highest Registered User':
                        col1,col2 = st.columns(2)
                        with col1:
                                df = pd.read_sql_query('''SELECT States, SUM(registeredUsers) AS 'Registered Users'
                                                FROM map_user GROUP BY States ORDER BY SUM(registeredUsers)
                                                DESC limit 10''', con = engine)
                                
                                fig = px.bar(df,x = 'States',y='Registered Users',
                                        color='States',
                                                        hover_data=['Registered Users'],
                                                        title='Top 10 state of highest Registered User',
                                                        color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True) 
                        
                        with col2:
                                df = pd.read_sql_query('''SELECT States, SUM(appOpens) AS 'App_Opened' FROM map_user
                                                       WHERE States IN(SELECT States FROM(SELECT States, SUM(registeredUsers) as RGTD_Users 
                                                       FROM map_user GROUP BY States ORDER BY SUM(registeredUsers) DESC LIMIT 10) as top_user)
                                                       GROUP BY States ORDER BY SUM(appOpens) DESC''',con = engine
                                                       )
                                
                                fig = px.bar(df,x = 'States',y='App_Opened',
                                        color='States',
                                                        hover_data=['App_Opened'],
                                                        title='Top 10 state of highest Registered and AppOpened User',
                                                        color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                
                if query == 'Top 10 District with highest transaction':
                        col1,col2 = st.columns(2)
                        with col1:
                               df = pd.read_sql_query('''SELECT Districts, SUM(TransactionAmount) AS 'Trans_Amount'
                                                FROM map_trans GROUP BY Districts ORDER BY SUM(TransactionAmount)
                                                DESC limit 10''', con = engine)
                               df['Districts']=df['Districts'].str.replace('Central','Delhi Central')

                               fig = px.bar(df,x = 'Districts',y='Trans_Amount', color = 'Districts',
                                            hover_data=['Trans_Amount'],
                                            title='Top 10 District with highest transaction',
                                            color_discrete_sequence= px.colors.qualitative.Vivid_r)
                               st.plotly_chart(fig,use_container_width=True)
                               st.dataframe(df,hide_index=True)
                        
                        with col2:
                                df = pd.read_sql_query('''SELECT Districts, SUM(TransactionCount) as 'Transaction Count'
                                                       FROM map_trans WHERE Districts IN(SELECT Districts FROM(
                                                       SELECT Districts, SUM(TransactionAmount) as Transaction_Amount
                                                       FROM map_trans
                                                       GROUP BY Districts ORDER BY Transaction_Amount DESC LIMIT 10)as top_disricts)
                                                       GROUP BY Districts ORDER BY SUM(TransactionCount) DESC''',con=engine)
                                fig = px.bar(df,x = 'Districts',y='Transaction Count', color ='Districts',
                                            hover_data=['Transaction Count'],
                                            title='Top 10 District with highest transaction',
                                            color_discrete_sequence= px.colors.qualitative.Vivid_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)

                if query == 'Top 10 District with lowest transaction':
                        col1,col2 = st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT Districts,sum(TransactionAmount) as 'Transaction Amount'
                                        from map_trans GROUP by Districts
                                        ORDER BY SUM(TransactionAmount) ASC LIMIT 10''',con=engine)

                                fig=px.bar(df,x='Districts',y='Transaction Amount',
                                                color='Districts',
                                                hover_data=['Transaction Amount'],
                                                title='Top 10 states of lowest Transaction Amount',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        with col2:        
                                df=pd.read_sql_query('''SELECT Districts, SUM(TransactionCount) AS 'Transaction Count' FROM map_trans
                                                WHERE Districts IN ( SELECT Districts FROM 
                                                (SELECT Districts, SUM(TransactionAmount) AS amount FROM map_trans 
                                                GROUP BY Districts ORDER BY amount ASC LIMIT 10 )as top_state )
                                                GROUP BY Districts order by sum(TransactionCount) ASC''',con=engine)
        
                
                                fig=px.bar(df,x='Districts',y='Transaction Count',
                                                color='Transaction Count',
                                                hover_data=['Transaction Count'],
                                                title='Top 10 states of lowest Transaction Count',
                                                color_continuous_scale=px.colors.carto.Emrld_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                
                if query == 'Top 10 District with highest Registered User':
                        col1,col2 = st.columns(2)
                        with col1:
                                df = pd.read_sql_query('''SELECT Districts, SUM(registeredUsers) AS 'Registered Users'
                                                FROM map_user GROUP BY Districts ORDER BY SUM(registeredUsers)
                                                DESC limit 10''', con = engine)
                                
                                fig = px.bar(df,x = 'Districts',y='Registered Users',
                                        color='Districts',
                                                        hover_data=['Registered Users'],
                                                        title='Top 10 state of highest Registered User',
                                                        color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True) 
                        
                        with col2:
                                df = pd.read_sql_query('''SELECT Districts, SUM(appOpens) AS 'App_Opened' FROM map_user
                                                       WHERE Districts IN(SELECT Districts FROM(SELECT Districts, SUM(registeredUsers) as RGTD_Users 
                                                       FROM map_user GROUP BY Districts ORDER BY SUM(registeredUsers) DESC LIMIT 10) as top_user)
                                                       GROUP BY Districts ORDER BY SUM(appOpens) DESC''',con = engine
                                                       )
                                
                                fig = px.bar(df,x = 'Districts',y='App_Opened',
                                        color='Districts',
                                                        hover_data=['App_Opened'],
                                                        title='Top 10 state of highest Registered and AppOpened User',
                                                        color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                
                if query == 'Top 10 Brands used for Transaction':
                        col1,col2 = st.columns(2)

                        with col1:
                                df=pd.read_sql_query('''SELECT DISTINCT Brands as 'User Brand' ,SUM(UserCount) as 'Count'
                                                FROM agg_phonepe_user GROUP BY Brands
                                                order by SUM(UserCount) DESC LIMIT 10''',con=engine)
                                fig=px.bar(df,x='User Brand',y='Count',
                                                color='User Brand',
                                                hover_data=['Count'],
                                                title='Top 10 Brands used for Transaction (sum of all states)',
                                                color_discrete_sequence=px.colors.qualitative.Alphabet_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        with col2:
                                df=pd.read_sql_query('''SELECT DISTINCT Brands AS 'User Brand', (SUM(UserCount) / total_count) * 100 AS 'Percentage'
                                                        FROM agg_phonepe_user
                                                        CROSS JOIN (SELECT SUM(UserCount) AS total_count FROM agg_phonepe_user) AS total
                                                        GROUP BY Brands
                                                        ORDER BY SUM(UserCount) DESC LIMIT 10;''',con=engine)
                                
                                fig=px.pie(df,names='User Brand',values='Percentage',color='User Brand',
                                                title='Percentage',
                                                color_discrete_sequence=px.colors.qualitative.Bold)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)

                if query == 'Sum of Transaction by Type or categories':
                        col1,col2=st.columns(2)
                        with col1:
                                df=pd.read_sql_query('''SELECT DISTINCT TransactionName as 'categories',SUM(TransactionAmount) as 'Transaction Amount'
                                                        from agg_phonpedata_trans GROUP BY TransactionName DESC''',con=engine)
                                
                                fig=px.pie(df,names='categories',values='Transaction Amount',color='categories',
                                                title='Sum of Transaction Amount by categories',hole=0.3,
                                                color_discrete_sequence=px.colors.qualitative.Bold)
                                st.plotly_chart(fig,use_container_width=True)
                        
                        with col2:
                                st.subheader('Sum of Transaction Amount')
                                st.dataframe(df,hide_index=True)

                if query == 'Top 10 Postal code with highest Registered user':
                        col1,col2 = st.columns(2)

                        with col1:
                                df=pd.read_sql_query('''SELECT pincodes, sum(registeredUsers) as 'Registered user' FROM top_user
                                                GROUP BY pincodes ORDER BY  sum(registeredUsers) DESC LIMIT 10''',con=engine)
                                
                                fig=px.pie(df,names='pincodes',values='Registered user',
                                                color='pincodes',
                                                title='Top 10 Postal code with highest Registered user ',
                                                color_discrete_sequence=px.colors.qualitative.Pastel_r)
                                st.plotly_chart(fig,use_container_width=True)

                        with col2:
                                st.write('Top 10 Postal code with highest Registered user')
                                st.dataframe(df,hide_index=True)
                
                if query == 'Top 10 Postal code with highest Transaction':
                        col1,col2 = st.columns(2)

                        with col1:
                                df = pd.read_sql_query('''SELECT pincodes, SUM(TransactionAmount) as 'Transaction Amount' 
                                                       FROM top_trans GROUP BY pincodes ORDER BY SUM(TransactionAmount) DESC LIMIT 10''',
                                                       con=engine)
                                fig=px.pie(df,names='pincodes',values='Transaction Amount',
                                                color="pincodes",
                                                title='Top 10 Postal code of highest Transaction Amount ',
                                                color_discrete_sequence=px.colors.qualitative.Pastel_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)
                        
                        with col2:
                                df = pd.read_sql_query('''SELECT pincodes, SUM(TransactionCount) as 'TransCount'
                                                        FROM top_trans WHERE pincodes IN (SELECT pincodes FROM(SELECT pincodes,
                                                        SUM(TransactionAmount) AS TAmount FROM top_trans
                                                       GROUP BY pincodes ORDER BY SUM(TransactionAmount) DESC LIMIT 10) as Top_trn)
                                                       GROUP BY pincodes ORDER BY SUM(TransactionCount) DESC;''',con=engine)
                                fig=px.pie(df,names='pincodes',values='TransCount',
                                                color='TransCount',
                                                title='TransCount',
                                                color_discrete_sequence=px.colors.qualitative.Dark2_r)
                                st.plotly_chart(fig,use_container_width=True)
                                st.dataframe(df,hide_index=True)

        if select_insight == 'FILTER INSIGHTS':
               fill_type = st.radio('Category Selection',["States","Districts"], index = None)
               st.write("You Selected :",f"<span style = 'color : #F8CD47'>{fill_type}</span>",unsafe_allow_html=True)

               if fill_type == 'States':
                       Question = ['Year and Quater wise Transaction Amount of all states',
                                'Quater wise Transaction Amount for specific state',
                                'Quater wise Transaction Amount for specific state and type',
                                'User Brand Count for selected state and year',]
                
                       Query = st.selectbox(':red[Select Query]',options=Question, index = None)

                       if Query == Question[0]:
                               df_year = pd.read_sql_query('''SELECT DISTINCT Years as 'Year' FROM agg_phonpedata_trans
                                                            ''',con= engine)
                               select_year = st.selectbox("Select Year",options=df_year['Year'].tolist(),index=None)
                               
                               df_quater = pd.read_sql_query('''SELECT DISTINCT Quarter as 'Quarter' FROM agg_phonpedata_trans
                                                             ''',con = engine)
                               select_Quater = st.selectbox("Select Quater",options=df_quater['Quarter'].tolist(),index=None)
                               bt=st.button('Show')

                               if bt:
                                       df = pd.read_sql_query('''SELECT States, SUM(TransactionAmount) as 'Transaction Amount' 
                                                              FROM agg_phonpedata_trans WHERE Years = %s and Quarter = %s
                                                              GROUP BY States''',con=engine, params=[(select_year,select_Quater)])
                                       fig=px.scatter(df,x='States',y='Transaction Amount',
                                                        title=f'Showing Transaction Amount of {select_year}-Q{select_Quater}')
                                       
                                       df1=pd.read_sql_query('''SELECT States, SUM(TransactionCount) as 'Transaction Count'
                                                            FROM agg_phonpedata_trans WHERE Years = %s and Quarter = %s
                                                            GROUP BY States''',con=engine,params=[(select_year,select_Quater)])

                                       fig=px.scatter(df1,x='States',y='Transaction Count',
                                                        title=f'Showing Transaction Count of {select_year}-Q{select_Quater}')
                                       st.plotly_chart(fig,use_container_width=True)
                                       st.plotly_chart(fig,use_container_width=True)
                                       col1,col2 = st.columns(2)
                                       with col1:
                                               st.dataframe(df,hide_index=True)
                                       with col2:
                                               st.dataframe(df1,hide_index=True)
                                       
                       if Query == Question[1]:
                               df_state = pd.read_sql_query('''SELECT DISTINCT States FROM agg_phonpedata_trans'''
                                                           , con=engine)
                               select_state = st.selectbox("Select state",options= df_state['States'].to_list(),index = None)

                               df_year=pd.read_sql_query('''SELECT DISTINCT Years as 'Year' from agg_phonpedata_trans''',con=engine)

                               select_year = st.selectbox("Select Year",options=df_year['Year'].tolist(),index=None)
                               bt = st.button('Show')

                               if bt:
                                       col1,col2 = st.columns(2)
                                       with col1:
                                        df = pd.read_sql_query('''SELECT Quarter, SUM(TransactionAmount) as 'TransAmt'
                                                                FROM agg_phonpedata_trans WHERE States = %s AND Years = %s
                                                                GROUP BY Quarter;''',con=engine,params = [(select_state,select_year)])
                                        
                                        fig = px.bar(df,x='Quarter',y='TransAmt', color ='TransAmt',hover_data=['TransAmt'],
                                                        title= f'Quarter wise Transaction Amount of {select_state} for the year:{select_year}',
                                                        color_continuous_scale=px.colors.carto.Emrld_r)
                                        st.plotly_chart(fig,use_container_width=True)
                                        st.dataframe(df,hide_index=True)
                                       with col2:
                                        df1 = pd.read_sql_query('''SELECT Quarter, SUM(TransactionCount) as 'TransCount'
                                                                FROM agg_phonpedata_trans WHERE States = %s AND Years = %s
                                                                GROUP BY Quarter;''',con=engine,params = [(select_state,select_year)])
                                        
                                        fig = px.bar(df1,x='Quarter',y='TransCount', color ='TransCount',hover_data=['TransCount'],
                                                        title= f'Quarter wise Transaction Amount of {select_state} for the year:{select_year}',
                                                        color_continuous_scale=px.colors.carto.Emrld_r)
                                        st.plotly_chart(fig,use_container_width=True)
                                        st.dataframe(df1,hide_index=True)
                        
                       if Query == Question[2]: #'Quater wise Transaction Amount for specific state and type'
                               df_state = pd.read_sql_query('''SELECT DISTINCT States FROM agg_phonpedata_trans''',con = engine)
                               select_state = st.selectbox('Select Type',options=df_state['States'].tolist(),index = None)

                               df_type = pd.read_sql_query('''SELECT DISTINCT TransactionName as 'Type' FROM agg_phonpedata_trans''',con = engine)
                               select_type = st.selectbox('Select Type',options=df_type['Type'].tolist(),index=None)

                               bt = st.button('Show')

                               if bt:
                                       df = pd.read_sql_query('''SELECT States,Quarter,SUM(TransactionAmount) as 'Amount' FROM agg_phonpedata_trans
                                                              WHERE States = %s AND TransactionName = %s GROUP BY States,Quarter''', con=engine,
                                                              params = [(select_state,select_type)])
                                       fig = px.bar(df,x='Quarter',y='Amount',
                                                    color='Amount',hover_data=['Amount'],
                                                    title = f'Quater wise Transaction Amount of {select_state} for specific {select_type}',
                                                    color_continuous_scale=px.colors.carto.Emrld_r,
                                                    )
                                       st.plotly_chart(fig,use_container_width=True)
                                       st.dataframe(df,hide_index=True)

                       if Query == Question[3]: #'User Brand Count for selected state and year'
                                df_state = pd.read_sql_query('''SELECT DISTINCT States FROM agg_phonepe_user''',con = engine)
                                select_state = st.selectbox('Select Type',options=df_state['States'].tolist(),index = None)

                                df_year = pd.read_sql_query('''SELECT DISTINCT Years as 'year' FROM agg_phonepe_user''',con = engine)
                                select_year = st.selectbox('Select Year',options=df_year['year'].tolist(),index = None)

                                bt = st.button('Show')

                                if bt:
                                   df=pd.read_sql_query('''SELECT Brands as 'User Brand',sum(UserCount) as 'Count' from agg_phonepe_user
                                                        WHERE States=%s and Years=%s
                                                        GROUP by Brands order by sum(UserCount) DESC''',con=engine,params=[(select_state,select_year)])
                                    
                                   fig=px.bar(df,x='User Brand',y='Count',
                                                        color='Count',hover_data=['Count'],
                                                        title=f'Showing User Brand Count of {select_state} for the year:{select_year}',
                                                        color_continuous_scale=px.colors.carto.Emrld_r)
                                   st.plotly_chart(fig,use_container_width=True)
                                   st.dataframe(df,hide_index=True)  

               if fill_type == "Districts":
                       Question1=['District wise Transaction Amount for selected state & year',
                                'Year wise Transaction Amount for specific District',
                                'Year wise Registered User Count for Specific District']
                       Query=st.selectbox(':red[select Query]',options=Question1,index=None)

                       if Question1[0]:
                               df_state = pd.read_sql_query('''SELECT DISTINCT States FROM map_trans''',con=engine)
                               select_state = st.selectbox('Select States',options= df_state['States'].tolist(),index=None)

                               df_year = pd.read_sql_query('''SELECT DISTINCT Years as 'Year' FROM map_trans''',con=engine)
                               select_year = st.selectbox('Select year',options= df_year['Year'].tolist(),index=None)

                               bt = st.button('Show')

                               if bt:
                                       df = pd.read_sql_query('''SELECT Districts, SUM(TransactionAmount) as Amount
                                                              FROM map_trans WHERE States = %s and Years = %s
                                                              GROUP BY Districts''',con = engine,params=[(select_state,select_year)])
                                       fig=px.bar(df,x='Districts',y='Amount',
                                                        color='Amount',hover_data=['Amount'],
                                                        title=f'Showing User Brand Count of {select_state} for the year:{select_year}',
                                                        color_continuous_scale=px.colors.carto.Emrld_r)
                                       st.plotly_chart(fig,use_container_width=True)
                                       st.dataframe(df,hide_index=True)

                       if Query==Question1[1]:
                                
                                df_state=pd.read_sql_query('''SELECT DISTINCT States from map_trans''',con=engine)
                                select_state=st.selectbox('Select state',options=df_state['States'].tolist(),index=None)

                                df_dist=pd.read_sql_query('''SELECT DISTINCT Districts FROM map_trans
                                                        where States=%s''',con=engine,params=[(select_state,)])
                                select_dist=st.selectbox('Select District',options=df_dist['Districts'].tolist(),index=None)
                                
                                bt=st.button('Show1')

                                if bt:
                                        
                                        df=pd.read_sql_query('''SELECT Years as 'Year',sum(TransactionAmount) as 'Transaction Amount' from map_trans
                                                where States=%s and Districts= %s
                                                GROUP by Years''',con=engine,params=[(select_state,select_dist)])
                                        
                                        fig=px.bar(df,x='Year',y='Transaction Amount',
                                                color='Transaction Amount',hover_data=['Transaction Amount'],
                                                title=f'Year wise Transaction Amount of {select_dist} District',
                                                color_continuous_scale=px.colors.colorbrewer.Blues_r)
                                        st.plotly_chart(fig,use_container_width=True)
                                        st.dataframe(df,hide_index=True)
                       
                       if Query==Question1[2]:
                                df_state=pd.read_sql_query('''SELECT DISTINCT States from map_trans''',con=engine)
                                select_state=st.selectbox('Select state',options=df_state['States'].tolist(),index=None)

                                df_dist=pd.read_sql_query('''SELECT DISTINCT Districts FROM map_trans
                                                        where States=%s''',con=engine,params=[(select_state,)])
                                select_dist=st.selectbox('Select District',options=df_dist['Districts'].tolist(),index=None)
                                bt=st.button('Show2')
                                if bt:
                        
                                        df=pd.read_sql_query('''SELECT Years,sum(registeredUsers) as 'Registered User' from map_user
                                                where States=%s and Districts= %s
                                                GROUP by Years''',con=engine,params=[(select_state,select_dist)])
                                        
                                        fig=px.bar(df,x='Years',y='Registered User',
                                                color='Registered User',hover_data=['Registered User'],
                                                title=f'Year wise Registered User of {select_dist} District',
                                                color_continuous_scale=px.colors.colorbrewer.Blues_r)
                                        st.plotly_chart(fig,use_container_width=True)
                                        st.dataframe(df,hide_index=True)
  
                                
                                    
                                
                               




                               
                               


                                                      
                               
