import customtkinter
import os
import sys
import pandas as pd
import time
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm


from PIL import Image
from PIL import ImageTk

from page import product_update
from page import product_state
from page import about

import logging


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # 路徑定義
        base_path = ""  # 運行路徑
        root_path = ""  # 腳本路徑
        image_path = ""  # 圖片路徑

        if getattr(sys, "frozen", False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        root_path = os.path.dirname(os.path.realpath(__file__))

        image_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_images"
        )
        # 路徑定義

        # 設定日誌
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s  - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(os.path.join(base_path, "sdc_data", "app.log")),
                logging.StreamHandler(),
            ],
        )

        logging.getLogger("PIL").setLevel(logging.WARNING)

        # 設定日誌

        self.iconpath = ImageTk.PhotoImage(file=os.path.join(image_path, "logo.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)

        self.title("SDC Importer - 商品更新器")
        self.geometry("850x650")

        # 檢查並建立資料夾
        os.makedirs(os.path.join(base_path, "sdc_data", "state"), exist_ok=True)
        os.makedirs(os.path.join(base_path, "sdc_data", "update"), exist_ok=True)

        style = {"font": ("微軟正黑體", 14, "bold")}

        # load images with light and dark mode image

        self.logo_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "logo.png")),
            size=(26, 26),
        )

        self.home_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "update_icon.png")),
            dark_image=Image.open(os.path.join(image_path, "update_icon.png")),
            size=(20, 20),
        )
        self.product_status_icon_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "product_status_icon.png")),
            dark_image=Image.open(os.path.join(image_path, "product_status_icon.png")),
            size=(20, 20),
        )

        self.about_icon_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "about_icon.png")),
            dark_image=Image.open(os.path.join(image_path, "about_icon.png")),
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
            text_color=("#438ab0"),
        )
        self.navigation_frame_label.pack(anchor="w", padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="更新商品資料",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("#b4eaff", "#b4eaff"),
            image=self.home_image,
            anchor="w",
            command=lambda: self.select_frame_by_name("home"),
        )
        self.home_button.pack(fill="x")
        self.home_button.configure(**style)

        self.frame_2_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="變更商品狀態",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("#b4eaff", "#b4eaff"),
            image=self.product_status_icon_image,
            anchor="w",
            command=lambda: self.select_frame_by_name("frame_2"),
        )
        self.frame_2_button.pack(fill="x")
        self.frame_2_button.configure(**style)

        self.about_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="About",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("#b4eaff", "#b4eaff"),
            image=self.about_icon_image,
            anchor="w",
            command=self.about_button_event,
        )
        self.about_button.pack(fill="x", side="bottom", pady=(0, 0))

        self.about_button.configure(**style)

        # create home frame

        self.product_update = product_update.ProductUpdate(
            self, image_path, base_path, root_path
        )

        # create second frame

        self.product_state = product_state.ProductState(
            self, image_path, base_path, root_path
        )

        self.about = about.About(self, image_path, base_path, root_path)

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        self.buttons = {
            "home": self.home_button,
            "frame_2": self.frame_2_button,
            "about": self.about_button,
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

        if name == "about":
            self.about.pack(fill="both", expand=True)
            self.buttons["about"].configure(fg_color="#b4eaff")
        else:
            self.about.pack_forget()

    def about_button_event(self):
        self.select_frame_by_name("about")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
