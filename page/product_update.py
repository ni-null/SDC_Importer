import customtkinter
from PIL import Image
import os
import threading
import json
from inc import product_update_combined
from inc import upload
from inc import cron

import logging

logger = logging.getLogger(__name__)


class ProductUpdate(customtkinter.CTkFrame):
    def __init__(self, parent, image_path, base_path, root_path):
        super().__init__(parent, corner_radius=0, fg_color="white")

        style = {"font": ("微軟正黑體", 14, "bold")}

        self.large_test_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "product_update.png")),
            size=(500, 100),
        )

        self.second_frame_large_image_label = customtkinter.CTkLabel(
            self, text="", image=self.large_test_image
        )
        self.second_frame_large_image_label.pack(padx=20, pady=10)

        image_path = os.path.join(root_path, "test_images")

        ### textbox_frame
        self.textbox_frame = customtkinter.CTkFrame(
            self, bg_color="transparent", fg_color="transparent"
        )

        self.textbox_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.textbox_frame_tool = customtkinter.CTkFrame(
            self.textbox_frame, bg_color="transparent", fg_color="transparent"
        )
        self.textbox_frame_tool.pack(fill="x", padx=20, pady=0)

        # textbox_frame_tool_sub1
        self.textbox_frame_tool_sub1 = customtkinter.CTkFrame(
            self.textbox_frame_tool, bg_color="transparent", fg_color="transparent"
        )
        self.textbox_frame_tool_sub1.pack(
            side="left", anchor="w", padx=20, pady=0, fill="both", expand=True
        )

        self.textbox_frame_tool_sub1_CTkLabel = customtkinter.CTkLabel(
            self.textbox_frame_tool_sub1,
            text="",
            fg_color="transparent",
            **style,
        )
        self.textbox_frame_tool_sub1_CTkLabel.pack(
            side="left", padx=(20, 0), pady=0, fill="both", expand=True
        )

        # textbox_frame_tool_sub1

        # textbox_frame_tool_sub2
        self.textbox_frame_tool_sub2 = customtkinter.CTkFrame(
            self.textbox_frame_tool, bg_color="transparent", fg_color="transparent"
        )
        self.textbox_frame_tool_sub2.pack(
            side="left", anchor="center", padx=20, pady=0, fill="both", expand=True
        )

        self.CTkLabel = customtkinter.CTkLabel(
            self.textbox_frame_tool_sub2,
            text="Console",
            text_color="#a3a3a3",
            fg_color="transparent",
            **style,
        )
        self.CTkLabel.pack(side="left", padx=(20, 0), pady=0, fill="both", expand=True)
        # textbox_frame_tool_sub2
        # textbox_frame_tool_sub3
        self.textbox_frame_tool_sub3 = customtkinter.CTkFrame(
            self.textbox_frame_tool, bg_color="transparent", fg_color="transparent"
        )
        self.textbox_frame_tool_sub3.pack(
            side="left", anchor="e", padx=0, pady=0, fill="both", expand=True
        )

        self.open_folder_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "folder.png")), size=(20, 20)
        )
        self.open_folder_image_button = customtkinter.CTkButton(
            self.textbox_frame_tool_sub3,
            width=10,
            fg_color="#fdf3a8",
            text_color="#796d13",
            hover_color="#fdf3a8",
            text="檔案位置",
            image=self.open_folder_image,
            command=lambda: os.startfile(os.path.join(base_path, "sdc_data/update")),
        )
        self.open_folder_image_button.pack(side="right", pady=5)
        self.open_folder_image_button.configure(**style)
        # textbox_frame_tool_sub3

        self.textbox = customtkinter.CTkTextbox(
            self.textbox_frame, width=300, height=300
        )
        self.textbox.pack(padx=20, pady=0, fill="both", expand=True)

        self.textbox.configure(
            **style,
            scrollbar_button_color="#ccf1ff",
            scrollbar_button_hover_color="#81dcff",
        )
        ### textbox_frame

        self.button_frame = customtkinter.CTkFrame(
            self, bg_color="transparent", fg_color="transparent"
        )

        self.button_frame.pack(fill="x", padx=20, pady=0, expand=True)

        self.button_1 = customtkinter.CTkButton(
            self.button_frame,
            text="文字更新",
            fg_color="#b4eaff",
            text_color="#56707a",
            hover_color="#b4eaff",
            image=customtkinter.CTkImage(
                Image.open(os.path.join(image_path, "product_update_text_icon.png")),
                size=(15, 15),
            ),
            command=lambda: self.on_button_click(base_path, root_path),
        )
        self.button_1.pack(side="left", padx=20, pady=20, fill="both", expand=True)
        self.button_1.configure(**style, height=40)

        self.button_2 = customtkinter.CTkButton(
            self.button_frame,
            text="文字/圖片更新",
            fg_color="#b4eaff",
            text_color="#56707a",
            hover_color="#b4eaff",
            image=customtkinter.CTkImage(
                Image.open(os.path.join(image_path, "product_update_img_icon.png")),
                size=(15, 15),
            ),
            command=lambda: self.on_button_click(base_path, root_path, {"img": True}),
        )
        self.button_2.pack(side="left", padx=20, pady=20, fill="both", expand=True)
        self.button_2.configure(**style, height=40)
        ### button_frame

        self.progress_bar = customtkinter.CTkProgressBar(
            self, width=200, fg_color="#b4eaff"
        )
        self.progress_bar.set(0)

    def on_button_click(self, base_path, root_path, product_config_obj=None):
        self.textbox.delete("1.0", customtkinter.END)

        def update_progress(progress):
            self.progress_bar.set(progress / 100)
            if progress < 100 and progress > 1:
                self.progress_bar.pack(
                    side="left", padx=20, pady=20, fill="both", expand=True
                )
            else:
                self.progress_bar.pack_forget()

        # 替換PT
        def pt(text):

            self.textbox.insert(customtkinter.END, "\n" + text)
            self.textbox.see(customtkinter.END)
            logging.info(text)

        def btn_state(val=None):
            if val == "lock":
                self.button_1.configure(state="disabled")
                self.button_2.configure(state="disabled")
            else:
                self.button_1.configure(state="normal")
                self.button_2.configure(state="normal")

        def run_upload_process():
            config_path = os.path.join(root_path, "config.json")
            with open(config_path, "r") as f:
                config_data = json.load(f)

            try:
                btn_state("lock")
                product_update_combined.run_process(
                    os.path.join(base_path, "sdc_data/update"), pt
                )

                update_type = (
                    "product_update_text_with_img"
                    if product_config_obj and product_config_obj.get("img")
                    else "product_update_text"
                )

                upload.run_process(
                    os.path.join(base_path, "sdc_data/update", "product_update.csv"),
                    pt,
                    config_data[update_type],
                    progress_callback=update_progress,
                )

                cron.run_process(base_path, pt, config_data[update_type])

                pt(f"\n\n-----------所有任務執行完畢-----------")
            except Exception as e:
                pt(f"{e}")
            btn_state()

        upload_thread = threading.Thread(target=run_upload_process)
        upload_thread.start()
