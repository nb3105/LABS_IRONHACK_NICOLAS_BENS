#Test 2 A_D_A
import os
import cv2
import fitz
import img2pdf
import tkinter as tk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from tkinter import filedialog
from PIL import Image

class File:
    def __init__(self, image_path, pdf_path, keywords_path):
        self.image_path = image_path
        self.pdf_path = pdf_path
        self.keywords_path = keywords_path

    def process(self):
        if self.image_path:
            processed_image_path, pdf_output_path, quality_percentage = scan_and_correct_alignment(self.image_path, self.keywords_path, 'output.pdf')
            show_processing_result(processed_image_path, pdf_output_path, quality_percentage)
            organize_file(processed_image_path)
        elif self.pdf_path:
            # Process the PDF file here
            convert_pdf_to_images(self.pdf_path, 'output_images')
            pdf_output_path = convert_images_to_pdf('output_images', 'output.pdf')
            show_processing_result('output_images', pdf_output_path, None)  # Pass None for quality_percentage
            organize_file(pdf_output_path)
        else:
            print("No file selected")

class Folder:
    def __init__(self, folder_name, keywords):
        self.folder_name = folder_name
        self.keywords = keywords

    def add_keywords(self, keyword):
        self.keywords.append(keyword)

    def remove_keyword(self, keyword):
        if keyword in self.keywords:
            self.keywords.remove(keyword)

def convert_images_to_pdf(images_folder, output_pdf_path):
    image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print("No image files found.")
        return None

    image_files.sort()

    pdf_path = output_pdf_path

    with open(pdf_path, "wb") as pdf_file:
        canvas = Canvas(pdf_file, pagesize=letter)

        for image_file in image_files:
            image_path = os.path.join(images_folder, image_file)
            image = Image.open(image_path)
            width, height = letter
            canvas.setPageSize((width, height))
            canvas.drawInlineImage(image, 0, 0, width, height)
            canvas.showPage()

    print(f"PDF created successfully: {pdf_path}")
    return pdf_path


def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path.set(file_path)
            # Process the image file here if needed
        elif file_path.lower().endswith('.pdf'):
            pdf_path.set(file_path)
            # Process the PDF file here if needed
        else:
            print("Unsupported file format")

def calculate_quality_percentage(image):
    try:
        import pytesseract

        def read_and_calculate_quality(img):
            text = pytesseract.image_to_string(img, config='--psm 6')
            quality_percentage = sum(c.isalpha() for c in text) / len(text) * 100 if text else 0
            return quality_percentage

        top_left_quality = read_and_calculate_quality(image)
        top_right_quality = read_and_calculate_quality(cv2.flip(image, 1))
        bottom_left_quality = read_and_calculate_quality(cv2.flip(image, 0))
        bottom_right_quality = read_and_calculate_quality(cv2.flip(image, -1))

        average_quality = (top_left_quality + top_right_quality + bottom_left_quality + bottom_right_quality) / 4

        return average_quality

    except Exception as e:
        print(f"Error calculating quality percentage: {e}")
        return 0

def save_file(image_path, folder_path, file_name):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    output_path = os.path.join(folder_path, file_name)
    cv2.imwrite(output_path, cv2.imread(image_path))


def scan_and_correct_alignment(image_path, keywords_path, pdf_path):
    aligned_document = cv2.imread(image_path)
    try:
        average_quality = calculate_quality_percentage(aligned_document)
        quality_threshold = 0

        if average_quality is None or average_quality < quality_threshold:
            raise Exception(f"Document quality is low (Average quality: {average_quality:.2f}%). Please load a new one.")

         # Create the 'output_images' directory if it doesn't exist
        output_images_folder = 'output_images'
        os.makedirs(output_images_folder, exist_ok=True)

        #convert_images_to_pdf('output_images', 'output.pdf')

        # Process the image and save it to 'output_images'
        processed_image_path = os.path.join(output_images_folder, 'processed_image.jpg')
        cv2.imwrite(processed_image_path, aligned_document)

        # Convert 'output_images' to PDF
        pdf_output_path = convert_images_to_pdf(output_images_folder, 'output.pdf')

        # Display the processing result
        show_processing_result(processed_image_path, pdf_output_path, average_quality)

        pdf_document = fitz.open(pdf_output_path)
        page = pdf_document[0]
        text_to_search = "Your desired text"
        found_text = page.search_for(text_to_search)

        if found_text:
            keyword = input("Enter a keyword for the file: ")
            folder_name = get_folder_for_keyword(keyword, keywords_path)
            folder_path = os.path.join(base_directory, folder_name)

            save_file(image_path, folder_path, f"{keyword}_output.jpg")
            print(f"File saved in folder: {folder_path}")

        pdf_document.close()

        return average_quality

    except Exception as e:
        print(f"Error processing image: {e}")
        return None, None, None     


def get_folder_for_keyword(keyword, keywords_path):
    with open(keywords_path, 'r') as keywords_file:
        lines = keywords_file.readlines()

    for line in lines:
        if keyword in line:
            return line.strip()

    return "default_folder"

def organize_file(file_path):
    if os.path.exists(file_path):
        try:
            keywords = extract_keywords(file_path)

            # Find the folder with the most matching keywords
            best_match_folder = find_best_match_folder(keywords)

            if best_match_folder:
                move_file(file_path, best_match_folder)
                print(f"File moved to folder: {best_match_folder}")
            else:
                print("No matching folder found.")
        except Exception as e:
            print(f"Error organizing file: {e}")

def extract_keywords(file_path):
    # Extract keywords from the file (modify this based on your file content)
    # For example, if the file is a text file, you can read the content and extract keywords
    # For now, we assume the file name itself contains keywords
    file_name = os.path.basename(file_path)
    keywords = [keyword.strip().lower() for keyword in file_name.split('_') if keyword]

    return keywords

def find_best_match_folder(file_keywords):
    # Loop through folders and calculate the match score
    max_score = -1
    best_match_folder = None

    for folder_name, folder_keywords in get_folders_with_keywords().items():
        match_score = calculate_match_score(file_keywords, folder_keywords)
        
        if match_score > max_score:
            max_score = match_score
            best_match_folder = folder_name

    return best_match_folder

def get_folders_with_keywords():
    folders_with_keywords = {}

    for folder_name in os.listdir(base_directory):
        folder_path = os.path.join(base_directory, folder_name)

        if os.path.isdir(folder_path):
            keywords_file_path = os.path.join(folder_path, 'KWords.txt')

            if os.path.exists(keywords_file_path):
                with open(keywords_file_path, 'r') as keywords_file:
                    folder_keywords = [line.strip().lower() for line in keywords_file.readlines()]
                    folders_with_keywords[folder_name] = folder_keywords

    return folders_with_keywords

def calculate_match_score(file_keywords, folder_keywords):
    common_keywords = set(file_keywords).intersection(folder_keywords)
    match_score = len(common_keywords) / len(file_keywords) * 100 if file_keywords else 0
    return match_score

def move_file(file_path, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    file_name = os.path.basename(file_path)
    destination_path = os.path.join(destination_folder, file_name)

    os.rename(file_path, destination_path)

# def show_processing_result(processed_image_path, pdf_output_path, quality_percentage):
#     result_window = tk.Toplevel()
#     result_window.title("Processing Result")

#     tk.Label(result_window, text="Processing Result", font=("Helvetica", 14)).pack(pady=10)

#     if quality_percentage is not None:
#         tk.Label(result_window, text=f"Quality Percentage: {quality_percentage:.2f}%").pack(pady=10)
#     else:
#         tk.Label(result_window, text="Error in processing image quality").pack(pady=10)

#     tk.Label(result_window, text=f"Processed Image Link: {processed_image_path}").pack(pady=10)

#     old_image = tk.PhotoImage(file=image_path.get())
#     new_image = tk.PhotoImage(file=processed_image_path)

#     tk.Label(result_window, image=old_image).pack(side="left", padx=10)
#     tk.Label(result_window, image=new_image).pack(side="right", padx=10)

#     tk.Button(result_window, text="Try Again", command=result_window.destroy).pack(side="left", pady=10, padx=10)
#     tk.Button(result_window, text="Save", command=lambda: open_folder(pdf_output_path)).pack(side="right", pady=10, padx=10)

def show_processing_result(processed_image_path, pdf_output_path, quality_percentage):
    result_window = tk.Toplevel()
    result_window.title("Processing Result")

    tk.Label(result_window, text="Processing Result", font=("Helvetica", 14)).pack(pady=10)

    if quality_percentage is not None:
        tk.Label(result_window, text=f"Quality Percentage: {quality_percentage:.2f}%").pack(pady=10)
    else:
        tk.Label(result_window, text="Error in processing image quality").pack(pady=10)

    tk.Label(result_window, text=f"Processed Image Link: {processed_image_path}").pack(pady=10)

    try:
        # Attempt to open the old image
        old_image = tk.PhotoImage(file=processed_image_path)
        tk.Label(result_window, image=old_image).pack(side="left", padx=10)
    except Exception as e:
        print(f"Error opening old image: {e}")

    try:
        # Attempt to open the new image
        new_image = tk.PhotoImage(file=pdf_output_path)
        tk.Label(result_window, image=new_image).pack(side="right", padx=10)
    except Exception as e:
        print(f"Error opening new image: {e}")

    tk.Button(result_window, text="Try Again", command=result_window.destroy).pack(side="left", pady=10, padx=10)
    tk.Button(result_window, text="Save", command=lambda: open_directory()).pack(side="right", pady=10, padx=10)

def open_directory():
    #browse_directory()
    os.system(f'explorer "{base_directory}"')

def process_files():
    file_obj = File(image_path.get(), pdf_path.get(), keywords_path)
    file_obj.process()

def create_directory_structure():
    main_folder = "A_S_F"

    if not os.path.exists(main_folder):
        os.makedirs(main_folder)

    base_directory = os.path.join(main_folder)

    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    global keywords_path
    keywords_path = os.path.join(base_directory, 'keywords.txt')

    if not os.path.exists(keywords_path):
        with open(keywords_path, 'w') as keywords_file:
            keywords_file.write("default_folder\n")

    return base_directory, keywords_path

def open_folder_creation_window():
    folder_window = tk.Toplevel(window)
    folder_window.title("New Folder")

    tk.Label(folder_window, text="Folder Name:").pack(pady=10)
    folder_name_entry = tk.Entry(folder_window)
    folder_name_entry.pack(pady=10)

    tk.Label(folder_window, text="Keywords (comma-separated):").pack(pady=10)
    keywords_entry = tk.Entry(folder_window)
    keywords_entry.pack(pady=10)

    add_folder_command = lambda: add_folder(folder_window, folder_name_entry, keywords_entry)

    tk.Button(folder_window, text="Add Folder", command=add_folder_command).pack(pady=10)
    tk.Button(folder_window, text="Exit", command=folder_window.destroy).pack(pady=10)

def add_folder(folder_window, folder_name_entry, keywords_entry):
    folder_name = folder_name_entry.get()
    keywords = keywords_entry.get().split(',')
    new_folder = Folder(folder_name, keywords)

    # Get the current working directory
    current_directory = os.getcwd() + '\A_S_F'

    # Create the path for the new folder in the current directory
    folder_path = os.path.join(current_directory, new_folder.folder_name)

    try:
        # Create the folder
        os.makedirs(folder_path)
        print(f"Folder '{new_folder.folder_name}' created successfully.")
        print(f"Keywords: {new_folder.keywords}")

        # Save keywords to a .txt file in the created folder
        keywords_file_path = os.path.join(folder_path, 'KWords.txt')
        with open(keywords_file_path, 'w') as keywords_file:
            keywords_file.write('\n'.join(new_folder.keywords))
        print(f"Keywords saved to {keywords_file_path}")
    except OSError as e:
        print(f"Failed to create folder '{new_folder.folder_name}': {e}")

    folder_window.destroy()



def open_keywords_window():
    global selected_folder  # Declare selected_folder as global

    # Function to update keywords in the selected folder
    def update_keywords(event = None):
        new_keywords = keywords_entry.get().split(',')
        for keyword in new_keywords:
            keyword = keyword.strip()
            if keyword and keyword not in selected_folder.keywords:
                selected_folder.add_keywords(keyword.strip())
                update_keywords_display()
                keywords_entry.delete(0, 'end')
            else: pass
        #update_keywords_display()
        #keywords_entry.delete(0, 'end')

    # Function to update the displayed keywords
    def update_keywords_display():
        current_keywords_text.set(' | '.join(selected_folder.keywords))

    # Function to remove a keyword
    def remove_keyword(event=None):
        keyword_to_remove = keyword_to_remove_entry.get().strip()
        if keyword_to_remove and keyword_to_remove in selected_folder.keywords:
            selected_folder.remove_keyword(keyword_to_remove)
            update_keywords_display()
            keyword_to_remove_entry.delete(0, 'end')
        else: pass

    # Set the initial directory for the file dialog
    initial_directory = os.getcwd() + '\A_S_F'  # Set your desired initial directory here

    # Open file dialog to select a folder
    folder_path = filedialog.askdirectory(title="Select a folder", initialdir=initial_directory)
    if folder_path:
        # Get folder name from the path
        folder_name = os.path.basename(folder_path)

        # Create or retrieve Folder instance
        selected_folder = Folder(folder_name, [])

        # Check for KWords.txt file and read existing keywords
        kwords_file_path = os.path.join(folder_path, 'KWords.txt')
        if os.path.exists(kwords_file_path):
            with open(kwords_file_path, 'r') as kwords_file:
                selected_folder.keywords = [line.strip() for line in kwords_file.readlines()]

        # Create a new window for keyword management
        keywords_window = tk.Toplevel(window)
        keywords_window.title(f"Manage Keywords for {selected_folder.folder_name}")

        # Display current keywords
        current_keywords_text = tk.StringVar()
        tk.Label(keywords_window, text="Current Keywords:").pack(pady=10)
        tk.Label(keywords_window, textvariable=current_keywords_text).pack(pady=10)
        update_keywords_display()

        # Entry for adding new keywords
        tk.Label(keywords_window, text="Add Keywords (comma-separated):").pack(pady=10)
        keywords_entry = tk.Entry(keywords_window)
        keywords_entry.pack(pady=10)
        tk.Button(keywords_window, text="Add Keywords", command=update_keywords).pack(pady=10)
        keywords_entry.bind('<Return>', lambda event=None: update_keywords())

        #keywords_entry.bind('<Return>', update_keywords)  # Bind Enter key to update_keywords function


        # Button to add new keywords
        #tk.Button(keywords_window, text="Add Keywords", command=update_keywords).pack(pady=10)

        # Entry for removing keywords
        tk.Label(keywords_window, text="Remove Keyword:").pack(pady=10)
        keyword_to_remove_entry = tk.Entry(keywords_window)
        keyword_to_remove_entry.pack(pady=10)
        tk.Button(keywords_window, text="Remove Keyword", command=remove_keyword).pack(pady=10)
        keyword_to_remove_entry.bind('<Return>', lambda event=None: remove_keyword())
        #keywords_entry.bind('<Return>', remove_keyword)  # Bind Enter key to remove_keyword function


        # Button to remove keywords
        #tk.Button(keywords_window, text="Remove Keyword", command=remove_keyword).pack(pady=10)
    else:
        # User canceled folder selection, you can add an optional message or action here
        print("Folder selection canceled.")
        
    """if folder_path:
        # Get folder name from the path
        folder_name = os.path.basename(folder_path)

        # Create or retrieve Folder instance
        selected_folder = Folder(folder_name, [])

        # Check for KWords.txt file and read existing keywords
        kwords_file_path = os.path.join(folder_path, 'KWords.txt')
        if os.path.exists(kwords_file_path):
            with open(kwords_file_path, 'r') as kwords_file:
                selected_folder.keywords = [line.strip() for line in kwords_file.readlines()]

        # Create a new window for keyword management
        keywords_window = tk.Toplevel(window)
        keywords_window.title(f"Manage Keywords for {selected_folder.folder_name}")

        # Display current keywords
        current_keywords_text = tk.StringVar()
        tk.Label(keywords_window, text="Current Keywords:").pack(pady=10)
        tk.Label(keywords_window, textvariable=current_keywords_text).pack(pady=10)
        update_keywords_display()

        # Entry for adding new keywords
        tk.Label(keywords_window, text="Add Keywords (comma-separated):").pack(pady=10)
        keywords_entry = tk.Entry(keywords_window)
        keywords_entry.pack(pady=10)

        # Button to add new keywords
        tk.Button(keywords_window, text="Add Keywords", command=update_keywords).pack(pady=10)

        # Entry for removing keywords
        tk.Label(keywords_window, text="Remove Keyword:").pack(pady=10)
        keyword_to_remove_entry = tk.Entry(keywords_window)
        keyword_to_remove_entry.pack(pady=10)

        # Button to remove keywords
        tk.Button(keywords_window, text="Remove Keyword", command=remove_keyword).pack(pady=10)
"""



    # # Function to delete a keyword
    # def delete_selected_keyword():
    #     selected_keyword = output_text.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
    #     if selected_keyword:
    #         selected_folder.remove_keyword(selected_keyword)
    #         update_keywords_display()

    # # Set the initial directory for the file dialog
    # initial_directory = os.getcwd() + '\A_S_F'  # Set your desired initial directory here

    # # Open file dialog to select a folder
    # folder_path = filedialog.askdirectory(title="Select a folder", initialdir=initial_directory)
    # if folder_path:
    #     # Get folder name from the path
    #     folder_name = os.path.basename(folder_path)

    #     # Create or retrieve Folder instance
    #     selected_folder = Folder(folder_name, [])

    #     # Create a new window for keyword management
    #     keywords_window = tk.Toplevel(window)
    #     keywords_window.title(f"Manage Keywords for {selected_folder.folder_name}")

    #     # Display current keywords
    #     current_keywords_text = tk.StringVar()
    #     tk.Label(keywords_window, text="Current Keywords:").pack(pady=10)
    #     tk.Label(keywords_window, textvariable=current_keywords_text).pack(pady=10)
    #     update_keywords_display()

    #     # Entry for adding new keywords
    #     tk.Label(keywords_window, text="Add Keywords (comma-separated):").pack(pady=10)
    #     keywords_entry = tk.Entry(keywords_window)
    #     keywords_entry.pack(pady=10)

    #     # Button to add new keywords
    #     tk.Button(keywords_window, text="Add Keywords", command=lambda: update_keywords(selected_folder)).pack(pady=10)

    #     # Entry for removing keywords
    #     tk.Label(keywords_window, text="Remove Keyword:").pack(pady=10)
    #     keyword_to_remove_entry = tk.Entry(keywords_window)
    #     keyword_to_remove_entry.pack(pady=10)

    #     # Button to remove keywords
    #     tk.Button(keywords_window, text="Remove Keyword", command=lambda: remove_keyword(selected_folder)).pack(pady=10)

    #     # Output window for keywords
    #     tk.Label(keywords_window, text="Keyword List:").pack(pady=10)
    #     output_text = tk.Text(keywords_window, height=10, width=30, state=tk.DISABLED)
    #     output_text.pack(pady=10)

    #     # Button to delete selected keyword
    #     tk.Button(keywords_window, text="Delete Selected Keyword", command=delete_selected_keyword).pack(pady=10)



# Create and pack widgets
window = tk.Tk()
window.title("File Organizer")

image_path = tk.StringVar()
pdf_path = tk.StringVar()
keywords_path = None
selected_folder = None
base_directory, keywords_path = create_directory_structure()

tk.Label(window, text="File Organizer", font=("Helvetica", 16)).pack(pady=10)
tk.Button(window, text="Open Directory", command=open_directory).pack(pady=10)
tk.Button(window, text="Add a Document", command=open_directory).pack(pady=10)
tk.Button(window, text="Add Photo", command=lambda: open_file_dialog()).pack(pady=10)
tk.Button(window, text="Add PDF File", command=lambda: open_file_dialog()).pack(pady=10)
tk.Button(window, text="New Folder", command=open_folder_creation_window).pack(pady=10)
# Button to open the keyword management window
tk.Button(window, text="Manage Keywords", command=open_keywords_window).pack(pady=10)

tk.Entry(window, textvariable=image_path, state='readonly').pack(pady=10)
tk.Entry(window, textvariable=pdf_path, state='readonly').pack(pady=10)

tk.Button(window, text="Process Files", command=process_files).pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
