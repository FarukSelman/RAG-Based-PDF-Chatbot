from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import StreamingResponse
import shutil
import os
from .rag_engine import rag_engine

app = FastAPI(title="RAG Ders Asistanı API")
# Tüm kaynaklardan (frontend'den) gelen isteklere izin ver
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Canlıya alınırken sadece site adresi yazılır ama şimdi * kalmalı
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PDF'lerin kaydedileceği klasör
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Kullanıcıdan PDF alır ve RAG sistemine yükler."""
    if not file.filename.endswith(".pdf"):
        return {"hata": "Lütfen sadece PDF dosyası yükleyin."}
    
    # Dosyayı kaydet
    dosya_yolu = os.path.join(UPLOAD_DIR, file.filename)
    with open(dosya_yolu, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # RAG motoruna işlet
    try:
        rag_engine.pdf_isle(dosya_yolu)
        return {"mesaj": f"{file.filename} başarıyla yüklendi ve sistem hazır."}
    except Exception as e:
        return {"hata": f"PDF işlenirken hata oluştu: {str(e)}"}

@app.post("/chat")
async def chat(soru: str = Form(...)):
    """Kullanıcıdan soru alır ve yapay zekadan stream cevap döner."""
    def cevap_uretici():
        for kelime in rag_engine.soru_sor_stream(soru):
            yield kelime
            
    return StreamingResponse(cevap_uretici(), media_type="text/plain")