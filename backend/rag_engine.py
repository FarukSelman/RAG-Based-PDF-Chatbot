from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class RAGEngine:
    def __init__(self):
        self.rag_zinciri = None

    def pdf_isle(self, pdf_yolu: str):
        """PDF'i okuyup vektör veritabanını oluşturur."""
        print(f"[BACKEND] İşleniyor: {pdf_yolu}")
        
        loader = PyPDFLoader(pdf_yolu)
        sayfalar = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        parcalar = text_splitter.split_documents(sayfalar)

        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vektor_db = Chroma.from_documents(parcalar, embeddings)
        retriever = vektor_db.as_retriever(search_kwargs={"k": 3})

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

        def format_parcalar(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.rag_zinciri = (
            {"context": retriever | format_parcalar, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        print("[BACKEND] PDF işlendi ve RAG zinciri hazır!")

    def soru_sor_stream(self, soru: str):
        """Soruya akıcı (stream) şekilde cevap verir."""
        if not self.rag_zinciri:
            yield "HATA: Lütfen önce bir PDF yükleyin."
            return

        for kelime_parcalari in self.rag_zinciri.stream(soru):
            yield kelime_parcalari

# Uygulama boyunca kullanılacak tekil bir örnek (Singleton)
rag_engine = RAGEngine()
