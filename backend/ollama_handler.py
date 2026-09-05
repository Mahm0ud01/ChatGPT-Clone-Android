"""
🤖 معالج Ollama
يتعامل مع الاتصال بـ Ollama وإرسال الطلبات
"""

import requests
from typing import Generator
import json
from config import settings


class OllamaHandler:
    """
    فئة للتعامل مع Ollama
    توفر وظائف للتواصل مع الخادم المحلي
    """
    
    def __init__(self):
        self.base_url = settings.OLLAMA_URL
        self.model = settings.OLLAMA_MODEL
    
    def check_connection(self) -> bool:
        """
        التحقق من الاتصال بـ Ollama
        
        Returns:
            bool: True إذا كان الاتصال نجح
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ خطأ في الاتصال بـ Ollama: {e}")
            return False
    
    def get_available_models(self) -> list:
        """
        الحصول على قائمة النماذج المتاحة
        
        Returns:
            list: قائمة أسماء النماذج
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                models = [model["name"] for model in data.get("models", [])]
                return models
            return []
        except Exception as e:
            print(f"❌ خطأ في الحصول على النماذج: {e}")
            return []
    
    def generate_response(self, prompt: str, model: str = None) -> Generator[str, None, None]:
        """
        إرسال استفسار إلى Ollama وتلقي الرد (Streaming)
        
        Args:
            prompt (str): السؤال/الطلب
            model (str): اسم النموذج (اختياري، يستخدم الافتراضي إن لم يُحدد)
        
        Yields:
            str: أجزاء الرد تدريجياً
        
        Example:
            >>> for chunk in handler.generate_response("مرحبا"):
            >>>     print(chunk, end='', flush=True)
        """
        
        if model is None:
            model = self.model
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": True,  # تفعيل الـ streaming
                    "temperature": 0.7,  # درجة العشوائية
                },
                stream=True,
                timeout=None
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if "response" in data:
                                yield data["response"]
                        except json.JSONDecodeError:
                            continue
            else:
                yield f"❌ خطأ: {response.status_code}"
                
        except requests.exceptions.Timeout:
            yield "⏱️ انتهت مهلة الانتظار - يرجى المحاولة لاحقاً"
        except requests.exceptions.ConnectionError:
            yield "🔌 خطأ في الاتصال - تأكد من تشغيل Ollama"
        except Exception as e:
            yield f"❌ خطأ غير متوقع: {str(e)}"
    
    def generate_response_sync(self, prompt: str, model: str = None) -> str:
        """
        إرسال استفسار وتلقي الرد الكامل (بدون streaming)
        
        Args:
            prompt (str): السؤال/الطلب
            model (str): اسم النموذج
        
        Returns:
            str: الرد الكامل
        """
        
        response_text = ""
        for chunk in self.generate_response(prompt, model):
            response_text += chunk
        
        return response_text


# إنشاء instance عام من المعالج
ollama_handler = OllamaHandler()
