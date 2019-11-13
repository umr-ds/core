"""
mobility configuration
"""
import logging
import tkinter as tk
from tkinter import filedialog, ttk

from coretk import appconfig
from coretk.dialogs.dialog import Dialog


class MobilityConfigDialog(Dialog):
    def __init__(self, master, app, canvas_node):
        """
        create an instance of mobility configuration

        :param app: core application
        :param root.master master:
        """
        super().__init__(master, app, "ns2script configuration", modal=True)
        self.canvas_node = canvas_node
        logging.info(app.canvas.core.mobilityconfig_management.configurations)
        self.node_config = app.canvas.core.mobilityconfig_management.configurations[
            canvas_node.core_id
        ]

        self.mobility_script_parameters()
        self.ns2script_options()
        self.loop = "On"

    def create_string_var(self, val):
        """
        create string variable for entry widget

        :return: nothing
        """
        var = tk.StringVar()
        var.set(val)
        return var

    def open_file(self, entry):
        filename = filedialog.askopenfilename(
            initialdir=str(appconfig.MOBILITY_PATH), title="Open"
        )
        if filename:
            entry.delete(0, tk.END)
            entry.insert(0, filename)

    def set_loop_value(self, value):
        """
        set loop value when user changes the option
        :param value:
        :return:
        """
        self.loop = value

    def create_label_entry_filebrowser(
        self, parent_frame, text_label, entry_text, filebrowser=False
    ):
        f = ttk.Frame(parent_frame)
        lbl = ttk.Label(f, text=text_label)
        lbl.grid(padx=3, pady=3)
        # f.grid()
        e = ttk.Entry(f, textvariable=self.create_string_var(entry_text))
        e.grid(row=0, column=1, padx=3, pady=3)
        if filebrowser:
            b = ttk.Button(f, text="...", command=lambda: self.open_file(e))
            b.grid(row=0, column=2, padx=3, pady=3)
        f.grid(sticky=tk.E)

    def mobility_script_parameters(self):
        lbl = ttk.Label(self.top, text="node ns2script")
        lbl.grid(sticky="ew")

        sb = ttk.Scrollbar(self.top, orient=tk.VERTICAL)
        sb.grid(row=1, column=1, sticky="ns")

        f = ttk.Frame(self.top)
        lbl = ttk.Label(f, text="ns-2 Mobility Scripts Parameters")
        lbl.grid(row=0, column=0, sticky=tk.W)

        f1 = tk.Canvas(
            f,
            yscrollcommand=sb.set,
            bg="#d9d9d9",
            relief=tk.RAISED,
            highlightbackground="#b3b3b3",
            highlightcolor="#b3b3b3",
            highlightthickness=0.5,
            bd=0,
        )
        self.create_label_entry_filebrowser(
            f1, "mobility script file", self.node_config["file"], filebrowser=True
        )
        self.create_label_entry_filebrowser(
            f1, "Refresh time (ms)", self.node_config["refresh_ms"]
        )

        # f12 = ttk.Frame(f1)
        #
        # lbl = ttk.Label(f12, text="Refresh time (ms)")
        # lbl.grid()
        #
        # e = ttk.Entry(f12, textvariable=self.create_string_var("50"))
        # e.grid(row=0, column=1)
        # f12.grid()

        f13 = ttk.Frame(f1)

        lbl = ttk.Label(f13, text="loop")
        lbl.grid()

        om = ttk.OptionMenu(
            f13, self.create_string_var("On"), "On", "Off", command=self.set_loop_value
        )
        om.grid(row=0, column=1)

        f13.grid(sticky=tk.E)

        self.create_label_entry_filebrowser(
            f1, "auto-start seconds (0.0 for runtime)", self.node_config["autostart"]
        )
        # f14 = ttk.Frame(f1)
        #
        # lbl = ttk.Label(f14, text="auto-start seconds (0.0 for runtime)")
        # lbl.grid()
        #
        # e = ttk.Entry(f14, textvariable=self.create_string_var(""))
        # e.grid(row=0, column=1)
        #
        # f14.grid()
        self.create_label_entry_filebrowser(
            f1, "node mapping (optional, e.g. 0:1, 1:2, 2:3)", self.node_config["map"]
        )
        # f15 = ttk.Frame(f1)
        #
        # lbl = ttk.Label(f15, text="node mapping (optional, e.g. 0:1, 1:2, 2:3)")
        # lbl.grid()
        #
        # e = ttk.Entry(f15, textvariable=self.create_string_var(""))
        # e.grid(row=0, column=1)
        #
        # f15.grid()

        self.create_label_entry_filebrowser(
            f1,
            "script file to run upon start",
            self.node_config["script_start"],
            filebrowser=True,
        )
        self.create_label_entry_filebrowser(
            f1,
            "script file to run upon pause",
            self.node_config["script_pause"],
            filebrowser=True,
        )
        self.create_label_entry_filebrowser(
            f1,
            "script file to run upon stop",
            self.node_config["script_stop"],
            filebrowser=True,
        )
        f1.grid()
        sb.config(command=f1.yview)
        f.grid(row=1, column=0)

    def ns2script_apply(self):
        """

        :return:
        """
        config_frame = self.grid_slaves(row=1, column=0)[0]
        canvas = config_frame.grid_slaves(row=1, column=0)[0]
        file = (
            canvas.grid_slaves(row=0, column=0)[0].grid_slaves(row=0, column=1)[0].get()
        )

        refresh_time = (
            canvas.grid_slaves(row=1, column=0)[0].grid_slaves(row=0, column=1)[0].get()
        )
        auto_start_seconds = (
            canvas.grid_slaves(row=3, column=0)[0].grid_slaves(row=0, column=1)[0].get()
        )

        node_mapping = (
            canvas.grid_slaves(row=4, column=0)[0].grid_slaves(row=0, column=1)[0].get()
        )

        file_upon_start = (
            canvas.grid_slaves(row=5, column=0)[0].grid_slaves(row=0, column=1)[0].get()
        )
        file_upon_pause = (
            canvas.grid_slaves(row=6, column=0)[0].grid_slaves(row=0, column=1)[0].get()
        )
        file_upon_stop = (
            canvas.grid_slaves(row=7, column=0)[0].grid_slaves(row=0, column=1)[0].get()
        )

        # print("mobility script file: ", file)
        # print("refresh time: ", refresh_time)
        # print("auto start seconds: ", auto_start_seconds)
        # print("node mapping: ", node_mapping)
        # print("script file to run upon start: ", file_upon_start)
        # print("file upon pause: ", file_upon_pause)
        # print("file upon stop: ", file_upon_stop)
        if self.loop == "On":
            loop = "1"
        else:
            loop = "0"
        self.app.canvas.core.mobilityconfig_management.set_custom_configuration(
            node_id=self.canvas_node.core_id,
            file=file,
            refresh_ms=refresh_time,
            loop=loop,
            autostart=auto_start_seconds,
            node_mapping=node_mapping,
            script_start=file_upon_start,
            script_pause=file_upon_pause,
            script_stop=file_upon_stop,
        )

        self.destroy()

    def ns2script_options(self):
        """
        create the options for ns2script configuration

        :return: nothing
        """
        f = ttk.Frame(self.top)
        b = ttk.Button(f, text="Apply", command=self.ns2script_apply)
        b.grid()
        b = ttk.Button(f, text="Cancel", command=self.destroy)
        b.grid(row=0, column=1)
        f.grid()
