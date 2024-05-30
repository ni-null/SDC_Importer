import tkinter
import tkinter.messagebox
import customtkinter
import customtkinter
import re
from PIL import Image
import os
import threading
import json
from inc import creat_product_state_csv


class ProductState(customtkinter.CTkFrame):
    def __init__(self, parent, large_test_image, base_path, root_path):
        super().__init__(parent, corner_radius=0, fg_color="white")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        style = {"font": ("微軟正黑體", 14, "bold")}

        self.second_frame_large_image_label = customtkinter.CTkLabel(
            self, text="", image=large_test_image
        )
        self.second_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.tabview.add("資料輸入")
        self.tabview.add("Console")
        self.tabview.tab("資料輸入").grid_columnconfigure(0, weight=1)
        self.tabview.tab("資料輸入").grid_columnconfigure(1, weight=1)
        self.tabview.tab("資料輸入").grid_columnconfigure(2, weight=1)
        self.tabview.tab("Console").grid_columnconfigure(0, weight=1)

        self.tabview.configure(
            fg_color="transparent", segmented_button_fg_color="#ffffff"
        )
        # 資料輸入
        self.textbox = customtkinter.CTkTextbox(
            self.tabview.tab("資料輸入"), width=300, height=300
        )
        self.textbox.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="EW")

        self.button_1 = customtkinter.CTkButton(
            self.tabview.tab("資料輸入"), text="資料解析", command=self.parse_text
        )
        self.button_1.grid(row=2, column=0, padx=20, pady=10, sticky="EW")

        self.button_2 = customtkinter.CTkButton(
            self.tabview.tab("資料輸入"),
            text="上架商品",
            command=lambda: self.start_it(base_path),
        )
        self.button_2.grid(row=2, column=1, padx=20, pady=10, sticky="EW")

        self.button_3 = customtkinter.CTkButton(
            self.tabview.tab("資料輸入"),
            text="下架商品",
            command=lambda: self.start_it(base_path),
        )
        self.button_3.grid(row=2, column=2, padx=20, pady=10, sticky="EW")

        # 資料輸入

        # Console

        self.textbox_console = customtkinter.CTkTextbox(
            self.tabview.tab("Console"), width=300, height=300
        )
        self.textbox_console.grid(
            row=1, column=0, columnspan=3, padx=20, pady=10, sticky="EW"
        )

        # Console

    def parse_text(self):
        content = self.textbox.get("1.0", "end-1c")
        pattern = r"\b\d{4,}-\d+\b"

        uid_product_array = re.findall(pattern, content)

        self.textbox.delete("1.0", customtkinter.END)
        self.textbox.insert(customtkinter.END, "\n" + "\n".join(uid_product_array))
        return uid_product_array

    def start_it(self, base_path):
        print("start_it")

        def pt(text):
            self.textbox_console.insert(customtkinter.END, "\n" + text)
            self.textbox_console.see(customtkinter.END)

        def run_upload_process():
            config_path = os.path.join(base_path, "config.json")

            with open(config_path, "r") as f:
                config_data = json.load(f)

            try:

                creat_product_state_csv.run_process(base_path, pt, self.parse_text())

            except Exception as e:
                print(f"\n")
                pt(f"{e}")

        upload_thread = threading.Thread(target=run_upload_process)
        upload_thread.start()
