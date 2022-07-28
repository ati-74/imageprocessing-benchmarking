from tkinter import *
import sys
from tkinter import messagebox
from tkinter import filedialog

sys.path.append("scripts")
from MicroColonyAnalysis import ProcessData


def StartProcessing(summary_statistic_method, target_proximity_strain=""):
    print(summary_statistic_method)
    msg = messagebox.showinfo("Processing is Started", "Processing is Started")
    print("input file: " + input_file)
    if CheckVar1.get() == 1:
        output_directory_path_as_input_folder = "/".join(input_file.split("/")[:-1])
        print("output directory: " + output_directory_path_as_input_folder)
        # start processing csv file
        ProcessData(
            input_file,
            relationship_file,
            output_directory_path_as_input_folder,
            summary_statistic_method,
        )

        msg = messagebox.showinfo(
            summary_statistic_method + " analysis was done",
            summary_statistic_method + " analysis was done",
        )
        msg = messagebox.showinfo(
            "The calculation files were written into "
            + output_directory_path_as_input_folder,
            "The calculation files were written into "
            + output_directory_path_as_input_folder,
        )

    else:
        print("output directory: " + output_directory_path)
        # start processing csv file
        ProcessData(
            input_file,
            relationship_file,
            output_directory_path,
            summary_statistic_method,
        )

        msg = messagebox.showinfo(
            summary_statistic_method + " analysis was done",
            summary_statistic_method + " analysis was done",
        )
        msg = messagebox.showinfo(
            "The calculation files were written into " + output_directory_path,
            "The calculation files were written into " + output_directory_path,
        )


def browseFiles():
    global input_file
    inputFile = filedialog.askopenfilename(
        initialdir="/",
        title="Select CellProfiler tracking file",
        filetypes=(("CSV files", "*.CSV"),),
    )
    # Change label contents
    browse_value.configure(text=inputFile.split("/")[-1].split("\\")[-1])
    input_file = inputFile


def browse_relationship_Files():
    global relationship_file
    input_relationship_File = filedialog.askopenfilename(
        initialdir="/",
        title="Select Object relationships File",
        filetypes=(("CSV files", "*.CSV"),),
    )
    # Change label contents
    browse_relationship_value.configure(
        text=input_relationship_File.split("/")[-1].split("\\")[-1]
    )
    relationship_file = input_relationship_File


def browseDirectory():
    global output_directory_path
    output_directory = filedialog.askdirectory()
    # Change label contents
    browse_directory_value.configure(text=output_directory)
    output_directory_path = output_directory


# Change the label text
def show():
    label.config(text=system_type_value.get())


if __name__ == "__main__":
    top = Tk()
    top.geometry("650x300")
    top.title("Summary Statistics")

    # browse File
    browse_file_lable = Label(top, text="Browse File:")
    browse_file_lable.pack(side=LEFT)
    browse_file_lable.place(x=30, y=60)
    button_browse_file = Button(
        top, text="CellProfiler tracking file", command=browseFiles
    )
    button_browse_file.pack()
    button_browse_file.place(x=120, y=56)
    browse_value = Label(top, text="")
    browse_value.pack(side=LEFT)
    browse_value.place(x=120, y=90)

    # browse Object relationships File
    browse_relationship_lable = Label(top, text="Browse Object relationships File:")
    browse_relationship_lable.pack(side=LEFT)
    browse_relationship_lable.place(x=30, y=130)
    button_browse_relationship_file = Button(
        top, text="Object relationships File", command=browse_relationship_Files
    )
    button_browse_relationship_file.pack()
    button_browse_relationship_file.place(x=220, y=125)
    browse_relationship_value = Label(top, text="")
    browse_relationship_value.pack(side=LEFT)
    browse_relationship_value.place(x=220, y=160)

    # browse directory
    browse_directory_lable = Label(top, text="Browse Output Directory:")
    browse_directory_lable.pack(side=LEFT)
    browse_directory_lable.place(x=300, y=60)

    button_browse_directory = Button(
        top, text="Output directory", command=browseDirectory
    )
    button_browse_directory.pack()
    button_browse_directory.place(x=460, y=56)
    browse_directory_value = Label(top, text="")
    browse_directory_value.pack(side=LEFT)
    browse_directory_value.place(x=300, y=90)

    # check box
    CheckVar1 = IntVar()
    checkBox_output_directory = Checkbutton(
        top,
        text="Use input folder as output folder ",
        variable=CheckVar1,
        onvalue=1,
        offvalue=0,
    )
    checkBox_output_directory.pack()
    checkBox_output_directory.place(x=115, y=190)

    '''
    aspect ratio process button
    '''
    start_process_aspect_ratio = Button(
        top, text="Aspect Ratio", command=lambda: StartProcessing("Aspect Ratio")
    )
    start_process_aspect_ratio.place(x=190, y=250)

    '''
    anisotropy process button
    '''
    start_process_anisotropy = Button(
        top, text="Anisotropy", command=lambda: StartProcessing("Anisotropy")
    )
    start_process_anisotropy.place(x=390, y=250)

    
    top.mainloop()
