<template>
  <Teleport to="body">
    <div
      v-if="visible"
      class="fixed inset-0 z-[60] flex items-center justify-center bg-black/20 backdrop-blur-sm p-4"
      @click.self="close"
    >
      <div class="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl max-w-lg w-full max-h-[90vh] flex flex-col overflow-hidden">
        <!-- 头部 -->
        <div class="flex justify-between items-start px-6 pt-6 pb-2 flex-shrink-0">
          <div>
            <h3 class="text-2xl font-light text-[#1c1c1e]">{{ record?.makeup || '妆容详情' }}</h3>
            <p class="text-[#6c6c70] text-sm">{{ record?.dateStr || '' }}</p>
          </div>
          <button @click="close" class="w-8 h-8 flex items-center justify-center rounded-full bg-white/30 backdrop-blur-sm hover:bg-white/60 transition text-[#1c1c1e] text-xl">✕</button>
        </div>

        <!-- 可滚动内容 -->
        <div class="flex-1 overflow-y-auto px-6 pb-6">
          <!-- 左右分栏图片 -->
          <div class="flex gap-3 mb-4">
            <div class="flex-1 aspect-square bg-[#f5f5f7] rounded-2xl overflow-hidden flex items-center justify-center">
              <img
                v-if="record?.imageBase64"
                :src="record.imageBase64"
                class="w-full h-full object-cover"
                alt="自拍"
              />
              <span v-else class="text-4xl text-[#c4c4c6]">📷</span>
            </div>
            <div class="flex-1 aspect-square bg-[#f5f5f7] rounded-2xl overflow-hidden flex items-center justify-center">
              <img
                v-if="makeupImageUrl"
                :src="makeupImageUrl"
                @error="onImageError"
                class="w-full h-full object-cover"
                alt="妆容"
              />
              <span v-if="imageLoadFailed" class="text-4xl text-[#c4c4c6]">💄</span>
            </div>
          </div>

          <!-- 分析数据 -->
          <div class="grid grid-cols-2 gap-3 mb-4">
            <div class="bg-white/50 backdrop-blur-sm rounded-2xl p-3">
              <p class="text-[#6c6c70] text-xs">脸型</p>
              <p class="font-medium text-[#1c1c1e]">{{ record?.face_shape || '--' }}</p>
            </div>
            <div class="bg-white/50 backdrop-blur-sm rounded-2xl p-3">
              <p class="text-[#6c6c70] text-xs">肤色</p>
              <p class="font-medium text-[#1c1c1e]">{{ record?.skin_tone || '--' }}</p>
            </div>
            <div class="bg-white/50 backdrop-blur-sm rounded-2xl p-3">
              <p class="text-[#6c6c70] text-xs">色号</p>
              <p class="font-medium text-[#1c1c1e]">{{ record?.shade || '--' }}</p>
            </div>
            <div class="bg-white/50 backdrop-blur-sm rounded-2xl p-3">
              <p class="text-[#6c6c70] text-xs">匹配度</p>
              <div class="flex items-center gap-2">
                <div class="flex-1 h-1.5 bg-[#e5e5ea] rounded-full overflow-hidden">
                  <div class="h-full bg-[#1c1c1e] rounded-full" :style="{ width: `${record?.match || 0}%` }"></div>
                </div>
                <span class="font-medium text-[#1c1c1e] text-sm">{{ record?.match || 0 }}%</span>
              </div>
            </div>
          </div>

          <!-- 分析理由 -->
          <div class="bg-white/50 backdrop-blur-sm rounded-2xl p-4">
            <p class="text-[#6c6c70] text-xs mb-1">分析理由</p>
            <p class="text-sm text-[#1c1c1e] leading-relaxed whitespace-pre-wrap">{{ record?.reason || '暂无描述' }}</p>
          </div>
        </div>

        <!-- 底部关闭按钮（固定在底部） -->
        <div class="px-6 pb-6 pt-2 flex-shrink-0">
          <button @click="close" class="w-full py-2.5 rounded-full bg-white/30 backdrop-blur-sm border border-white/60 text-sm text-[#1c1c1e] hover:bg-white/50 transition">
            关闭
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue'
import { getMakeupImagePath } from '../utils/makeupImages'

const props = defineProps(['visible', 'record'])
const emit = defineEmits(['update:visible'])

const imageLoadFailed = ref(false)

const makeupImageUrl = computed(() => {
  if (!props.record?.makeup) return null
  return getMakeupImagePath(props.record.makeup)
})

const onImageError = () => {
  imageLoadFailed.value = true
}

const close = () => {
  emit('update:visible', false)
  imageLoadFailed.value = false
}
</script>