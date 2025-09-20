# Công cụ Phân tích Văn bản (FastAPI + spaCy + Tailwind)

Một web app nhỏ minh hoạ pipeline NLP cơ bản: **Tokenization → POS → NER**.

## 🎯 Tính năng
- Nhập đoạn văn bản và bấm **Phân tích**
- Bảng **Token / Lemma / POS / Tag (Penn Treebank)**
- **NER** hiển thị dạng nhãn (PERSON, ORG, GPE, …)
- **Sentences** tách câu
- Chú thích (legend) POS/Tag/Entity bằng tiếng Việt

## 🔧 Công nghệ
- Backend: **FastAPI**
- NLP: **spaCy** (`en_core_web_sm`)
- Template: **Jinja2**
- UI: **Tailwind CSS (CDN)**
- Server dev: **Uvicorn**

## 📂 Cấu trúc
```
.
├── main.py
├── templates/
│   └── index.html
├── requirements.txt
└── README.md
```

## ▶️ Hướng dẫn chạy
```bash
python -m venv env
# Windows: env\Scripts\activate
# macOS/Linux: source env/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm

uvicorn main:app --reload
# Mở http://127.0.0.1:8000
```

## 🔌 API Endpoints
- `GET /` — Trang giao diện
- `POST /api/analyze` — Phân tích văn bản
  ```json
  {
    "tokens": [{"t":"Apple","lemma":"Apple","pos":"PROPN","tag":"NNP"}],
    "entities": [{"text":"Ho Chi Minh City","label":"GPE"}],
    "sentences": ["Apple will open ...", "Tim Cook met ..."]
  }
  ```
- `GET /api/legend` — Chú thích nhãn (POS/Tag/NER)

## 🧠 Mapping theo đề bài
- **Token list** → bảng *Tokens & POS*
- **POS tag cho từng token** → cột POS/Tag kèm tooltip
- **NER** → chip nhãn ở mục *Thực thể đặt tên (NER)*

 