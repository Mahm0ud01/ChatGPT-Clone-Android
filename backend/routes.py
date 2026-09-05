"""
📡 المسارات (Routes) - نقاط نهاية API
تعريف جميع endpoints الخاصة بالتطبيق
"""

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import List, Optional
from datetime import datetime

from models import Base, Conversation, Message
from ollama_handler import ollama_handler
from config import settings

# إنشاء قاعدة البيانات
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# إنشاء router
router = APIRouter()

# ============ Pydantic Models (للتحقق من البيانات) ============

class MessageCreate(BaseModel):
    """نموذج لإنشاء رسالة جديدة"""
    content: str
    conversation_id: int
    model: Optional[str] = None


class ConversationCreate(BaseModel):
    """نموذج لإنشاء محادثة جديدة"""
    title: str


class MessageResponse(BaseModel):
    """نموذج الرد مع الرسالة"""
    id: int
    conversation_id: int
    content: str
    role: str
    model_used: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """نموذج الرد مع المحادثة"""
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    is_archived: bool
    
    class Config:
        from_attributes = True


# ============ Health Check ============

@router.get("/health")
async def health_check():
    """
    التحقق من صحة الخادم
    
    Returns:
        dict: حالة الخادم والاتصال بـ Ollama
    """
    ollama_connected = ollama_handler.check_connection()
    
    return {
        "status": "✅ السيرفر يعمل",
        "ollama_connected": ollama_connected,
        "ollama_url": settings.OLLAMA_URL,
        "database": "✅ قاعدة البيانات متصلة",
    }


# ============ Ollama Routes ============

@router.get("/ollama/models")
async def get_models():
    """
    الحصول على قائمة النماذج المتاحة في Ollama
    
    Returns:
        dict: قائمة النماذج
    """
    models = ollama_handler.get_available_models()
    
    if not models:
        raise HTTPException(
            status_code=503,
            detail="❌ Ollama غير متصل أو لا توجد نماذج متاحة"
        )
    
    return {"models": models, "count": len(models)}


# ============ Conversation Routes ============

@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(conv: ConversationCreate):
    """
    إنشاء محادثة جديدة
    
    Args:
        conv: بيانات المحادثة
    
    Returns:
        ConversationResponse: بيانات المحادثة الجديدة
    """
    db = SessionLocal()
    
    try:
        new_conversation = Conversation(title=conv.title)
        db.add(new_conversation)
        db.commit()
        db.refresh(new_conversation)
        
        return new_conversation
    finally:
        db.close()


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(skip: int = Query(0), limit: int = Query(10)):
    """
    الحصول على قائمة المحادثات
    
    Args:
        skip: عدد المحادثات المراد تخطيها
        limit: عدد المحادثات المراد عرضها
    
    Returns:
        List[ConversationResponse]: قائمة المحادثات
    """
    db = SessionLocal()
    
    try:
        conversations = db.query(Conversation).offset(skip).limit(limit).all()
        return conversations
    finally:
        db.close()


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: int):
    """
    الحصول على محادثة معينة
    
    Args:
        conversation_id: معرّف المحادثة
    
    Returns:
        ConversationResponse: بيانات المحادثة
    """
    db = SessionLocal()
    
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="❌ المحادثة غير موجودة")
        
        return conversation
    finally:
        db.close()


# ============ Message Routes ============

@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
async def send_message(conversation_id: int, message: MessageCreate, background_tasks: BackgroundTasks):
    """
    إرسال رسالة وتلقي رد من Ollama
    
    Args:
        conversation_id: معرّف المحادثة
        message: محتوى الرسالة
    
    Returns:
        MessageResponse: الرسالة المحفوظة
    """
    db = SessionLocal()
    
    try:
        # التحقق من وجود المحادثة
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="❌ المحادثة غير موجودة")
        
        # حفظ رسالة المستخدم
        user_message = Message(
            conversation_id=conversation_id,
            content=message.content,
            role="user",
            model_used=message.model or settings.OLLAMA_MODEL
        )
        db.add(user_message)
        db.commit()
        
        # الحصول على رد من Ollama
        response_text = ollama_handler.generate_response_sync(
            message.content,
            message.model
        )
        
        # حفظ رد المساعد
        assistant_message = Message(
            conversation_id=conversation_id,
            content=response_text,
            role="assistant",
            model_used=message.model or settings.OLLAMA_MODEL
        )
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)
        
        # تحديث وقت المحادثة
        conversation.updated_at = datetime.utcnow()
        db.commit()
        
        return assistant_message
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"❌ خطأ: {str(e)}")
    finally:
        db.close()


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(conversation_id: int, skip: int = Query(0), limit: int = Query(50)):
    """
    الحصول على جميع رسائل محادثة معينة
    
    Args:
        conversation_id: معرّف المحادثة
        skip: عدد الرسائل المراد تخطيها
        limit: عدد الرسائل المراد عرضها
    
    Returns:
        List[MessageResponse]: قائمة الرسائل
    """
    db = SessionLocal()
    
    try:
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).offset(skip).limit(limit).all()
        
        return messages
    finally:
        db.close()


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: int):
    """
    حذف محادثة ورسائلها
    
    Args:
        conversation_id: معرّف المحادثة
    
    Returns:
        dict: رسالة تأكيد الحذف
    """
    db = SessionLocal()
    
    try:
        # حذف الرسائل أولاً
        db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).delete()
        
        # ثم حذف المحادثة
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="❌ المحادثة غير موجودة")
        
        db.delete(conversation)
        db.commit()
        
        return {"message": "✅ تم حذف المحادثة بنجاح"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"❌ خطأ: {str(e)}")
    finally:
        db.close()
