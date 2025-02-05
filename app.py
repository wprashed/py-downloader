import os
import threading
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

        # Simulate progress for the download
        for i in range(101):
            progress['value'] = i
            root.update_idletasks()
            time.sleep(0.05)  # Simulate download progress

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
root.geometry("600x400")
root.resizable(False, False)
root.configure(bg="#f0f2f5")  # Set background color

# Load Instagram logo
logo_image = Image.open("instagram_logo.png")  # Ensure you have an 'instagram_logo.png' file
logo_image = logo_image.resize((150, 150), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)

# Display Instagram logo
logo_label = Label(root, image=logo_photo, bg="#f0f2f5")
logo_label.grid(row=0, column=0, columnspan=2, pady=10)

# Project name
project_name = Label(root, text="Instagram Media Downloader", font=("Helvetica", 18, "bold"), bg="#f0f2f5", fg="#E1306C")
project_name.grid(row=1, column=0, columnspan=2, pady=10)

# URL input field
Label(root, text="Instagram Post URL:", font=("Helvetica", 12), bg="#f0f2f5").grid(row=2, column=0, sticky="e", padx=10)
url_var = StringVar()
Entry(root, textvariable=url_var, width=40, font=("Helvetica", 12)).grid(row=2, column=1, padx=10, pady=10)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=3, column=0, columnspan=2, pady=20)

# Download button with animation
def animate_button(button):
    original_bg = button.cget("bg")
    button.config(bg="#FF6F61")
    root.update_idletasks()
    root.after(200, lambda: button.config(bg=original_bg))

download_button = Button(root, text="Download", command=start_download, bg="#4CAF50", fg="white", font=("Helvetica", 12),
                          padx=20, pady=5, relief="flat", borderwidth=0, activebackground="#45A049")
download_button.grid(row=4, column=0, columnspan=2, pady=10)
download_button.bind("<Button-1>", lambda event: animate_button(download_button))

# Run the application
root.mainloop()