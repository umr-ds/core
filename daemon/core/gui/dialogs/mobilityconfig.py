"""
mobility configuration
"""
from tkinter import ttk
from typing import TYPE_CHECKING, Dict, Optional

import grpc

from core.api.grpc.common_pb2 import ConfigOption
from core.api.grpc.core_pb2 import Node
from core.gui.dialogs.dialog import Dialog
from core.gui.themes import PADX, PADY
from core.gui.widgets import ConfigFrame

if TYPE_CHECKING:
    from core.gui.app import Application
    from core.gui.graph.node import CanvasNode


class MobilityConfigDialog(Dialog):
    def __init__(self, app: "Application", canvas_node: "CanvasNode") -> None:
        super().__init__(app, f"{canvas_node.core_node.name} Mobility Configuration")
        self.canvas_node: "CanvasNode" = canvas_node
        self.node: Node = canvas_node.core_node
        self.config_frame: Optional[ConfigFrame] = None
        self.has_error: bool = False
        try:
            config = self.canvas_node.mobility_config
            if not config:
                config = self.app.core.get_mobility_config(self.node.id)
            self.config: Dict[str, ConfigOption] = config
            self.draw()
        except grpc.RpcError as e:
            self.app.show_grpc_exception("Get Mobility Config Error", e)
            self.has_error: bool = True
            self.destroy()

    def draw(self) -> None:
        self.top.columnconfigure(0, weight=1)
        self.top.rowconfigure(0, weight=1)
        self.config_frame = ConfigFrame(self.top, self.app, self.config)
        self.config_frame.draw_config()
        self.config_frame.grid(sticky="nsew", pady=PADY)
        self.draw_apply_buttons()

    def draw_apply_buttons(self) -> None:
        frame = ttk.Frame(self.top)
        frame.grid(sticky="ew")
        for i in range(2):
            frame.columnconfigure(i, weight=1)

        button = ttk.Button(frame, text="Apply", command=self.click_apply)
        button.grid(row=0, column=0, padx=PADX, sticky="ew")

        button = ttk.Button(frame, text="Cancel", command=self.destroy)
        button.grid(row=0, column=1, sticky="ew")

    def click_apply(self) -> None:
        self.config_frame.parse_config()
        self.canvas_node.mobility_config = self.config
        self.destroy()
