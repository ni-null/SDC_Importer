import tkinter
import tkinter.messagebox
import customtkinter
import customtkinter
import re
from PIL import Image
import os
import threading
import json
from inc import product_state_creat_csv


class ProductState(customtkinter.CTkFrame):
    def __init__(self, parent, large_test_image, base_path, root_path):
        super().__init__(parent, corner_radius=0, fg_color="white")

        style = {"font": ("微軟正黑體", 14, "bold")}

        self.second_frame_large_image_label = customtkinter.CTkLabel(
            self, text="", image=large_test_image
        )
        self.second_frame_large_image_label.pack(
            fill="both", expand=True, padx=20, pady=10
        )

        # 資料輸入
        self.textbox_CTkLabel = customtkinter.CTkLabel(
            self, text="資料輸入", fg_color="transparent", text_color="#56707a", **style
        )
        self.textbox_CTkLabel.pack(padx=(20, 0), pady=(40, 0))

        self.textbox = customtkinter.CTkTextbox(self, height=150)
        self.textbox.pack(fill="both", expand=True, padx=20, pady=(0, 10))

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
            command=lambda: self.creat_csv(base_path, "publish"),
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
            command=lambda: self.creat_csv(base_path, "trash"),
        )
        self.button_3.pack(side="left", expand=True, padx=10, pady=0)

        # Console

        textbox_console_frame = customtkinter.CTkFrame(
            self, bg_color="transparent", fg_color="transparent"
        )

        textbox_console_frame.pack(fill="x", padx=20, pady=0)

        image_path = os.path.join(root_path, "test_images")

        self.clear_textbox_console_button = customtkinter.CTkButton(
            textbox_console_frame,
            width=10,
            fg_color="transparent",
            hover_color="",
            text="",
            image=customtkinter.CTkImage(
                Image.open(os.path.join(image_path, "eraser.png")), size=(20, 20)
            ),
            command=lambda: self.textbox_console.delete("1.0", customtkinter.END),
        )
        self.clear_textbox_console_button.pack(
            side="left", expand=True, padx=0, pady=(40, 0), anchor="w"
        )

        self.textbox_console_label = customtkinter.CTkLabel(
            textbox_console_frame,
            text="Console     ",
            fg_color="transparent",
            text_color="#ccc",
            **style,
            anchor="center",
        )
        self.textbox_console_label.pack(side="left", expand=True, pady=(40, 0))
        self.textbox_console_label2 = customtkinter.CTkLabel(
            textbox_console_frame,
            text="",
            fg_color="transparent",
            **style,
            anchor="center",
        ).pack(side="left", expand=True, padx=0, pady=(40, 0))

        self.textbox_console = customtkinter.CTkTextbox(self, width=300, height=150)
        self.textbox_console.pack(fill="both", expand=True, padx=20, pady=(0, 10))

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

    def creat_csv(self, base_path, state_str):

        def pt(text):
            self.textbox_console.insert(customtkinter.END, "\n" + text)
            self.textbox_console.see(customtkinter.END)

        def run_upload_process():
            config_path = os.path.join(base_path, "config.json")

            with open(config_path, "r") as f:
                config_data = json.load(f)

            try:

                product_state_creat_csv.run_process(
                    base_path, pt, self.parse_text(), state_str
                )

            except Exception as e:
                pt(f"{e}\n")

        upload_thread = threading.Thread(target=run_upload_process)
        upload_thread.start()
