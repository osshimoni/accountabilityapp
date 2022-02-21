import streamlit as st
from datetime import date
import pandas as pd
import gspread as gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gs
import randfacts as rd

gc = gspread.service_account(filename="credentials.json")


ws = gc.open('accountability').worksheet('data')
df = pd.DataFrame.from_dict(ws.get_all_records())

st.subheader('Workout Tracker')

st.sidebar.title('History')
st.sidebar.table(df.sort_values(by = ['Date'], ascending = False))
st.sidebar.button('Refresh')

# update data in google sheets with new data
def upload_df(ws, df):
    gs.set_with_dataframe(worksheet=ws, dataframe=df, include_index=False, include_column_header=True,
                          resize=True)

# get date
input_date = str(st.date_input('Date'))

# set fact
ws_fact = gc.open('facts').worksheet('facts')
df_fact = pd.DataFrame.from_dict(ws_fact.get_all_records())

if df_fact.at[0,'Date'] != str(date.today()):
    df_fact = df_fact.append(df_fact.iloc[0])
    df_fact.iloc[0] = (input_date, str(rd.get_fact()))

    upload_df(ws_fact, df_fact)

# main code
if df.at[0,'Date'] != str(date.today()):
    df = df.append(df.iloc[0])
    df.iloc[0] = (input_date, 'No', 'No')
    upload_df(ws,df)

# get user name
name = st.radio('Name', options = ['Osher', 'Ryan'])

# completed workout
col1, col2 = st.columns([1, 1])
with col1:
    if st.button('Log Workout'):
        df.at[0,name] = ('Yes')
        upload_df(ws, df)

# rest day
with col2:
    if st.button('Rest'):
        df.at[0,name] = ('Rest')
        st.write('You better have a good reason...')
        upload_df(ws, df)


# if all users completed workouts, show secret
if 'No' not in list(df.iloc[0]) and 'Rest' not in list(df.iloc[0]):
    st.subheader('Good job fellas')
    if st.button('Show Daily Fact'):
        st.write(df_fact.at[0,'Fact'])



