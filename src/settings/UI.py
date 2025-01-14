import tkinter, ntkutils, darkdetect
from tkinter import ttk, font
from generatesize import system

import config
import vars as v

def dark():
    if cfg["theme"] == "Dark" or (cfg["theme"] == "System" and darkdetect.isDark()):
        return True
    else:
        return False


def appearance():
    global boxtheme, boxfont, boxsize, btnnumbers, btnhighlight, page

    savechanges()
    clearstates()

    btnappearence.configure(style="Accent.TButton")
    if dark(): btnappearence.configure(image=v.brush_light)
    else: btnappearence.configure(image=v.brush_dark)

    ntkutils.clearwin(frameright)

    page = "appearance"

    lbltheme = tkinter.Label(frameright, text="Theme:").place(x=10, y=15)
    boxtheme = ttk.Combobox(frameright, values=["Dark", "Light", "System"], state="readonly", width=25)
    boxtheme.set(cfg["theme"])
    boxtheme.pack(padx=10, pady=10, anchor="e")

    lblfont = tkinter.Label(frameright, text="Font:").place(x=10, y=67)
    boxfont = ttk.Combobox(frameright, state="readonly", values=fonts, width=15)
    boxfont.set(cfg["font"])
    boxfont.pack(padx=80, pady=10, anchor="e")
    boxsize = ttk.Entry(frameright, width=5)
    boxsize.insert(0, cfg["font-size"])
    boxsize.place(x=260, y=63)

    lblnumbers = tkinter.Label(frameright, text="Display line numbers:").place(x=10, y=118)
    btnnumbers = ttk.Checkbutton(frameright, style="Switch.TCheckbutton")
    btnnumbers.pack(padx=10, pady=10, anchor="e")
    btnnumbers.state(["!alternate"])
    if cfg["linenumbers"]: btnnumbers.state(["!alternate", "selected"])
    numbersinfo = tkinter.Label(frameright, text="Requires restart", justify="left", fg="grey").place(x=10, y=148)

    lblhighlight = tkinter.Label(frameright, text="Syntax Highlighting:").place(x=10, y=200)
    btnhighlight = ttk.Checkbutton(frameright, style="Switch.TCheckbutton")
    btnhighlight.pack(padx=10, pady=40, anchor="e")
    btnhighlight.state(["!alternate"])
    if cfg["syntax-highlighting"]: btnhighlight.state(["!alternate", "selected"])


def experimental():
    global page, btnmica, btnhotkeys

    savechanges()
    clearstates()

    btnexperimental.configure(style="Accent.TButton")
    if dark(): btnexperimental.configure(image=v.warn_light)
    else: btnexperimental.configure(image=v.warn_dark)

    ntkutils.clearwin(frameright)

    page = "experimental"

    lblmica = tkinter.Label(frameright, text="Mica Blur:").place(x=10, y=12)
    btnmica = ttk.Checkbutton(frameright, style="Switch.TCheckbutton")
    btnmica.pack(padx=10, pady=10, anchor="e")
    btnmica.state(["!alternate"])
    if cfg["mica"]: btnmica.state(["!alternate", "selected"])
    micainfo = tkinter.Label(frameright, text="When switching from dark to light theme with this\noption enabled, you have to perform a restart!", justify="left", fg="grey").place(x=10, y=42)

def hotkeys():
    global page, entryopen, entrysave

    savechanges()
    clearstates()

    btnhotkeys.configure(style="Accent.TButton")
    if dark(): btnhotkeys.configure(image=v.keyboard_light)
    else: btnhotkeys.configure(image=v.keyboard_dark)


    ntkutils.clearwin(frameright)

    page = "hotkeys"

    lblopen = tkinter.Label(frameright, text="Open:").place(x=10, y=12)
    entryopen = ttk.Entry(frameright, width=25)
    entryopen.insert(0, cfg["hkey-open"])
    entryopen.pack(padx=10, pady=10, anchor="e")

    lblsave = tkinter.Label(frameright, text="Save:").place(x=10, y=67)
    entrysave = ttk.Entry(frameright, width=25)
    entrysave.insert(0, cfg["hkey-save"])
    entrysave.pack(padx=10, pady=10, anchor="e")

    lblrestart = tkinter.Label(frameright, text="These will take effect after a restart", fg="grey").pack(pady=5, anchor="w", padx=10)

def savechanges():
    if page == "appearance":
        cfg["theme"] = boxtheme.get()
        cfg["font"] = boxfont.get()
        cfg["font-size"] = boxsize.get()
        cfg["linenumbers"] = btnnumbers.instate(["selected"])
        cfg["syntax-highlighting"] = btnhighlight.instate(["selected"])

        if dark(): btnappearence.configure(image=v.brush_dark)
        else: btnappearence.configure(image=v.brush_light)
    elif page == "experimental":
        cfg["mica"] = btnmica.instate(["selected"])

        if dark(): btnexperimental.configure(image=v.warn_dark)
        else: btnexperimental.configure(image=v.warn_light)
    elif page == "hotkeys":
        cfg["hkey-open"] = entryopen.get()
        cfg["hkey-save"] = entrysave.get()

        if dark(): btnhotkeys.configure(image=v.keyboard_dark)
        else: btnhotkeys.configure(image=v.keyboard_light)

def apply():
    global page, save

    savechanges()

    ntkutils.cfgtools.SaveCFG(cfg)
    save = True
    settings.destroy()


def build():
    global frameright, frameleft, btnappearence, btnexperimental, btnhotkeys, settings, page, cfg, save

    cfg = config.get()
    page = ""
    save = False

    settings = tkinter.Toplevel()
    ntkutils.windowsetup(settings, "txt2 - Settings", "assets/logo.png", False, "500x400")
    if system != "Darwin":
        ntkutils.dark_title_bar(settings)

    frameleft = tkinter.Frame(settings, width=175, bg="#f3f3f3")
    frameleft.pack(side=tkinter.LEFT, fill="y")
    frameleft.pack_propagate(False)

    frameright = tkinter.Frame(settings, width=325)
    frameright.pack(side=tkinter.LEFT, fill="both")
    frameright.pack_propagate(False)

    btnappearence = ttk.Button(frameleft, text="Appearence", style="Accent.TButton", width=16, command=appearance, image=v.brush_dark, compound="left")
    btnappearence.pack(pady=10)

    btnhotkeys = ttk.Button(frameleft, text="Hotkeys", width=16, command=hotkeys, image=v.keyboard_light, compound="left")
    btnhotkeys.pack()

    btnexperimental = ttk.Button(frameleft, text="Unstable Features", width=16, command=experimental, image=v.warn_light, compound="left")
    btnexperimental.pack(pady=10)

    btnapply = ttk.Button(frameleft, text="Apply", style="Accent.TButton", width=20, command=apply)
    btnapply.pack(side=tkinter.BOTTOM, pady=10)

    if dark():
        frameleft.configure(bg="#202020")

        btnappearence.configure(image=v.brush_light)
        btnexperimental.configure(image=v.warn_dark)
        btnhotkeys.configure(image=v.keyboard_dark)

    getfonts()
    appearance()

def clearstates():
    for i in frameleft.pack_slaves():
        i.configure(style="TButton")

def getfonts():
    global fonts
    fonts=list(font.families())
    fonts.sort()
