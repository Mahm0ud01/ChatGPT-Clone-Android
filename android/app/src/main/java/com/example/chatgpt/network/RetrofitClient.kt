package com.example.chatgpt.network

import com.google.gson.GsonBuilder
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit
import okhttp3.OkHttpClient

/**
 * 🔗 Retrofit Client
 * إعداد الاتصال بـ Backend
 */
object RetrofitClient {
    // تغيير هذا العنوان حسب عنوان الخادم الفعلي
    private const val BASE_URL = "http://192.168.1.100:8000/" // غيّر إلى عنوان خادمك

    private val httpClient = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()

    private val gson = GsonBuilder()
        .setLenient()
        .create()

    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(httpClient)
        .addConverterFactory(GsonConverterFactory.create(gson))
        .build()

    val apiService: ApiService = retrofit.create(ApiService::class.java)
}
