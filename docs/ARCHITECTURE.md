# 🏗️ شرح العمارة (Architecture)

شرح تفصيلي لهيكل المشروع والمكونات الرئيسية

## 📐 Diagram العمارة

```
┌─────────────────────────────────────────────────────────┐
│              📱 ANDROID APP (Kotlin + Compose)          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐        ┌──────────────────────┐  │
│  │   UI Layer       │        │   ViewModel Layer    │  │
│  │ - ChatScreen     │───────▶│  - ChatViewModel     │  │
│  │ - ChatMessage    │        │  - StateFlow         │  │
│  └──────────────────┘        └──────────────────────┘  │
│                                      │                 │
│                                      │                 │
│  ┌────────────────────────────────────▼──────────┐    │
│  │          Network Layer (Retrofit)            │    │
│  │  - ApiService                                 │    │
│  │  - RetrofitClient                             │    │
│  │  - Request/Response Models                    │    │
│  └────────────────────────────────────┬──────────┘    │
│                                       │                │
└───────────────────────────────────────┼────────────────┘
                                        │
                                        │ HTTP REST API
                                        │
┌───────────────────────────────────────▼────────────────┐
│         🐍 PYTHON BACKEND (FastAPI + Ollama)          │
├───────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────────────────────────────────────────┐   │
│  │      FastAPI Application (app.py)            │   │
│  │  - CORS Middleware                           │   │
│  │  - Lifespan Events                           │   │
│  │  - Routes Include                            │   │
│  └──────────────────────────────────────────────┘   │
│                                                       │
│  ┌──────────────────────────────────────────────┐   │
│  │    API Routes (routes.py)                    │   │
│  │  - GET    /health                            │   │
│  │  - GET    /ollama/models                     │   │
│  │  - POST   /conversations                     │   │
│  │  - POST   /conversations/{id}/messages       │   │
│  │  - GET    /conversations/{id}/messages       │   │
│  └──────────────────────────────────────────────┘   │
│                                                       │
│  ┌────────────────────┐   ┌─────────────────────┐   │
│  │ Ollama Handler     │   │   Database Layer    │   │
│  │ (ollama_handler.py)│   │  (models.py)        │   │
│  │                    │   │  - Conversation     │   │
│  │ - check_connection │   │  - Message          │   │
│  │ - get_models       │   │  (SQLAlchemy ORM)   │   │
│  │ - generate_response│   │  - SQLite DB        │   │
│  └────────────────────┘   └─────────────────────┘   │
│                                                       │
└───────────────────────────────────────┬───────────────┘
                                        │
                           HTTP Request to
                                        │
┌───────────────────────────────────────▼───────────────┐
│        🤖 OLLAMA (Local AI Model Server)             │
├───────────────────────────────────────────────────────┤
│  - llama2                                            │
│  - mistral                                           │
│  - neural-chat                                       │
│  - dolphin-mixtral                                   │
│  - (أي نموذج آخر)                                   │
└───────────────────────────────────────────────────────┘
```

---

## 🎯 مكونات النظام

### 1️⃣ طبقة واجهة المستخدم (UI Layer)

**الملفات:**
- `ChatScreen.kt` - الشاشة الرئيسية
- `ChatMessage.kt` - مكون الرسالة
- `Theme.kt` - إعدادات المظهر
- `Color.kt` - الألوان

**المسؤوليات:**
- عرض الرسائل
- جمع مدخلات المستخدم
- عرض حالة التحميل

### 2️⃣ طبقة ViewModel

**الملف:** `ChatViewModel.kt`

**المسؤوليات:**
- إدارة حالة الرسائل (StateFlow)
- معالجة منطق الأعمال
- التواصل مع Network Layer
- إدارة الأخطاء

```kotlin
class ChatViewModel : ViewModel() {
    private val _messages = MutableStateFlow<List<MessageResponse>>()
    val messages: StateFlow<List<MessageResponse>> = _messages
    
    fun sendMessage(content: String) {
        // Logic هنا
    }
}
```

### 3️⃣ طبقة الشبكة (Network Layer)

**الملفات:**
- `ApiService.kt` - تعريف الـ endpoints
- `RetrofitClient.kt` - إعداد Retrofit

**المسؤوليات:**
- تحويل الطلبات إلى HTTP requests
- تحويل الردود إلى objects
- التعامل مع الأخطاء

### 4️⃣ طبقة Backend (FastAPI)

**الملفات:**
- `app.py` - التطبيق الرئيسي
- `routes.py` - نقاط نهاية API
- `models.py` - نماذج قاعدة البيانات
- `ollama_handler.py` - التواصل مع Ollama

**المسؤوليات:**
- معالجة طلبات HTTP
- إدارة قاعدة البيانات
- التواصل مع Ollama

### 5️⃣ Ollama (نماذج AI)

**الوظيفة:**
- تحليل الأسئلة
- توليد الردود
- معالجة اللغة الطبيعية

---

## 🔄 تدفق البيانات (Data Flow)

### عند إرسال رسالة:

```
1. المستخدم يكتب الرسالة في TextField
   ↓
2. يضغط زر الإرسال → onSendClick() في ChatScreen
   ↓
3. ChatViewModel.sendMessage(text) يُستدعى
   ↓
4. إعداد MessageRequest وإرسالها عبر ApiService
   ↓
5. RetrofitClient يحول الطلب إلى HTTP POST
   ↓
6. FastAPI routes.py يستقبل الطلب
   ↓
7. حفظ الرسالة في قاعدة البيانات (User)
   ↓
8. استدعاء ollama_handler.generate_response()
   ↓
9. Ollama يولد الرد
   ↓
10. حفظ الرد في قاعدة البيانات (Assistant)
   ↓
11. إرجاع MessageResponse إلى Android
   ↓
12. تحديث _messages StateFlow
   ↓
13. UI تعاد رسمه تلقائياً (Recompose)
   ↓
14. الرسالة الجديدة تظهر على الشاشة
```

---

## 💾 قاعدة البيانات (Database Schema)

### جدول Conversations

```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_archived BOOLEAN DEFAULT FALSE
);
```

### جدول Messages

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    role VARCHAR NOT NULL,  -- 'user' or 'assistant'
    model_used VARCHAR,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_edited BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
```

---

## 🔌 التكامل بين الطبقات

### Android → Backend

```kotlin
// في ViewModel
val response = apiService.sendMessage(conversationId, request)
```

### Backend → Database

```python
# في routes.py
new_message = Message(...)
db.add(new_message)
db.commit()
```

### Backend → Ollama

```python
# في ollama_handler.py
for chunk in self.generate_response(prompt):
    response_text += chunk
```

---

## 🚀 نقاط التحسين المستقبلية

1. **Authentication** - إضافة نظام تسجيل دخول
2. **Caching** - تخزين مؤقت للنتائج
3. **Streaming** - بث الردود في الوقت الفعلي
4. **Offline Mode** - وضع بدون اتصال
5. **Analytics** - تحليل الاستخدام
6. **Multi-user** - دعم عدة مستخدمين

---

**آخر تحديث:** 2024-01-15
