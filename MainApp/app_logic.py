import os #Built-in package
import shutil #Built-in package
import tkinter #Built-in package
import webbrowser #Built-in package
from io import BytesIO #Built-in package
from urllib.request import urlopen #Built-in package
from PIL import Image, ImageTk # pip install Pillow
import eyed3 # pip install eyed3
from mutagen.mp3 import MP3 #pip install mutagen
from mutagen.id3 import APIC, ID3, error
import webscrape #Bundled File - Webscraper code from Stackoverflow
# webscrape:
# import requests / Built-in package
# from bs4 import BeautifulSoup / pip install beautifulsoup4

def open_folder():
    """
    Opens a folder window using tkinter.
    Here the user can pick a folder directory.'

    :return: folder contents as a list
    :return: folder directory / None when FileNotFound
    """
    folder = tkinter.filedialog.askdirectory()
    try:
        folder_contents = os.listdir(folder)
    except FileNotFoundError as error:
        folder = None
        folder_contents = error
    return folder_contents, folder

def open_folder_as_list(folder):
    """
    opens a folder as a list.

    :param: folder directory
    :return: list of the contents
    """
    file_names_list = []
    for file in os.listdir(folder):
        file_names_list.append(file)
    return file_names_list

def move_files_according_to_list(source_dir, output_dir,names_list):
    """
    moves files according to a list using shutil.move

    :param: source directory
    :param: output directory
    :param: list of files to be moved
    """
    for file in names_list:
        file_location = os.path.join(source_dir,file)
        shutil.move(file_location,output_dir)

def delete_files_according_to_list(source_dir, names_list):
    """
    deletes files according to a list using os.remove

    :param: source directory
    :param: list of files to be deleted
    """
    for file in names_list:
        file_location = os.path.join(source_dir,file)
        os.remove(file_location)

def create_temp_folder(directory):
    """
    creates a temporary directory if one does not exist.
    if one exists clears the directory and creates a new one
    using shutil.rmtree

    :param: directory for the temporary folder
    :return: the directory for the temporary folder
    """
    temp_folder_dir = os.path.join(directory,"temp")
    if not os.path.exists(temp_folder_dir):
        os.makedirs(temp_folder_dir)
    else: #clean out temp folder
        if os.listdir(temp_folder_dir):
            shutil.rmtree(temp_folder_dir)
            os.makedirs(temp_folder_dir)
    return temp_folder_dir

def delete_temp_folder(directory):
    """
    deletes the temporary folder if it exists
    using shutil.rmtree .

    :param: directory for the folder
    """
    temp_folder_dir = os.path.join(directory,"temp")
    if os.path.exists(temp_folder_dir):
        shutil.rmtree(temp_folder_dir)

def delete_file_by_dir(directory):
    """
    deletes a file by it's path using os.remove

    :param: file location 
    """
    if os.path.exists(directory):
        os.remove(directory)

def clear_textbox(textbox):
    """
    clears the contents of a textbox.

    :param: textbox variable
    """
    textbox.delete("1.0", "end")

def print_list(textbox, list):
    """
    writes a list line by line into a textbox.

    :param: textbox variable
    :param: list to be printed
    """
    textbox.configure("normal")
    for item in list:
        textbox.insert("end", f"\n{item}")

def str_order(filename, string1, string_list):
    """
    Checks the order of strings inside a filename:
    Returns False if [string2] before string1 else True.

    :param: filename
    :param: string1 for example " - "
    :param: list of strings
    :return: Boolean True/False
    """
    string1_index = filename.find(string1) # " - "
    for string2 in string_list: # [" & " , " ft ", " ft. " " feat " , ","]
        string2_index = filename.lower().find(string2)
        if string2_index == -1 :
            continue
        if string1_index > string2_index:
            return False
    return True

def print_settings(textbox, input_dir, output_dir):
    """
    prints the users input and output directories into a textbox.

    :param: textbox variable
    :param: input directory
    :param: output directory
    """
    textbox.configure(state="normal")
    if input_dir != None or output_dir != None:
        textbox.insert("end",f"\nFound data from last session:")
    if input_dir != None:
        textbox.insert("end",f"\nInput is set to {input_dir}")
    if output_dir != None:
        textbox.insert("end", f"\nOutput is set to {output_dir}")
    textbox.configure(state="disabled")

def copy_files(textbox, source, destination, report=True): #copy
    """
    Copies files from input directory into output directory.
    If report = True, it prints out updates about the process
    into a textbox.
    
    :param: textbox variable
    :param: input directory
    :param: output directory
    :param: boolean True/False
    """
    Index = 0
    textbox.configure(state="normal")
    for path, _, files in os.walk(source): # _ = subdirs
        for name in files:
            Index += 1
            file_source_directory = os.path.join(path,name)
            if report:
                textbox.insert("end", f"\nFile at {file_source_directory} was moved")
            shutil.copy(file_source_directory,destination)
    if Index == 0:
        textbox.insert("end", f"\nSource folder is empty")

    textbox.configure(state="disabled")

def name_filter(textbox, source):
    """
    Filters out a list:
    Checks where the list items are .mp3
    Checks if string " - " is present
    Checks for the order of strings in check_list

    :param: textbox variable
    :param: source directory
    :return: returns a list of poorly formatted filenames
    """
    check_list = [" & " , " ft ", " ft. ", " feat "," feat. ", ","] #" x ", " with "," w "
    wrong_format_list = []
    file_names_list = open_folder_as_list(source)
    textbox.configure(state="normal")
    for file in file_names_list:
        if not file.lower().endswith(".mp3"):
            textbox.insert("end", f"\nFile: {file} not a .mp3")
            continue
        if " - " in file:
            if str_order(file," - ",check_list):
                textbox.insert("end", f"\nFile: {file} was formatted correctly")
                continue
        # File is mp3 and formatted incorrectly'
        textbox.insert("end",f"\nFile: {file} was formatted incorrectly")
        wrong_format_list.append(file)
    textbox.insert("end",f"\nFound {len(wrong_format_list)} wrongly named .mp3 files")
    textbox.insert("end",f"\nFound {len(wrong_format_list)} Click the Rename button to rename these files")
    textbox.configure(state="disabled")
    return wrong_format_list

def rename_according_to_list(textbox, source_dir, new_names_list, old_names_list):
    """
    Renames files according to a list using os.rename
    
    :param: textbox variable
    :param: source directory
    :param: old_names_list
    :param: new_names_list
    """
    textbox.configure("normal")
    if len(new_names_list) != len(old_names_list):
        textbox.insert("end",f"\nDifferent ammount of source items and renamed names - operation failed")
    else:
        for new_name, old_name in zip(old_names_list,new_names_list):
            old_file_location = os.path.join(source_dir,old_name)
            new_file_location = os.path.join(source_dir,new_name)
            try:
                os.rename(new_file_location,old_file_location)
            except Exception as error:
                textbox.insert("end",f"\nOperation Failed, error message was{error}")
    textbox.configure("disabled")

def sort_into_folders(input_folder, output_folder, filename_list):
    """
    Sorts songs into folders according to the artist.
    If no folder with the artist's name is present.
    It makes a new folder [artist]. 

    :param: input directory
    :param: output directory
    :param: list of Filenames
    """
    for file in filename_list:
        folder_name = file.split(" - ")[0]
        folder_dir = os.path.join(output_folder, folder_name.lower())
        current_location = os.path.join(input_folder,file)
        if os.path.isdir(folder_dir):
            shutil.move(current_location,folder_dir)
            print(folder_dir)
        else:
            folder_dir2 = os.path.join(output_folder,folder_name) 
            os.mkdir(folder_dir2)
            shutil.move(current_location,folder_dir)
            print("made", folder_dir)

def compare_lists(textbox, folder_list1, folder_list2):
    """
    compares to folders by their contents.

    :param: textbox variable
    :param: folder1 contents as a list
    :param: folder2 contents as a list
    """
    num_of_differences = 0
    textbox.configure(state="normal")
    for file1 in folder_list1:
        if file1 not in folder_list2:
            textbox.insert("end",f"\n{file1} not in folder2")
            textbox.see("end")
            num_of_differences += 1
    for file2 in folder_list2:
        if file2 not in folder_list1:
            textbox.insert("end",f"\n{file2} not in folder1")
            textbox.see("end")
            num_of_differences += 1
    if num_of_differences != 0:
        textbox.insert("end",f"\nFound {num_of_differences} difference(s)")
    else:
        textbox.insert("end",f"\nDidn't find any differences")
    textbox.configure(state="disabled")

def check_list_filetype(textbox, filename_list, extension):
    """
    Checks if list items end with extension variable.
    For example, files that end with .mp3

    :param: textbox variable
    :param: filenames in a list
    :param: extension string
    :return: list ending with extension variable
    """
    corrected_list = []
    for file in filename_list:
        if file.endswith(extension):
            corrected_list.append(file)
        else:
            textbox.configure(state="normal")
            textbox.insert("end",f"\nFile {file} is not a {extension}")
            textbox.configure(state="disabled")
    return corrected_list

def check_metadata(textbox, input_dir, filename_list):
    """
    Checks if mp3 file contains cover art metadata using mutagen.

    :param: textbox variable
    :param: input directory
    :param: list of filenames
    :return: list of files with no cover art
    """
    no_albumart_list = []
    for file in filename_list:
        curr_file_dir = os.path.join(input_dir,file) #Removes all metadata
        #mp3 = MP3(curr_file_dir)
        #mp3.delete()
        #mp3.save()
        audio = eyed3.load(curr_file_dir)
        print(curr_file_dir)
        try:
            audio_file = ID3(curr_file_dir)
            print(audio_file['APIC'])
            if audio.tag.images:
                textbox.configure(state="normal")
                textbox.insert("end",f"\nFile {file} already has a cover art")
                textbox.configure(state="disabled")
            else:
                no_albumart_list.append(file)
        except Exception: #No tags
            no_albumart_list.append(file)

    return no_albumart_list

def set_cover_art(input_dir, file, url):
    """
    Function that attaches a url picture into mp3 metadata
    This function is quite weak, mutagen doesn't seem to be clearing the metadata properly.
    :param: input directory
    :param: file .mp3
    :param: image url
    """
    raw_data = url_open(url)
    photo_path = os.path.join(input_dir,"coverart.jpeg")
    image = Image.open(BytesIO(raw_data)).resize((350,350))
    image.save(photo_path,"JPEG")
    filedir = os.path.join(input_dir,file)
    mp3 = MP3(filedir)
    try:
        mp3.delete()
        mp3.save()
        mp3.add_tags()
        mp3.save()
    except error as error1:
        print(error1)
        print("already has a ID3 Tag - edit anyway")
    audio_file = ID3(filedir)
    with open(photo_path, "rb") as albumart:
        audio_file['APIC'] = APIC(
            encoding=2,
            mime='image/jpeg',
            type=3,
            desc=u'Cover',
            data=albumart.read()
        )
    audio_file.save()

def search_image(filename,index):
    """
    Finds the image urls according to a bing search
    This is achieved by code copied from stackoverflow:
    https://stackoverflow.com/questions/61170959/python-image-scraper-not-working-properly-on-bing

    :param: search word e.g. filename
    :param: index for a list
    :return: url (str) using the index
    :return: whole list of url's
    """
    index2 = str(index)
    url_list = webscrape.imagescrape_keyword(filename,index2)
    return url_list[index], url_list

def url_open(url):
    """
    opens a url as raw data.

    :param: url (str)
    :return: raw_data behind url
    """
    url_open = urlopen(url)
    raw_data = url_open.read()
    url_open.close()
    return raw_data

def url_picture_conversion(url):
    """
    opens the url image into imageTK.photoimage
    :param: url (str)
    :return: photo ImageTk.Photoimage
    """
    raw_data = url_open(url)
    image = Image.open(BytesIO(raw_data)).resize((250,250))
    photo = ImageTk.PhotoImage(image)
    return photo

def open_url(url):
    webbrowser.open_new_tab(url)

    
