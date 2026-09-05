package com.example.chatgpt.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.chatgpt.network.MessageRequest
import com.example.chatgpt.network.MessageResponse
import com.example.chatgpt.network.RetrofitClient
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

/**
 * 🧠 ViewModel لشاشة الدردشة
 * يدير حالة الرسائل والعمليات
 */
class ChatViewModel : ViewModel() {

    private val apiService = RetrofitClient.apiService
    private var currentConversationId: Int = 1

    // ===== States =====
    private val _messages = MutableStateFlow<List<MessageResponse>>(emptyList())
    val messages: StateFlow<List<MessageResponse>> = _messages

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error

    init {
        loadMessages()
    }

    /**
     * تحميل الرسائل من الخادم
     */
    fun loadMessages() {
        viewModelScope.launch {
            try {
                val messages = apiService.getMessages(currentConversationId)
                _messages.value = messages
            } catch (e: Exception) {
                _error.value = "خطأ: ${e.message}"
            }
        }
    }

    /**
     * إرسال رسالة جديدة
     */
    fun sendMessage(content: String) {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val request = MessageRequest(
                    content = content,
                    conversation_id = currentConversationId
                )

                val response = apiService.sendMessage(currentConversationId, request)

                // إضافة الرسالة الجديدة إلى القائمة
                val updatedMessages = _messages.value.toMutableList()
                updatedMessages.add(response)
                _messages.value = updatedMessages

            } catch (e: Exception) {
                _error.value = "❌ فشل الإرسال: ${e.message}"
            } finally {
                _isLoading.value = false
            }
        }
    }
}
