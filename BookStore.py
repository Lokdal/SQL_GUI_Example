# Import packages
import tkinter as tkin
import backend
import exceptions as Ex

# =====
# Define functions


def fGetSelected(event):
    list = listbox_Results.curselection()
    if len(list) != 0:
        selected = listbox_Results.get(listbox_Results.curselection()[0])
        entry_Title_val.set(selected[1])
        entry_Author_val.set(selected[2])
        entry_Year_val.set(selected[3])
        entry_ISBN_val.set(selected[4])


def fCheckValidProperties():
    tTitle = entry_Title_val.get().strip()
    tAuthor = entry_Author_val.get().strip()
    tYear = entry_Year_val.get().strip()
    tISBN = entry_ISBN_val.get().strip()
    for e in (tTitle, tAuthor, tYear, tISBN):
        if e == "":
            raise Ex.EmptyEntryError
    tYear = int(tYear)
    tISBN = int(tISBN)
    return(tTitle, tAuthor, tYear, tISBN)


def fView(books):
    listbox_Results.delete(0, tkin.END)
    for b in books:
        listbox_Results.insert(tkin.END, b)


def fViewAll():
    fView(backend.fSelectAll())


def fSearchEntry():
    try:
        tTitle = entry_Title_val.get().strip()
        tAuthor = entry_Author_val.get().strip()
        tYear = entry_Year_val.get().strip()
        tISBN = entry_ISBN_val.get().strip()
        if tTitle + tAuthor + tYear + tISBN == "":
            raise Ex.NoEntriesError
        if tYear != "":
            tYear = int(tYear)
        if tISBN != "":
            tISBN = int(tISBN)
    except ValueError:
        print("Year and ISBN must be integers.")
    except Ex.NoEntriesError:
        print("At least one of the fields must not be empty.")
    else:
        books = backend.fSearchEntry(tTitle, tAuthor, tYear, tISBN)
        fView(books)


def fAddEntry():
    try:
        tTitle, tAuthor, tYear, tISBN = fCheckValidProperties()
        tID = backend.fCheckForMultipleEntries(
            tTitle, tAuthor, tYear, tISBN)
        if len(tID) == 1:
            raise Ex.EntryExistsError
    except ValueError:
        print("Year and ISBN must be integers.")
    except Ex.EmptyEntryError:
        print("All fields must have a value.")
    except Ex.EditionExistsError:
        print("Found book(s) with this title and author, but different years "
              "and ISBN. Rename new entry with edition?")
    except Ex.MultipleIdenticalEntriesError:
        print("Many entries exist with these properties. Clean database.")
    except Ex.EntryExistsError:
        print("Entry already in database.")
    else:
        backend.fAddEntry(tTitle, tAuthor, tYear, tISBN)
        fViewAll()


def fDeleteSelected():
    try:
        tTitle, tAuthor, tYear, tISBN = fCheckValidProperties()
    except ValueError:
        print("Year and ISBN must be integers.")
    except Ex.EmptyEntryError:
        print("All fields must have a value.")
    else:
        tID = listbox_Results.get(listbox_Results.curselection()[0])[0]
        backend.fDeleteEntry(tID, tTitle, tAuthor, tYear, tISBN)
        fViewAll()


def fUpdateSelected():
    try:
        tTitle, tAuthor, tYear, tISBN = fCheckValidProperties()
        tID = backend.fCheckForMultipleEntries(
            tTitle, tAuthor, tYear, tISBN)
        if len(tID) == 1:
            raise Ex.EntryExistsError
        else:
            tID = listbox_Results.get(listbox_Results.curselection()[0])[0]
    except ValueError:
        print("Year and ISBN must be integers.")
    except Ex.EmptyEntryError:
        print("All fields must have a value.")
    except Ex.EntryExistsError:
        print("The updated information matches a book in the database.")
    else:
        backend.fUpdateEntry(tID, tTitle, tAuthor, tYear, tISBN)
        fViewAll()


def fClose():
    print("Close")


# =====
# Set constants

BUTTON_WIDTH = 12
ENTRY_WIDTH = 20
LABEL_WIDTH = 6

# =====
# Initialize the Window
window_Main = tkin.Tk()

# =====
# Buttons
# Initialize and place the Button widgets
button_ViewAll = tkin.Button(
    window_Main, width=BUTTON_WIDTH,
    text="View All", command=fViewAll)
button_SearchEntry = tkin.Button(
    window_Main, width=BUTTON_WIDTH,
    text="Search Entry", command=fSearchEntry)
button_AddEntry = tkin.Button(
    window_Main, width=BUTTON_WIDTH,
    text="Add Entry", command=fAddEntry)
button_UpdateSelected = tkin.Button(
    window_Main, width=BUTTON_WIDTH,
    text="Update Selected", command=fUpdateSelected)
button_DeleteSelected = tkin.Button(
    window_Main, width=BUTTON_WIDTH,
    text="Delete Selected", command=fDeleteSelected)
button_Close = tkin.Button(
    window_Main, width=BUTTON_WIDTH,
    text="Close", command=window_Main.destroy)

button_ViewAll.grid(row=2, column=3)
button_SearchEntry.grid(row=3, column=3)
button_AddEntry.grid(row=4, column=3)
button_UpdateSelected.grid(row=5, column=3)
button_DeleteSelected.grid(row=6, column=3)
button_Close.grid(row=7, column=3)

# =====
# Entry fields
# The values of the Entry fields needs to be defined before the Entry
entry_Title_val = tkin.StringVar()
entry_Year_val = tkin.StringVar()
entry_Author_val = tkin.StringVar()
entry_ISBN_val = tkin.StringVar()

# Initialize and place the Entry widgets
entry_Title = tkin.Entry(window_Main, width=ENTRY_WIDTH,
                      textvariable=entry_Title_val)
entry_Author = tkin.Entry(window_Main, width=ENTRY_WIDTH,
                       textvariable=entry_Author_val)
entry_Year = tkin.Entry(window_Main, width=ENTRY_WIDTH,
                     textvariable=entry_Year_val)
entry_ISBN = tkin.Entry(window_Main, width=ENTRY_WIDTH,
                     textvariable=entry_ISBN_val)

entry_Title.grid(row=0, column=1)
entry_Author.grid(row=0, column=3)
entry_Year.grid(row=1, column=1)
entry_ISBN.grid(row=1, column=3)

# =====
# Labels
# Initialize and place the Label widgets
label_Title = tkin.Label(window_Main, width=LABEL_WIDTH, text="Title")
label_Year = tkin.Label(window_Main, width=LABEL_WIDTH, text="Year")
label_Author = tkin.Label(window_Main, width=LABEL_WIDTH, text="Author")
label_ISBN = tkin.Label(window_Main, width=LABEL_WIDTH, text="ISBN")

label_Title.grid(row=0, column=0)
label_Author.grid(row=0, column=2)
label_Year.grid(row=1, column=0)
label_ISBN.grid(row=1, column=2)

# =====
# Listbox and Scrollbar
# Initialize and place the Listbox and Scrollbar widgets
listbox_Results = tkin.Listbox(
    window_Main, width=2 * LABEL_WIDTH + ENTRY_WIDTH)
scrollbar_Results = tkin.Scrollbar(window_Main)

listbox_Results.grid(row=2, column=0, rowspan=6, columnspan=2)
listbox_Results.configure(
    yscrollcommand=scrollbar_Results.set, exportselection=False)
listbox_Results.bind("<<ListboxSelect>>", fGetSelected)

scrollbar_Results.grid(row=2, column=2, rowspan=6)
scrollbar_Results.configure(command=listbox_Results.yview)

# =====
# Main Process

window_Main.after_idle(fViewAll)
window_Main.mainloop()
