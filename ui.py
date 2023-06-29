import tkinter as tk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("下厨房菜谱图片下载")
        self.geometry("300x300")
        self.resizable(False, False)

        self.recipe_label = tk.Label(self, text="菜谱名称：")
        self.recipe_label.pack()

        self.recipe_name_var = tk.StringVar()
        self.recipe_name_entry = tk.Entry(
            self, textvariable=self.recipe_name_var)
        self.recipe_name_entry.pack()

        self.button = tk.Button(
            self, text="下载", command=self.download)
        self.button.pack()

    
    def download(self):
        print(self.recipe_name_var.get())


if __name__ == "__main__":
    window = Window()
    window.mainloop()       