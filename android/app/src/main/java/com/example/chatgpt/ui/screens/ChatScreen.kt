package com.example.chatgpt.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.chatgpt.ui.components.ChatMessage
import com.example.chatgpt.viewmodel.ChatViewModel

/**
 * 💬 شاشة الدردشة الرئيسية
 * تعرض المحادثات والرسائل
 */
@Composable
fun ChatScreen(
    viewModel: ChatViewModel = viewModel()
) {
    val messages by viewModel.messages.collectAsState(initial = emptyList())
    var inputText by remember { mutableStateOf("") }
    val isLoading by viewModel.isLoading.collectAsState(initial = false)

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background),
        verticalArrangement = Arrangement.SpaceBetween
    ) {
        // ===== Header =====
        HeaderSection()

        // ===== Messages List =====
        LazyColumn(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth()
                .padding(16.dp),
            reverseLayout = true,
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(messages.reversed()) { message ->
                ChatMessage(
                    text = message.content,
                    isUser = message.role == "user"
                )
            }
        }

        // ===== Input Area =====
        InputSection(
            inputText = inputText,
            onInputChange = { inputText = it },
            onSendClick = {
                if (inputText.isNotBlank()) {
                    viewModel.sendMessage(inputText)
                    inputText = ""
                }
            },
            isLoading = isLoading
        )
    }
}

@Composable
fun HeaderSection() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(MaterialTheme.colorScheme.primary)
            .padding(16.dp)
    ) {
        Text(
            "🤖 ChatGPT Clone",
            style = MaterialTheme.typography.headlineSmall,
            color = Color.White
        )
        Text(
            "محادثة ذكية مع Ollama",
            style = MaterialTheme.typography.bodySmall,
            color = Color.White.copy(alpha = 0.7f)
        )
    }
}

@Composable
fun InputSection(
    inputText: String,
    onInputChange: (String) -> Unit,
    onSendClick: () -> Unit,
    isLoading: Boolean
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        TextField(
            value = inputText,
            onValueChange = onInputChange,
            modifier = Modifier
                .weight(1f)
                .height(50.dp),
            placeholder = { Text("اكتب سؤالك...") },
            shape = RoundedCornerShape(12.dp),
            enabled = !isLoading,
            colors = TextFieldDefaults.colors(
                focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant
            )
        )

        Button(
            onClick = onSendClick,
            modifier = Modifier
                .size(50.dp),
            enabled = !isLoading && inputText.isNotBlank(),
            shape = RoundedCornerShape(12.dp)
        ) {
            if (isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(24.dp),
                    color = Color.White
                )
            } else {
                Icon(
                    Icons.Default.Send,
                    contentDescription = "إرسال",
                    tint = Color.White
                )
            }
        }
    }
}
