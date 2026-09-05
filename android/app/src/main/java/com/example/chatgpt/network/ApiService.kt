package com.example.chatgpt.network

import com.google.gson.annotations.SerializedName
import retrofit2.http.*

/**
 * 📡 Retrofit API Service
 * تعريف جميع endpoints الخاصة بـ Backend
 */
interface ApiService {

    // ===== Health Check =====
    @GET("/health")
    suspend fun healthCheck(): HealthResponse

    // ===== Ollama Routes =====
    @GET("/ollama/models")
    suspend fun getAvailableModels(): ModelsResponse

    // ===== Conversations =====
    @POST("/conversations")
    suspend fun createConversation(@Body request: ConversationRequest): ConversationResponse

    @GET("/conversations")
    suspend fun getConversations(
        @Query("skip") skip: Int = 0,
        @Query("limit") limit: Int = 10
    ): List<ConversationResponse>

    @GET("/conversations/{id}")
    suspend fun getConversation(@Path("id") conversationId: Int): ConversationResponse

    @DELETE("/conversations/{id}")
    suspend fun deleteConversation(@Path("id") conversationId: Int): DeleteResponse

    // ===== Messages =====
    @POST("/conversations/{id}/messages")
    suspend fun sendMessage(
        @Path("id") conversationId: Int,
        @Body request: MessageRequest
    ): MessageResponse

    @GET("/conversations/{id}/messages")
    suspend fun getMessages(
        @Path("id") conversationId: Int,
        @Query("skip") skip: Int = 0,
        @Query("limit") limit: Int = 50
    ): List<MessageResponse>
}

// ===== Request/Response Models =====

data class ConversationRequest(
    val title: String
)

data class ConversationResponse(
    val id: Int,
    val title: String,
    val created_at: String,
    val updated_at: String,
    val is_archived: Boolean
)

data class MessageRequest(
    val content: String,
    val conversation_id: Int,
    val model: String? = null
)

data class MessageResponse(
    val id: Int,
    val conversation_id: Int,
    val content: String,
    val role: String,
    val model_used: String,
    val created_at: String
)

data class HealthResponse(
    val status: String,
    val ollama_connected: Boolean,
    val ollama_url: String,
    val database: String
)

data class ModelsResponse(
    val models: List<String>,
    val count: Int
)

data class DeleteResponse(
    val message: String
)
