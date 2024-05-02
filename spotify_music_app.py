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
        
        # Perform collaborative filtering
        collab_filtering_result = collaborative_filtering(closest_match, music_data)
        
        # Display the top 10 similar tracks
        if collab_filtering_result:
            st.success(f"🎶 Top 10 tracks similar to '{closest_match}' based on Collaborative Filtering:")
            st.markdown('<style>.spotify-list {list-style-type: none; margin: 0; padding: 0;}</style>', unsafe_allow_html=True)
            st.markdown('<style>.spotify-list li {padding: 10px; border-bottom: 1px solid #333333; color: #ffffff; font-size: 16px;}</style>', unsafe_allow_html=True)
            st.markdown('<style>.spotify-list li:last-child {border-bottom: none;}</style>', unsafe_allow_html=True)
            st.markdown('<ul class="spotify-list">', unsafe_allow_html=True)
            for i, track in enumerate(collab_filtering_result[:10], start=1):
                st.markdown(f'<li>{i}. {track}</li>', unsafe_allow_html=True)
            st.markdown('</ul>', unsafe_allow_html=True)
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
    st.title("Music Recommender")
    
    # Get user input
    user_input = st.text_input("Enter a track title:", "")

    # Recommend similar tracks
    recommend(user_input, track_titles, music_data)

if __name__ == "__main__":
    main()
