import customtkinter
import os
from PIL import Image

import webbrowser


class About(customtkinter.CTkFrame):
    def __init__(self, parent, image_path, base_path, root_path):
        super().__init__(parent, corner_radius=0, fg_color="white")
        style = {"font": ("微軟正黑體", 14, "bold")}

        self.large_test_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "about.png")),
            size=(500, 100),
        )

        self.second_frame_large_image_label = customtkinter.CTkLabel(
            self, text="", image=self.large_test_image
        )
        self.second_frame_large_image_label.pack(padx=20, pady=10)

        self.CTkLabel = customtkinter.CTkLabel(
            self,
            text="Developer : ninull \nSource Code :",
            text_color="#a3a3a3",
            fg_color="transparent",
            justify="left",
            **style,
        )
        self.CTkLabel.pack(padx=(0, 0), pady=(100, 0), fill="both")

        self.label = customtkinter.CTkLabel(
            self,
            text="https://github.com/ni-null/SDC_Importer",
            text_color="#4fa5e2",
            **style,
            cursor="hand2",
        )
        self.label.pack(padx=0, pady=0)

        self.label._label.bind(
            "<Button-1>",
            lambda event: webbrowser.open_new_tab(
                "https://github.com/ni-null/SDC_Importer"
            ),
        )
