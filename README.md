# NotebookLM Watermark Remover

A powerful tool that cleanly removes the "NotebookLM" watermark from your PDF slides and images (PNG, JPG) using advanced computer vision techniques.

## What It Does

**Smart Removal (Inpainting):**
Instead of just covering the watermark with a solid color box (which looks bad on gradients or textured backgrounds), this tool uses **AI-based Inpainting (Computer Vision)**.
- **Detects** the watermark by analyzing local contrast and blur differences.
- **Reconstructs** the background behind the text, preserving gradients, textures, and slide borders.
- **Smart Filtering:** Intelligently ignores slide content (text, lines) that might be close to the watermark area, ensuring only the logo/text is removed.

**Supported Formats:**
- **PDF Documents:** Patches the watermark on every page seamlessly.
- **Images:** Supports PNG (including transparency/alpha channel), JPG, JPEG, and WEBP.

**Features:**
- Batch processing: Clean entire folders in one go.
- Progress bar for tracking large tasks.
- Preview mode (PDFs) to test settings on the first page.
- Smart auto-detection of file types.

## Getting Started

1. **Set things up:**
```bash
python -m venv venv
source venv/bin/activate  # Windows folks: venv\Scripts\activate
```

2. **Grab the dependencies:**
```bash
pip install -r requirements.txt
```

## How to Use It

### Single file (PDF or Image)
```bash
python remover.py presentation.pdf
# OR
python remover.py slide.png
```
Creates `presentation_cleaned.pdf` or `slide_cleaned.png` in the same folder.

### Batch process a folder
```bash
python remover.py ./my_folder/
```
Automatically detects and cleans all supported files (`.pdf`, `.png`, `.jpg`, etc.) in the directory.

### Try before you commit (PDF only)
Check how it looks on just the first page:
```bash
python remover.py file.pdf --preview
```
### Build To EXE

```
pip install pyinstaller
pyinstaller --noconsole --onefile --name "PDF水印去除助手" gui_watermark_remover.py
```
## What's Inside

- `remover.py` - Core logic using PyMuPDF and OpenCV.
- `requirements.txt` - Dependencies: `pymupdf`, `tqdm`, `Pillow`, `opencv-python-headless`, `numpy`.
- `LICENSE` - MIT License

## Want to Help?

Pull requests are welcome. Found a bug? Open an issue.
