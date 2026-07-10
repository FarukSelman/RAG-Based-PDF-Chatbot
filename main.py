from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

print("Sistem başlatılıyor... Lütfen bekleyin.")
print("(İlk çalıştırmada beyin dokümanları işleneceği için biraz uzun sürebilir)\n")

# 1. PDF'i Yükle
pdf_yolu = "ornek_ders_notu.pdf"
loader = PyPDFLoader(pdf_yolu)
sayfalar = loader.load()
print(f"[✓] PDF yüklendi. Toplam {len(sayfalar)} sayfa bulundu.")

# 2. Metni Parçalara Bölme (Chunking)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200 
)
parcalar = text_splitter.split_documents(sayfalar)
print(f"[✓] PDF {len(parcalar)} adet parçaya bölündü.")

# 3. YEREL Vektör Veritabanını Oluşturma (ÜCRETSİZ)
# PDF parçalarını sayısal verilere çeviriyoruz (Embedding)
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vektor_db = Chroma.from_documents(parcalar, embeddings)
retriever = vektor_db.as_retriever(search_kwargs={"k": 3}) 
print("[✓] Vektör veritabanı oluşturuldu (Yerel/Ücretsiz).\n")

# 4. YEREL Yapay Zeka Modelini Hazırlama (ÜCRETSİZ)
# Bilgisayarında çalışan Llama 3 modelini çağırıyoruz
llm = OllamaLLM(model="llama3") 

sistem_talimati = """
Sana verilen bağlam bilgilerini kullanarak kullanıcının sorusunu yanıtla.
Eğer cevabı bağlam bilgileri içinde bulamazsan "Bu belgede bu sorunun cevabı yoktur." yaz.
Uydurma cevaplar üretme, sadece sana verilen metne güven.

KRİTİK KURAL: Çıktını KESİNLİKLE VE SADECE TÜRKÇE VER. 
İngilizce hiçbir kelime, cümle veya açıklama kullanma. Tamamen ana dilinde konuş.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", sistem_talimati + "\n\nBağlam Bilgisi:\n{context}"),
    ("human", "Soru: {question}")
])

# 5. Modern RAG Zincirini Kurma
def format_parcalar(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_zinciri = (
    {"context": retriever | format_parcalar, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print("=====================================")
print("Sistem Hazır! Çıkmak için 'q' yazın.")
print("=====================================\n")

# 6. Kullanıcıdan Soru Alma Döngüsü
while True:
    soru = input("Soru: ")
    
    if soru.lower() == 'q':
        print("Görüşürüz!")
        break
        
    print("\n🤖 CEVAP: ", end="", flush=True)
    
    # invoke yerine stream kullanıyoruz ki kelime kelime yazsın
    for kelime_parcalari in rag_zinciri.stream(soru):
        print(kelime_parcalari, end="", flush=True)
        
    print("\n\n" + "-" * 40 + "\n")