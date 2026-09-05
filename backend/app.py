"""
🚀 تطبيق FastAPI الرئيسي
نقطة البداية لخادم الويب
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from routes import router
from ollama_handler import ollama_handler

# ============ Startup/Shutdown Events ============

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    إدارة دورة حياة التطبيق (البدء والإيقاف)
    """
    # Startup
    print("=" * 60)
    print("🚀 بدء تشغيل التطبيق...")
    print(f"📡 عنوان Ollama: {settings.OLLAMA_URL}")
    print(f"🤖 النموذج الافتراضي: {settings.OLLAMA_MODEL}")
    
    # التحقق من الاتصال بـ Ollama
    if ollama_handler.check_connection():
        print("✅ متصل بـ Ollama بنجاح!")
        models = ollama_handler.get_available_models()
        print(f"📋 النماذج المتاحة: {', '.join(models)}")
    else:
        print("⚠️  تحذير: لم يتمكن من الاتصال بـ Ollama")
        print("   تأكد من تشغيل: ollama serve")
    
    print("=" * 60)
    
    yield
    
    # Shutdown
    print("=" * 60)
    print("🛑 إيقاف التطبيق...")
    print("=" * 60)


# ============ إنشاء التطبيق ============

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="تطبيق ChatGPT متكامل مع Ollama",
    lifespan=lifespan
)

# ============ إضافة CORS Middleware ============
# هذا يسمح بالطلبات من تطبيق Android

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # السماح من أي مصدر (يمكن تحديدها لاحقاً)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ تضمين الـ Routes ============

app.include_router(router)

# ============ Root Endpoint ============

@app.get("/")
async def root():
    """
    الصفحة الرئيسية للـ API
    """
    return {
        "name": "🤖 ChatGPT Clone API",
        "version": settings.API_VERSION,
        "message": "مرحباً! استخدم /docs لرؤية جميع الـ endpoints",
        "docs_url": "/docs",
        "health_url": "/health"
    }


# ============ التشغيل ============

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
