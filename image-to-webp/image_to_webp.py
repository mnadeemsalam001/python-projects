import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from PIL import Image
import threading

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    _HEIC_SUPPORTED = True
except ImportError:
    _HEIC_SUPPORTED = False

SUPPORTED = {
    ".png", ".jpg", ".jpeg",
    ".bmp",
    ".tiff", ".tif",
    ".gif",
    ".ico",
    *([".heic", ".heif"] if _HEIC_SUPPORTED else []),
}


class ImageToWebpApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image to WebP Converter")
        self.resizable(False, False)
        self.configure(padx=20, pady=20)

        self.files: list[Path] = []
        self.output_dir: Path | None = None
        self._build_ui()

    # ------------------------------------------------------------------ UI --

    def _build_ui(self):
        # --- File selection ---
        file_frame = ttk.LabelFrame(self, text="Input Files", padding=10)
        file_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.file_listbox = tk.Listbox(file_frame, width=60, height=8,
                                       selectmode=tk.EXTENDED)
        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL,
                                  command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        self.file_listbox.grid(row=0, column=0, columnspan=3)
        scrollbar.grid(row=0, column=3, sticky="ns")

        ttk.Button(file_frame, text="Add Files",
                   command=self._add_files).grid(row=1, column=0, pady=(8, 0))
        ttk.Button(file_frame, text="Add Folder",
                   command=self._add_folder).grid(row=1, column=1, pady=(8, 0))
        ttk.Button(file_frame, text="Clear",
                   command=self._clear_files).grid(row=1, column=2, pady=(8, 0))

        # --- Output directory ---
        out_frame = ttk.LabelFrame(self, text="Output Directory", padding=10)
        out_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        self.out_var = tk.StringVar(value="Same folder as each input file")
        ttk.Entry(out_frame, textvariable=self.out_var,
                  width=48, state="readonly").grid(row=0, column=0, padx=(0, 8))
        ttk.Button(out_frame, text="Browse",
                   command=self._pick_output).grid(row=0, column=1)
        ttk.Button(out_frame, text="Reset",
                   command=self._reset_output).grid(row=0, column=2, padx=(4, 0))

        # --- Quality slider ---
        q_frame = ttk.LabelFrame(self, text="WebP Quality", padding=10)
        q_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        self.quality_var = tk.IntVar(value=85)
        slider = ttk.Scale(q_frame, from_=1, to=100, orient=tk.HORIZONTAL,
                           variable=self.quality_var, length=380,
                           command=lambda _: self._update_quality_label())
        slider.grid(row=0, column=0, columnspan=2)

        self.quality_label = ttk.Label(q_frame, text="85  (Recommended: 80–90)",
                                       width=30)
        self.quality_label.grid(row=0, column=2, padx=(8, 0))

        self.lossless_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(q_frame, text="Lossless (ignores quality slider)",
                        variable=self.lossless_var).grid(row=1, column=0,
                                                         columnspan=3,
                                                         sticky="w",
                                                         pady=(6, 0))

        # --- Progress ---
        prog_frame = ttk.LabelFrame(self, text="Progress", padding=10)
        prog_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        self.progress_bar = ttk.Progressbar(prog_frame, length=480,
                                            mode="determinate")
        self.progress_bar.grid(row=0, column=0)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(prog_frame, textvariable=self.status_var).grid(
            row=1, column=0, sticky="w", pady=(4, 0))

        # --- Convert button ---
        self.convert_btn = ttk.Button(self, text="Convert to WebP",
                                      command=self._start_conversion)
        self.convert_btn.grid(row=4, column=0, ipady=6)

    # ----------------------------------------------------------- callbacks --

    def _add_files(self):
        heic_entry = ("HEIC / HEIF", "*.heic *.heif") if _HEIC_SUPPORTED else ()
        filetypes = [
            ("All supported images",
             "*.png *.jpg *.jpeg *.bmp *.tiff *.tif *.gif *.ico"
             + (" *.heic *.heif" if _HEIC_SUPPORTED else "")),
            ("PNG", "*.png"),
            ("JPEG", "*.jpg *.jpeg"),
            ("BMP", "*.bmp"),
            ("TIFF", "*.tiff *.tif"),
            ("GIF", "*.gif"),
            ("ICO", "*.ico"),
            *([heic_entry] if heic_entry else []),
        ]
        paths = filedialog.askopenfilenames(title="Select images",
                                            filetypes=filetypes)
        self._add_paths(paths)

    def _add_folder(self):
        folder = filedialog.askdirectory(title="Select folder")
        if not folder:
            return
        paths = [p for p in Path(folder).iterdir()
                 if p.suffix.lower() in SUPPORTED]
        if not paths:
            messagebox.showinfo("No images",
                                "No supported image files found in that folder.")
            return
        self._add_paths([str(p) for p in paths])

    def _add_paths(self, paths):
        existing = {str(p) for p in self.files}
        for p in paths:
            path = Path(p)
            if str(path) not in existing and path.suffix.lower() in SUPPORTED:
                self.files.append(path)
                self.file_listbox.insert(tk.END, path.name)

    def _clear_files(self):
        self.files.clear()
        self.file_listbox.delete(0, tk.END)

    def _pick_output(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_dir = Path(folder)
            self.out_var.set(str(self.output_dir))

    def _reset_output(self):
        self.output_dir = None
        self.out_var.set("Same folder as each input file")

    def _update_quality_label(self):
        q = self.quality_var.get()
        hint = "(Low)" if q < 50 else "(Recommended: 80–90)" if q < 91 else "(Max)"
        self.quality_label.config(text=f"{q}  {hint}")

    # ---------------------------------------------------------- conversion --

    def _start_conversion(self):
        if not self.files:
            messagebox.showwarning("No files", "Please add at least one image.")
            return
        self.convert_btn.config(state=tk.DISABLED)
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = len(self.files)
        thread = threading.Thread(target=self._convert_all, daemon=True)
        thread.start()

    def _convert_all(self):
        quality = self.quality_var.get()
        lossless = self.lossless_var.get()
        errors = []

        for i, src in enumerate(self.files):
            dest_dir = self.output_dir if self.output_dir else src.parent
            dest = dest_dir / (src.stem + ".webp")
            self.status_var.set(f"Converting: {src.name}")
            try:
                with Image.open(src) as img:
                    if img.mode in ("RGBA", "LA") or \
                       (img.mode == "P" and "transparency" in img.info):
                        img = img.convert("RGBA")
                    else:
                        img = img.convert("RGB")
                    img.save(dest, "WEBP",
                             quality=quality,
                             lossless=lossless,
                             method=6)
            except Exception as e:
                errors.append(f"{src.name}: {e}")

            self.progress_bar["value"] = i + 1
            self.update_idletasks()

        self._finish(errors)

    def _finish(self, errors: list[str]):
        self.convert_btn.config(state=tk.NORMAL)
        total = len(self.files)
        ok = total - len(errors)

        if errors:
            self.status_var.set(f"Done with errors — {ok}/{total} converted")
            messagebox.showerror(
                "Some files failed",
                "The following files could not be converted:\n\n" +
                "\n".join(errors))
        else:
            self.status_var.set(f"Done — {ok} file(s) converted successfully")
            messagebox.showinfo("Success",
                                f"All {ok} file(s) converted to WebP.")


if __name__ == "__main__":
    app = ImageToWebpApp()
    app.mainloop()
