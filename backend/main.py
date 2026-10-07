from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import subprocess
import tempfile
import os
import shutil
import uuid

app = FastAPI(title="Panda Converter API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_SIZE = 100 * 1024 * 1024

ALLOWED_EXTS = {
    "docx", "doc", "xlsx", "xls", "pptx", "ppt",
    "accdb", "mdb", "one", "pub", "vsdx", "vsd", "mpp", "pst"
}

CONVERSION_MAP = {
    "docx": {"pdf": "writer_pdf_Export", "txt": "Text", "html": "HTML (StarWriter)", "rtf": "Rich Text Format", "odt": "writer8"},
    "doc":  {"pdf": "writer_pdf_Export", "docx": "MS Word 2007 XML", "txt": "Text", "html": "HTML (StarWriter)", "odt": "writer8"},
    "xlsx": {"pdf": "calc_pdf_Export", "csv": "Text - txt - csv (StarCalc)", "html": "HTML (StarCalc)", "xls": "MS Excel 97", "ods": "calc8"},
    "xls":  {"pdf": "calc_pdf_Export", "csv": "Text - txt - csv (StarCalc)", "html": "HTML (StarCalc)", "xlsx": "Calc MS Excel 2007 XML", "ods": "calc8"},
    "pptx": {"pdf": "impress_pdf_Export", "ppt": "MS PowerPoint 97", "odp": "impress8"},
    "ppt":  {"pdf": "impress_pdf_Export", "pptx": "Impress MS PowerPoint 2007 XML", "odp": "impress8"},
    "vsdx": {"pdf": "draw_pdf_Export", "svg": "SVG - Scalable Vector Graphics", "vsd": "Visio 2000/2002/2003 XML"},
    "vsd":  {"pdf": "draw_pdf_Export", "svg": "SVG - Scalable Vector Graphics", "vsdx": "Visio 2013 XML"},
    "pub":  {"pdf": "writer_pdf_Export"},
}

def validate_file(file):
    if not file.filename:
        raise HTTPException(400, "Filename required")
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTS:
        raise HTTPException(400, "Unsupported format: " + ext)
    return ext

@app.post("/api/convert")
async def convert(file: UploadFile = File(...), target: str = Form(...)):
    source_ext = validate_file(file)
    target = target.lower().strip()
    if source_ext not in CONVERSION_MAP:
        raise HTTPException(400, "Conversion not supported")
    if target not in CONVERSION_MAP[source_ext]:
        raise HTTPException(400, "Conversion not supported")
    workdir = tempfile.mkdtemp(prefix="panda_")
    try:
        input_path = os.path.join(workdir, "input." + source_ext)
        contents = await file.read()
        if len(contents) > MAX_SIZE:
            raise HTTPException(413, "File too large")
        with open(input_path, "wb") as f:
            f.write(contents)
        output_dir = os.path.join(workdir, "out")
        os.makedirs(output_dir, exist_ok=True)
        filter_name = CONVERSION_MAP[source_ext][target]
        cmd = ["libreoffice", "--headless", "--norestore",
               "--convert-to", target + ":" + filter_name,
               "--outdir", output_dir, input_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            raise HTTPException(500, "LibreOffice error")
        output_files = os.listdir(output_dir)
        if not output_files:
            raise HTTPException(500, "No output file")
        output_path = os.path.join(output_dir, output_files[0])
        output_name = "panda-converted." + target
        final_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()) + "." + target)
        shutil.copy(output_path, final_path)
        return FileResponse(final_path, media_type="application/octet-stream", filename=output_name)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

@app.get("/api/formats")
def formats():
    return {"source": list(CONVERSION_MAP.keys()),
            "conversions": {s: list(t.keys()) for s, t in CONVERSION_MAP.items()}}

@app.get("/")
def root():
    return {"name": "Panda Converter API", "version": "1.0.0", "powered_by": "Razn"}
