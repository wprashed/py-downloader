import os
import threading
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, filedialog, ttk
import instaloader

# Function to download Instagram media from a single post
def download_single_post(url, download_folder, progress):
    try:
        L = instaloader.Instaloader()
        L.download_pictures = True
        L.download_videos = True
        L.download_video_thumbnails = False
        L.save_metadata = False
        L.compress_json = False
        L.post_metadata_txt_pattern = ""

        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.dirname_pattern = download_folder

        # Simulate progress for the download
        progress['value'] = 0
        root.update_idletasks()

        L.download_post(post, target=shortcode)

        progress['value'] = 100
        root.update_idletasks()

        messagebox.showinfo("Success", "Media downloaded successfully!")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Failed to download media: {e}")

# Function to handle the download button click
def start_download():
    url = url_var.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a valid Instagram URL.")
        return

    download_folder = filedialog.askdirectory(title="Select Download Folder")
    if not download_folder:
        messagebox.showwarning("Folder Error", "Please select a valid download folder.")
        return

    # Start the download in a separate thread to avoid freezing the GUI
    threading.Thread(target=download_single_post, args=(url, download_folder, progress_bar)).start()

# Create the main application window
root = Tk()
root.title("Instagram Media Downloader")
root.geometry("600x300")
root.resizable(False, False)

# Styling
font_style = ("Helvetica", 12)
button_style = {"bg": "#4CAF50", "fg": "white", "padx": 10, "pady": 5, "font": font_style}

# URL input field
Label(root, text="Instagram Post URL:", font=font_style).pack(pady=10)
url_var = StringVar()
Entry(root, textvariable=url_var, width=50, font=font_style).pack(pady=5)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=20)

# Download button
Button(root, text="Download", command=start_download, **button_style).pack(pady=10)

# Run the application
root.mainloop()