import streamlit as st
from datetime import date
import pandas as pd
import gspread as gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gs
import randfacts as rd

# To add a user: add them to source dataset, add them to name radio, add a 'No' to the new data creation

gc = gspread.service_account(filename="credentials.json")


ws = gc.open('accountability').worksheet('data')
df = pd.DataFrame.from_dict(ws.get_all_records())

st.subheader('Workout Tracker')


# update data in google sheets with new data
def upload_df(ws, df):
    gs.set_with_dataframe(worksheet=ws, dataframe=df, include_index=False, include_column_header=True,
                          resize=True)

# get date
input_date = str(st.date_input('Date'))

# set fact
ws_fact = gc.open('facts').worksheet('facts')
df_fact = pd.DataFrame.from_dict(ws_fact.get_all_records())

if str(input_date) not in list(df_fact['Date']):
    new_fact_data = {'Date':[input_date], 'Fact':[str(rd.get_fact())]}
    new_fact_data_df = pd.DataFrame.from_dict(new_fact_data)
    df_fact = df_fact.append(new_fact_data_df)

    upload_df(ws_fact, df_fact)



# main code
if str(input_date) not in list(df['Date']):
    new_day_data = {'Date':[input_date], 'Osher':['--'], 'Ryan':['--'], 'Sumana':['--']}
    new_day_data_df = pd.DataFrame.from_dict(new_day_data)
    df = df.append(new_day_data_df)
    upload_df(ws,df)

st.sidebar.title('History')
st.sidebar.table(df.sort_values(by = ['Date'], ascending = False))
st.sidebar.button('Refresh')
    
# get user name
name = st.radio('Name', options = ['Osher', 'Ryan','Sumana'])

# completed workout
col1, col2 = st.columns([1, 1])
with col1:
    if st.button('Log Workout'):
        df.loc[df['Date'] == input_date, name] = 'Yes'
        upload_df(ws, df)
        st.write('Saved')

# rest day
with col2:
    if st.button('Rest'):
        df.loc[df['Date'] == input_date, name] = 'Rest'
        st.write('You better have a good reason...')
        upload_df(ws, df)



# if all users completed workouts, show secret
if '--' not in df[df['Date']==input_date].values and 'Rest' not in df[df['Date']==input_date].values:
    st.subheader('Good job fellas')
    if st.button('Show Daily Fact'):
        st.write(df_fact.loc[df_fact['Date'] == input_date]['Fact'])





