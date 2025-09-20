from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import spacy

app = FastAPI()
templates = Jinja2Templates(directory="templates")

nlp = spacy.load("en_core_web_sm")

# Chú thích chuẩn hóa (UPOS, Penn Treebank, spaCy NER)
POS_DESC = {
    "PROPN":"Danh từ riêng","NOUN":"Danh từ","VERB":"Động từ","AUX":"Trợ động từ",
    "ADJ":"Tính từ","ADV":"Trạng từ","ADP":"Giới từ","DET":"Từ hạn định",
    "PRON":"Đại từ","NUM":"Số từ","CCONJ":"Liên từ đẳng lập","SCONJ":"Liên từ phụ thuộc",
    "PART":"Tiểu từ","PUNCT":"Dấu câu","SYM":"Ký hiệu","X":"Khác"
}
TAG_DESC = {
    "NNP":"Danh từ riêng số ít","NNPS":"Danh từ riêng số nhiều","NN":"Danh từ số ít","NNS":"Danh từ số nhiều",
    "VB":"Động từ nguyên mẫu","VBD":"Động từ quá khứ","VBG":"Động từ V-ing","VBN":"Quá khứ phân từ",
    "VBP":"Hiện tại (không ngôi 3)","VBZ":"Hiện tại (ngôi 3)","MD":"Trợ động chỉ khả năng",
    "JJ":"Tính từ","JJR":"So sánh hơn","JJS":"So sánh nhất",
    "RB":"Trạng từ","RBR":"Trạng từ so sánh hơn","RBS":"Trạng từ so sánh nhất",
    "IN":"Giới từ / liên từ phụ thuộc","DT":"Từ hạn định","CC":"Liên từ đẳng lập",
    "CD":"Số đếm","PRP":"Đại từ nhân xưng","PRP$":"Đại từ sở hữu",
    "TO":"to (nguyên mẫu)","EX":"there tồn tại","UH":"Thán từ","FW":"Từ mượn",
    "LS":"Ký hiệu liệt kê","SYM":"Ký hiệu",".":"Dấu chấm",",":"Dấu phẩy",":":"Dấu hai chấm"
}
ENT_DESC = {
    "PERSON":"Người","ORG":"Tổ chức","GPE":"Địa danh hành chính","LOC":"Địa điểm",
    "DATE":"Ngày/Thời gian","TIME":"Thời điểm","NORP":"Quốc tịch/nhóm người","MONEY":"Tiền tệ",
    "PERCENT":"Phần trăm","PRODUCT":"Sản phẩm","EVENT":"Sự kiện","WORK_OF_ART":"Tác phẩm",
    "LANGUAGE":"Ngôn ngữ","LAW":"Văn bản luật","FAC":"Công trình","QUANTITY":"Đại lượng",
    "ORDINAL":"Thứ tự","CARDINAL":"Số đếm"
}

class AnalyzeIn(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/analyze", response_class=JSONResponse)
async def analyze(payload: AnalyzeIn):
    doc = nlp(payload.text or "")
    tokens = [{"t": t.text, "lemma": t.lemma_, "pos": t.pos_, "tag": t.tag_} for t in doc]
    ents = [{"text": e.text, "label": e.label_} for e in doc.ents]
    sents = [s.text for s in doc.sents]
    return {"tokens": tokens, "entities": ents, "sentences": sents}

@app.get("/api/legend", response_class=JSONResponse)
async def legend():
    return {"pos": POS_DESC, "tag": TAG_DESC, "ent": ENT_DESC}
