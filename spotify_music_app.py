import streamlit as st
from difflib import get_close_matches

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

# Function to handle the recommendation process
def recommend(user_input, track_titles):
    # Check if the user input is empty
    if not user_input:
        st.error("Please enter a track title.")
        return
    
    # Find closest match to user input
    closest_match = find_closest_match(user_input, track_titles)
    
    if closest_match:
        # Show the closest match
        st.write(f"Closest match: {closest_match}")
        
        # Perform collaborative filtering
        collab_filtering_result = collaborative_filtering(closest_match)
        
        # Display the top 10 similar tracks
        st.write("Top 10 tracks similar to", closest_match, "based on Collaborative Filtering:")
        for track in collab_filtering_result:
            st.write(track)
    else:
        st.error(f"No close match found for '{user_input}'. Please enter another title.")

# Main function
def main():
    # Load your data here
    track_titles = music_data['Track'].tolist()
    
    # Set up the Streamlit app
    st.title("Spotify Recommender System")
    
    # Get user input
    user_input = st.text_input("Enter a track title:")
    
    # Display recommendation button
    if st.button("Recommend"):
        recommend(user_input, track_titles)

if __name__ == "__main__":
    main()
