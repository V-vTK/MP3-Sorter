# App libraries

import os #Built-in package
import json #Built-in package
from PIL import Image # pip install Pillow
import customtkinter #pip install customtkinter
import app_logic as lg #bundled module 
### app_logic - Requires more libraries: ###
"""
# import shutil #Built-in package
# import tkinter #Built-in package
# import webbrowser #Built-in package
# from io import BytesIO #Built-in package
# from urllib.request import urlopen #Built-in package
# from PIL import Image, ImageTk # pip install Pillow
# import mutagen #pip install mutagen

Contains an imported file: #bundled module 
import webscrape:
# import requests / Built-in package
# from bs4 import BeautifulSoup / pip install beautifulsoup4
"""

# Dictionary for saving settings

app_state_dictionary = {
    "appearance_mode" : "dark",
    "color_theme" : "dark-blue",
    "home_textbox" : None,
    "metadata_textbox" : None,
    "metadata_textbox2" : None,
    "metadata_imagebox" : None,
    "metadata_image" : None,
    "metadata_image_url_list" : None,
    "metadata_image_index" : 0,
    "folder_textbox" : None,
    "input_directory" : None,
    "output_directory" : None,
    "incorrect_file_names" : None,
    "metadata_filename_list" : None,
    "folder_compare_directory1" : None,
    "folder_compare_directory2" : None
}

# Functions that read/write to permanent storage

def Json_read_state_data():
    '''Imports past settings from a json file'''
    with open("app_state.json") as file:
        data = json.load(file)
        app_state_dictionary["appearance_mode"] = data["appearance_mode"]
        app_state_dictionary["input_directory"] = data["input_directory"]
        app_state_dictionary["output_directory"] = data["output_directory"]
        app_state_dictionary["color_theme"] =  data["color_theme"]

def update_json():
    '''Exports current settings to a json file'''
    json_dict = {
        "appearance_mode" : app_state_dictionary["appearance_mode"],
        "color_theme" : app_state_dictionary["color_theme"],
        "input_directory" : app_state_dictionary["input_directory"],
        "output_directory" : app_state_dictionary["output_directory"]
    }
    json_object = json.dumps(json_dict, indent=4)
    with open("app_state.json","w") as file:
        file.write(json_object)

Json_read_state_data()


# Main UI

customtkinter.set_appearance_mode(app_state_dictionary["appearance_mode"])
customtkinter.set_default_color_theme(app_state_dictionary["color_theme"])

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        ### Initialize User Interface ###

        # Window config
        self.title("MP3Sorter")
        self.geometry(f"{1600}x{800}")

        # configure grid layout (1x2)
        self.grid_rowconfigure(0, weight=1) #0
        self.grid_columnconfigure(1, weight=1) #

        # load images 
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "media")
        self.test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "MusicLogo.jpg")), size=(250, 250))


        "Home - first frame"

        # Create Navigation sidebar (left)
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.navigation_frame, text="MP3Sorter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(2, weight=1)
        self.home_frame.grid_rowconfigure(2, weight=1)

        # create sidebar options (right)
        self.label_settings = customtkinter.CTkLabel(self.home_frame, text="Settings", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_settings.grid(row=0, column=2, padx=(0,50), pady=(20, 0), sticky="EN")

        self.home_frame_input_folder = customtkinter.CTkButton(self.home_frame, text="Input Folder", command=self.control_input_folder)
        self.home_frame_input_folder.grid(row=0, column=2, padx=20, pady=(60,0), sticky="EN")

        self.home_frame_output_folder = customtkinter.CTkButton(self.home_frame, text="Output Folder", command=self.control_output_folder)
        self.home_frame_output_folder.grid(row=0, column=2, padx=20, pady=(100,0), sticky="EN")

        self.home_frame_theme = customtkinter.CTkButton(self.home_frame, text="Theme", command=self.appearance_change)
        self.home_frame_theme.grid(row=0, column=2, padx=20, pady=(140,0), sticky="EN")

        # Home - Create user instructions
        self.label_features = customtkinter.CTkLabel(self.home_frame, text="Features:", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.label_features.grid(row=0, column=2, pady=(30, 0), sticky="N")

        self.label_feature_nameformat = customtkinter.CTkLabel(self.home_frame, text="NameFormat: Identifies non-conforming [Artist - Song] files.", font=customtkinter.CTkFont(size=22))
        self.label_feature_nameformat.grid(row=0, column=2, pady=(90, 0), sticky="N")

        self.label_feature_metadatalink = customtkinter.CTkLabel(self.home_frame, text="MetaDataLink: Associates a thumbnail image with each individual song.", font=customtkinter.CTkFont(size=22))
        self.label_feature_metadatalink.grid(row=0, column=2, pady=(130, 0), sticky="N")

        self.label_feature_foldersort = customtkinter.CTkLabel(self.home_frame, text="FolderSort: Organizes songs into folders based on artist.", font=customtkinter.CTkFont(size=22))
        self.label_feature_foldersort.grid(row=0, column=2, pady=(170, 0), sticky="N")

        self.label_instruction1 = customtkinter.CTkLabel(self.home_frame, text="Instructions:", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.label_instruction1.grid(row=0, column=2, pady=(220, 0), sticky="N")

        self.label_instruction2 = customtkinter.CTkLabel(self.home_frame, text="1. Choose input and output folders", font=customtkinter.CTkFont(size=22))
        self.label_instruction2.grid(row=0, column=2, pady=(260, 0), sticky="N")

        self.label_instruction3 = customtkinter.CTkLabel(self.home_frame, text="2. Choose a functionality", font=customtkinter.CTkFont(size=22))
        self.label_instruction3.grid(row=0, column=2, pady=(290, 0), sticky="N")
        
        self.label_instruction4 = customtkinter.CTkLabel(self.home_frame, text="3. More instructions at: ", font=customtkinter.CTkFont(size=22))
        self.label_instruction4.grid(row=0, column=2, pady=(320, 0), sticky="N")

        self.label_github_link = customtkinter.CTkLabel(self.home_frame, text="https://github.com/V-vTK", font=customtkinter.CTkFont(size=16), cursor= "hand2")
        self.label_github_link.grid(row=0, column=2, pady=(350, 0), sticky="N")
        self.label_github_link.bind("<Button-1>", lambda e:lg.open_url("https://github.com/V-vTK"))

        #Home - Texbox Label
        self.label_text = customtkinter.CTkLabel(self.home_frame, text="Console", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_text.grid(row=3, column=2, padx=(0, 0), pady=(0,380), sticky="S")
        
        # Home - TextBox
        self.textbox = customtkinter.CTkTextbox(self.home_frame, width=750, height=300)
        self.textbox.grid(row=3, column=2, padx=(0, 0), pady=(0, 50))
        app_state_dictionary["home_textbox"] = self.textbox
        self.textbox.insert("0.0", "Hello, This is your console")
        lg.print_settings(
            app_state_dictionary["home_textbox"],
            app_state_dictionary["input_directory"],
            app_state_dictionary["output_directory"]
        )


        "NameFormat - Second frame"

        # create second frame - NameFormat
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(1, weight=1)
        self.second_frame.grid_rowconfigure(1, weight=1)

        # second frame - Title
        self.name_namesorter = customtkinter.CTkLabel(self.second_frame, text="Name Sorter", font=customtkinter.CTkFont(size=34, weight="bold"))
        self.name_namesorter.grid(row=0, column=0, pady=(50, 0), padx=(93,20), sticky="NW")

        self.logo_name_sortmethod = customtkinter.CTkLabel(self.second_frame, text="Sort Method", font=customtkinter.CTkFont(size=28, weight="bold"))
        self.logo_name_sortmethod.grid(row=1, column=0, pady=(100, 0), padx=(110,20), sticky="NW")

        self.logo_name_label1 = customtkinter.CTkLabel(self.second_frame, text="Artist - Song", font=customtkinter.CTkFont(size=18))
        self.logo_name_label1.grid(row=1, column=0, pady=(145, 0), padx=(145,20), sticky="NW")

        self.logo_name_label2 = customtkinter.CTkLabel(self.second_frame, text="Must not contain:", font=customtkinter.CTkFont(size=18))
        self.logo_name_label2.grid(row=1, column=0, pady=(180, 0), padx=(130,20), sticky="NW")

        self.logo_name_label3 = customtkinter.CTkLabel(self.second_frame, text="ft, ft., feat. or &", font=customtkinter.CTkFont(size=18))
        self.logo_name_label3.grid(row=1, column=0, pady=(220, 0), padx=(135,20), sticky="NW")

        self.logo_name_label4 = customtkinter.CTkLabel(self.second_frame, text="Before ' - ' ", font=customtkinter.CTkFont(size=18))
        self.logo_name_label4.grid(row=1, column=0, pady=(260, 0), padx=(155,20), sticky="NW")

        self.logo_name_console1 = customtkinter.CTkLabel(self.second_frame, text="Console", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_name_console1.grid(row=0, column=1, pady=(50, 0), padx=(0,20), sticky="N")

        self.logo_name_browse_folders = customtkinter.CTkLabel(self.second_frame, text="Browse Folders", font=customtkinter.CTkFont(size=34, weight="bold"))
        self.logo_name_browse_folders.grid(row=1, column=0, pady=(0, 190), padx=(65,20), sticky="SW")

        # second frame - Textbox
        self.name_textbox = customtkinter.CTkTextbox(self.second_frame, width=1000, height=1600, font=("TkDefaultFont",16))
        self.name_textbox.grid(row=1, column=1, padx=(0, 50), pady=(20, 40), sticky="N")
        app_state_dictionary["name_textbox"] = self.name_textbox
        self.name_textbox.insert("0.0", "Hello, This is your console")
        self.name_textbox.configure(state="disabled")

        # second frame - Button
        self.name_filter = customtkinter.CTkButton(self.second_frame, text="Filter", command=self.control_name_sorter)
        self.name_filter.grid(row=1, column=0, padx=(43,0), pady=(20,0), sticky="NW")

        self.name_rename = customtkinter.CTkButton(self.second_frame, text="Rename", command=self.control_user_rename)
        self.name_rename.grid(row=1, column=0, padx=(203,0), pady=(20,0), sticky="NW")

        self.name_input = customtkinter.CTkButton(self.second_frame, text="Input", command=self.browse_folder_input)
        self.name_input.grid(row=1, column=0, padx=(40,0), pady=(20,140), sticky="SW")  

        self.name_output = customtkinter.CTkButton(self.second_frame, text="Output", command=self.browse_folder_output)
        self.name_output.grid(row=1, column=0, padx=(200,0), pady=(20,140), sticky="SW")  

        # second frame - Instructions

        self.logo_instructions1 = customtkinter.CTkLabel(self.second_frame, text="1. Filter - Gather improperly named songs.", font=customtkinter.CTkFont(size=20))
        self.logo_instructions1.grid(row=1, column=0, padx=(30, 0), pady=(0, 70), sticky="WS")
        
        self.logo_instructions2 = customtkinter.CTkLabel(self.second_frame, text="2. Rename - Prints a list of collected songs for editing", font=customtkinter.CTkFont(size=20))
        self.logo_instructions2.grid(row=1, column=0, padx=(30, 40), pady=(0, 40), sticky="WS")


        "MetaDataLink - Third frame"

        # create third frame - MetaDataLink
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(1, weight=1)
        self.third_frame.grid_rowconfigure(1, weight=1)

        # third frame - Title
        self.metadatalink_label_console = customtkinter.CTkLabel(self.third_frame, text="Console", font=customtkinter.CTkFont(size=26, weight="bold"))
        self.metadatalink_label_console.grid(row=0, column=1, padx=(50, 90), pady=(30, 15), sticky="N")

        self.logo_metadatalink_label1 = customtkinter.CTkLabel(self.third_frame, text="Metadata Management", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_metadatalink_label1.grid(row=0, column=0, padx=(90, 0), pady=(20, 0), sticky="NW")

        # third frame - Imagebox
        self.metadata_imagebox = customtkinter.CTkLabel(self.third_frame, text="", image=self.test_image)
        self.metadata_imagebox.grid(row=1, column=0, padx=(120,250), pady=30, sticky="N")
        app_state_dictionary["metadata_imagebox"] = self.metadata_imagebox

        # third frame - Textbox
        self.metadata_textbox = customtkinter.CTkTextbox(self.third_frame, width=1600, height=1720)
        self.metadata_textbox.grid(row=1, column=1, padx=(0, 50), pady=(0, 50), sticky="E")
        app_state_dictionary["metadata_textbox"] = self.metadata_textbox
        self.metadata_textbox.insert("0.0", "Hello, This is your console")
        self.metadata_textbox.configure(state="disabled")

        self.metadata_textbox2 = customtkinter.CTkTextbox(self.third_frame, width=375, height=30, activate_scrollbars=False)
        self.metadata_textbox2.grid(row=1, column=0, padx=(65, 200), pady=(300, 20), sticky="N")
        app_state_dictionary["metadata_textbox2"] = self.metadata_textbox2
        self.metadata_textbox2.insert("0.0", "Filenames will appear here")
        self.metadata_textbox2.configure(state="disabled")

        # third frame - Buttons
        self.metadata_button_no = customtkinter.CTkButton(self.third_frame, text="NO", width=50, height=50, fg_color=("#a60d0d"), hover_color=("red", "darkred"), command=self.metadata_no)
        self.metadata_button_no.grid(row=1, column=0, padx=(30,400), pady=(370,10), sticky="N")

        self.metadata_button_skip = customtkinter.CTkButton(self.third_frame, text="Skip", width=75, height=50, fg_color=("#575b61"), hover_color=("#383b40"), command=self.metadata_skip)
        self.metadata_button_skip.grid(row=1, column=0, padx=(30,160), pady=(370,10), sticky="N")  

        self.metadata_button_ok = customtkinter.CTkButton(self.third_frame, text="OK", width=50, height=50, fg_color="green", hover_color=("green", "darkgreen"), command=self.metadata_ok)
        self.metadata_button_ok.grid(row=1, column=0, padx=(180,70), pady=(370,10), sticky="N")

        self.metadata_button_start = customtkinter.CTkButton(self.third_frame, text="Start", width=100, height=60, command=self.control_metadata_sort)
        self.metadata_button_start.grid(row=1, column=0, padx=(30,160), pady=(480,10), sticky="N")

        # third frame - Instuctions

        self.logo_metadatalink_label2 = customtkinter.CTkLabel(self.third_frame, text="Start - Finds all MP3's lacking cover art and suggest images for them.", font=customtkinter.CTkFont(size=18))
        self.logo_metadatalink_label2.grid(row=1, column=0, padx=(30, 0), pady=(0, 130), sticky="WS")

        self.logo_metadatalink_label3 = customtkinter.CTkLabel(self.third_frame, text="No - Finds another picture | Back - undoes this", font=customtkinter.CTkFont(size=18))
        self.logo_metadatalink_label3.grid(row=1, column=0, padx=(30, 0), pady=(0, 100), sticky="WS")

        self.logo_metadatalink_label4 = customtkinter.CTkLabel(self.third_frame, text="Yes - links the current picture to the mp3 metadata", font=customtkinter.CTkFont(size=18))
        self.logo_metadatalink_label4.grid(row=1, column=0, padx=(30, 40), pady=(0, 70), sticky="WS")

        self.logo_metadatalink_label5 = customtkinter.CTkLabel(self.third_frame, text="For better results use this after NameFormatter", font=customtkinter.CTkFont(size=18))
        self.logo_metadatalink_label5.grid(row=1, column=0, padx=(30, 0), pady=(0, 40), sticky="WS")

        "FolderSort - Fourth frame"

        # create fourth frame - FolderSort
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fourth_frame.grid_columnconfigure(1, weight=1)
        self.fourth_frame.grid_rowconfigure(1, weight=1)
        
        # fourth frame - Title
        self.logo_foldersort_label1 = customtkinter.CTkLabel(self.fourth_frame, text="Folder Management", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_foldersort_label1.grid(row=0, column=0, padx=(90, 0), pady=(20, 0), sticky="NW")

        self.logo_foldersort_label2 = customtkinter.CTkLabel(self.fourth_frame, text="File Management", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_foldersort_label2.grid(row=1, column=0, padx=(105, 0), pady=(110, 0), sticky="NW")
    
        self.logo_foldersort_label3 = customtkinter.CTkLabel(self.fourth_frame, text="Folder Compare", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_foldersort_label3.grid(row=1, column=0, padx=(115, 0), pady=(270, 0), sticky="NW")

        self.logo_foldersort_label4 = customtkinter.CTkLabel(self.fourth_frame, text="Console", font=customtkinter.CTkFont(size=26, weight="bold"))
        self.logo_foldersort_label4.grid(row=0, column=1, padx=(50, 90), pady=(30, 15), sticky="N")

        self.logo_foldersort_label5 = customtkinter.CTkLabel(self.fourth_frame, text="Coming Soon", font=customtkinter.CTkFont(size=16))
        self.logo_foldersort_label5.grid(row=1, column=0, padx=(180, 0), pady=(180, 0), sticky="NW")

        self.logo_foldersort_label6 = customtkinter.CTkLabel(self.fourth_frame, text="Browse Folders", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_foldersort_label6.grid(row=1, column=0, padx=(120, 0), pady=(20,210), sticky="SW")

        # fourth frame - Textbox
        self.folder_textbox = customtkinter.CTkTextbox(self.fourth_frame, width=1600, height=1720)
        self.folder_textbox.grid(row=1, column=1, padx=(0, 50), pady=(0, 50), sticky="E")
        app_state_dictionary["folder_textbox"] = self.folder_textbox
        self.folder_textbox.insert("0.0", "Hello, This is your console")
        self.folder_textbox.configure(state="disabled")

        # fourth frame - Buttons
        self.folder_unpack = customtkinter.CTkButton(self.fourth_frame, text="Folder Unpack", command=self.control_unpack_folder)
        self.folder_unpack.grid(row=1, column=0, padx=60, pady=(30,0), sticky="NW")  

        self.folder_pack = customtkinter.CTkButton(self.fourth_frame, text="Folder Pack", command=self.control_folder_pack)
        self.folder_pack.grid(row=1, column=0, padx=260, pady=(30,0), sticky="NW")

        # # # Coming in the future # # #
        # self.folder_unpack = customtkinter.CTkButton(self.fourth_frame, text="Remove Duplicates", command=self.control_unpack_folder) coming soon
        # self.folder_unpack.grid(row=1, column=0, padx=60, pady=(180,0), sticky="NW")  

        # self.folder_unpack = customtkinter.CTkButton(self.fourth_frame, text="Remove Duplicates (1)", command=self.control_folder_pack) coming soon
        # self.folder_unpack.grid(row=1, column=0, padx=260, pady=(180,0), sticky="NW")

        self.folder_folder1 = customtkinter.CTkButton(self.fourth_frame, text="Folder1", command=self.control_compare_folder1)
        self.folder_folder1.grid(row=1, column=0, padx=60, pady=(340,0), sticky="NW")  

        self.folder_folder2 = customtkinter.CTkButton(self.fourth_frame, text="Folder2", command=self.control_compare_folder2)
        self.folder_folder2.grid(row=1, column=0, padx=260, pady=(340,0), sticky="NW")

        self.folder_compare = customtkinter.CTkButton(self.fourth_frame, text="Compare", command=self.control_folder_compare_start)
        self.folder_compare.grid(row=1, column=0, padx=158, pady=(390,0), sticky="NW")


        self.foldersort_input = customtkinter.CTkButton(self.fourth_frame, text="Input Folder", command=self.browse_folder_input)
        self.foldersort_input.grid(row=1, column=0, padx=60, pady=(30,160), sticky="SW")  

        self.foldersort_output = customtkinter.CTkButton(self.fourth_frame, text="Output Folder", command=self.browse_folder_output)
        self.foldersort_output.grid(row=1, column=0, padx=260, pady=(30,160), sticky="SW")

        # fourth frame - Instructions

        self.logo_foldersort_instruction1 = customtkinter.CTkLabel(self.fourth_frame, text="Unpack - unpacks all the contents from subfolders", font=customtkinter.CTkFont(size=18))
        self.logo_foldersort_instruction1.grid(row=1, column=0, padx=(30, 0), pady=(0, 100), sticky="WS")
        
        self.foldersort_instruction2 = customtkinter.CTkLabel(self.fourth_frame, text="Pack - categorizes songs by artist and packs them into subfolders.", font=customtkinter.CTkFont(size=18))
        self.foldersort_instruction2.grid(row=1, column=0, padx=(30, 40), pady=(0, 70), sticky="WS")
        
        self.foldersort_instruction3 = customtkinter.CTkLabel(self.fourth_frame, text="It is adviced that you only use Folder Pack after NameFormatter", font=customtkinter.CTkFont(size=18))
        self.foldersort_instruction3.grid(row=1, column=0, padx=(30, 0), pady=(0, 40), sticky="WS")
                 
        "Navigational buttons"

        # create navigation buttons (left)
        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="NameFormat",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="MetadataLink",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="FolderSort",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.select_frame_by_name("home")


    # Navigational functions - updates app state

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget() 

    def home_button_event(self):
        """Selects the frame"""
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        """
        Prints the current input and output directories into a textbox
        Selects the frame
        """
        self.select_frame_by_name("frame_2")

        textbox = app_state_dictionary["name_textbox"]
        input_dir = app_state_dictionary["input_directory"]
        output_dir = app_state_dictionary["output_directory"]

        textbox.configure(state="normal")
        textbox.insert("end", f"\nCurrent:")
        textbox.insert("end", f"\nInput: {input_dir}")
        textbox.insert("end", f"\nOutput: {output_dir}")
        textbox.see("end")
        textbox.configure(state="disabled")

    def frame_3_button_event(self):
        """Selects the frame"""
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        """
        Prints the current input and output directories into a textbox
        Selects the frame
        """
        self.select_frame_by_name("frame_4")

        textbox = app_state_dictionary["folder_textbox"]
        input_dir = app_state_dictionary["input_directory"]
        output_dir = app_state_dictionary["output_directory"]

        textbox.configure(state="normal")
        textbox.insert("end", f"\nCurrent:")
        textbox.insert("end", f"\nInput: {input_dir}")
        textbox.insert("end", f"\nOutput: {output_dir}")
        textbox.see("end")
        textbox.configure(state="disabled")
    

    # Theme Functions

    def appearance_change(self):
        """
        Changes the theme and updates the settings json
        """
        if app_state_dictionary["appearance_mode"] == "dark":
            app_state_dictionary["appearance_mode"] = "light"
            customtkinter.set_appearance_mode("light")
        else:
            app_state_dictionary["appearance_mode"] = "dark"
            customtkinter.set_appearance_mode("dark")
        update_json()


    # Main Logic driver functions

    def control_input_folder(self):
        """
        Activates on button press:
        Selects input folder and updates the settings
        """
        textbox = app_state_dictionary["home_textbox"]
        folder_contents, folder = lg.open_folder()
        if folder is None:
            print(folder_contents) #errorMessage contained in this variable
            textbox.configure(state="normal")
            textbox.insert("end", f"\nCouldn't open folder error message was:\n{folder_contents}")
            app_state_dictionary["input_directory"] = None 
            textbox.configure(state="disabled")
        else:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nSuccess, folder at {folder}\ncontains {len(folder_contents)} items.")
            app_state_dictionary["input_directory"] = folder
            textbox.configure(state="disabled")
            update_json()
            

    def control_output_folder(self):
        """
        Activates on button press:
        Selects output folder and updates the settings
        """
        textbox = app_state_dictionary["home_textbox"]
        folder_contents, folder = lg.open_folder()
        if folder is None:
            #print(folder_contents) #errorMessage contained in this variable
            textbox.configure(state="normal")
            textbox.insert("end", f"\nCouldn't open folder error message was:\n{folder_contents}")
            app_state_dictionary["output_directory"] = None 
            textbox.configure(state="disabled")
        else:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nOutput folder at {folder} was selected")
            app_state_dictionary["output_directory"] = folder
            textbox.configure(state="disabled")
            update_json()

    def control_unpack_folder(self):
        """
        Activates on button press:
        Copies files over without folders
        """
        textbox = app_state_dictionary["folder_textbox"]
        source_dir = app_state_dictionary["input_directory"]
        destination_dir = app_state_dictionary["output_directory"]
        if app_state_dictionary["input_directory"] == None or app_state_dictionary["output_directory"] == None:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nPlease select folder first")
            textbox.configure(state="disabled")
        else:
            try:
                lg.copy_files(textbox,source_dir,destination_dir)
                textbox.insert("end", f"\nAll files have been moved successfully")
            except Exception as error:
                textbox.insert("end", f"\nOperation failed error message was: {error}")

    def control_folder_pack(self):
        """
        Activates on button press:
        Packs files into folders according to the artist [artist] - [song]
        """
        textbox = app_state_dictionary["folder_textbox"]
        source_dir = app_state_dictionary["input_directory"]
        destination_dir = app_state_dictionary["output_directory"]
        try:
            temp_folder = lg.create_temp_folder(destination_dir)
            lg.copy_files(textbox,source_dir,temp_folder,False)
            Filename_list = lg.open_folder_as_list(temp_folder)
        except Exception as error:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nOperation failed error message was {error}")
            textbox.configure(state="disabled")
        if Filename_list != []:
            try:
                lg.sort_into_folders(temp_folder,destination_dir,Filename_list)
                lg.delete_temp_folder(destination_dir)
                textbox.configure(state="normal")
                textbox.insert("end", f"\nOperation successful")
                textbox.configure(state="disabled")
            except Exception as error:
                textbox.configure(state="normal")
                textbox.insert("end", f"\nOperation failed error message was {error}")
                textbox.configure(state="disabled")
        else:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nInput folder is empty")
            textbox.configure(state="disabled")



    def control_name_sorter(self):
        """
        Activates on button press:
        Filters wrongly formatted names
        """
        report = False
        textbox = app_state_dictionary["name_textbox"]
        source_dir = app_state_dictionary["input_directory"]
        destination_dir = app_state_dictionary["output_directory"]
        if app_state_dictionary["input_directory"] == None or app_state_dictionary["output_directory"] == None:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nPlease select folder first")
            textbox.configure(state="disabled")
        else:
            try:
                textbox.configure(state="normal")
                temp_folder = lg.create_temp_folder(destination_dir)
                lg.copy_files(textbox,source_dir,temp_folder,report)
                wrong_format_files = lg.name_filter(textbox,temp_folder)
                app_state_dictionary["incorrect_file_names"] = wrong_format_files
                textbox.configure(state="disabled")
            except Exception as error:
                textbox.configure(state="normal")
                textbox.insert("end", f"\nOperation failed error message was {error}")
                textbox.configure(state="disabled")
    
    def control_excecute_rename(self):  # Option to move all or just some
        """
        Activates on button press:
        Renames Files according textbox contents
        """
        report = False
        textbox = app_state_dictionary["name_textbox"]
        incorrect_file_list = app_state_dictionary["incorrect_file_names"]
        output_dir = app_state_dictionary["output_directory"]
        input_dir = app_state_dictionary["input_directory"]

        self.name_ready.destroy()
        textbox.configure(state="normal")
        renamed_filenames = textbox.get("2.0","end")
        renamed_list = renamed_filenames.split("\n")
        del renamed_list[-1] #empty string leftover from split method
        source_dir = os.path.join(output_dir,"temp")
        try:
            lg.rename_according_to_list(textbox, source_dir, renamed_list, incorrect_file_list)
            lg.move_files_according_to_list(source_dir, output_dir, renamed_list)
            lg.delete_temp_folder(output_dir)
            lg.delete_files_according_to_list(input_dir,incorrect_file_list)
            lg.copy_files(textbox,input_dir,output_dir,report)
            input_dir_list = lg.open_folder_as_list(input_dir)
            lg.delete_files_according_to_list(input_dir, input_dir_list)
            textbox.configure(state="normal")
            textbox.insert("end",f"\nOperation Successful! Files can be found at {output_dir}")
        except Exception as error:
            textbox.configure(state="normal")
            textbox.insert("end",f"\nOperation Failed, error message was {error}")
        textbox.configure(state="disabled")

    def control_user_rename(self):
        """
        Activates on button press:
        Prints a list of files into a textbox for the user to rename
        """
        textbox = app_state_dictionary["name_textbox"]
        output_dir = app_state_dictionary["output_directory"]
        incorrect_file_list = app_state_dictionary["incorrect_file_names"]
        if incorrect_file_list is not None and incorrect_file_list != []:
            textbox.configure(state="normal")
            lg.clear_textbox(textbox)
            textbox.insert("end", f"Rename your files here, when you are done click Ready!")
            lg.print_list(textbox, incorrect_file_list)
            self.name_ready = customtkinter.CTkButton(self.second_frame, text="Ready!", command=self.control_excecute_rename)
            self.name_ready.grid(row=1, column=0, padx=(116,0), pady=(260,0), sticky="NW")
        else:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nPlease use the filter function first")
            lg.delete_temp_folder(output_dir)
            textbox.configure(state="disabled")

    def browse_folder_input(self):
        """
        Activates on button press:
        Opens current input folder using Windows file explorer
        """
        try:
            directory = app_state_dictionary["input_directory"]
            command = 'start ' + directory
            os.system(command)
        except Exception as error:
            textbox = app_state_dictionary["folder_textbox"]
            textbox.configure("normal")
            textbox.insert("end", f"\nOperation failed error message was {error}")

    def browse_folder_output(self):
        """
        Activates on button press:
        Opens current output folder using Windows file explorer
        """
        try:
            directory = app_state_dictionary["output_directory"]
            command = 'start ' + directory
            os.system(command)
        except Exception as error:
            textbox = app_state_dictionary["folder_textbox"]
            textbox.configure("normal")
            textbox.insert("end", f"\nOperation failed error message was {error}")

    def control_compare_folder1(self):
        """
        Activates on button press:
        Selects folder1 for comparison
        """
        textbox = app_state_dictionary["folder_textbox"]
        folder_contents, folder = lg.open_folder()
        if folder is None:
            #print(folder_contents) #errorMessage contained in this variable
            textbox.configure(state="normal")
            textbox.insert("end", f"\nCouldn't open folder error message was:\n{folder_contents}")
            app_state_dictionary["folder_compare_directory1"] = None 
            textbox.configure(state="disabled")
        else:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nfolder at {folder} was selected")
            app_state_dictionary["folder_compare_directory1"] = folder
            textbox.configure(state="disabled")

    def control_compare_folder2(self):
        """
        Activates on button press:
        Selects folder2 for comparison
        """
        textbox = app_state_dictionary["folder_textbox"]
        folder_contents, folder = lg.open_folder()
        if folder is None:
            #print(folder_contents) #errorMessage contained in this variable
            textbox.configure(state="normal")
            textbox.insert("end", f"\nCouldn't open folder error message was:\n{folder_contents}")
            app_state_dictionary["folder_compare_directory2"] = None 
            textbox.configure(state="disabled")
        else:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nfolder at {folder} was selected")
            app_state_dictionary["folder_compare_directory2"] = folder
            textbox.configure(state="disabled")

    def control_folder_compare_start(self):
        """
        Activates on button press:
        Starts comparison between folder1 and folder2
        """
        textbox = app_state_dictionary["folder_textbox"]
        folder1 = app_state_dictionary["folder_compare_directory1"]
        folder2 = app_state_dictionary["folder_compare_directory2"]
        try:
            folder1_list = lg.open_folder_as_list(folder1)
            folder2_list = lg.open_folder_as_list(folder2)
            lg.compare_lists(textbox,folder1_list,folder2_list)
        except Exception as error:
            textbox.configure("normal")
            textbox.insert("end", f"\nOperation failed error message was {error}")


    def control_metadata_sort(self):
        """
        Activates on button press:
        Displays an image of the current song
        """
        textbox = app_state_dictionary["metadata_textbox"]
        textbox2 = app_state_dictionary["metadata_textbox2"]
        output_dir = app_state_dictionary["output_directory"]
        filename_list = app_state_dictionary["metadata_filename_list"]
        metadata_imagebox = app_state_dictionary["metadata_imagebox"]
        url_list = app_state_dictionary["metadata_image_url_list"]
        image_index = app_state_dictionary["metadata_image_index"]

        if filename_list == []: #Task Finished
            textbox.configure(state="normal")
            textbox.insert("end", f"\nList of files is empty - task complete")
            temp_folder = os.path.join(output_dir,"temp")
            lg.delete_file_by_dir(os.path.join(temp_folder,"coverart.jpeg"))
            lg.copy_files(textbox, temp_folder, output_dir, report=False)
            lg.delete_temp_folder(output_dir)
            self.metadata_button_stop.destroy()
            self.metadata_button_back.destroy()
            app_state_dictionary["metadata_filename_list"] = None
        else:
            if filename_list == None: #First time setup
                input_dir = app_state_dictionary["input_directory"]
                temp_folder = lg.create_temp_folder(output_dir)
                lg.copy_files(textbox, input_dir, temp_folder, False)
                filename_list = lg.open_folder_as_list(temp_folder)
                mp3_file_list = lg.check_list_filetype(textbox, filename_list, ".mp3")
                outstanding_files_list = lg.check_metadata(textbox,temp_folder,mp3_file_list)
                app_state_dictionary["metadata_filename_list"] = outstanding_files_list
                self.metadata_create_buttons()
            else: 
                outstanding_files_list = app_state_dictionary["metadata_filename_list"]
        
            filename = outstanding_files_list[0].split(".mp3")[0]
            textbox2.configure(state="normal")
            lg.clear_textbox(textbox2)
            textbox2.configure(state="normal")
            textbox2.insert("end", f"{filename}")
            try: #https://stackoverflow.com/questions/61170959/python-image-scraper-not-working-properly-on-bing
                if url_list == None: 
                    url, url_list = lg.search_image(filename, image_index) #Uses WebScraper from Stackoverflow ^^
                    app_state_dictionary["metadata_image_url_list"] = url_list
                else: 
                    url = url_list[image_index]

                photo = lg.url_picture_conversion(url)
                metadata_imagebox.configure(image=photo)
                textbox.configure(state="normal")
                textbox.insert("end", f"\nPicture found - Choose: Yes, No, skip")
                textbox.configure(state="disabled")
            except Exception as error:
                textbox.configure("normal")
                textbox.insert("end", f"\nOperation failed error message was {error}")

    def metadata_stop(self):
        """
        Activates on button press:
        Stops the Metadata change loop, 
        and moves the files over to the output
        """
        textbox = app_state_dictionary["metadata_textbox"]
        output = app_state_dictionary["output_directory"]
        temp_folder = os.path.join(output,"temp")
        temp_coverart = os.path.join(temp_folder,"coverart.jpeg")
        self.metadata_button_start = customtkinter.CTkButton(self.third_frame, text="Start", width=100, height=60, command=self.control_metadata_sort)
        self.metadata_button_start.grid(row=1, column=0, padx=(30,160), pady=(480,10), sticky="N")
        self.metadata_button_stop.destroy()
        self.metadata_button_back.destroy()
        lg.delete_file_by_dir(temp_coverart)
        lg.copy_files(textbox, temp_folder,output, report=False)
        lg.delete_temp_folder(output)
        textbox.configure(state="normal")
        textbox.insert("end", f"\nOperation stopped, files have been moved")
        textbox.configure(state="disabled")

    def metadata_skip(self):
        """
        Activates on button press:
        Skips the current song so that the cover art wont be changed
        """
        textbox = app_state_dictionary["metadata_textbox"]
        if app_state_dictionary["metadata_filename_list"] != None:
            file = app_state_dictionary["metadata_filename_list"][0]
            del app_state_dictionary["metadata_filename_list"][0]
            textbox.configure(state="normal")
            textbox.insert("end", f"\n{file} - skipped")
            textbox.see("end")
            textbox.configure(state="disabled")
            app_state_dictionary["metadata_image_index"] = 0
            app_state_dictionary["metadata_image_url_list"] = None
            self.control_metadata_sort()
        else:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nNo more files to skip")
            textbox.configure(state="disabled")

    def metadata_back(self):
        """
        Activates on button press:
        Shows the previous image
        """
        textbox = app_state_dictionary["metadata_textbox"]
        if app_state_dictionary["metadata_filename_list"] != None:
            app_state_dictionary["metadata_image_index"] -= 1
            textbox.configure(state="normal")
            textbox.insert("end", f"\nFound previous picture")
            textbox.configure(state="disabled")
            self.control_metadata_sort()
        else:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nNothing selected")
            textbox.configure(state="disabled")

    def metadata_no(self):
        """
        Activates on button press:
        Finds a new image for the cover art
        """
        textbox = app_state_dictionary["metadata_textbox"]
        if app_state_dictionary["metadata_filename_list"] != None:
            app_state_dictionary["metadata_image_index"] += 1
            textbox.configure(state="normal")
            textbox.insert("end", f"\nFound another picture")
            textbox.see("end")
            textbox.configure(state="disabled")
            self.control_metadata_sort()
        else:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nNothing selected")
            textbox.configure(state="disabled")

    def metadata_ok(self):
        """
        Activates on button press:
        Binds the current image to the mp3 metadata as cover art
        """
        textbox = app_state_dictionary["metadata_textbox"]
        if app_state_dictionary["metadata_filename_list"] != None:
            output = app_state_dictionary["output_directory"]
            temp_folder = os.path.join(output,"temp")
            file = app_state_dictionary["metadata_filename_list"][0]
            index = app_state_dictionary["metadata_image_index"]
            url =  app_state_dictionary["metadata_image_url_list"][index]
            lg.set_cover_art(temp_folder, file, url)
            textbox.configure(state="normal")
            textbox.insert("end", f"\n{file} - Cover art selected and embedded")
            textbox.see("end")
            textbox.configure(state="disabled")
            del app_state_dictionary["metadata_filename_list"][0]
            app_state_dictionary["metadata_image_index"] = 0
            app_state_dictionary["metadata_image_url_list"] = None
            try:
                lg.move_files_according_to_list(temp_folder,output,[file])
                self.control_metadata_sort()
            except Exception as error:
                textbox.configure(state="normal")
                textbox.insert("end", f"\nOperation failed error was {error}")
                textbox.configure(state="disabled")
        else:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nNothing selected")
            textbox.configure(state="disabled")

    def metadata_create_buttons(self):
        """
        Creates additional buttons (back/stop) for MetaDataLinker
        """
        self.metadata_button_back = customtkinter.CTkButton(self.third_frame, text="Back", width=100, height=60, command=self.metadata_back, fg_color=("#302d2d"), hover_color=("#383b40"))
        self.metadata_button_back.grid(row=1, column=0, padx=(30,400), pady=(480,10), sticky="N")
        self.metadata_button_stop = customtkinter.CTkButton(self.third_frame, text="Stop", width=100, height=60, command=self.metadata_stop, fg_color=("#a60d0d"), hover_color=("red", "darkred"))
        self.metadata_button_stop.grid(row=1, column=0, padx=(180,70), pady=(480,10), sticky="N")  

 
if __name__ == "__main__":
    app = App()
    app.mainloop()


# Features for the future:
# - Optimize
# - Catch errors from libraries and print them better
# - Remove all mp3 metadata
# - Add [artist] - [Song] to metadata