import { useState, useRef, useEffect } from 'react';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Yeni mesaj geldiğinde scroll'u en alta kaydır
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // PDF Yükleme Fonksiyonu
  const handleUpload = async () => {
    if (!file) return alert('Lütfen bir PDF dosyası seçin!');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/upload-pdf', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      
      if (data.mesaj) {
        setMessages(prev => [...prev, { role: 'system', content: data.mesaj }]);
        setFile(null);
      } else {
        alert('Hata: ' + data.hata);
      }
    } catch (err) {
      alert('Sunucuya bağlanılamadı. FastAPI çalışıyor mu?');
    }
  };

  // Soru Sorma Fonksiyonu
  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    const formData = new FormData();
    formData.append('soru', input);

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        body: formData
      });
      
      // Backend'den akıcı (stream) geldiği için text olarak topluyoruz
      const data = await res.text(); 
      setMessages(prev => [...prev, { role: 'ai', content: data }]);
    } catch (err) {
      alert('Soru sorulurken hata oluştu.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', fontFamily: 'Arial, sans-serif', backgroundColor: '#343541', color: 'white' }}>
      
      {/* Üst Bar ve PDF Yükleme */}
      <div style={{ padding: '15px', backgroundColor: '#202123', borderBottom: '1px solid #4d4d4f', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <h2 style={{ margin: 0, flexGrow: 1 }}>🎓 RAG Ders Asistanı</h2>
        <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} style={{ display: 'none' }} id="pdfInput" />
        <label htmlFor="pdfInput" style={{ cursor: 'pointer', padding: '8px 12px', backgroundColor: '#565869', borderRadius: '5px', fontSize: '14px' }}>
          {file ? file.name : 'PDF Seç'}
        </label>
        <button onClick={handleUpload} style={{ padding: '8px 12px', backgroundColor: '#10a37f', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold' }}>
          Yükle ve İşle
        </button>
      </div>

      {/* Sohbet Alanı */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '20px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {messages.length === 0 && (
          <div style={{ margin: 'auto', textAlign: 'center', color: '#8e8ea0' }}>
            <h3>Hoş Geldiniz!</h3>
            <p>Lütfen soldaki butondan bir ders notu PDF'i yükleyin.</p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} style={{ display: 'flex', justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start' }}>
            <div style={{ 
              maxWidth: '70%', 
              padding: '12px 18px', 
              borderRadius: '15px', 
              backgroundColor: msg.role === 'user' ? '#343541' : '#444654', 
              border: msg.role === 'system' ? '1px dashed #10a37f' : 'none',
              whiteSpace: 'pre-wrap' // Enter karakterlerini saymak için
            }}>
              {msg.content}
            </div>
          </div>
        ))}

        {isLoading && (
          <div style={{ color: '#8e8ea0' }}>Yapay Zeka düşünüyor...</div>
        )}
        <div ref={chatEndRef} />
      </div>

      // Alt Input Alanı
      <div style={{ padding: '15px', backgroundColor: '#343541', borderTop: '1px solid #4d4d4f', display: 'flex', gap: '10px' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Sorunuzu buraya yazın..."
          style={{ flex: 1, padding: '12px', borderRadius: '10px', border: '1px solid #565869', backgroundColor: '#40414f', color: 'white', fontSize: '16px' }}
        />
        <button 
          onClick={handleSend} 
          disabled={isLoading}
          style={{ padding: '0 20px', backgroundColor: '#10a37f', color: 'white', border: 'none', borderRadius: '10px', cursor: 'pointer', fontSize: '16px', fontWeight: 'bold' }}
        >
          Gönder
        </button>
      </div>
    </div>
  );
}

export default App;