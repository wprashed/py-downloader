import os
import threading
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, filedialog
import instaloader

# Function to download Instagram media
def download_instagram_media(url, download_folder):
    try:
        # Create an Instaloader instance
        L = instaloader.Instaloader()

        # Optional: Log in to Instagram if the post is private
        # Uncomment the lines below and replace with your credentials
        # username = "your_username"
        # password = "your_password"
        # L.login(username, password)

        print("Initializing Instaloader...")
        shortcode = url.split("/")[-2]
        print(f"Extracting shortcode from URL: {shortcode}")

        post = instaloader.Post.from_shortcode(L.context, shortcode)
        print(f"Fetching post with shortcode: {shortcode}")

        print(f"Downloading media to folder: {download_folder}")
        L.download_post(post, target=download_folder)

        messagebox.showinfo("Success", "Media downloaded successfully!")
    except Exception as e:
        print(f"Error: {e}")  # Print the error to the console for debugging
        messagebox.showerror("Error", f"Failed to download media: {e}")

# Function to handle the download button click
def start_download():
    url = url_var.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a valid Instagram URL.")
        return

    # Open a dialog to select the download folder
    download_folder = filedialog.askdirectory(title="Select Download Folder")
    if not download_folder:
        messagebox.showwarning("Folder Error", "Please select a valid download folder.")
        return

    # Start the download in a separate thread to avoid freezing the GUI
    threading.Thread(target=download_instagram_media, args=(url, download_folder)).start()

# Create the main application window
root = Tk()
root.title("Instagram Media Downloader")
root.geometry("500x200")

# URL input field
Label(root, text="Instagram URL:").pack(pady=5)
url_var = StringVar()
Entry(root, textvariable=url_var, width=50).pack(pady=5)

# Download button
Button(root, text="Download", command=start_download).pack(pady=20)

# Run the application
root.mainloop()