import click
import logging
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

filepath = Path(__file__).resolve()


# Set logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)


class GUI(ttk.Frame):
    def __init__(self, root: tk.Tk, click_cmd: click.Command) -> None:
        """
        Populates a ttk GUI with widgets based on Click parameters.
        
        :param tk.Tk root: Tkinter top-level widget / main window.
        :param click.Command click_cmd: Click Command function.
        """
        
        super().__init__(root)
        self.root = root
        self.params = click_cmd.params
        self.padx = 0
        self.pady = 15
        self.padx_widget = 10
        self.pady_widget = 5
        
        # Define return variables.
        self.args = list()
        self.kwargs = list()
        self.kwargs_opts = dict()
        self.cli_args = list()
        
        # Make GUI frame responsive.
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Create canvas to hold frame for widgets.
        # Note: Required to associate scrollbar with all widgets since scrollbar cannot associate with root or frame.
        self.canvas = tk.Canvas(self)
        self.canvas.grid(column=0, row=0, sticky="nsew")
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.rowconfigure(0, weight=1)
        
        # Create frame for widgets.
        self.widget_frame = ttk.Frame(self.canvas)
        self.widget_frame.columnconfigure(0, weight=0)
        self.widget_frame.columnconfigure(1, weight=1)
        self.widget_frame.columnconfigure(2, weight=0)
        self.widget_frame.grid(column=0, row=0, padx=self.padx, pady=self.pady, sticky="nsew")
        
        # Iterate click parameters and create widgets.
        for idx, param in enumerate(self.params):
            self.create_widget(param_info=param.to_info_dict(), row_idx=idx)
        
        # Create scrollbar and associate yview with canvas containing widgets frame.
        # Note: Window required within canvas to be scrollable.
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(column=1, row=0, sticky="ns")
        self._window_id = self.canvas.create_window((0, 0), window=self.widget_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self._on_configure)
        
        # Add button widget (in new frame) for starting code execution.
        run_frame = ttk.Frame(self)
        run_frame.columnconfigure(0, weight=1)
        run_frame.columnconfigure(1, weight=1)
        run_frame.columnconfigure(2, weight=1)
        run_frame.grid(column=0, row=1, padx=self.padx, pady=self.pady * 2, sticky="nsew")
        run_button = ttk.Button(run_frame, text="Run", command=lambda: self.run())
        run_button.grid(column=1, row=0, padx=self.padx, pady=self.pady, sticky="ew")
    
    def _on_configure(self, event: tk.Event) -> None:
        """
        Update scrollable area and canvas window width when canvas changes size.
        
        :param tk.Event event: Tkinter event.
        """
        
        self.canvas.configure(scrollregion=self.widget_frame.bbox("all"))
        self.canvas.itemconfig(self._window_id, width=self.canvas.winfo_width())
    
    def create_widget(self, param_info: dict, row_idx: int) -> None:
        """
        Creates a ttk widget from a Click parameter.
        
        :param dict pram_info: Dictionary of click parameter information returned by `to_info_dict`.
        :param int row_idx: Index of the row where the widget will be placed.
        """
        
        # Compile common parameter info.
        param_arg_kwarg = param_info["param_type_name"]
        param_kwargs = param_info["type"]
        param_type = param_info["type"]["param_type"]
        param_default = param_info["default"]
        param_name = param_info["name"]
        param_opts = param_info["opts"][0]
        
        # Store parameter name under arg or kwarg tracker.
        if param_arg_kwarg == "argument":
            self.args.append(param_name)
        else:
            self.kwargs.append(param_name)
            self.kwargs_opts[param_name] = param_opts
        
        # Create label widget and set grid position.
        label = ttk.Label(self.widget_frame, text=f"{param_name.title()}:")
        label.grid(column=0, row=row_idx, padx=self.padx_widget, pady=self.pady_widget, sticky="w")
        
        # Create placeholder for button.
        button = None
        
        # Click type: Int
        if param_type == "Int":
            
            # Create entry widget.
            widget = ttk.Entry(self.widget_frame, name=param_name)
            if param_default:
                widget.insert(0, param_default)
        
        # Click type: String
        elif param_type == "String":
            
            # Create entry widget.
            widget = ttk.Entry(self.widget_frame, name=param_name)
            if param_default:
                widget.insert(0, param_default)
        
        # Click type: Bool.
        elif param_type == "Bool":
            
            # Create entry widget.
            widget = ttk.Checkbutton(self.widget_frame, name=param_name)
            state = "selected" if (param_default and isinstance(param_default, bool)) else "active"
            widget.state([f"{state} !alternate"])
        
        # Click type: Choice.
        elif param_type == "Choice":
            
            # Create combobox widget.
            widget = ttk.Combobox(self.widget_frame, name=param_name, values=param_kwargs["choices"])
            widget.current(0 if not param_default else param_kwargs["choices"].index(param_default))
        
        # Click type: IntRange
        elif param_type == "IntRange":
            
            # Create spinbox widget.
            widget = ttk.Spinbox(self.widget_frame, name=param_name, from_=param_kwargs["min"], to=param_kwargs["max"])
            if param_default:
                widget.insert(0, param_default)
        
        # Click type: Path
        elif param_type == "Path":
            
            # Flag invalid file / dir combinations.
            if all([param_kwargs["file_okay"], param_kwargs["dir_okay"]]) or \
            not any([param_kwargs["file_okay"], param_kwargs["dir_okay"]]):
                logger.exception(f"Invalid parameters for name={param_name}, type={param_type}. One, and only one, of "\
                                 "'file_okay' and 'dir_okay' must be True.", exc_info=False)
                sys.exit(1)
            
            # Create entry widget.
            widget = ttk.Entry(self.widget_frame, name=param_name)
            if param_default:
                widget.insert(0, param_default)
            
            # Create file dialog button.
            button = ttk.Button(self.widget_frame, text="Browse", command=lambda: 
                                self.populate_path(widget=widget, file_okay=param_kwargs["file_okay"]))
        
        # Click type: None.
        else:
            
            logger.exception(f"Unsupported Click parameter type={param_type} for name={param_name}.", exc_info=False)
            sys.exit(1)
        
        # Set widget and button grid positions.
        if button:
            widget.grid(column=1, row=row_idx, columnspan=2, padx=self.padx_widget, pady=self.pady_widget, sticky="ew")
            button.grid(column=3, row=row_idx, columnspan=1, padx=self.padx_widget, pady=self.pady_widget, sticky="ew")
        else:
            widget.grid(column=1, row=row_idx, columnspan=3, padx=self.padx_widget, pady=self.pady_widget, sticky="ew")
    
    def populate_path(self, widget: ttk.Entry, file_okay: bool) -> None:
        """
        Opens the file dialog window and inserts the selected file / directory path into the corresponding widget.
        
        :param ttk.Entry widget: Entry widget to be populated.
        :param bool file_okay: Indicates if the path should be a file, as opposed to a directory.
        """
        
        # Get file path.
        if file_okay:
            path = filedialog.askopenfilename(initialdir="C:/")
        else:
            path = filedialog.askdirectory(initialdir="C:/")
        
        # Insert path into widget.
        widget.delete(0, "end")
        widget.insert(0, path)
    
    def run(self) -> None:
        """Compiles the names and values of all valid widgets as a list of CLI args."""
        
        # Compile widget values.
        for widget in self.widget_frame.winfo_children():
            name = widget.winfo_name()
            
            # Get value - Revert to using selection status of `state` for widgets without `get`.
            if "get" in dir(widget):
                value = widget.get()
            elif isinstance(widget, ttk.Checkbutton):
                if len(widget.state()):
                    value = bool(widget.state()[0] == "selected")
                else:
                    value = False
            else:
                continue
            
            # Compile args.
            if name in self.args:
                self.cli_args.append(value)
            
            # Compile kwargs.
            elif name in self.kwargs:
                self.cli_args.extend([self.kwargs_opts[name], value])
            
            # Skip others values (they come from non-widgets).
            else:
                continue
        
        # Close gui.
        self.root.destroy()


def gui(click_cmd: click.Command, calling_script: Path) -> list[str, ...]:
    """
    Creates a GUI wrapper around Click CLI.
    
    :param click.Command click_cmd: Click Command function.
    :param Path calling_script: Path of the calling script.
    
    :return list[str, ...]: List of CLI args.
    """
    
    # Define main window; hide (withdraw) until all contents are created.
    root = tk.Tk()
    root.withdraw()
    root.title(calling_script.stem.replace("_", " ").title())
    
    # Set theme.
    root.tk.call("source", f"{filepath.parent}/theme/theme.tcl")
    root.tk.call("set_theme", "dark")
    
    # Create GUI in window.
    gui_ = GUI(root=root, click_cmd=click_cmd)
    gui_.pack(fill="both", expand=True)
    
    # Set window size and position.
    root.minsize(width=int(root.winfo_screenwidth() / 4), height=int(root.winfo_screenheight() / 2))
    root.maxsize(width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    root.update()
    x_coords = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_coords = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry(f"+{x_coords}+{y_coords - 20}")
    
    # Make window resizable and add sizegrip.
    root.resizable(width=True, height=True)
    sizegrip = ttk.Sizegrip(root)
    sizegrip.place(relx=1, rely=1, anchor="se")
    
    # Add button widget for switching theme.
    switch_theme_button = ttk.Checkbutton(root, text="Dark / Light Mode", style="SwitchTheme.TCheckbutton", 
                                          command=lambda: switch_theme(root))
    switch_theme_button.place(relx=0, rely=1, anchor="sw")
    
    # Unhide (deiconify) main window and start mainloop.
    root.deiconify()
    root.mainloop()
    
    # Return CLI args once gui is closed.
    return gui_.cli_args


def switch_theme(root: tk.Tk) -> None:
    """
    Switches the theme between dark and light mode.
    
    :param tk.Tk root: Tkinter top-level widget / main window.
    """
    
    # Switch to light mode.
    if root.tk.call("ttk::style", "theme", "use") == "dark":
        root.tk.call("set_theme", "light")
    
    # Switch to dark mode.
    else:
        root.tk.call("set_theme", "dark")
