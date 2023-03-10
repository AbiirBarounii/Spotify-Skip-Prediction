import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import webbrowser
import streamlit as st
import warnings
warnings.filterwarnings('ignore')
from PIL import Image


# All Page Functions: 
def home():

    st.write("# :house: Home Page")
    st.write("#### This is the home page.")

    st.subheader(':pushpin: Overiew')
    st.write(
    """
    Spotify is an online music streaming service with over 190 million active users interacting with a library of over 40 million tracks. A central challenge for Spotify is to recommend the right music to each user. While there is a large related body of work on recommender systems, there is very little work, or data, describing how users sequentially interact with the streamed content they are presented with. In particular within music, the question of if, and when, a user skips a track is an important implicit feedback signal.
    Our challenge focuses on the task of session-based sequential skip prediction, i.e. predicting whether users will skip tracks, given their immediately preceding interactions in their listening session.
    """
    )

    st.subheader(':pushpin: Dataset')
    st.write(
    """
    The public part of the dataset consists of roughly 130 million listening sessions with associated user interactions on the Spotify service. In addition to the public part of the dataset, approximately 30 million listening sessions are used for the challenge leaderboard. For these leaderboard sessions the participant is provided all the user interaction features for the first half of the session, but only the track id’s for the second half. In total, users interacted with almost 4 million tracks during these sessions, and the dataset includes acoustic features and metadata for all of these tracks.
    If you use this dataset in an academic publication, please cite the following paper:@inproceedings{brost2019music, title={The Music Streaming Sessions Dataset}, author={Brost, Brian and Mehrotra, Rishabh and Jehan, Tristan}, booktitle={Proceedings of the 2019 Web Conference}, year={2019}, organization={ACM} }
    """
    )

    st.subheader(':pushpin: Challenge')
    st.write(
    """
    The task is to predict whether individual tracks encountered in a listening session will be skipped by a particular user. In order to do this, complete information about the first half of a user’s listening session is provided, while the prediction is to be carried out on the second half. Participants have access to metadata, as well as acoustic descriptors, for all the tracks encountered in listening sessions.
    The output of a prediction is a binary variable for each track in the second half of the session indicating if it was skipped or not, with a 1 indicating that the track skipped, and a 0 indicating that the track was not skipped. For this challenge we use the skip_2 field of the session logs as our ground truth.
    """
    )
    
def eda():

    # Define a function to plot countplot
    def plot_countplot(df, col_name, hue=None):
        """ To plot bargraph to get the count of each score feature"""
        custom_palette = sns.color_palette(['#262730', '#1bd760'])
        plt.figure(figsize=(8, 4))
        plt.title(f'Datapoint distribution of {col_name}')
        sns.countplot(x=col_name, hue=hue, data=df, palette=custom_palette)
        st.pyplot()

    # Set the title and introduction of the Streamlit page
    st.write("# :closed_book: Exploratory Data Analysis")
    st.write("## Dataset (Simplified View)")

    # Load the data and display it
    df = pd.read_csv('./data/model.csv')
    st.write(df.head(10))
    st.text("")

    # Set the configuration to not show deprecation warning for global use of pyplot
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Display the section for data visualization
    st.write("## Data Visualization")

    # Define the columns to plot countplots for
    cols = ['context_switch', 'context_type',
            'no_pause_before_play', 'long_pause_before_play',
            'hist_user_behavior_n_seekfwd', 'hist_user_behavior_n_seekback',
            'hist_user_behavior_is_shuffle', 'premium', 'hist_user_behavior_reason_start',
            'hist_user_behavior_reason_end']
    
    # Divide the page into 10 columns
    for i, col in enumerate(cols):
        if i % 2 == 0:
            col_left, col_right = st.columns(2)
            with col_left:
                plot_countplot(df, col, hue=df['target'])
            with col_right:
                if i+1 < len(cols):
                    plot_countplot(df, cols[i+1], hue=df['target'])

def prediction():
    status = '"Click on Predict Skip"' # Initialize the status variable

    # Write the title and subtitle
    st.write(""" # :telescope: Spotify Track Skip Prediction """)

    
    # Load and display the image
    image = Image.open('./images/Spotify_Logo_RGB_Green.png')

    col1, col2, col3 = st.columns([0.4,1,0.1])
    with col1:
        st.write('')

    with col2:
        new_image = image.resize((680, 200))
        st.image(new_image,caption='Music is personal')

    with col3:
        st.write('')
    

    # st.image(image, caption='Music is personal')
    
    # Use st.container() to divide the page into three columns
    with st.container():
        col1, col2, col3 = st.columns(3)

        # Create dropdown menus for different user actions
        hist_user_behavior_reason_start = col1.selectbox('User action: Pre Track Play',
                                                         ['trackdone','fwdbtn','backbtn','clickrow','appload',
                                                          'playbtn','remote','trackerror','endplay'])
        hist_user_behavior_reason_end = col1.selectbox('User action: Post Track Play',
                                                       ['trackdone', 'fwdbtn', 'backbtn', 'endplay', 'logout',
                                                        'remote', 'clickrow'])
        
        # Create a dropdown menu for the number of pauses before playing a song
        no_pause_before_play = col1.selectbox('Set the number of pauses before play',
                                              [0,1,2,3,4,5,6,7,8,9,10])
        
        # Create a dropdown menu for the status of shuffle mode
        hist_user_behavior_is_shuffle = col2.selectbox('Status of Shuffle Mode',
                                                       ['Shuffle Mode On','Shuffle Mode Off'])
        
        # Create a dropdown menu for the type of premium account
        premium = col2.selectbox('Select the premium type', ['Premium','Freemium'])
        
        # Create a dropdown menu for context switching
        context_switch = col3.selectbox('Select the context switch', ['Yes','No'])
        
        # Create a dropdown menu for the type of context
        context_type = col3.selectbox('Status of Context Type',
                                      ['user_collection', 'catalog','editorial_playlist','radio',
                                       'personalized_playlist','charts'])
        
        # Create a dictionary to encode the dropdown menu values for use in the model
        encode_dict = {
            'premium' : {'Premium': 1 , 'Freemium': 0},
            'context_switch': {'Yes': 1, 'No': 0},
            'hist_user_behavior_is_shuffle' : {'Shuffle Mode On': 1, 'Shuffle Mode Off': 0},
            'context_type' : {'user_collection': 5, 'catalog':0 ,'editorial_playlist':2 ,
                            'radio':4 , 'personalized_playlist':3,  'charts':1}
        }

    # Define the function to load and use the model for prediction
    def model_pred(context_switch, no_pause_before_play, premium, hist_user_behavior_is_shuffle,
                context_type, hist_user_behavior_reason_start, hist_user_behavior_reason_end):
        
        with open('./models/model_pkl',"rb") as file:
            model = pickle.load(file)
        
        input_filters = [[context_switch,no_pause_before_play,0,0,0,0,hist_user_behavior_is_shuffle,
                        premium,context_type,hist_user_behavior_reason_start,hist_user_behavior_reason_end]]

        return model.predict(input_filters)

    # Divide the page into five columns, leaving the third column blank for the button
    col1, col2, col3 = st.columns([0.3,1,1.6])

    with col1:
        pass
    with col2:
        pass
    with col3 :
        if st.button("Predict Skip"):

            hist_user_behavior_is_shuffle = encode_dict['hist_user_behavior_is_shuffle'][hist_user_behavior_is_shuffle]
            premium = encode_dict['premium'][premium]
            context_switch = encode_dict['context_switch'][context_switch]
            context_type = encode_dict['context_type'][context_type]

            skip = model_pred(context_switch, no_pause_before_play,premium,hist_user_behavior_is_shuffle,context_type,hist_user_behavior_reason_start,hist_user_behavior_reason_end)

            if skip[0] == 1:
                status = 'Song is Skipped'
            else:
                status = 'Song is played'



    st.write('### Status of the Track:fast_forward: ' + str(status))
            
    

# Driver Code:

# Define the pages in a dictionary
pages = {
    "Home": home,
    "Data Analysis": eda,
    "Prediction": prediction
}

#Page Icon
page_icon = Image.open('./images/page_icon_spotify.png')

#Page config setup
st.set_page_config(
page_title="Spotify Skip Prediction",
page_icon=page_icon,
layout="wide"
)

# Set the default page
default_page = "Home"

# Define the sidebar
image = Image.open('./images/Spotify_Logo_RGB_Green.png')
st.sidebar.image(image,width=210,use_column_width=False)
st.sidebar.title("""Spotify Track Skip Prediction""")

#Sidebar selection
selection = st.sidebar.radio("Go to", list(pages.keys()), index=list(pages.keys()).index(default_page))
st.sidebar.text("")

url = 'https://www.linkedin.com/in/aniruddha95/'
if st.sidebar.button('Get in touch'):
    webbrowser.open_new_tab(url)



# Display the selected page with the corresponding function
pages[selection]()

