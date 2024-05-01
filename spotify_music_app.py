import streamlit as st
import pandas as pd
from difflib import get_close_matches
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load the dataset
@st.cache
def load_data():
    return pd.read_csv("Spotify_Youtube.csv")

# Function to handle errors and variations in user input
def find_closest_match(user_input, track_titles):
    # Find closest match using difflib's get_close_matches function
    closest_matches = get_close_matches(user_input, track_titles, n=1, cutoff=0.6)
    
    if closest_matches:
        # Return the closest match
        return closest_matches[0]
    else:
        # Return None if no close match found
        return None

# Initialize the Spotify client
def get_song_album_cover_url(song_name, artist_name):
    CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
    CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

    # Initialize the Spotify client
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

# Function to handle the recommendation process
def recommend(user_input, track_titles, music_data):
    # Check if the user input is empty
    if not user_input:
        st.error("Please enter a track title.")
        return
    
    # Find closest match to user input
    closest_match = find_closest_match(user_input, track_titles)
    
    if closest_match:
        # Show the closest match
        st.success(f"🎵 Closest match found: {closest_match}")
        
        # Perform collaborative filtering
        collab_filtering_result = collaborative_filtering(closest_match, music_data)
        
        # Display the top 10 similar tracks
        if collab_filtering_result:
            st.success(f"🎶 Top 10 tracks similar to '{closest_match}' based on Collaborative Filtering:")
            for i, track in enumerate(collab_filtering_result[:10], start=1):
                st.write(f"{i}. {track}")
                st.image(get_song_album_cover_url(track, music_data['artist']))
        else:
            st.warning("No similar tracks found based on Collaborative Filtering.")
    else:
        st.error(f"No close match found for '{user_input}'. Please enter another title.")

# Collaborative filtering function (replace this with your actual collaborative filtering function)
def collaborative_filtering(track_title, music_data):
    # Dummy implementation: return top 10 track titles from the dataset excluding the input track
    similar_tracks = music_data[music_data['song'] != track_title]['song'].head(10).tolist()
    return similar_tracks

# Main function
def main():
    # Set up the Streamlit app
    st.set_page_config(page_title="Spotify Recommender System", page_icon=":musical_note:")
    st.markdown('<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500&display=swap" rel="stylesheet">', unsafe_allow_html=True)
    st.markdown('<style>body {font-family: "Montserrat", sans-serif; background-color: #1DB954;}</style>', unsafe_allow_html=True)
    st.title("🎧 Spotify Recommender System")
    
    # Load the dataset
    music_data = load_data()
    
    # Extract track titles
    track_titles = music_data['song'].tolist()
    
    # Get user input
    user_input = st.text_input("🔍 Enter a track title:", "")
    
    # Display recommendation button
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🚀 Recommend"):
            recommend(user_input, track_titles, music_data)
    with col2:
        st.empty()

if __name__ == "__main__":
    main()
