"""
🗄️ نماذج قاعدة البيانات
تعريف جداول قاعدة البيانات للمحادثات والرسائل
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# إنشاء base class لجميع النماذج
Base = declarative_base()


class Conversation(Base):
    """
    نموذج المحادثة
    يحتفظ بمعلومات كل محادثة
    """
    
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    """معرّف المحادثة الفريد"""
    
    title = Column(String, index=True)
    """عنوان المحادثة"""
    
    created_at = Column(DateTime, default=datetime.utcnow)
    """وقت إنشاء المحادثة"""
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    """آخر تحديث للمحادثة"""
    
    is_archived = Column(Boolean, default=False)
    """هل تم أرشفة المحادثة"""


class Message(Base):
    """
    نموذج الرسالة
    يحتفظ بكل رسالة في المحادثة
    """
    
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    """معرّف الرسالة الفريد"""
    
    conversation_id = Column(Integer, index=True)
    """معرّف المحادثة التابعة لها الرسالة"""
    
    content = Column(Text)
    """محتوى الرسالة"""
    
    role = Column(String)  # "user" أو "assistant"
    """دور المرسل (مستخدم أو مساعد)"""
    
    model_used = Column(String)
    """اسم النموذج المستخدم في الرد"""
    
    created_at = Column(DateTime, default=datetime.utcnow)
    """وقت إنشاء الرسالة"""
    
    is_edited = Column(Boolean, default=False)
    """هل تم تعديل الرسالة"""
