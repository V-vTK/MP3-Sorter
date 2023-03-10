# MP3-Sorter
A pastime project focused on enhancing the metadata and naming conventions of MP3 files obtained from CDs.

The App is built on top of CustomTKinter which provides an efficient way to create a modern UI. 
I found that the documentation and examples provided with it were extremely helpful.
Developement with it was mostly smooth sailing.

https://github.com/TomSchimansky/CustomTkinter

# Preview
![python_T9Kt4Df75E](https://user-images.githubusercontent.com/97534406/216664783-d84c958d-827a-4e2e-b9a9-0ee500e603db.png)

# Home:
![python_yj9dwdgcrb](https://user-images.githubusercontent.com/97534406/216659653-0d9870ea-cd7d-44d6-a7a2-cc71ffb914e1.png)

Here you can modify the input and output directories and switch between a dark and light interface theme.

# NameSort
![python_sAdETuOwef](https://user-images.githubusercontent.com/97534406/216659909-60dee645-b419-494b-b669-60a23f1d2f01.png)

**NameSort** is a tool that helps you quickly identify files that are not named in the standard [artist] - [song] format.

**For example:**

Kygo, Sasha Alex Sloan - I'll Wait -> False

The Score - Who I am -> True

NameSort can improve the accuracy of your search results (MetadataLink). 
It also ensures that when you organize your files into folders, they are properly sorted by artist.

# MetadataLink
![python_EdAfMoUVRN](https://user-images.githubusercontent.com/97534406/216660174-fba49afd-236b-49bf-9146-69bbbc7a9846.png)

**MetadataLink:**
Finds a picture associated with the filename. Allows you to find another picture, skip the file altogheter or link the current picture to the file.
Using ID3v2 tags the picture is embedded into the MP3 file.

**In action:**
![python_PAeFBdNqYX](https://user-images.githubusercontent.com/97534406/216674146-7353d242-d6f7-4b06-a5ef-05aba5a3d7d1.png)

# FolderSort
![python_j9xJ8YC5jV](https://user-images.githubusercontent.com/97534406/216660395-3d55018c-9fde-4f08-bbe4-b8877fed669f.png)

**Folder Unpack**
Extracts files from a directory and all it's sub folders into the output folder.

**Folder Pack**
Packs MP3 Files into folders by their artist ([Artist] - [Song])

**Folder Compare:**
Allows you to compare the contents of two folders.

The current input and output folders can be viewed by clicking the buttons in the Browse section.

**Future Ideas**
- Remove all metadata from mp3 files
- Optimize the operations - Reduce unnecessary file movements
- Better error catching - the current version has a lot of broad try except blocks
- Not happy with the current Metadata functions
  The eyeD3 and mutagen libraries used for metadata manipulation seem to have a bunch of false positives and -negatives.
  Either way my implementation is quite the "it works" solution
  
**EW, white theme**
![python_gZ4coErCGd](https://user-images.githubusercontent.com/97534406/216667656-e0ad34ac-f3a4-45fa-b22a-91325a947fde.png)
###### but it is there :D
