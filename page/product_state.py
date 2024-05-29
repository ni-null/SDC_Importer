import customtkinter
from PIL import Image
import os
import threading
import json
from inc import combined
from inc import upload
from inc import cron


class ProductState(customtkinter.CTkFrame):
    def __init__(self, parent, large_test_image, base_path, root_path):
        super().__init__(parent, corner_radius=0, fg_color="white")

        style = {"font": ("微軟正黑體", 14, "bold")}

        self.second_frame_large_image_label = customtkinter.CTkLabel(
            self, text="", image=large_test_image
        )
        self.second_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        image_path = os.path.join(root_path, "test_images")

        self.clear_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "eraser.png")), size=(20, 20)
        )
        self.clear_image_button_ = customtkinter.CTkButton(
            self,
            width=10,
            fg_color="transparent",
            hover_color="",
            text="",
            image=self.clear_image,
            command=lambda: self.textbox.delete("1.0", customtkinter.END),
        )
        self.clear_image_button_.grid(row=1, column=0, padx=(20, 0), pady=0, sticky="w")

        self.open_folder_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "folder.png")), size=(20, 20)
        )
        self.open_folder_image = customtkinter.CTkButton(
            self,
            width=10,
            fg_color="#fdf3a8",
            text_color="#796d13",
            hover_color="#fdf3a8",
            text="檔案位置",
            image=self.open_folder_image,
            command=lambda: os.startfile(os.path.join(base_path, "files")),
        )
        self.open_folder_image.grid(row=1, column=0, pady=5, padx=(0, 20), sticky="e")
        self.open_folder_image.configure(**style)

        self.frame = customtkinter.CTkFrame(self)
        self.frame.configure(fg_color="transparent")

        self.frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nEW")

        self.grid_columnconfigure(0, weight=1)

        # self.second_frame_large_image_label = customtkinter.CTkLabel(self, text="", image=large_test_image)
        # self.second_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.frame_2 = customtkinter.CTkFrame(self)

        self.frame_2.grid(row=3, column=0, padx=20, pady=10, sticky="nEW")
        self.frame_2.grid_columnconfigure(0, weight=1)
        self.frame_2.grid_columnconfigure(1, weight=1)
        self.frame_2.configure(fg_color="transparent")

        # 添加一个按钮
        self.button_1 = customtkinter.CTkButton(
            self.frame_2,
            text="批量上架",
            fg_color="#b4eaff",
            text_color="#56707a",
            hover_color="#b4eaff",
            command=lambda: self.on_button_click(base_path),
        )
        self.button_1.grid(row=3, column=0, padx=20, pady=20)
        self.button_1.configure(**style, height=40)
        self.button_2 = customtkinter.CTkButton(
            self.frame_2,
            text="批量下架",
            fg_color="#b4eaff",
            text_color="#56707a",
            hover_color="#b4eaff",
            command=lambda: self.on_button_click(base_path),
        )
        self.button_2.grid(row=3, column=1, padx=20, pady=20)
        self.button_2.configure(**style, height=40)

        self.progress_bar = customtkinter.CTkProgressBar(
            self.frame_2, width=200, fg_color="#b4eaff"
        )
        self.progress_bar.set(0)

        # 添加一个文本框
        self.textbox = customtkinter.CTkTextbox(self, width=300, height=300)
        self.textbox.grid(row=2, column=0, columnspan=2, padx=20, pady=0, sticky="EW")
        style = {"font": ("微軟正黑體", 14, "bold")}

        self.textbox.configure(
            **style,
            scrollbar_button_color="#ccf1ff",
            scrollbar_button_hover_color="#81dcff",
        )

        #  self.entry = customtkinter.CTkEntry(self.frame_2, placeholder_text="CTkEntry")

    #  self.entry.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="EW")
    #  self.entry.configure(**style, height=40, border_width=0, border_color="gray50")

    #  self.entry_button_2 = customtkinter.CTkButton(
    #      self.frame_2,
    #      text="手動下架",
    #      fg_color="#b4eaff",
    #      text_color="#56707a",
    #      hover_color="#b4eaff",
    #      command=lambda: self.on_button_click(base_path),
    #  )
    #  self.entry_button_2.grid(row=4, column=3, padx=20, pady=20, sticky="e")
    #  self.entry_button_2.configure(**style, height=40)

    def on_button_click(self, base_path):

        def update_progress(progress):
            self.progress_bar.set(progress / 100)
            if progress < 100 and progress > 1:
                self.progress_bar.grid(
                    row=4, column=0, columnspan=3, padx=20, pady=20, sticky="EW"
                )
            else:
                self.progress_bar.grid_forget()

        # 替換PT
        def pt(text):

            self.textbox.insert(customtkinter.END, "\n" + text)
            self.textbox.see(customtkinter.END)

        def btn_state(val=None):
            if val == "lock":
                self.button_1.configure(state="disabled")
                self.button_2.configure(state="disabled")
            else:
                self.button_1.configure(state="normal")
                self.button_2.configure(state="normal")

        def run_upload_process():
            config_path = os.path.join(base_path, "config.json")

            with open(config_path, "r") as f:
                config_data = json.load(f)

            try:
                btn_state("lock")
                combined.run_process(base_path, pt)
                upload.run_process(
                    base_path,
                    pt,
                    config_data["update"]["text"],
                    progress_callback=update_progress,
                )
                cron.run_process(base_path, pt, config_data["update"]["text"])
                pt(f"\n\n-----------所有任務執行完畢-----------")
            except Exception as e:
                print(f"\n")
                pt(f"{e}")
            btn_state()

        # Execute upload process asynchronously
        upload_thread = threading.Thread(target=run_upload_process)
        upload_thread.start()
