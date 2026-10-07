# Panda Converter

**Powered by Razn**

A modern multilingual file converter for Microsoft Office files.

---

## Project Structure

panda-converter/
  frontend/
    index.html
    config.js
    README.md
  backend/
    main.py
    requirements.txt
    Dockerfile
  render.yaml
  .gitignore
  README.md

---

## Quick Start

### Backend (local)

    cd backend
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000

### Frontend

Open frontend/index.html in a browser.

### Deploy (Render.com)

1. Push to GitHub
2. Create a Web Service on Render.com
3. Environment: Docker
4. Deploy

---

## Languages

- Kurdish (Sorani) - RTL
- English - LTR
- Arabic - RTL

---

## Supported Formats

- DOCX, DOC -> PDF, TXT, HTML, RTF, ODT
- XLSX, XLS -> PDF, CSV, HTML, ODS
- PPTX, PPT -> PDF, PPT, ODP
- VSDX, VSD -> PDF, SVG, VSD
- PUB -> PDF

---

## Themes

- 4 seasonal themes: Spring, Summer, Autumn, Winter
- Light / Dark mode

---

## Privacy

Files are converted on your own server.
No third-party APIs are used.

---

## YouTube

https://www.youtube.com/@pandatechkurd

---

## License

(c) 2026 Panda Converter. All rights reserved.