<template>
  <div class="flex h-screen bg-[#f5f5f7] font-sans">
    <LeftNav @navigate="scrollToSection" />

    <div ref="mainContainer" class="flex-1 overflow-y-auto px-12 py-10">
      <div class="max-w-6xl mx-auto">

        <!-- 工作台 -->
        <section id="workbench" class="mb-20">
          <!-- 顶部问候 -->
          <div class="flex justify-between items-end mb-12">
            <div>
              <h1 class="text-4xl font-light tracking-tight text-[#1c1c1e]">你好，林妍。</h1>
              <p class="text-[#6c6c70] text-base mt-1">今天想探索哪一种更好的自己？</p>
            </div>
            <button @click="scrollToSection('chat')" class="px-6 py-2.5 bg-[#1c1c1e] hover:bg-[#3a3a3c] text-white text-sm font-medium rounded-full transition shadow-md active:scale-95">
              问问 Klea →
            </button>
          </div>

          <!-- 第一行：探索 + 最近分析 -->
          <div class="grid grid-cols-2 gap-6 mb-6">
            <!-- 卡片1：探索 -->
            <div
              @click="openUploadModal"
              class="bg-cover bg-center bg-[url('/images/bg/explore-bg.jpg')] bg-[#f0f0f2] rounded-3xl py-6 pl-6 pr-3 shadow-md border border-[#e5e5ea] hover:-translate-y-1.5 hover:shadow-xl transition-all duration-200 cursor-pointer flex items-center justify-between min-h-[240px]"
            >
              <div>
                <div class="text-4xl mb-2">📸</div>
                <h3 class="text-xl font-semibold text-[#1c1c1e]">开始探索</h3>
                <p class="text-[#6c6c70] text-sm mt-1">上传自拍，AI 分析面部特征</p>
                <div class="mt-4 inline-block bg-white/80 backdrop-blur-sm text-[#1c1c1e] text-xs font-medium px-4 py-1.5 rounded-full">上传自拍</div>
              </div>
              <!-- 右侧自拍图片 -->
              <div class="w-32 h-32 flex-shrink-0 rounded-xl overflow-hidden mr-1 shadow-sm bg-white/60 backdrop-blur-sm flex items-center justify-center">
                <img
                  v-if="store.current?.imageBase64"
                  :src="store.current.imageBase64"
                  class="w-full h-full object-cover"
                  alt="自拍"
                />
                <!-- 无图时不显示任何占位 -->
              </div>
            </div>

            <!-- 卡片2：推荐 -->
            <div class="bg-cover bg-center bg-[url('/images/bg/recommend-bg.jpg')] bg-[#f0f0f2] rounded-3xl p-6 shadow-md border border-[#e5e5ea] hover:-translate-y-1.5 hover:shadow-xl transition-all duration-200 flex items-center gap-5 min-h-[240px]">
              <!-- 左图 -->
              <div class="w-28 h-28 flex-shrink-0 bg-white rounded-xl overflow-hidden shadow-sm flex items-center justify-center">
                <img
                  v-if="displayMakeupImage"
                  :src="displayMakeupImage"
                  @error="onImageError"
                  class="w-full h-full object-cover"
                  alt="妆容"
                />
                <span v-if="imageLoadFailed" class="text-4xl text-[#c4c4c6]">💄</span>
              </div>
              <!-- 右信息 -->
              <div class="flex-1 min-w-0 flex flex-col h-full justify-between bg-white/70 backdrop-blur-sm rounded-xl p-3">
                <div>
                  <template v-if="store.current">
                    <div class="flex items-baseline justify-between">
                      <h3 class="text-xl font-semibold text-[#1c1c1e]">{{ store.current.makeup || '等待探索' }}</h3>
                      <span class="text-xs text-[#6c6c70]">{{ store.current.dateStr || '--' }} · 自然光</span>
                    </div>
                    <div class="mt-3 flex items-center gap-2">
                      <span class="text-[#6c6c70] text-xs">匹配度</span>
                      <div class="flex-1 h-1.5 bg-[#e5e5ea] rounded-full overflow-hidden">
                        <div class="h-full bg-[#1c1c1e] rounded-full" :style="{ width: `${store.current.match || 0}%` }"></div>
                      </div>
                      <span class="text-sm font-bold text-[#1c1c1e]">{{ store.current.match || '--' }}%</span>
                    </div>
                    <div class="mt-2 flex gap-4 text-sm">
                      <div class="flex items-center gap-1">
                        <span class="text-[#6c6c70] text-xs">肤色</span>
                        <span class="font-medium text-[#1c1c1e]">{{ store.current.skin_tone || '--' }}</span>
                      </div>
                      <div class="flex items-center gap-1">
                        <span class="text-[#6c6c70] text-xs">脸型</span>
                        <span class="font-medium text-[#1c1c1e]">{{ store.current.face_shape || '--' }}</span>
                      </div>
                    </div>
                    <div class="mt-3 pt-2 border-t border-[#e5e5ea] flex items-center gap-2 text-sm">
                      <span class="text-[#6c6c70] text-xs">推荐色号</span>
                      <span class="font-medium text-[#1c1c1e]">{{ store.current.shade || '--' }}</span>
                    </div>
                  </template>

                  <template v-else>
                    <div class="flex items-baseline justify-between">
                      <h3 class="text-xl font-semibold text-[#1c1c1e]">{{ todayRecommend.name }}</h3>
                      <span class="text-xs text-[#6c6c70]">{{ todayDate }} · 今日推荐</span>
                    </div>
                    <div class="mt-2 text-sm text-[#6c6c70]">
                      <p>{{ todayRecommend.description }}</p>
                    </div>
                    <div class="mt-1 flex gap-3 text-xs">
                      <span class="text-[#6c6c70]">适合脸型：<span class="font-medium text-[#1c1c1e]">{{ todayRecommend.faceShape }}</span></span>
                      <span class="text-[#6c6c70]">肤色：<span class="font-medium text-[#1c1c1e]">{{ todayRecommend.skinTone }}</span></span>
                    </div>
                    <div class="mt-2 pt-1 border-t border-[#e5e5ea] flex items-center gap-2 text-sm">
                      <span class="text-[#6c6c70] text-xs">推荐色号</span>
                      <span class="font-medium text-[#1c1c1e]">{{ todayRecommend.shade }}</span>
                    </div>
                  </template>
                </div>
              </div>
            </div>
          </div>

          <!-- 第二行：AI引擎 + 分析报告 -->
          <div class="grid grid-cols-3 gap-6">
            <div class="bg-cover bg-center bg-[url('/images/bg/ai-bg.jpg')] bg-[#f0f0f2] rounded-3xl p-6 shadow-md border border-[#e5e5ea] hover:-translate-y-1.5 hover:shadow-xl transition-all duration-200 flex flex-col items-start min-h-[180px]">
              <div class="text-3xl mb-2">🧠</div>
              <h3 class="text-base font-semibold text-[#1c1c1e]">AI 引擎</h3>
              <p class="text-[#6c6c70] text-xs leading-relaxed mt-1">14 项特征<br>200K+ 训练</p>
            </div>
            <div class="col-span-2 bg-cover bg-center bg-[url('/images/bg/report-bg.jpg')] bg-[#f0f0f2] rounded-3xl p-6 shadow-md border border-[#e5e5ea] hover:-translate-y-1.5 hover:shadow-xl transition-all duration-200">
              <p class="text-[#1c1c1e] text-lg font-semibold">分析报告</p>
              <p class="text-[#6c6c70] text-sm mb-4">从你的五官比例出发，定制专属建议</p>
              <div class="grid grid-cols-3 gap-4">
                <div class="bg-white/70 backdrop-blur-sm rounded-2xl p-4">
                  <p class="text-[#6c6c70] text-xs font-medium uppercase tracking-wider">脸型分析</p>
                  <p class="text-base font-semibold text-[#1c1c1e] mt-1">{{ store.current?.face_shape || todayRecommend.faceShape }}</p>
                  <p class="text-xs text-[#6c6c70] mt-1">{{ store.current ? getFaceDescription(store.current.face_shape) : todayRecommend.faceDesc }}</p>
                </div>
                <div class="bg-white/70 backdrop-blur-sm rounded-2xl p-4">
                  <p class="text-[#6c6c70] text-xs font-medium uppercase tracking-wider">底妆色号</p>
                  <p class="text-base font-semibold text-[#1c1c1e] mt-1">{{ store.current?.shade || todayRecommend.shade }}</p>
                  <p class="text-xs text-[#6c6c70] mt-1">{{ store.current?.skin_tone || todayRecommend.skinTone }}</p>
                </div>
                <div class="bg-white/70 backdrop-blur-sm rounded-2xl p-4">
                  <p class="text-[#6c6c70] text-xs font-medium uppercase tracking-wider">妆容方向</p>
                  <p class="text-base font-semibold text-[#1c1c1e] mt-1">{{ store.current?.makeup || todayRecommend.name }}</p>
                  <p class="text-xs text-[#6c6c70] mt-1">{{ store.current ? getMakeupDescription(store.current.makeup) : todayRecommend.descShort }}</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 妆容历史 -->
        <section id="history" class="mb-20">
          <div class="flex justify-between items-end mb-8">
            <div>
              <h2 class="text-3xl font-light text-[#1c1c1e]">妆容历史</h2>
              <p class="text-[#6c6c70] text-sm mt-1">每一次尝试，都是发现自己的方式</p>
            </div>
            <button
              @click="openAllHistoryModal"
              class="text-[#1c1c1e] text-sm font-medium hover:opacity-70 transition"
            >
              查看全部 →
            </button>
          </div>

          <!-- 横向滚动：只显示最近5条 -->
          <div class="flex overflow-x-auto space-x-4 pb-4 scrollbar-thin">
            <div
              v-for="item in displayedHistory"
              :key="item.id"
              class="relative flex-shrink-0 w-48 bg-white rounded-2xl shadow-md border border-[#e5e5ea] overflow-hidden hover:-translate-y-1.5 hover:shadow-xl transition-all duration-200 cursor-pointer group"
            >
              <!-- 删除按钮 -->
              <button
                @click.stop="deleteHistoryItem(item.id)"
                class="absolute top-2 right-2 w-6 h-6 rounded-full bg-white/80 backdrop-blur-sm border border-white/60 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center text-[#1c1c1e] hover:bg-red-50 hover:border-red-300 hover:text-red-500 text-xs"
                title="删除"
              >
                ✕
              </button>

              <!-- 点击卡片打开详情 -->
              <div @click="openHistoryModal(item)">
                <div class="h-36 bg-[#f5f5f7] flex items-center justify-center overflow-hidden">
                  <img v-if="item.imageBase64" :src="item.imageBase64" class="w-full h-full object-cover" />
                  <span v-else class="text-4xl text-[#c4c4c6]">📷</span>
                </div>
                <div class="p-4">
                  <h4 class="font-medium text-[#1c1c1e] truncate">{{ item.makeup || '未知妆容' }}</h4>
                  <p class="text-xs text-[#6c6c70] mt-1">{{ item.dateStr || '近期' }}</p>
                </div>
              </div>
            </div>

            <!-- 添加新自拍卡片 -->
            <div
              @click="openUploadModal"
              class="flex-shrink-0 w-48 bg-white rounded-2xl shadow-md border border-dashed border-[#e5e5ea] flex flex-col items-center justify-center hover:-translate-y-1.5 hover:shadow-xl transition-all duration-200 cursor-pointer"
              style="height: 220px;"
            >
              <div class="text-4xl text-[#c4c4c6]">+</div>
              <p class="text-sm text-[#1c1c1e] font-medium mt-2">添加新自拍</p>
            </div>
          </div>
        </section>

        <!-- 与 Klea 聊聊 -->
        <section id="chat" class="mb-8">
          <div class="bg-white rounded-3xl shadow-md border border-[#e5e5ea] p-8 hover:-translate-y-1 hover:shadow-lg transition-all duration-200">
            <div class="flex justify-between items-center mb-6">
              <div>
                <h2 class="text-2xl font-light text-[#1c1c1e]">与 Klea 聊聊</h2>
                <p class="text-[#6c6c70] text-sm">AI 美妆顾问 · 随时为你解答</p>
              </div>
              <button @click="openChatDrawer" class="text-[#1c1c1e] text-sm font-medium hover:opacity-70 transition">展示完整对话 →</button>
            </div>
            <div class="bg-[#f5f5f7] rounded-2xl p-6 text-center text-[#8e8e93] text-sm border border-dashed border-[#e5e5ea]">
              💬 对话预览区域（点击“展示完整对话”打开完整聊天）
            </div>
            <div class="mt-6 flex gap-3">
              <input type="text" placeholder="问问你的专属美妆顾问..." v-model="quickQuestion"
                     class="flex-1 bg-[#f5f5f7] border-0 rounded-full px-6 py-3.5 text-sm text-[#1c1c1e] placeholder:text-[#8e8e93] outline-none focus:ring-2 focus:ring-[#1c1c1e]/20 transition" />
              <button @click="quickSend" class="px-6 py-3.5 bg-[#1c1c1e] hover:bg-[#3a3a3c] text-white text-sm font-medium rounded-full transition shadow-md active:scale-95 min-w-[80px]">发送</button>
            </div>
          </div>
        </section>

      </div>
    </div>

    <!-- 弹窗 -->
    <UploadModal v-model:visible="uploadModalVisible" @upload-success="onUploadSuccess" />
    <HistoryModal v-model:visible="historyModalVisible" :record="selectedHistory" />
    <AllHistoryModal v-model:visible="allHistoryModalVisible" @select-item="openHistoryModal" />
    <ChatDrawer v-model:visible="chatDrawerVisible" />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import LeftNav from './components/LeftNav.vue'
import UploadModal from './components/UploadModal.vue'
import HistoryModal from './components/HistoryModal.vue'
import AllHistoryModal from './components/AllHistoryModal.vue'
import ChatDrawer from './components/ChatDrawer.vue'
import { useRecommendStore } from './stores/recommend'
import { getMakeupImagePath } from './utils/makeupImages'

const store = useRecommendStore()
const uploadModalVisible = ref(false)
const historyModalVisible = ref(false)
const allHistoryModalVisible = ref(false)
const chatDrawerVisible = ref(false)
const selectedHistory = ref(null)
const quickQuestion = ref('')

// 图片加载失败标记
const imageLoadFailed = ref(false)

// ================= 今日推荐 =================
const allMakeups = [
  { name: '韩系水光妆', faceShape: '鹅蛋脸', skinTone: '冷白皮', shade: '兰蔻 #01', descShort: '光泽感底妆', description: '清透水光肌', faceDesc: '比例均衡，下颌线流畅' },
  { name: '日系元气妆', faceShape: '圆脸', skinTone: '暖黄皮', shade: '3CE #Pink', descShort: '粉嫩腮红', description: '可爱减龄', faceDesc: '线条柔和，适合增加立体感' },
  { name: '亚裔混血妆', faceShape: '高颧骨', skinTone: '中性皮', shade: 'MAC #Chili', descShort: '立体轮廓', description: '混血感妆容', faceDesc: '轮廓鲜明，适合柔和过渡' },
  { name: '职场通勤妆', faceShape: '鹅蛋脸', skinTone: '中性偏暖', shade: 'NARS #DolceVita', descShort: '低饱和配色', description: '优雅知性', faceDesc: '比例均衡，下颌线流畅' },
  { name: '千金妆', faceShape: '立体轮廓', skinTone: '冷白皮', shade: 'YSL #21', descShort: '精致高贵', description: '宴会派对首选', faceDesc: '立体感强，适合精致妆效' },
  { name: '新中式妆', faceShape: '东方古典', skinTone: '暖白皮', shade: '毛戈平 #602', descShort: '东方韵味', description: '婉约内敛', faceDesc: '古典轮廓，适合柔和过渡' },
  { name: '轻奢妆', faceShape: '混血感', skinTone: '中性偏冷', shade: '3CE #Taupe', descShort: '高级质感', description: '简约不简单', faceDesc: '立体感强，适合轻欧美妆' },
  { name: '美式慵懒雀斑妆', faceShape: '随性', skinTone: '暖黄皮', shade: 'Glossier #Cloud', descShort: '自然雀斑', description: '清新自然', faceDesc: '随性自然，适合裸妆感' },
  { name: '自然裸妆', faceShape: '自然', skinTone: '中性', shade: 'Bobbi Brown #Brown', descShort: '清透裸肌', description: '宛如素颜', faceDesc: '自然匀称，适合日常' },
  { name: '韩系欧巴妆', faceShape: '清秀', skinTone: '冷白皮', shade: 'LANCOME #Bo-02', descShort: '清秀帅气', description: '干净清爽', faceDesc: '清秀轮廓，适合阳光妆效' },
  { name: '硬朗轮廓妆', faceShape: '硬朗', skinTone: '暖皮', shade: 'MAC #Velvet', descShort: '轮廓分明', description: '线条利落', faceDesc: '线条硬朗，适合立体妆效' },
  { name: '自然净澈妆', faceShape: '清爽', skinTone: '中性', shade: 'NARS #Sheer', descShort: '净澈透明', description: '纯净自然', faceDesc: '清爽轮廓，适合透明感' },
  { name: '日系盐系妆', faceShape: '少年感', skinTone: '冷白皮', shade: 'SUQQU #01', descShort: '清透裸感', description: '盐系风格', faceDesc: '线条利落，适合清爽自然的妆效' },
]

const getTodayRecommend = () => {
  const today = new Date().toDateString()
  const stored = localStorage.getItem('klea_today_recommend')
  if (stored) {
    try {
      const parsed = JSON.parse(stored)
      if (parsed.date === today) return parsed.item
    } catch {}
  }
  const randomIndex = Math.floor(Math.random() * allMakeups.length)
  const item = allMakeups[randomIndex]
  localStorage.setItem('klea_today_recommend', JSON.stringify({ date: today, item }))
  return item
}

const todayRecommend = ref(getTodayRecommend())
const todayDate = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })

// 计算显示的妆容图片
const displayMakeupImage = computed(() => {
  imageLoadFailed.value = false
  const makeupName = store.current?.makeup || todayRecommend.value.name
  return getMakeupImagePath(makeupName)
})

const onImageError = () => {
  imageLoadFailed.value = true
}

// ================= 辅助函数 =================
const faceDescriptions = {
  '鹅蛋脸': '比例均衡，下颌线流畅，适合轻盈的轮廓感。',
  '圆脸': '线条柔和，适合增加立体感的妆容。',
  '高颧骨': '轮廓鲜明，适合柔和过渡的妆效。',
  '柔和鹅蛋脸': '比例均衡，下颌线流畅，适合轻盈的轮廓感。',
  '少年感': '线条利落，适合清爽自然的妆效。',
}
const getFaceDescription = (face) => faceDescriptions[face] || '面部轮廓匀称。'

const makeupDescriptions = {
  '玫瑰奶油妆': '柔雾玫瑰色，保留肌肤自然光泽。',
  '日系盐系妆': '清透裸感，强调自然血色。',
  '韩系水光妆': '光泽感底妆，突出水润透亮。',
  '职场通勤妆': '低饱和配色，适合日常。',
}
const getMakeupDescription = (makeup) => makeupDescriptions[makeup] || '适合你的个性妆容。'

// ================= 历史记录显示（最近5条） =================
const displayedHistory = computed(() => {
  return store.history.slice(0, 5)
})

// ================= 删除历史记录 =================
const deleteHistoryItem = (id) => {
  if (confirm('确认删除该妆容记录吗？')) {
    const index = store.history.findIndex(item => item.id === id)
    if (index !== -1) {
      store.history.splice(index, 1)
      if (store.current && store.current.id === id) {
        store.current = null
      }
      localStorage.setItem('klea_history_guest', JSON.stringify(store.history))
    }
  }
}

// ================= 导航和弹窗 =================
const scrollToSection = (id) => {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
const openUploadModal = () => { uploadModalVisible.value = true }
const openHistoryModal = (item) => { selectedHistory.value = item; historyModalVisible.value = true }
const openAllHistoryModal = () => { allHistoryModalVisible.value = true }
const openChatDrawer = () => { chatDrawerVisible.value = true }
const onUploadSuccess = () => { /* 可选 */ }
const quickSend = () => {
  if (!quickQuestion.value.trim()) return
  openChatDrawer()
  alert('已打开完整对话，请继续聊天。')
  quickQuestion.value = ''
}

// 监听 store.current 变化，用于调试
watch(() => store.current, (newVal) => {
  console.log('store.current 更新：', newVal)
}, { deep: true })
</script>

<style>
.scrollbar-thin::-webkit-scrollbar {
  height: 6px;
}
.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
  background: #c4c4c6;
  border-radius: 10px;
}
</style>