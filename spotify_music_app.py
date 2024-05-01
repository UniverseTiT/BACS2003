import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from difflib import get_close_matches

# Function to handle errors and variations in user input
def find_closest_match(user_input):
    # List of track titles from the dataset
    track_titles = music_data['Track'].tolist()
    
    # Find closest match using difflib's get_close_matches function
    closest_matches = get_close_matches(user_input, track_titles, n=1, cutoff=0.6)
    
    if closest_matches:
        # Return the closest match
        return closest_matches[0]
    else:
        # Return None if no close match found
        return None

# Function to handle the recommendation process
def recommend():
    # Get user input from the entry widget
    user_input = entry.get().strip()
    
    # Check if the user input is empty
    if not user_input:
        messagebox.showerror("Error", "Please enter a track title.")
        return
    
    # Find closest match to user input
    closest_match = find_closest_match(user_input)
    
    if closest_match:
        # Show the closest match in the label widget
        label.config(text=f"Closest match: {closest_match}")
        
        # Perform collaborative filtering
        collab_filtering_result = collaborative_filtering(closest_match)
        
        # Display the top 10 similar tracks in the listbox widget
        listbox.delete(0, tk.END)
        for track in collab_filtering_result:
            listbox.insert(tk.END, music_data.iloc[track[0]]['Track'])
    else:
        messagebox.showerror("Error", f"No close match found for '{user_input}'. Please enter another title.")

# Create the main window
root = tk.Tk()
root.title("Spotify Recommender System")

# Create a label and entry widget for user input
tk.Label(root, text="Enter a track title:").pack()
entry = tk.Entry(root)
entry.pack()

# Create a button to trigger the recommendation process
tk.Button(root, text="Recommend", command=recommend).pack()

# Create a label widget to display the closest match
label = tk.Label(root, text="")
label.pack()

# Create a listbox widget to display the recommended tracks
listbox = tk.Listbox(root)
listbox.pack()

# Run the Tkinter event loop
root.mainloop()
