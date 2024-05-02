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
            for i, track_title in enumerate(collab_filtering_result[:10], start=1):
                track_row = music_data[music_data['Track'] == track_title].iloc[0]
                artist = track_row['Artist']
                spotify_url = track_row['Url_spotify']
                spotify_link = f"[Listen on Spotify]({spotify_url})"
                table_data.append((i, track_title, artist, spotify_link, spotify_url))  # Add Spotify URL to table data
            df = pd.DataFrame(table_data, columns=["#", "Track", "Artist", "Spotify", "Spotify URL"])  # Include Spotify URL column
            st.table(df)
        else:
            st.warning("No similar tracks found based on Collaborative Filtering.")
    else:
        st.error(f"No close match found for '{user_input}'. Please enter another title.")

