import tkinter


def search(v):
    return "Here is result"


def do_search():
    value = entry.get()
    content = search(value)
    result = tkinter.Tk()
    result.title("Search Result")
    result.geometry("800x500")
    result.resizable(width=True, height=True)
    result_label = tkinter.Label(result, text="Search Result About " + value, fg="blue",
                                 font=("media/Product Sans.ttf", 36))
    result_label.pack()
    result_content = tkinter.Label(result, text=content, fg="black", font=("media/Product Sans.ttf", 24))
    result_content.pack()
    result_back_button = tkinter.Button(result, text="back", font=("media/Product Sans.ttf", 16),
                                        command=result.destroy)
    result_back_button.pack(side="bottom")


# basic interface
ui = tkinter.Tk()
ui.title("Opinion Spam Detection @ dianping.com")
ui.geometry("800x500")
ui.resizable(width=False, height=False)
label = tkinter.Label(ui, text="\n\n\nOpinion Spam Detection @ dianping.com", fg="blue",
                      font=("media/Product Sans.ttf", 36))
label.pack(side="top")
# entry
entry = tkinter.Entry(ui, font=("media/Product Sans.ttf", 24))
entry.pack()
# search button
search_button = tkinter.Button(ui, text="search", font=("media/Product Sans.ttf", 16), command=do_search)
search_button.pack()
# quit button
quit_button = tkinter.Button(ui, text="quit", font=("media/Product Sans.ttf", 16), command=ui.destroy)
quit_button.pack(side="bottom")
# start and loop
ui.mainloop()
