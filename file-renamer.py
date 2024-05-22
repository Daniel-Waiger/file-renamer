import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def get_common_parts(filenames):
    """
    Identify common parts in a list of filenames, treating words separated by underscores and periods.
    """
    parts_lists = [set(filename.replace('.', '_').split('_')) for filename in filenames]
    common_parts = set.intersection(*parts_lists)
    return {part for part in common_parts if len(part) > 1}  # Exclude trivial segments

def remove_specific_patterns(filename):
    """
    Remove specific patterns like 'A06f00d1', 'C06f00d1', 'A05f00d1' from the filename.
    """
    # Regex to match patterns like 'A06f00d1'
    pattern = re.compile(r'[A-Z]\d{2}f\d{2}d\d')
    return pattern.sub('', filename)

def clean_filename(filename):
    """
    Clean up the filename by removing double underscores and trailing underscores.
    """
    filename = re.sub(r'__+', '_', filename)  # Replace multiple underscores with a single one
    filename = filename.strip("_-")  # Remove leading/trailing underscores and hyphens
    return filename

def remove_common_parts(filenames, common_parts):
    """
    Remove common parts from filenames.
    """
    new_filenames = []
    for filename in filenames:
        name, ext = os.path.splitext(filename)  # Split the filename and its suffix
        new_name = name
        for part in common_parts:
            new_name = new_name.replace(part, "")
        new_name = clean_filename(new_name)  # Clean up the filename
        new_filenames.append(new_name + ext)  # Append the suffix back
    return new_filenames

def rename_files(input_folder, suffix_filter):
    """
    Rename files in the specified folder by removing common parts and specific patterns.
    """
    filenames = [f for f in os.listdir(input_folder) if f.endswith(suffix_filter)]
    
    if not filenames:
        print("No files found with the specified suffix in the input folder.")
        return [], []

    print(f"Original filenames: {filenames}")
    
    common_parts = get_common_parts(filenames)
    print(f"Initial common parts: {common_parts}")

    # Remove common parts once
    filenames_no_common = remove_common_parts(filenames, common_parts)
    print(f"Filenames after removing common parts: {filenames_no_common}")

    new_filenames = []
    for filename in filenames_no_common:
        name, ext = os.path.splitext(filename)  # Split the filename and its suffix
        new_name = remove_specific_patterns(name)
        new_name = clean_filename(new_name)
        new_filenames.append(new_name + ext)  # Append the suffix back

    print(f"New filenames: {new_filenames}")
    
    return filenames, new_filenames

def select_folders():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    input_folder = filedialog.askdirectory(title="Select Input Folder")
    if not input_folder:
        messagebox.showerror("Error", "No input folder selected")
        return
    
    suffix_filter = simpledialog.askstring("Input", "Enter the file suffix to filter (e.g., '.tif'):")
    if not suffix_filter:
        suffix_filter = ""
    
    old_names, new_names = rename_files(input_folder, suffix_filter)
    
    if old_names and new_names:
        preview_window = tk.Toplevel()
        preview_window.title("File Renaming Preview")
        
        text = tk.Text(preview_window)
        text.pack()
        
        text.insert(tk.END, "Old Names -> New Names\n")
        text.insert(tk.END, "----------------------\n")
        
        for old_name, new_name in zip(old_names, new_names):
            text.insert(tk.END, f"{old_name} -> {new_name}\n")

        def proceed_renaming():
            for old_name, new_name in zip(old_names, new_names):
                os.rename(os.path.join(input_folder, old_name), os.path.join(input_folder, new_name))
            messagebox.showinfo("Success", "Files have been renamed successfully")
            preview_window.destroy()

        tk.Button(preview_window, text="Proceed with Renaming", command=proceed_renaming).pack()
        tk.Button(preview_window, text="Cancel", command=preview_window.destroy).pack()

        preview_window.mainloop()

if __name__ == "__main__":
    select_folders()
