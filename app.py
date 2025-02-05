import os
import threading
import time  # Import the time module
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, filedialog, ttk
from PIL import Image, ImageTk  # For displaying the Instagram logo
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

        # Simulate smooth progress for the download
        for i in range(101):
            progress['value'] = i
            root.update_idletasks()
            time.sleep(0.02)  # Smooth animation

        L.download_post(post, target=shortcode)

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
root.geometry("600x600")
root.resizable(False, False)
root.configure(bg="#1C1C1E")  # Dark mode background

# Load Instagram logo
logo_image = Image.open("instagram_logo.png")  # Ensure you have an 'instagram_logo.png' file
logo_image = logo_image.resize((80, 80), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)

# Header Section
header_frame = Label(root, bg="#1C1C1E", pady=20)
header_frame.pack(fill="x")

# Display Instagram logo
logo_label = Label(header_frame, image=logo_photo, bg="#1C1C1E")
logo_label.grid(row=0, column=0, padx=20)

# Project name
project_name = Label(header_frame, text="Social Downloader", font=("Helvetica", 18, "bold"), bg="#1C1C1E", fg="#007AFF")
project_name.grid(row=0, column=1, padx=10)

# Input Field Section
input_frame = Label(root, bg="#1C1C1E", pady=20)
input_frame.pack(fill="x")

Label(input_frame, text="Enter Instagram Post URL:", font=("Helvetica", 14), bg="#1C1C1E", fg="#FFFFFF").pack(anchor="w", padx=20)
url_var = StringVar()
entry_style = {"font": ("Helvetica", 14), "bd": 0, "bg": "#2C2C2E", "fg": "#FFFFFF", "relief": "flat",
               "highlightthickness": 1, "highlightbackground": "#3A3A3C", "highlightcolor": "#007AFF"}
url_entry = Entry(input_frame, textvariable=url_var, width=50, **entry_style)
url_entry.pack(fill="x", padx=20, pady=10, ipady=8)

# Download Button Section
button_frame = Label(root, bg="#1C1C1E", pady=20)
button_frame.pack(fill="x")

# Download button with hover effect
def on_enter(event):
    download_button.config(bg="#007AFF", fg="#FFFFFF")

def on_leave(event):
    download_button.config(bg="#3A3A3C", fg="#FFFFFF")

download_button = Button(button_frame, text="Download", command=start_download, bg="#3A3A3C", fg="#FFFFFF",
                         font=("Helvetica", 14), padx=20, pady=5, relief="flat", borderwidth=0, activebackground="#007AFF")
download_button.pack()
download_button.bind("<Enter>", on_enter)
download_button.bind("<Leave>", on_leave)

# Progress Bar Section
progress_frame = Label(root, bg="#1C1C1E", pady=20)
progress_frame.pack(fill="x")

style = ttk.Style()
style.theme_use("clam")
style.configure("TProgressbar", thickness=10, troughcolor="#2C2C2E", background="#007AFF", bordercolor="#1C1C1E")
progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=400, mode="determinate", style="TProgressbar")
progress_bar.pack(fill="x", padx=20)

# Run the application
root.mainloop()