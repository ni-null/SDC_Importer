import tkinter
import customtkinter
import re
from PIL import Image
import os
import threading
import json
import logging

logger = logging.getLogger(__name__)

from inc import product_state_creat_csv
from inc import upload
from inc import cron


class ProductState(customtkinter.CTkFrame):
    def __init__(self, parent, image_path, base_path, root_path):
        super().__init__(parent, corner_radius=0, fg_color="white")

        style = {"font": ("微軟正黑體", 14, "bold")}

        self.large_test_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "product_status.png")),
            size=(500, 100),
        )

        self.second_frame_large_image_label = customtkinter.CTkLabel(
            self, text="", image=self.large_test_image
        )
        self.second_frame_large_image_label.pack(padx=20, pady=10)

        # 資料輸入
        self.textbox_CTkLabel = customtkinter.CTkLabel(
            self, text="資料輸入", fg_color="transparent", text_color="#56707a", **style
        )
        self.textbox_CTkLabel.pack(padx=(20, 0), pady=(10, 0))

        self.textbox = customtkinter.CTkTextbox(self, height=150)
        self.textbox.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.textbox.configure(
            **style,
            scrollbar_button_color="#ccf1ff",
            scrollbar_button_hover_color="#81dcff",
        )

        self.textbox.insert(
            customtkinter.END,
            "\n 透過 ctrl + v 在此貼上內容 \n 點擊下方按鈕將自動過濾UID格式",
        )

        # 按鈕行
        self.button_frame = customtkinter.CTkFrame(
            self, bg_color="transparent", fg_color="transparent"
        )

        self.button_frame.pack(fill="x", padx=20, pady=0)

        self.button_1 = customtkinter.CTkButton(
            self.button_frame,
            **style,
            fg_color="#fbefa5",
            text_color="#66643A",
            hover_color="#fbefa5",
            height=40,
            text="輸入解析",
            image=customtkinter.CTkImage(
                Image.open(os.path.join(image_path, "product_filter_icon.png")),
                size=(15, 15),
            ),
            command=self.parse_text,
        )
        self.button_1.pack(side="left", expand=True, padx=10, pady=0)

        self.button_2 = customtkinter.CTkButton(
            self.button_frame,
            **style,
            fg_color="#b4eaff",
            text_color="#56707a",
            hover_color="#b4eaff",
            height=40,
            text="上架商品",
            image=customtkinter.CTkImage(
                Image.open(os.path.join(image_path, "product_on_icon.png")),
                size=(15, 15),
            ),
            command=lambda: self.creat_csv(base_path, root_path, "publish"),
        )
        self.button_2.pack(side="left", expand=True, padx=10, pady=0)

        self.button_3 = customtkinter.CTkButton(
            self.button_frame,
            **style,
            fg_color="#b4eaff",
            text_color="#56707a",
            hover_color="#b4eaff",
            height=40,
            text="下架商品",
            image=customtkinter.CTkImage(
                Image.open(os.path.join(image_path, "product_off_icon.png")),
                size=(15, 15),
            ),
            command=lambda: self.creat_csv(base_path, root_path, "trash"),
        )
        self.button_3.pack(side="left", expand=True, padx=10, pady=0)

        # Console

        textbox_console_frame = customtkinter.CTkFrame(
            self, bg_color="transparent", fg_color="transparent"
        )

        textbox_console_frame.pack(fill="x", padx=20, pady=0)

        self.textbox_CTkLabel = customtkinter.CTkLabel(
            textbox_console_frame,
            text="Console",
            fg_color="transparent",
            text_color="#a3a3a3",
            **style,
            anchor="center",
        )
        self.textbox_CTkLabel.pack(padx=(20, 0), pady=(10, 0))

        self.textbox_console = customtkinter.CTkTextbox(self, width=300, height=150)
        self.textbox_console.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.textbox_console.configure(
            **style,
            scrollbar_button_color="#ccf1ff",
            scrollbar_button_hover_color="#81dcff",
        )

    def parse_text(self):
        content = self.textbox.get("1.0", "end-1c")
        pattern = r"\b\d{4,}-\d+\b"

        uid_product_array = re.findall(pattern, content)

        unique_uid_product_array = list(dict.fromkeys(uid_product_array))

        self.textbox.delete("1.0", customtkinter.END)
        self.textbox.insert(
            customtkinter.END, "\n" + "\n".join(unique_uid_product_array)
        )
        return unique_uid_product_array

    def creat_csv(self, base_path, root_path, state_str):

        def pt(text):
            self.textbox_console.insert(customtkinter.END, "\n" + text)
            self.textbox_console.see(customtkinter.END)
            logging.info(text)

        def btn_state(val=None):
            if val == "lock":
                self.button_1.configure(state="disabled")
                self.button_2.configure(state="disabled")
                self.button_3.configure(state="disabled")
            else:
                self.button_1.configure(state="normal")
                self.button_2.configure(state="normal")
                self.button_3.configure(state="normal")

        def run_upload_process():
            btn_state("lock")
            config_path = os.path.join(root_path, "config.json")
            with open(config_path, "r") as f:
                config_data = json.load(f)

            self.textbox_console.delete("1.0", customtkinter.END)
            try:

                product_state_creat_csv.run_process(
                    base_path, pt, self.parse_text(), state_str
                )

                upload.run_process(
                    os.path.join(base_path, "sdc_data/state", "product_state.csv"),
                    pt,
                    config_data["product_state"],
                    # progress_callback=update_progress,
                )

                cron.run_process(base_path, pt, config_data["product_state"])

            except Exception as e:
                pt(f"{e}\n")
            btn_state()

        upload_thread = threading.Thread(target=run_upload_process)
        upload_thread.start()
