import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from pathlib import Path
from PIL import Image
import threading

class WebPConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("圖片轉 WebP 工具 (Image to WebP Converter)")
        self.root.geometry("600x450")

        # Variables
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()

        # UI Setup
        self.create_widgets()

    def create_widgets(self):
        # Input Directory
        input_frame = tk.LabelFrame(self.root, text="輸入資料夾 (Input Directory)", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Entry(input_frame, textvariable=self.input_dir).pack(side="left", fill="x", expand=True, padx=(0, 5))
        tk.Button(input_frame, text="瀏覽...", command=self.browse_input).pack(side="right")

        # Output Directory
        output_frame = tk.LabelFrame(self.root, text="輸出資料夾 (Output Directory)", padx=10, pady=10)
        output_frame.pack(fill="x", padx=10, pady=5)

        tk.Entry(output_frame, textvariable=self.output_dir).pack(side="left", fill="x", expand=True, padx=(0, 5))
        tk.Button(output_frame, text="瀏覽...", command=self.browse_output).pack(side="right")

        # Action Buttons
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack(fill="x", padx=10)
        
        tk.Button(btn_frame, text="開始轉換 (Start Convert)", command=self.start_conversion_thread, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(fill="x")

        # Log Area
        log_frame = tk.LabelFrame(self.root, text="轉換日誌 (Log)", padx=10, pady=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, state='disabled')
        self.log_text.pack(fill="both", expand=True)

    def browse_input(self):
        directory = filedialog.askdirectory()
        if directory:
            self.input_dir.set(directory)

    def browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def start_conversion_thread(self):
        input_path = self.input_dir.get()
        output_path = self.output_dir.get()

        if not input_path or not output_path:
            messagebox.showerror("錯誤", "請選擇輸入和輸出資料夾！")
            return

        # Disable button? No simple way here without ref propert, but okay for simple app
        threading.Thread(target=self.convert_images, args=(input_path, output_path), daemon=True).start()

    def convert_images(self, input_dir_str, output_dir_str):
        self.log("-" * 30)
        self.log(f"開始轉換: {input_dir_str} -> {output_dir_str}")
        
        input_path = Path(input_dir_str)
        output_path = Path(output_dir_str)

        if not output_path.exists():
            try:
                output_path.mkdir(parents=True, exist_ok=True)
                self.log(f"建立輸出資料夾: {output_path}")
            except Exception as e:
                self.log(f"無法建立輸出資料夾: {e}")
                return

        supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        files = [f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() in supported_extensions]

        if not files:
            self.log("未找到可轉換的圖片檔案。")
            return

        success_count = 0
        total_count = len(files)

        for i, file_path in enumerate(files):
            try:
                img = Image.open(file_path)
                
                original_size = os.path.getsize(file_path)
                
                output_file = output_path / (file_path.stem + ".webp")
                img.save(output_file, "webp")
                
                new_size = os.path.getsize(output_file)
                if original_size > 0:
                    reduction = (1 - (new_size / original_size)) * 100
                    self.log(f"[{i+1}/{total_count}] 轉換成功: {file_path.name} ({original_size/1024:.1f}KB -> {new_size/1024:.1f}KB, 減少 {reduction:.1f}%)")
                else:
                    self.log(f"[{i+1}/{total_count}] 轉換成功: {file_path.name} (大小未知)")
                
                success_count += 1
            except Exception as e:
                self.log(f"[{i+1}/{total_count}] 轉換失敗: {file_path.name} - {e}")

        self.log(f"轉換完成！成功: {success_count}/{total_count}")
        messagebox.showinfo("完成", f"轉換完成！\n成功: {success_count}\n總共: {total_count}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebPConverterApp(root)
    root.mainloop()
