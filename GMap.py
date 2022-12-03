import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pyproj
import simplekml
import os

BACKGROUND_COLOR = "#2F4F4F"
FOREGROUND_COLOR = "#FFFFFF"
FONT = "Ebrima 14"
FONT_ONLY = "Ebrima"
BUTTON_CLICK_COLOR = "#98F5FF"

root = Tk()
root.title("GMap")
root.config(bg=BACKGROUND_COLOR)
root.geometry("800x750")
root.resizable(False,False)
root_icon = tkinter.Image("photo", file="title_icon.png")
root.iconphoto(True,root_icon)

canvas = Canvas(root,bg=BACKGROUND_COLOR,highlightthickness=0, width=200, height=200)
canvas.grid(column=1, row=0, padx=40)

icon = PhotoImage(file="png_resize.png")
image_file = canvas.create_image(100, 100, image=icon)

excel_label = Label(root, text="• Import an excel .csv file which has co-ordinate information about the plot of land\n\n"
                                 "• Let the columns be arranged in the following order:"
                                 " Northings(N), Eastings(E), Label(L) \n", justify="left", font=FONT, bg=BACKGROUND_COLOR,
                    fg=FOREGROUND_COLOR)
excel_label.grid(column=1, row=1, columnspan=2, pady=20)

excel_entry = Entry(root, width=70, font=("Courier 10 italic"))
excel_entry.grid(column=1, row=2, pady=20, padx=10)

def browse_excel():
    filename = filedialog.askopenfilename(initialdir="/", title="Select Co-ordinate File",
                                          filetypes=(("csv file", "*.csv"),
                                                     ))
    excel_entry.insert(END, string=filename)

# Browse button
excel_browse = Button(root, text="BROWSE", command=browse_excel, width=20, activebackground=BUTTON_CLICK_COLOR)
excel_browse.grid(row=2, column=2, padx=20)

# Plotting the plot
def plot():
    is_success = True
    csv_file = excel_entry.get()

    output_file = filedialog.asksaveasfile(title="Select where you want to save the file",
                                           confirmoverwrite=True)
    output_data = output_file.name
    print(output_data)

    with open(csv_file) as csv:
        cord_line = csv.readlines()

    co_ordinate_pairs = []
    with open(f"{output_data}.txt", mode="a") as google_coordinates:
        google_coordinates.write(f"Longitude,Latitude,Label\n")
        for co_ordinates in cord_line:
            only_co_ordinates = co_ordinates.strip("\n")
            co_ordinates_list = only_co_ordinates.split(",")
            print(co_ordinates_list)
            try:
                source_eastings = float(co_ordinates_list[1])
                source_northings = float(co_ordinates_list[0])
                war_to_wgs_84 = pyproj.Transformer.from_crs(2136, 4326)
                wgs_value = war_to_wgs_84.transform(source_eastings, source_northings)
                # putting converted wgs coordinate in a tuple along with the names
                converted_coord = (wgs_value[1], wgs_value[0], co_ordinates_list[2])
                decimal_degree = f"{round(wgs_value[1], 6)}, {round(wgs_value[0], 6)}, {co_ordinates_list[2]}"
                google_coordinates.write(f"{decimal_degree}\n")
                co_ordinate_pairs.append(converted_coord)
                messagebox.showinfo(title="Success", message="Your co-ordinates have been successfully converted and is"
                                                             " being plotted on google earth. Please make sure you have"
                                                             " google earth installed on your pc")
                is_success = True
            except ValueError:
                is_success = False
                pass

    print(co_ordinate_pairs)

    # plotting on to google earth
    map_kml = simplekml.Kml()
    # plotting points

    line_points = []
    for co_ordinate in co_ordinate_pairs:
        map_kml.newpoint(name=co_ordinate[2], coords=[(co_ordinate[0], co_ordinate[1])])
        line_co_ordinate = (co_ordinate[0], co_ordinate[1])
        line_points.append(line_co_ordinate)

    # plotting lines
    pol = map_kml.newpolygon(name="boundary", outerboundaryis=line_points)
    pol.style.polystyle.color = '990000ff'

    map_kml.save(f"{output_data}.kml")

    os.startfile(os.path.abspath(f"{output_data}.kml"))

    if is_success:
        messagebox.showinfo(title="Success", message="Your co-ordinates have successfully been converted and plotted. If you have google earth"
                                                     "installed, the plot should be automatically plotted unto google earth.")
    else:
        messagebox.showerror(title="Error", message="There was an error. Please press the 'MANUAL' button to see how the app works"
                                                    ". Make sure there are no numericals in the label column. If you still face challenges,"
                                                    "send an email to: paintsil610@gmail.com")

def about():
    about_window = Tk()
    about_window.title("About Gmap")
    about_window.resizable(False, False)
    about_label = Label(about_window, justify="left", font=(f"{FONT_ONLY} 10"), text="This app enables you to plot your siteplan co-ordinates (in Ghana War Office system)\n"
                                           " directly unto google earth. Please make sure you have google earth installed first.")
    about_label.pack(padx=20, pady=20)
    developer_label = Label(about_window,justify="center",font=(f"{FONT_ONLY} 10"), text="This app was developed by Joseph Paintsil\n"
                                                                         "email: paintsil610@gmail.com\n"
                                                                                       "© 2022")
    developer_label.pack(padx=20, pady=20)
    about_window.mainloop()

def view_sample():
    os.startfile(os.path.abspath("sample_data.csv"))

def plot_sample():
    is_success = True
    sample_file = os.path.abspath("sample_data.csv")

    output_file = filedialog.asksaveasfile(title="Select where you want to save the file",
                                           confirmoverwrite=True)
    output_data = output_file.name
    print(output_data)

    with open(sample_file) as csv:
        cord_line = csv.readlines()

    co_ordinate_pairs = []
    with open(f"{output_data}.txt", mode="a") as google_coordinates:
        google_coordinates.write(f"Longitude,Latitude,Label\n")
        for co_ordinates in cord_line:
            only_co_ordinates = co_ordinates.strip("\n")
            co_ordinates_list = only_co_ordinates.split(",")
            print(co_ordinates_list)
            try:
                source_eastings = float(co_ordinates_list[1])
                source_northings = float(co_ordinates_list[0])
                war_to_wgs_84 = pyproj.Transformer.from_crs(2136, 4326)
                wgs_value = war_to_wgs_84.transform(source_eastings, source_northings)
                # putting converted wgs coordinate in a tuple along with the names
                converted_coord = (wgs_value[1], wgs_value[0], co_ordinates_list[2])
                decimal_degree = f"{round(wgs_value[1], 6)}, {round(wgs_value[0], 6)}, {co_ordinates_list[2]}"
                google_coordinates.write(f"{decimal_degree}\n")
                co_ordinate_pairs.append(converted_coord)
                is_success = True

            except ValueError:
                is_success = False
                pass
    # plotting on to google earth
    map_kml = simplekml.Kml()
    # plotting points

    line_points = []
    for co_ordinate in co_ordinate_pairs:
        map_kml.newpoint(name=co_ordinate[2], coords=[(co_ordinate[0], co_ordinate[1])])
        line_co_ordinate = (co_ordinate[0], co_ordinate[1])
        line_points.append(line_co_ordinate)

    # plotting lines
    pol = map_kml.newpolygon(name="boundary", outerboundaryis=line_points)
    pol.style.polystyle.color = '990000ff'

    map_kml.save(f"{output_data}.kml")

    os.startfile(os.path.abspath(f"{output_data}.kml"))

    if is_success:
        messagebox.showinfo(title="Success", message="Your co-ordinates have successfully been converted and plotted. If you have google earth"
                                                     "installed, the plot should be automatically plotted unto google earth.")
    else:
        messagebox.showerror(title="Error", message="There was an error. Please press the 'MANUAL' button to see how the app works"
                                                    ". Make sure there are no numericals in the label column. If you still face challenges,"
                                                    "send an email to: paintsil610@gmail.com")

def manual():
    os.startfile(os.path.abspath("README.txt"))
#
# Plot Button
plot_button = Button(root, text="PLOT", command=plot, width=45, activebackground=BUTTON_CLICK_COLOR)
plot_button.grid(row=3, column=1, columnspan=2, pady=20)

# View Sample Data
sample_button = Button(root, text="VIEW SAMPLE DATA", command=view_sample, width=45, activebackground=BUTTON_CLICK_COLOR)
sample_button.grid(row=4, column=1, columnspan=2, pady=20)

# Plot Sample Data
plot_sample = Button(root, text="PLOT SAMPLE DATA", command=plot_sample, width=45, activebackground=BUTTON_CLICK_COLOR)
plot_sample.grid(row=5, column=1, columnspan=2, pady=20)

# Manual
manual_button = Button(root, text="MANUAL", command=manual, width=45, activebackground=BUTTON_CLICK_COLOR)
manual_button.grid(row=6, column=1, columnspan=2, pady=20)

# About App
about_button = Button(root, text="ABOUT APP", command=about, width=45, activebackground=BUTTON_CLICK_COLOR)
about_button.grid(row=7, column=1, columnspan=2, pady=20)

root.mainloop()