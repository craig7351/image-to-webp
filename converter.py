import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pathlib import Path
from PIL import Image
import threading
import webbrowser

# Import upload logic
from upload_logic import batch_upload

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class WebPConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("圖片轉 WebP 與上傳工具")
        self.geometry("800x650")

        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Main content (tabs)
        self.grid_rowconfigure(1, weight=0) # Log area

        # --- Tab View ---
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.tab_convert = self.tab_view.add("圖片轉檔")
        self.tab_upload = self.tab_view.add("圖片上傳")

        # --- Setup Tabs ---
        self.setup_convert_tab()
        self.setup_upload_tab()

        # --- Log Area (Shared) ---
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.log_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.log_frame, text="操作日誌 (Log):", anchor="w").grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
        self.log_text = ctk.CTkTextbox(self.log_frame, height=150, state='disabled')
        self.log_text.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")

    # ==========================
    # Tab 1: Converter Logic
    # ==========================
    def setup_convert_tab(self):
        # Variables
        self.input_dir = ctk.StringVar()
        self.output_dir = ctk.StringVar()
        self.quality = ctk.IntVar(value=80)
        self.lossless = ctk.BooleanVar(value=False)

        # Tab Layout
        self.tab_convert.grid_columnconfigure(0, weight=1)

        # Input
        frame_in = ctk.CTkFrame(self.tab_convert)
        frame_in.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        frame_in.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame_in, text="輸入資料夾:").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(frame_in, textvariable=self.input_dir, placeholder_text="選擇圖片來源路徑...").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(frame_in, text="瀏覽...", command=self.browse_input, width=80).grid(row=0, column=2, padx=10, pady=10)

        # Output
        frame_out = ctk.CTkFrame(self.tab_convert)
        frame_out.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        frame_out.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame_out, text="輸出資料夾:").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(frame_out, textvariable=self.output_dir, placeholder_text="選擇轉換與輸出路徑...").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(frame_out, text="瀏覽...", command=self.browse_output, width=80).grid(row=0, column=2, padx=10, pady=10)

        # Settings
        frame_set = ctk.CTkFrame(self.tab_convert)
        frame_set.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        frame_set.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame_set, text="品質 (Quality):").grid(row=0, column=0, padx=10, pady=10)
        
        slider_box = ctk.CTkFrame(frame_set, fg_color="transparent")
        slider_box.grid(row=0, column=1, sticky="ew", padx=10)
        slider_box.grid_columnconfigure(0, weight=1)
        
        self.quality_slider = ctk.CTkSlider(slider_box, from_=1, to=100, variable=self.quality, command=self.update_quality_label)
        self.quality_slider.grid(row=0, column=0, sticky="ew")
        self.quality_label = ctk.CTkLabel(slider_box, text=f"{self.quality.get()}", width=30)
        self.quality_label.grid(row=0, column=1, padx=(5, 0))

        ctk.CTkCheckBox(frame_set, text="無損壓縮 (Lossless)", variable=self.lossless).grid(row=0, column=2, padx=20, pady=10)

        # Button
        self.convert_btn = ctk.CTkButton(self.tab_convert, text="開始轉換 (Start Convert)", command=self.start_conversion_thread, height=40, font=("Arial", 16, "bold"))
        self.convert_btn.grid(row=3, column=0, padx=10, pady=20, sticky="ew")

    def update_quality_label(self, value):
        self.quality_label.configure(text=f"{int(value)}")

    def browse_input(self):
        d = filedialog.askdirectory()
        if d: self.input_dir.set(d)

    def browse_output(self):
        d = filedialog.askdirectory()
        if d: self.output_dir.set(d)

    def start_conversion_thread(self):
        i_path, o_path = self.input_dir.get(), self.output_dir.get()
        if not i_path or not o_path:
            messagebox.showerror("錯誤", "請選擇輸入和輸出資料夾！")
            return
        
        self.convert_btn.configure(state="disabled")
        threading.Thread(target=self.convert_images, args=(i_path, o_path, self.quality.get(), self.lossless.get()), daemon=True).start()

    def convert_images(self, input_dir_str, output_dir_str, quality, lossless):
        try:
            self.log_on_main("-" * 30)
            self.log_on_main(f"[轉換] 開始: {input_dir_str} -> {output_dir_str}")
            
            input_path = Path(input_dir_str)
            output_path = Path(output_dir_str)

            if not output_path.exists():
                output_path.mkdir(parents=True, exist_ok=True)
                self.log_on_main(f"[轉換] 建立資料夾: {output_path}")

            supported = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
            files = [f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() in supported]

            if not files:
                self.log_on_main("[轉換] 未找到可轉換檔案。")
                return

            success = 0
            total = len(files)
            for i, fpath in enumerate(files):
                try:
                    img = Image.open(fpath)
                    original_size = os.path.getsize(fpath)
                    outfile = output_path / (fpath.stem + ".webp")
                    img.save(outfile, "webp", quality=quality, lossless=lossless)
                    new_size = os.path.getsize(outfile)
                    
                    reduction = (1 - (new_size/original_size))*100 if original_size > 0 else 0
                    self.log_on_main(f"[轉換] [{i+1}/{total}] 成功: {fpath.name} ({original_size/1024:.1f}KB -> {new_size/1024:.1f}KB, -{reduction:.1f}%)")
                    success += 1
                except Exception as e:
                    self.log_on_main(f"[轉換] [{i+1}/{total}] 失敗: {fpath.name} - {e}")

            self.log_on_main(f"[轉換] 完成！成功率: {success}/{total}")
            messagebox.showinfo("完成", f"轉換完成！\n成功: {success}\n總共: {total}")

        except Exception as e:
            self.log_on_main(f"[轉換] 錯誤: {e}")
        finally:
            self.convert_btn.configure(state="normal")

    # ==========================
    # Tab 2: Upload Logic
    # ==========================
    def setup_upload_tab(self):
        self.upload_api_key = ctk.StringVar()
        self.upload_dir_path = ctk.StringVar()

        self.tab_upload.grid_columnconfigure(0, weight=1)

        # API Key
        frame_key = ctk.CTkFrame(self.tab_upload)
        frame_key.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        frame_key.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame_key, text="ImgBB API Key:").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(frame_key, textvariable=self.upload_api_key, placeholder_text="輸入您的 API Key", show="*").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        link_lbl = ctk.CTkLabel(frame_key, text="(申請 Key)", text_color="blue", cursor="hand2")
        link_lbl.grid(row=0, column=2, padx=10)
        link_lbl.bind("<Button-1>", lambda e: webbrowser.open("https://api.imgbb.com/"))

        # Folder Selection
        frame_dir = ctk.CTkFrame(self.tab_upload)
        frame_dir.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        frame_dir.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame_dir, text="上傳資料夾:").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkEntry(frame_dir, textvariable=self.upload_dir_path, placeholder_text="選擇包含圖片的目錄...").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(frame_dir, text="瀏覽...", command=self.browse_upload_dir, width=80).grid(row=0, column=2, padx=10, pady=10)

        # Info Label (Limit)
        ctk.CTkLabel(self.tab_upload, text="注意：每次批次上傳限制最多 20 張圖片", text_color="gray").grid(row=2, column=0, pady=(0, 10))

        # Button
        self.upload_btn = ctk.CTkButton(self.tab_upload, text="開始上傳 (Start Upload)", command=self.start_upload_thread, height=40, font=("Arial", 16, "bold"), fg_color="#E04F5F", hover_color="#C0392B") # Red-ish for caution/distinction
        self.upload_btn.grid(row=3, column=0, padx=10, pady=20, sticky="ew")

    def browse_upload_dir(self):
        d = filedialog.askdirectory()
        if d: self.upload_dir_path.set(d)

    def start_upload_thread(self):
        key = self.upload_api_key.get()
        path = self.upload_dir_path.get()
        
        if not key:
            messagebox.showerror("錯誤", "請輸入 API Key")
            return
        if not path or not os.path.exists(path):
            messagebox.showerror("錯誤", "請選擇有效的資料夾")
            return

        self.upload_btn.configure(state="disabled")
        threading.Thread(target=self.run_upload, args=(path, key), daemon=True).start()

    def run_upload(self, folder, key):
        try:
            self.log_on_main("-" * 30)
            self.log_on_main(f"[上傳] 開始上傳目錄: {folder}")
            
            # Using shared logic
            batch_upload(folder, key, log_callback=self.log_on_main)
            
            messagebox.showinfo("完成", "上傳作業結束，請查看 Log 或 output.json")
        except Exception as e:
            self.log_on_main(f"[上傳] 錯誤: {e}")
            messagebox.showerror("錯誤", str(e))
        finally:
            self.upload_btn.configure(state="normal")

    # ==========================
    # Shared Helper
    # ==========================
    def log_on_main(self, msg):
        # Ensure thread safety for UI updates
        # CTk doesn't strictly require .after for text insert like Tkinter sometimes does, 
        # but it's safer to use .after if called from thread. Or verify if CTK handles it.
        # CustomTkinter widgets are generally not thread-safe either.
        self.after(0, lambda: self._log_impl(msg))

    def _log_impl(self, msg):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, str(msg) + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')

if __name__ == "__main__":
    app = WebPConverterApp()
    app.mainloop()
