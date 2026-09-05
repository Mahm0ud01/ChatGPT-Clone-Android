# 🤖 ChatGPT Clone Backend

تطبيق Backend متكامل بـ Python و FastAPI للتواصل مع Ollama

## 📋 المتطلبات

```bash
python --version  # Python 3.9+
ollama --version  # Ollama
```

## ⚙️ التثبيت والإعداد

### 1️⃣ تثبيت المكتبات

```bash
# الدخول إلى مجلد Backend
cd backend

# تثبيت المكتبات من requirements.txt
pip install -r requirements.txt
```

### 2️⃣ تثبيت Ollama

قم بتحميل Ollama من: https://ollama.ai

بعد التثبيت، قم بتحميل نموذج:

```bash
# تحميل نموذج llama2 (الافتراضي)
ollama pull llama2

# أو نماذج أخرى:
ollama pull mistral
ollama pull neural-chat
ollama pull dolphin-mixtral
```

### 3️⃣ تشغيل Ollama

افتح Terminal جديد:

```bash
ollama serve
```

ستظهر رسالة:
```
LLM server started on 127.0.0.1:11434
```

### 4️⃣ تشغيل Backend

```bash
# في المجلد backend/
python app.py
```

ستظهر رسالة:
```
Uvicorn running on http://0.0.0.0:8000
```

## 🌐 اختبار API

### استخدام Swagger UI (الواجهة التفاعلية)

```
http://localhost:8000/docs
```

أو ReDoc:

```
http://localhost:8000/redoc
```

### باستخدام curl

```bash
# 1. التحقق من صحة الخادم
curl http://localhost:8000/health

# 2. الحصول على قائمة النماذج
curl http://localhost:8000/ollama/models

# 3. إنشاء محادثة جديدة
curl -X POST http://localhost:8000/conversations \
  -H "Content-Type: application/json" \
  -d '{"title": "محادثتي الأولى"}'

# 4. إرسال رسالة
curl -X POST http://localhost:8000/conversations/1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "content": "مرحبا، كيف حالك؟",
    "conversation_id": 1,
    "model": "llama2"
  }'
```

### باستخدام Python

```python
import requests

# 1. إنشاء محادثة
response = requests.post(
    "http://localhost:8000/conversations",
    json={"title": "محادثتي"}
)
conversation_id = response.json()["id"]

# 2. إرسال رسالة
response = requests.post(
    f"http://localhost:8000/conversations/{conversation_id}/messages",
    json={
        "content": "أخبرني عن التعلم الآلي",
        "conversation_id": conversation_id
    }
)

print(response.json()["content"])
```

## 📚 API Endpoints

### Health Check

```
GET /health
```

**الرد:**
```json
{
  "status": "✅ السيرفر يعمل",
  "ollama_connected": true,
  "ollama_url": "http://localhost:11434",
  "database": "✅ قاعدة البيانات متصلة"
}
```

### المحادثات (Conversations)

#### إنشاء محادثة جديدة
```
POST /conversations
```

**البيانات:**
```json
{
  "title": "عنوان المحادثة"
}
```

#### الحصول على جميع المحادثات
```
GET /conversations?skip=0&limit=10
```

#### الحصول على محادثة معينة
```
GET /conversations/{conversation_id}
```

#### حذف محادثة
```
DELETE /conversations/{conversation_id}
```

### الرسائل (Messages)

#### إرسال رسالة والحصول على رد
```
POST /conversations/{conversation_id}/messages
```

**البيانات:**
```json
{
  "content": "السؤال أو الطلب",
  "conversation_id": 1,
  "model": "llama2"  // اختياري
}
```

#### الحصول على رسائل المحادثة
```
GET /conversations/{conversation_id}/messages?skip=0&limit=50
```

### Ollama

#### الحصول على قائمة النماذج
```
GET /ollama/models
```

**الرد:**
```json
{
  "models": ["llama2", "mistral", "neural-chat"],
  "count": 3
}
```

## 🔧 الإعدادات

تعديل الإعدادات من ملف `.env`:

```env
# عنوان Ollama
OLLAMA_URL=http://localhost:11434

# اسم النموذج الافتراضي
OLLAMA_MODEL=llama2

# رابط قاعدة البيانات
DATABASE_URL=sqlite:///./chat_history.db

# وضع التطوير
DEBUG=True
```

## 🗄️ قاعدة البيانات

### جداول قاعدة البيانات

**جدول Conversations:**
```sql
CREATE TABLE conversations (
  id INTEGER PRIMARY KEY,
  title VARCHAR NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  is_archived BOOLEAN DEFAULT FALSE
);
```

**جدول Messages:**
```sql
CREATE TABLE messages (
  id INTEGER PRIMARY KEY,
  conversation_id INTEGER NOT NULL,
  content TEXT NOT NULL,
  role VARCHAR NOT NULL,  -- 'user' أو 'assistant'
  model_used VARCHAR,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  is_edited BOOLEAN DEFAULT FALSE
);
```

### عرض البيانات

```bash
# تثبيت sqlite3 CLI
sqlite3 chat_history.db

# عرض جميع المحادثات
SELECT * FROM conversations;

# عرض جميع الرسائل
SELECT * FROM messages;
```

## 🐛 استكشاف الأخطاء

### خطأ: "Cannot connect to Ollama"

✅ **الحل:**
- تأكد من تشغيل Ollama: `ollama serve`
- تحقق من العنوان: `http://localhost:11434`

### خطأ: "Model not found"

✅ **الحل:**
```bash
# قائمة النماذج المثبتة
ollama list

# تحميل نموذج جديد
ollama pull llama2
```

### خطأ: "Database is locked"

✅ **الحل:**
```bash
# حذف قاعدة البيانات وإنشاء جديدة
rm chat_history.db
python app.py  # سيتم إنشاء قاعدة بيانات جديدة
```

## 📊 شرح الأكواد الرئيسية

### config.py - الإعدادات

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OLLAMA_URL = "http://localhost:11434"
    OLLAMA_MODEL = "llama2"
    DATABASE_URL = "sqlite:///./chat_history.db"
```

**الشرح:**
- `BaseSettings`: من Pydantic للتعامل مع متغيرات البيئة
- يمكن تعديل القيم من ملف `.env` تلقائياً

### models.py - نماذج قاعدة البيانات

```python
from sqlalchemy import Column, String, DateTime

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    title = Column(String)
```

**الشرح:**
- استخدام SQLAlchemy ORM
- تعريف جداول قاعدة البيانات كفئات Python

### ollama_handler.py - معالج Ollama

```python
def generate_response(self, prompt: str) -> Generator:
    """إرسال طلب مع Streaming"""
    response = requests.post(
        f"{self.base_url}/api/generate",
        json={"prompt": prompt, "stream": True}
    )
    for line in response.iter_lines():
        yield data["response"]
```

**الشرح:**
- `Generator`: يرسل البيانات تدريجياً بدل الانتظار
- `stream=True`: يسمح بالـ streaming (الرد يأتي بالتدريج)

### routes.py - API Endpoints

```python
@router.post("/conversations/{conversation_id}/messages")
async def send_message(conversation_id: int, message: MessageCreate):
    """إرسال رسالة والحصول على رد"""
    # حفظ رسالة المستخدم
    # الحصول على رد من Ollama
    # حفظ الرد
```

**الشرح:**
- `@router.post()`: تعريف endpoint لطلب POST
- `async`: استخدام Async للأداء الأفضل
- `Pydantic models`: التحقق التلقائي من صحة البيانات

## 🚀 نصائح الأداء

### 1. استخدام النماذج الأخف

```bash
# سريع وخفيف
ollama pull neural-chat

# متوازن
ollama pull mistral

# قوي لكن بطيء
ollama pull llama2-70b
```

### 2. ضبط درجة الحرارة (Temperature)

```python
# قيم منخفضة = ردود منطقية وثابتة
"temperature": 0.3

# قيم عالية = ردود إبداعية
"temperature": 0.9
```

### 3. قاعدة البيانات

```bash
# نسخ احتياطية
cp chat_history.db chat_history.backup.db

# حذف السجل القديم
rm chat_history.db
```

## 📞 الدعم والمساعدة

- 📚 توثيق Ollama: https://github.com/ollama/ollama
- 📚 توثيق FastAPI: https://fastapi.tiangolo.com/
- 🐛 الإبلاغ عن الأخطاء: استخدم Issues في GitHub

---

**حظاً موفقاً! 🎉**
