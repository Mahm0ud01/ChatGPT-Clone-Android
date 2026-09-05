# 🤖 ChatGPT Clone - Android App

تطبيق موبايل متكامل لـ Android يتصل بـ **Ollama** للذكاء الاصطناعي مع واجهة مستخدم احترافية.

## ✨ الميزات الرئيسية

- ✅ **محادثات ذكية** - اتصال مباشر مع Ollama
- ✅ **حفظ السجل** - حفظ المحادثات في قاعدة بيانات محلية
- ✅ **واجهة احترافية** - تصميم حديث باستخدام Jetpack Compose
- ✅ **دعم النماذج المختلفة** - استخدم أي نموذج محلي في Ollama
- ✅ **معالجة الأخطاء** - نظام قوي للتعامل مع الأخطاء
- ✅ **Offline أولاً** - يعمل بدون اتصال إنترنت (محليٌ فقط)
- ✅ **Dark/Light Theme** - دعم المظهر الفاتح والداكن
- ✅ **Real-time Streaming** - عرض الرد تدريجياً أثناء الكتابة

## 📋 متطلبات المشروع

### Backend (Python)
- Python 3.9+
- FastAPI
- Ollama
- SQLAlchemy (قاعدة بيانات)
- Pydantic (التحقق من البيانات)

### Android
- Android Studio
- Android SDK 24+
- Kotlin
- Jetpack Compose
- Retrofit (HTTP Client)

## 🏗️ هيكل المشروع

```
ChatGPT-Clone-Android/
├── backend/                    # Backend بـ Python
│   ├── app.py                 # تطبيق FastAPI الرئيسي
│   ├── models.py              # نماذج قاعدة البيانات
│   ├── routes.py              # المسارات (Routes)
│   ├── ollama_handler.py       # معالج Ollama
│   ├── requirements.txt        # المكتبات المطلوبة
│   └── config.py              # الإعدادات
├── android/                   # تطبيق Android
│   ├── app/
│   │   ├── src/
│   │   │   ├── main/
│   │   │   │   ├── java/com/example/chatgpt/
│   │   │   │   │   ├── MainActivity.kt
│   │   │   │   │   ├── ui/
│   │   │   │   │   ├── network/
│   │   │   │   │   ├── database/
│   │   │   │   │   └── viewmodel/
│   │   │   │   └── res/
│   │   │   └── test/
│   │   └── build.gradle
│   └── settings.gradle
├── docs/                      # التوثيق
│   ├── SETUP.md              # خطوات التثبيت
│   ├── API.md                # توثيق API
│   └── ARCHITECTURE.md       # شرح العمارة
└── README.md                 # هذا الملف
```

## 🚀 البدء السريع

### 1. تثبيت Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 2. إنشاء تطبيق Android

```bash
cd android
./gradlew build
./gradlew installDebug  # تثبيت على جهاز/محاكي
```

## 📚 التوثيق الكاملة

- [SETUP.md](./docs/SETUP.md) - شرح التثبيت بالتفصيل
- [API.md](./docs/API.md) - توثيق API الكامل
- [ARCHITECTURE.md](./docs/ARCHITECTURE.md) - شرح العمارة والمكونات

## 🔧 الإعدادات

### إعدادات Backend
يمكن تعديل الإعدادات من ملف `backend/config.py`:

```python
OLLAMA_URL = "http://localhost:11434"  # عنوان Ollama
MODEL_NAME = "llama2"                  # اسم النموذج
DATABASE_URL = "sqlite:///./chat.db"   # قاعدة البيانات
```

### إعدادات Android
في `android/app/build.gradle`:

```gradle
defaultConfig {
    applicationId "com.example.chatgpt"
    minSdk 24
    targetSdk 34
}
```

## 🤝 كيفية المساهمة

نرحب بالمساهمات! يرجى:

1. عمل Fork للمستودع
2. إنشاء فرع للميزة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add AmazingFeature'`)
4. Push إلى الفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

## 📄 الترخيص

هذا المشروع مرخص تحت MIT License - انظر ملف [LICENSE](./LICENSE) للتفاصيل.

## 📞 التواصل والدعم

- 📧 البريد الإلكتروني: [أضف بريدك]
- 🐛 الإبلاغ عن الأخطاء: استخدم [Issues](https://github.com/Mahm0ud01/ChatGPT-Clone-Android/issues)
- 💬 النقاشات: استخدم [Discussions](https://github.com/Mahm0ud01/ChatGPT-Clone-Android/discussions)

---

**صُنع بـ ❤️ من قبل Mahm0ud01**
