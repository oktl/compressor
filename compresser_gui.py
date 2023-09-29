# Script with GUI to make image size on disc smaller.
# Adjust the script to change the max_size in kilobytes.
# Created by oktl - 26 September 2023.

from os import chdir, stat
from pathlib import Path

import PySimpleGUI as sg
from PIL import Image

keys_to_clear = [
    "-FOLDER-",
    "-INFO-",
    "-MESSAGE-",
    "-STATUS-"
]


def file_size(filename) -> int:
    """
    Get the size of a file in bytes.

    Args:
        filename (str): The path to the file.

    Returns:
        int: The size of the file in bytes.
    """
    return stat(filename).st_size  # bytes


def make_file_list(folder: Path, file_extension: str) -> list:
    """
    Get a list of all filenames of type 'extension' in a folder.

    Args:
        folder (Path): The folder to search for files.
        file_extension (str): The ile extension to filter by.

    Returns:
        list: A list of filenames with the specified extension.
    """
    return [file.name for file in folder.glob(file_extension)]


def compress_image_file(folder: Path, max_file_size: int) -> None:
    """
    Compresses files in a specified folder.

    The function retrieves a list of filenames with the specified extension in the given folder.
    It then iterates through the list and compresses each file until its size is below
    the maximum size.

    Args:
        None

    Returns:
        None
    """
    filenames = make_file_list(folder, '*.jpg')
    window["-MESSAGE-"].update("Files compressed:")
    for filename in filenames:
        print(filename,"Initial Size:", file_size(filename))
        
        while file_size(filename) >= max_file_size:
            image = Image.open(filename)
            image.save(filename,quality=80)
            
            print(filename,"Final Size:",file_size(filename))    
        
        
def multiline_frame(title: str) -> sg.Frame:
    """_summary_

    Args:
        title (str): _description_

    Returns:
        sg.Frame: _description_
    """

    return [sg.Frame(title,
        [
            # [B("Compress Images",
            #     size=(40, 1),
            #     button_color="#52524e",
            #     expand_x=True,
            #     enable_events=True,
            #     pad=((40, 40), (30, 20)))
            # ],            
            [T("", 
                size=(46, 1),
                background_color="#303030",
                key="-MESSAGE-")
            ], 
            # [T("", 
            #     size=(46, 1),
            #     background_color="#303030",
            #     key="-HEADER-")
            # ],           
            [sg.Multiline(
                    default_text="",  # So it doesn't show up as an empty.
                    size=(47, 18),
                    disabled=True,
                    border_width=0,
                    autoscroll=False,
                    justification="l",
                    focus=False,
                    background_color="#303030",
                    text_color="#e9e8e4",
                    key="-INFO-",
                    reroute_stdout=True,
                    reroute_cprint=True,
                    # echo_stdout_stderr = True,
                    sbar_trough_color="#303030",
                    sbar_background_color="#303030",
                    sbar_arrow_color="#9a9b94",
                    sbar_frame_color="#303030",
                    sbar_relief="flat",
                ),
            ]
        ],
        background_color="#303030",
        font=("Calibri", 14, "bold"),
        relief="flat",
        expand_x=True,
        pad=((20, 20), (0, 20)),
    )
    ]
        

def action_buttons_frame(title: str) -> sg.Frame:
    """User defined custom PySimpleGUI Frame element for placing buttons.
    
    Args:
        title (str): title for PySimpleGUI Frame.
    
    Returns:
        sg.Frame: PySimpleGUI Frame element with Button elements.
    """
    return [sg.Frame(
            layout=[
                [sg.Column(
                        layout=[
                            [
                                B("Clear Inputs",
                                    button_color="#52524e",
                                    pad=((40, 40), (0, 0)),
                                    ),
                                B("Exit",
                                    button_color="#52524e",
                                    pad=((40, 40), (0, 0)),),
                            ],
                        ],
                        background_color="#3a3a3a",
                        pad=((0, 0), (15, 15)),
                    )
                ],
            ],
            title=title,
            title_location=sg.TITLE_LOCATION_TOP,
            expand_x=True,
            element_justification="center",
            font=("Calibri", 14, "bold"),
            background_color="#3a3a3a",
            relief="flat",
            pad=((40, 40), (0, 20)),
        )
    ]


# Declare some sg aliases.
B = sg.Button
Frame = sg.Frame
In = sg.Input
T = sg.Text    

# Input for folder to find image files in.
filename_input_column = [    
    [
        T("Maximum size for compressed files:",
            background_color="#3a3a3a",
            expand_x=True,
            # pad=(0, 30)
            ), 
    ],
    
    [
        In("Folder...",
            size=(30, 1),
            disabled=True,
            use_readonly_for_disable=False,
            enable_events=True,
            # pad=(0, 40),
            key="-FOLDER-",
        ),
    ],
    
]

filename_button_column = (
    
    [   In(size=(12,1), 
            default_text='550000',
            justification='c',
            key="-MAX-SIZE-")],
    [
        sg.FolderBrowse(
            button_text="  Set Folder...   ",
            # file_types=(("SQL", ".sql"),),
            button_color="#52524e",
            enable_events=True,
            target="-FOLDER-",
            auto_size_button=False,
            # pad=(0, 40)
            
        )
    ],

)

filename_frame = [
    Frame("Get File Path \n",
        [
            [
                sg.Column(
                    filename_input_column,
                    element_justification="right",
                    pad=((20, 0), (20, 20)),
                    background_color="#3a3a3a",
                ),
                sg.Column(
                    filename_button_column,
                    element_justification="left",
                    pad=((0, 20), (20,20)),
                    background_color="#3a3a3a",
                ),
            ],
            [
                B("Compress Images",
                size=(40, 1),
                button_color="#52524e",
                expand_x=True,
                enable_events=True,
                pad=((40, 40), (20, 30))
                )
            ],            
        ],
        element_justification="center",
        relief="flat",
        background_color="#3a3a3a",
        expand_x=True,
        font=("Calibri", 14, "bold"),
        pad=((20, 20), (20, 0)),
    )
]

info_frame = [
    Frame("",
        [
            filename_frame,
            multiline_frame("Info"),
        ],
        background_color="#52524e",
        relief="flat",
        # pad=((20, 20), (0, 0)),
    )
]

status_bar = (
        [
            T("",
            expand_x=True,
            pad=((40, 40), (0, 10)),
            background_color="#3a3a3a",
            text_color="light green",
            key="-STATUS-",
        ),
        ]
)

layout = [
    # [titlebar],
    [info_frame],
    [action_buttons_frame("")],
]

sg.theme("DarkGrey4")
window = sg.Window(
    "Image Compresser",
    layout,
    auto_size_buttons=False,
    default_button_element_size=(12, 1),
    button_color="#52524e",
    font="Calibri 14",
    return_keyboard_events=True,
    finalize=True,
)

while True:  # Event Loop
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit", "Alt-x", "F4:115"):
        break    
    
    # Do the deed.
    if event == 'Compress Images':
        # max_file_size = values["-MAX-SIZE-"]
        image_folder = Path(values["-FOLDER-"])
        chdir(image_folder)
        compress_image_file(image_folder, int(values["-MAX-SIZE-"]))
        
    elif event == "Clear Inputs":
        for key in keys_to_clear:
            window[key].update('')            
        window["-INFO-"].update(".")
        window.refresh()

window.close()
