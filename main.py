import customtkinter
import os
import sys
import pandas as pd
import time
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm

from PIL import Image

from page import product_update
from page import product_state
from page import about_frame


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("SDC Importer - 商品資料更新器")
        self.geometry("850x650")

        custom_font = ("Times", 30, "bold")

        # 專案路徑定義
        base_path = ""

        if getattr(sys, "frozen", False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.dirname(os.path.realpath(__file__))
        # 專案路徑定義

        # 檢查並建立資料夾
        os.makedirs(os.path.join(base_path, "sdc_data", "state"), exist_ok=True)
        os.makedirs(os.path.join(base_path, "sdc_data", "update"), exist_ok=True)

        style = {"font": ("微軟正黑體", 14, "bold")}

        # load images with light and dark mode image
        image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_images"
        )
        self.logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
            size=(26, 26),
        )
        self.large_test_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "large_test_image.png")),
            size=(500, 150),
        )
        self.image_icon_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20)
        )
        self.home_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "home_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "home_light.png")),
            size=(20, 20),
        )
        self.chat_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
            size=(20, 20),
        )
        self.add_user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")),
            size=(20, 20),
        )

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.pack(side="left", fill="y")
        self.navigation_frame.configure(fg_color="#d9f4ff")

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="  SDC Importer",
            image=self.logo_image,
            compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_label.pack(anchor="w", padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="商品資料更新",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("#b4eaff", "#b4eaff"),
            image=self.home_image,
            anchor="w",
            command=self.home_button_event,
        )
        self.home_button.pack(fill="x")
        self.home_button.configure(**style)

        self.frame_2_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="商品上下架",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("#b4eaff", "#b4eaff"),
            image=self.chat_image,
            anchor="w",
            command=self.frame_2_button_event,
        )
        self.frame_2_button.pack(fill="x")
        self.frame_2_button.configure(**style)

        self.frame_3_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="商品上下架",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("#b4eaff", "#b4eaff"),
            image=self.chat_image,
            anchor="w",
        )
        self.frame_3_button.pack(fill="x", side="bottom", pady=(0, 0))

        self.frame_3_button.configure(**style)

        # create home frame

        self.product_update = product_update.ProductUpdate(
            self, self.large_test_image, base_path, root_path
        )

        # create second frame

        self.product_state = product_state.ProductState(
            self, self.large_test_image, base_path, root_path
        )

        # create third frame
        self.about_frame = about_frame.AboutFrame(self, self.large_test_image)

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        self.buttons = {
            "home": self.home_button,
            "frame_2": self.frame_2_button,
        }
        for button in self.buttons.values():
            button.configure(fg_color="transparent")
        # show selected frame
        if name == "home":
            self.product_update.pack(fill="both", expand=True)
            self.buttons["home"].configure(fg_color="#b4eaff")
        else:
            self.product_update.pack_forget()
        if name == "frame_2":
            self.product_state.pack(fill="both", expand=True)
            self.buttons["frame_2"].configure(fg_color="#b4eaff")
        else:
            self.product_state.pack_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
