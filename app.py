import os
import threading
import time
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, filedialog
import instaloader


# Function to download Instagram media from a single post
def download_single_post(url, download_folder):
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
        L.download_post(post, target=shortcode)
        messagebox.showinfo("Success", "Media downloaded successfully!")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Failed to download media: {e}")


# Function to download all content from a specific Instagram user
def download_user_content(username, download_folder):
    try:
        L = instaloader.Instaloader()
        L.download_pictures = True
        L.download_videos = True
        L.download_video_thumbnails = False
        L.save_metadata = False
        L.compress_json = False
        L.post_metadata_txt_pattern = ""

        # Log in to Instagram
        username_insta = "your_username"
        password_insta = "your_password"
        L.login(username_insta, password_insta)

        print(f"Downloading all content from user: {username}")
        L.dirname_pattern = download_folder
        profile = instaloader.Profile.from_username(L.context, username)

        # Retry mechanism with exponential backoff
        retries = 0
        max_retries = 5
        for post in profile.get_posts():
            while retries < max_retries:
                try:
                    print(f"Downloading post: {post.shortcode}")
                    L.download_post(post, target=profile.username)
                    time.sleep(5)  # Add a delay between downloads
                    break  # Exit the retry loop if successful
                except Exception as e:
                    retries += 1
                    print(f"Error downloading post {post.shortcode}: {e}. Retrying ({retries}/{max_retries})...")
                    time.sleep(10 * retries)  # Exponential backoff
            if retries == max_retries:
                print(f"Failed to download post {post.shortcode} after {max_retries} attempts.")

        messagebox.showinfo("Success", f"All content from @{username} downloaded successfully!")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Failed to download content: {e}")


# Function to handle the download button click
def start_download():
    url_or_username = url_var.get()
    if not url_or_username:
        messagebox.showwarning("Input Error", "Please enter a valid Instagram URL or username.")
        return

    download_folder = filedialog.askdirectory(title="Select Download Folder")
    if not download_folder:
        messagebox.showwarning("Folder Error", "Please select a valid download folder.")
        return

    if "instagram.com/p/" in url_or_username:
        threading.Thread(target=download_single_post, args=(url_or_username, download_folder)).start()
    else:
        threading.Thread(target=download_user_content, args=(url_or_username, download_folder)).start()


# Create the main application window
root = Tk()
root.title("Instagram Media Downloader")
root.geometry("500x200")

Label(root, text="Instagram URL or Username:").pack(pady=5)
url_var = StringVar()
Entry(root, textvariable=url_var, width=50).pack(pady=5)

Button(root, text="Download", command=start_download).pack(pady=20)

root.mainloop()