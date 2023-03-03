import pandas as pd
import datetime
import pickle
import streamlit as st



st.write(
            """
            # Spotify Squential Skip Prediction
            """
        )



col1, col2, col3 = st.columns(3)

hist_user_behavior_reason_start = col1.selectbox('User action which lead to play that song',['trackdone','fwdbtn','backbtn','clickrow','appload','playbtn','remote','trackerror','endplay'])
hist_user_behavior_reason_end = col1.selectbox('User action which lead to end of that that song',['trackdone', 'fwdbtn', 'backbtn', 'endplay', 'logout', 'remote', 'clickrow'])

no_pause_before_play = col1.selectbox('Set the no of pauses before play',[0,1,2,3,4,5,6,7,8,9,10])
hist_user_behavior_is_shuffle = col2.selectbox('Status of Suffle Mode', ['Suffle Mode On','Suffle Mode Off'])
premium = col2.selectbox('Select the premium type', ['premium','freemium'])

context_switch = col3.selectbox('Select the context switch', ['Yes','No'])
context_type = col3.selectbox('Status of Context Type', ['user_collection', 'catalog','editorial_playlist','radio','personalized_playlist','charts'])



# encode_dict = {
#     'premium' : {'premium': 1 , 'freemium': 0},
#     'context_switch': {'Yes': 1, 'No': 0},
#     'hist_user_behavior_is_shuffle' : {'Suffle Mode On': 1, 'Suffle Mode Off': 0},
#     'context_type' : {'user_collection': 5, 'catalog':0 ,'editorial_playlist':2 , 'radio':4 , 'personalized_playlist':3,  'charts':1}
# }


def model_pred(context_switch, no_pause_before_play,premium,hist_user_behavior_is_shuffle,context_type,hist_user_behavior_reason_start,hist_user_behavior_reason_end):
    
    with open('model_pkl',"rb") as file:
        model = pickle.load(file)
    
    input_filters = [[context_switch,no_pause_before_play,0,0,0,0,hist_user_behavior_is_shuffle,premium,context_type,hist_user_behavior_reason_start,hist_user_behavior_reason_end]]
    #input_filters =  [[0,0,1,1,0,0,0,1,4,1,3]]

    return model.predict(input_filters)


if st.button("Predict Skip"):
    # hist_user_behavior_is_shuffle = encode_dict['hist_user_behavior_is_shuffle'][hist_user_behavior_is_shuffle]
    # premium = encode_dict['premium'][premium]
    # context_switch = encode_dict['context_switch'][context_switch]
    # context_type = encode_dict['context_type'][context_type]

    skip = model_pred(context_switch, no_pause_before_play,premium,hist_user_behavior_is_shuffle,context_type,hist_user_behavior_reason_start,hist_user_behavior_reason_end)

    # if skip[0] == 1:
    #     skip = 'Song is Skipped'
    # else:
    #     skip = 'Song is played'


    st.subheader("Skip or Not:" + str(skip))