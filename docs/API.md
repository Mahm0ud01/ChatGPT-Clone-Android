# 📡 توثيق API الكاملة

## 🌐 Base URL

```
http://localhost:8000
```

## ✅ Health Check

### GET /health

التحقق من صحة الخادم والاتصال بـ Ollama

**Response:**
```json
{
  "status": "✅ السيرفر يعمل",
  "ollama_connected": true,
  "ollama_url": "http://localhost:11434",
  "database": "✅ قاعدة البيانات متصلة"
}
```

---

## 🤖 Ollama Endpoints

### GET /ollama/models

الحصول على قائمة النماذج المتاحة

**Response:**
```json
{
  "models": ["llama2", "mistral", "neural-chat"],
  "count": 3
}
```

---

## 💬 Conversation Endpoints

### POST /conversations

إنشاء محادثة جديدة

**Request Body:**
```json
{
  "title": "عنوان المحادثة"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "عنوان المحادثة",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00",
  "is_archived": false
}
```

### GET /conversations

الحصول على قائمة المحادثات

**Query Parameters:**
- `skip` (optional): عدد المحادثات المراد تخطيها (افتراضي: 0)
- `limit` (optional): عدد المحادثات المراد عرضها (افتراضي: 10)

**Response:**
```json
[
  {
    "id": 1,
    "title": "محادثتي الأولى",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "is_archived": false
  }
]
```

### GET /conversations/{id}

الحصول على محادثة معينة

**Response:**
```json
{
  "id": 1,
  "title": "محادثتي الأولى",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00",
  "is_archived": false
}
```

### DELETE /conversations/{id}

حذف محادثة ورسائلها

**Response:**
```json
{
  "message": "✅ تم حذف المحادثة بنجاح"
}
```

---

## 📨 Message Endpoints

### POST /conversations/{id}/messages

إرسال رسالة والحصول على رد

**Request Body:**
```json
{
  "content": "مرحباً، كيف حالك؟",
  "conversation_id": 1,
  "model": "llama2"  // اختياري
}
```

**Response:**
```json
{
  "id": 2,
  "conversation_id": 1,
  "content": "مرحباً! أنا بخير، شكراً لسؤالك...",
  "role": "assistant",
  "model_used": "llama2",
  "created_at": "2024-01-15T10:35:00"
}
```

### GET /conversations/{id}/messages

الحصول على جميع رسائل محادثة

**Query Parameters:**
- `skip` (optional): عدد الرسائل المراد تخطيها (افتراضي: 0)
- `limit` (optional): عدد الرسائل المراد عرضها (افتراضي: 50)

**Response:**
```json
[
  {
    "id": 1,
    "conversation_id": 1,
    "content": "مرحباً، كيف حالك؟",
    "role": "user",
    "model_used": "llama2",
    "created_at": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "conversation_id": 1,
    "content": "مرحباً! أنا بخير...",
    "role": "assistant",
    "model_used": "llama2",
    "created_at": "2024-01-15T10:35:00"
  }
]
```

---

## 🔴 Error Responses

### 404 - Not Found
```json
{
  "detail": "❌ المحادثة غير موجودة"
}
```

### 500 - Server Error
```json
{
  "detail": "❌ خطأ: رسالة الخطأ"
}
```

### 503 - Service Unavailable
```json
{
  "detail": "❌ Ollama غير متصل أو لا توجد نماذج متاحة"
}
```

---

## 🧪 أمثلة استخدام

### مثال 1: محادثة كاملة بـ cURL

```bash
# 1. إنشاء محادثة
curl -X POST http://localhost:8000/conversations \
  -H "Content-Type: application/json" \
  -d '{"title": "محادثتي الأولى"}'

# 2. إرسال رسالة
curl -X POST http://localhost:8000/conversations/1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "content": "ما هو الذكاء الاصطناعي؟",
    "conversation_id": 1
  }'

# 3. الحصول على جميع الرسائل
curl http://localhost:8000/conversations/1/messages
```

### مثال 2: استخدام Python

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. إنشاء محادثة
response = requests.post(
    f"{BASE_URL}/conversations",
    json={"title": "محادثتي"}
)
conversation_id = response.json()["id"]

# 2. إرسال رسالة
response = requests.post(
    f"{BASE_URL}/conversations/{conversation_id}/messages",
    json={
        "content": "أخبرني عن Python",
        "conversation_id": conversation_id
    }
)

print(response.json())
```

### مثال 3: استخدام Android (Kotlin)

```kotlin
viewModelScope.launch {
    try {
        val request = MessageRequest(
            content = "مرحباً",
            conversation_id = 1
        )
        
        val response = apiService.sendMessage(1, request)
        println("الرد: ${response.content}")
    } catch (e: Exception) {
        println("خطأ: ${e.message}")
    }
}
```

---

## 📝 ملاحظات مهمة

- جميع الرسائل محفوظة محلياً في قاعدة البيانات
- الردود تأتي من نموذج Ollama المحلي
- لا توجد بيانات تُرسل إلى الإنترنت (Offline)
- يمكن استخدام أي نموذج من نماذج Ollama المتاحة

---

**آخر تحديث:** 2024-01-15
