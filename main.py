import os
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "file.json"

def get_authenticated_service():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/drive'])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'file.json',
                ['https://www.googleapis.com/auth/drive']
            )
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)

def get_full_path(service, file_id):
    path = []
    current_id = file_id

    while current_id:
        try:
            file_metadata = service.files().get(fileId=current_id, fields="name, parents").execute()
            path.insert(0, file_metadata['name'])
            current_id = file_metadata.get('parents', [None])[0]
        except HttpError as error:
            print(f"An error occurred while retrieving the path: {error}")
            break

    return '/'.join(path)

def search_files_by_keyword(keyword):
    service = get_authenticated_service()
    file_info = []

    try:
        page_token = None
        while True:
            response = service.files().list(
                q=f"name contains '{keyword}'",
                spaces='drive',
                fields="nextPageToken, files(id, name)",
                pageToken=page_token
            ).execute()

            for file in response.get('files', []):
                file_path = get_full_path(service, file['id'])
                file_url = f"https://drive.google.com/file/d/{file['id']}/view?usp=sharing"
                file_info.append((file_path, file_url))

            page_token = response.get('nextPageToken', None)
            if not page_token:
                break
    
    except HttpError as error:
        print(f"An error occurred: {error}")

    return file_info

def display_results():
    keyword = simpledialog.askstring("Input", "Enter keyword to search for:", parent=root)

    if not keyword:
        messagebox.showerror("Input Error", "Please enter a keyword to search.")
        return

    file_info = search_files_by_keyword(keyword)

    result_text.delete(1.0, tk.END)

    if file_info:
        for path, url in file_info:
            result_text.insert(tk.END, f"Path: {path}\n", ("path_style",))
            url_button = ttk.Button(result_text, text="Open File", command=lambda url=url: webbrowser.open(url))
            result_text.window_create(tk.END, window=url_button)
            result_text.insert(tk.END, "\n\n")
    else:
        result_text.insert(tk.END, "No files found matching the keyword.")

def handle_click(event):
    index = result_text.index("@%s,%s" % (event.x, event.y))
    url = result_text.get(index, f"{index}+100c")  # Extract text at the clicked position

    if url.startswith("http"):  # If the clicked text is a URL, open it in a web browser
        webbrowser.open(url)

root = tk.Tk()
root.title("Google Drive File Search")
root.geometry("600x400")
root.configure(bg="#f0f8ff")

title_label = tk.Label(root, text="Google Drive File Search", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#333")
title_label.pack(pady=10)

result_text = tk.Text(root, height=15, width=60, wrap=tk.WORD, bg="#fff", fg="#333", font=("Arial", 12))
result_text.pack(pady=10)
result_text.tag_configure("link_style", foreground="blue", underline=1)
result_text.tag_bind("link_style", "<Button-1>", handle_click)
result_text.tag_configure("path_style", foreground="black", font=("Arial", 11, "italic"))

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)
style.map("TButton", background=[("active", "#0078d7")])

search_button = ttk.Button(root, text="Search Files", command=display_results)
search_button.pack(pady=5)

exit_button = ttk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=5)

root.mainloop()
