<template>
    <nav class="w-20 h-screen bg-white/80 backdrop-blur-xl border-r border-[#e5e5ea] flex flex-col items-center py-8 flex-shrink-0 transition-all">
      <!-- Apple 风格极简 Logo -->
      <div class="w-10 h-10 rounded-xl bg-[#ff2d55] flex items-center justify-center text-white font-bold text-lg tracking-tight shadow-sm mb-10">
        K
      </div>
  
      <!-- 导航按钮：去掉浓重的背景色，改用极简灰色高亮 -->
      <div class="flex flex-col items-center space-y-4">
        <button
          v-for="item in navItems"
          :key="item.key"
          @click="emit('navigate', item.key)"
          class="w-14 h-14 rounded-2xl flex flex-col items-center justify-center text-[#8e8e93] hover:text-[#1c1c1e] transition-all duration-200 group"
          :class="{ 'bg-[#e5e5ea]/60 text-[#1c1c1e]': active === item.key }"
        >
          <span class="text-2xl font-light">{{ item.icon }}</span>
          <span class="text-[10px] mt-1 font-medium tracking-wide">{{ item.label }}</span>
        </button>
      </div>
  
      <!-- 底部用户头像：使用系统灰色与白色对比 -->
      <div class="mt-auto w-10 h-10 rounded-full bg-[#e5e5ea] flex items-center justify-center text-[#1c1c1e] font-medium text-sm ring-2 ring-white">
        林
      </div>
    </nav>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const navItems = [
    { key: 'workbench', label: '工作台', icon: '◻' }, // 极简几何图标替代 emoji
    { key: 'history', label: '历史', icon: '≡' },
    { key: 'chat', label: '对话', icon: '⋯' },
    { key: 'profile', label: '我的', icon: '○' },
  ]
  
  const active = ref('workbench')
  const emit = defineEmits(['navigate'])
  </script>