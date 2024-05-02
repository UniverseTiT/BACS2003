import streamlit as st
import pandas as pd
from difflib import get_close_matches
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
@st.cache
def load_data():
    return pd.read_csv("Spotify_Youtube.csv")

# Function to handle errors and variations in user input
def find_closest_match(user_input, track_titles):
    closest_matches = get_close_matches(user_input, track_titles, n=1, cutoff=0.6)
    if closest_matches:
        return closest_matches[0]
    else:
        return None

# Collaborative Filtering
def collaborative_filtering(track_title, music_data):
    music_data_cleaned = music_data.dropna(subset=['Likes', 'Views'])
    similarity_matrix = cosine_similarity(music_data_cleaned[['Likes', 'Views']])
    track_index = music_data_cleaned[music_data_cleaned['Track'] == track_title].index[0]
    similar_tracks = list(enumerate(similarity_matrix[track_index]))
    sorted_similar_tracks = sorted(similar_tracks, key=lambda x: x[1], reverse=True)
    top_similar_tracks = sorted_similar_tracks[1:11]
    top_indices = [index for index, _ in top_similar_tracks]
    top_track_titles = music_data_cleaned.iloc[top_indices]['Track'].tolist()
    return top_track_titles

# Function to handle the recommendation process
def recommend(user_input, track_titles, music_data):
    if not user_input:
        st.error("Please enter a track title.")
        return
    
    closest_match = find_closest_match(user_input, track_titles)
    
    if closest_match:
        st.success(f"🎵 Closest match found: {closest_match}")
        
        closest_match_row = music_data[music_data['Track'] == closest_match].iloc[0]
        collab_filtering_result = collaborative_filtering(closest_match, music_data)
        
        if collab_filtering_result:
            st.success(f"🎶 Top 10 tracks similar to '{closest_match}' based on Collaborative Filtering:")
            table_data = []
            for i, track_title in enumerate(collab_filtering_result[:10], start=1):
                track_row = music_data[music_data['Track'] == track_title].iloc[0]
                artist = track_row['Artist']
                spotify_url = track_row['Url_spotify']
                spotify_link = f"<a href='{spotify_url}' target='_blank'>Listen on Spotify</a>"
                table_data.append((i, track_title, artist, spotify_link))
            df = pd.DataFrame(table_data, columns=["No.", "Song Name", "Artist", "Spotify"])
            st.write(df.to_html(escape=False), unsafe_allow_html=True,)

# Main function
def main():
    st.set_page_config(page_title="Music Recommender", page_icon="🎵")
    music_data = load_data()
    track_titles = music_data['Track'].tolist()
    st.title("Music Recommender")
    input_method = st.radio("Select Input Method:", ("Search", "Choose from menu"))
    
    if input_method == "Search":
        user_input = st.text_input("Enter a track title:", "")
    else:
        user_input = st.selectbox("Select a track:", track_titles)

    recommend(user_input, track_titles, music_data)

if __name__ == "__main__":
    main()
