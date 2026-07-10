# 🤖 RAG-Based PDF Chatbot Assistant

Bu proje, kullanıcıların yüklediği PDF dokümanlarını analiz ederek içerikleri hakkında doğal dilde sorular sorabilmelerini sağlayan **Retrieval-Augmented Generation (RAG)** tabanlı bir yapay zekâ asistanıdır. Sistem, vektör tabanlı benzerlik araması sayesinde yalnızca yüklenen dokümandaki ilgili içerikleri kullanarak bağlam farkındalığı yüksek yanıtlar üretir ve büyük dil modellerinin (LLM) halüsinasyon üretme olasılığını azaltmayı hedefler.

---

# 🖥️ Uygulama Arayüzü

> Proje ekran görüntüsünü aşağıdaki dosya adıyla ekleyebilirsiniz.

```text
assets/
└── application_screenshot.png
```

Markdown kullanımı:

```markdown
<p align="center">
  <img src="assets/application_screenshot.png" width="90%" alt="Application Screenshot">
</p>
```

---

# 🏗️ RAG Pipeline

Uygulama, klasik Retrieval-Augmented Generation mimarisini temel alan aşağıdaki veri akışını kullanmaktadır.

## 1. PDF Yükleme

Kullanıcı arayüz üzerinden PDF dosyasını sisteme yükler.

---

## 2. Metin Ayrıştırma

PDF içerisindeki metinler ayrıştırılır ve işlenebilir hale getirilir.

---

## 3. Text Chunking

Uzun metinler anlamsal bütünlüğü koruyacak şekilde küçük parçalara (chunks) ayrılır.

---

## 4. Embedding Oluşturma

Her metin parçası embedding modeli kullanılarak yüksek boyutlu vektörlere dönüştürülür.

---

## 5. Vector Database

Oluşturulan embedding'ler vektör veritabanına kaydedilir.

Desteklenebilecek veritabanları:

- ChromaDB
- FAISS
- Pinecone

---

## 6. Similarity Search

Kullanıcının sorusu da embedding'e dönüştürülür ve vektör veritabanında benzerlik araması gerçekleştirilir.

---

## 7. Response Generation

Bulunan en alakalı içerikler büyük dil modeline (LLM) gönderilir ve yalnızca ilgili bağlam kullanılarak cevap oluşturulur.

---

# 🛠️ Kullanılan Teknolojiler

## Backend

- Python 3.x
- FastAPI
- LangChain
- LlamaIndex

## Vector Database

- ChromaDB
- FAISS
- Pinecone

## Large Language Models

- OpenAI GPT
- Hugging Face Models
- Ollama

## Frontend

- React
- Vite
- HTML5
- CSS3
- JavaScript

## API

- REST API
- Fetch API
- Axios

---

# 🏗️ Proje Yapısı

```text
RAG-PDF-Chatbot/
│
├── backend/
│   ├── main.py
│   └── ...
│
├── frontend/
│   ├── src/
│   └── ...
│
├── assets/
│   └── application_screenshot.png
│
└── README.md
```

---

# 🔧 Kurulum

## 1. Repoyu Klonlayın

```bash
git clone https://github.com/FarukSelman/RAG-PDF-Chatbot.git
```

## 2. Proje Klasörüne Girin

```bash
cd RAG-PDF-Chatbot
```

---

# 🐍 Backend Kurulumu

## Sanal Ortamı Aktifleştirin

### Windows

```bash
.\venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Gerekli Kütüphaneleri Kurun

```bash
pip install fastapi uvicorn langchain chromadb faiss-cpu pypdf openai
```

## Backend'i Başlatın

```bash
uvicorn backend.main:app --reload
```

---

# ⚛️ Frontend Kurulumu

Frontend klasörüne geçin.

```bash
cd frontend
```

Bağımlılıkları yükleyin.

```bash
npm install
```

Uygulamayı başlatın.

```bash
npm run dev
```

---

# 📈 Uygulama Akışı

1. Kullanıcı PDF yükler.
2. PDF metni ayrıştırılır.
3. Metin küçük parçalara bölünür.
4. Embedding'ler oluşturulur.
5. Embedding'ler vektör veritabanına kaydedilir.
6. Kullanıcının sorusu embedding'e dönüştürülür.
7. Similarity Search yapılır.
8. En ilgili içerikler LLM'e gönderilir.
9. Yapay zekâ bağlama uygun cevabı üretir.

---

# 💡 Projenin Amacı

Bu çalışma;

- Retrieval-Augmented Generation (RAG) mimarisini uygulamak,
- PDF tabanlı soru-cevap sistemleri geliştirmek,
- Büyük dil modellerini özel dokümanlarla entegre etmek,
- Vektör veritabanlarının kullanımını öğrenmek,
- Embedding ve Similarity Search süreçlerini deneyimlemek,
- FastAPI ve React kullanarak uçtan uca yapay zekâ uygulamaları geliştirmek

amacıyla hazırlanmıştır.

---

# 👨‍💻 Geliştirici

**Faruk Selman**

GitHub: https://github.com/FarukSelman
