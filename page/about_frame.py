import customtkinter
from PIL import Image


class AboutFrame(customtkinter.CTkFrame):
    def __init__(self, parent, large_test_image):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.second_frame_large_image_label = customtkinter.CTkLabel(
            self, text="", image=large_test_image
        )
        self.second_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # 添加一个按钮
        self.button = customtkinter.CTkButton(
            self, text="Click Me", command=self.on_button_click
        )
        self.button.grid(row=2, column=0, padx=20, pady=10)

        # 添加一个文本框
        self.textbox = customtkinter.CTkTextbox(self, width=300, height=300)
        self.textbox.grid(row=1, column=0, padx=20, pady=10, sticky="EW")

    def on_button_click(self):
        message = "Button clicked!"
        self.textbox.insert(customtkinter.END, message + "\n")  # 插入新的内容
        self.textbox.see(customtkinter.END)  # 滚动到文本框底部
        print("Button clicked!")
