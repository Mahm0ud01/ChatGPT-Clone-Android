"""
⚙️ إعدادات التطبيق
هنا يتم تعريف جميع إعدادات التطبيق مثل عنوان Ollama وقاعدة البيانات
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    إعدادات التطبيق الرئيسية
    
    يمكن تعديل هذه القيم من خلال متغيرات البيئة (.env)
    """
    
    # إعدادات Ollama
    OLLAMA_URL: str = "http://localhost:11434"
    """عنوان خادم Ollama الذي يعمل محلياً"""
    
    OLLAMA_MODEL: str = "llama2"
    """اسم النموذج المستخدم في Ollama"""
    
    # إعدادات قاعدة البيانات
    DATABASE_URL: str = "sqlite:///./chat_history.db"
    """رابط قاعدة البيانات SQLite"""
    
    # إعدادات FastAPI
    API_TITLE: str = "ChatGPT Clone API"
    """عنوان API"""
    
    API_VERSION: str = "1.0.0"
    """إصدار API"""
    
    DEBUG: bool = True
    """وضع التطوير/الاختبار"""
    
    # إعدادات CORS (للسماح بالطلبات من Android)
    ALLOWED_ORIGINS: list = [
        "http://localhost:8000",
        "http://localhost:3000",
    ]
    """المصادر المسموحة للطلبات"""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# إنشاء instance من الإعدادات
settings = Settings()
