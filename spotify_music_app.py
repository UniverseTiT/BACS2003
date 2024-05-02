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
    # Find closest match using difflib's get_close_matches function
    closest_matches = get_close_matches(user_input, track_titles, n=1, cutoff=0.6)
    
    if closest_matches:
        # Return the closest match
        return closest_matches[0]
    else:
        # Return None if no close match found
        return None

# Collaborative Filtering
def collaborative_filtering(track_title, music_data):
    # Drop rows with missing or invalid values in 'Likes' and 'Views' columns
    music_data_cleaned = music_data.dropna(subset=['Likes', 'Views'])
    
    # Compute similarity matrix
    similarity_matrix = cosine_similarity(music_data_cleaned[['Likes', 'Views']])
    
    # Find index of the input track
    track_index = music_data_cleaned[music_data_cleaned['Track'] == track_title].index[0]
    
    # Retrieve similar tracks with their similarity scores
    similar_tracks = list(enumerate(similarity_matrix[track_index]))
    
    # Sort similar tracks by similarity score in descending order
    sorted_similar_tracks = sorted(similar_tracks, key=lambda x: x[1], reverse=True)
    
    # Extract top similar tracks excluding the input track itself
    top_similar_tracks = sorted_similar_tracks[1:11]
    
    # Get the indices of the top similar tracks
    top_indices = [index for index, _ in top_similar_tracks]
    
    # Retrieve the actual track titles corresponding to the indices
    top_track_titles = music_data_cleaned.iloc[top_indices]['Track'].tolist()
    
    # Return top similar tracks
    return top_track_titles

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
        
        # Get the row corresponding to the closest match
        closest_match_row = music_data[music_data['Track'] == closest_match].iloc[0]
        
        # Perform collaborative filtering
        collab_filtering_result = collaborative_filtering(closest_match, music_data)
        
        # Display the top 10 similar tracks
        if collab_filtering_result:
            st.success(f"🎶 Top 10 tracks similar to '{closest_match}' based on Collaborative Filtering:")
            table_data = []
            for track_title in collab_filtering_result[:10]:
                track_row = music_data[music_data['Track'] == track_title].iloc[0]
                artist = track_row['Artist']
                spotify_url = track_row['Url_spotify']
                table_data.append((track_title, artist, spotify_url))
            df = pd.DataFrame(table_data, columns=["Track", "Artist", "Spotify"])
            st.table(df)
        else:
            st.warning("No similar tracks found based on Collaborative Filtering.")
    else:
        st.error(f"No close match found for '{user_input}'. Please enter another title.")

# Main function
def main():
    # Set page title and favicon
    st.set_page_config(page_title="Music Recommender", page_icon="🎵")
    
    # Load the data
    music_data = load_data()
    
    # Extract track titles
    track_titles = music_data['Track'].tolist()

    # Set app title
    st.title("Spotify Search")

    # Set background color and padding for the whole page
    st.markdown(
        """
        <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #181818;
            color: #fff;
            margin: 0;
            padding: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Search form
    st.markdown(
        """
        <div id="search-form" style="text-align: center; margin-bottom: 20px;">
            <input type="text" id="search-input" placeholder="Search for an artist or track..." style="width: 300px; padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #ccc; margin-right: 10px;">
            <button id="search-button" style="padding: 10px 20px; font-size: 16px; border-radius: 5px; border: none; cursor: pointer; background-color: #1db954; color: #fff;">Search</button>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Recommendation results
    recommend(user_input, track_titles, music_data)

if __name__ == "__main__":
    main()
