<template>
    <Teleport to="body">
      <div v-if="visible" class="fixed inset-0 z-50 flex justify-end">
        <div class="absolute inset-0 bg-black/10 backdrop-blur-sm" @click="close"></div>
        <div class="relative w-[480px] max-w-full h-full bg-white shadow-2xl flex flex-col animate-slideIn">
          <div class="flex items-center justify-between px-6 py-4 border-b border-[#e5e5ea]">
            <h3 class="text-lg font-light text-[#1c1c1e]">Klea 美妆顾问</h3>
            <button @click="close" class="text-[#8e8e93] text-2xl leading-none">&times;</button>
          </div>
          <div ref="messageContainer" class="flex-1 overflow-y-auto p-6 space-y-4">
            <div v-if="messages.length === 0" class="text-center text-[#8e8e93] text-sm mt-20">💬 开始与 Klea 对话吧</div>
            <div v-for="(msg, idx) in messages" :key="idx" class="flex" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
              <div class="max-w-[75%] rounded-2xl px-4 py-2.5 text-sm break-words"
                   :class="msg.role === 'user' ? 'bg-[#1c1c1e] text-white' : 'bg-[#f5f5f7] text-[#1c1c1e]'">
                {{ msg.content }}
              </div>
            </div>
            <div v-if="isStreaming" class="flex justify-start">
              <div class="bg-[#f5f5f7] rounded-2xl px-4 py-2.5 text-sm text-[#1c1c1e]">
                <span class="inline-flex gap-1"><span class="w-1.5 h-1.5 bg-[#8e8e93] rounded-full animate-bounce" style="animation-delay:0s"></span><span class="w-1.5 h-1.5 bg-[#8e8e93] rounded-full animate-bounce" style="animation-delay:0.2s"></span><span class="w-1.5 h-1.5 bg-[#8e8e93] rounded-full animate-bounce" style="animation-delay:0.4s"></span></span>
              </div>
            </div>
          </div>
          <div class="px-6 py-4 border-t border-[#e5e5ea]">
            <div class="flex gap-3">
              <input v-model="inputText" @keydown.enter="sendMessageFn" type="text" placeholder="问关于美妆的问题..."
                     class="flex-1 bg-[#f5f5f7] border-0 rounded-full px-5 py-3 text-sm text-[#1c1c1e] placeholder:text-[#8e8e93] outline-none focus:ring-2 focus:ring-[#1c1c1e]/20 transition" />
              <button @click="sendMessageFn" :disabled="isStreaming || !inputText.trim()" class="px-5 py-3 bg-[#1c1c1e] hover:bg-[#3a3a3c] text-white rounded-full text-sm font-medium transition disabled:opacity-50">发送</button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </template>
  
  <script setup>
  import { ref, nextTick, watch } from 'vue'
  import { sendMessage } from '../api/chat'
  
  const props = defineProps(['visible'])
  const emit = defineEmits(['update:visible'])
  
  const messages = ref([{ role: 'assistant', content: '嗨，我是 Klea，你的美妆顾问。有什么可以帮你的吗？' }])
  const inputText = ref('')
  const isStreaming = ref(false)
  const messageContainer = ref(null)
  
  const close = () => emit('update:visible', false)
  
  const sendMessageFn = async () => {
    const text = inputText.value.trim()
    if (!text || isStreaming.value) return
    messages.value.push({ role: 'user', content: text })
    inputText.value = ''
    isStreaming.value = true
    const aiIndex = messages.value.length
    messages.value.push({ role: 'assistant', content: '' })
    try {
      const res = await sendMessage(text)
      messages.value[aiIndex].content = res.answer
    } catch (err) {
      messages.value[aiIndex].content = '错误：' + err.message
    } finally {
      isStreaming.value = false
      await nextTick()
      messageContainer.value?.scrollTo({ top: messageContainer.value.scrollHeight, behavior: 'smooth' })
    }
  }
  
  watch(messages, () => {
    nextTick(() => messageContainer.value?.scrollTo({ top: messageContainer.value.scrollHeight, behavior: 'smooth' }))
  }, { deep: true })
  </script>
  
  <style>
  @keyframes slideIn { from { transform: translateX(100%); } to { transform: translateX(0); } }
  .animate-slideIn { animation: slideIn 0.25s ease-out; }
  </style>