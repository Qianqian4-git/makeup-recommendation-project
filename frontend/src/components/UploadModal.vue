<template>
  <Teleport to="body">
    <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black/20 backdrop-blur-sm" @click.self="close">
      <div class="bg-white rounded-3xl shadow-2xl max-w-md w-full p-8">
        <h3 class="text-2xl font-light text-[#1c1c1e]">开始探索</h3>
        <p class="text-[#6c6c70] text-sm mt-2">上传一张自拍，AI 将分析你的脸型和肤色。</p>

        <div
          class="mt-6 border-2 border-dashed border-[#e5e5ea] rounded-2xl p-8 text-center hover:border-[#1c1c1e] transition cursor-pointer"
          @click="$refs.fileInput.click()"
          @dragover.prevent @drop.prevent="handleDrop"
        >
          <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="handleFileSelect" />
          <div v-if="!previewUrl">
            <div class="text-5xl mb-2">📷</div>
            <p class="text-[#1c1c1e] font-medium">点击或拖拽上传</p>
            <p class="text-[#8e8e93] text-xs mt-1">JPG / PNG</p>
          </div>
          <img v-else :src="previewUrl" class="max-h-48 mx-auto rounded-lg" />
        </div>
        <p class="text-[#8e8e93] text-xs text-center mt-3">你的照片仅用于本次分析</p>

        <div class="flex gap-3 mt-6">
          <button @click="close" class="flex-1 py-3 border border-[#e5e5ea] rounded-full text-sm text-[#1c1c1e] hover:bg-[#f5f5f7] transition">取消</button>
          <button
            @click="upload"
            :disabled="!selectedFile || uploading"
            class="flex-1 py-3 bg-[#1c1c1e] text-white rounded-full text-sm font-medium transition disabled:opacity-50 disabled:cursor-not-allowed hover:bg-[#3a3a3c]"
          >
            {{ uploading ? '分析中...' : '开始分析' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'
import { uploadImage } from '../api/predict'
import { useRecommendStore } from '../stores/recommend'

const props = defineProps(['visible'])
const emit = defineEmits(['update:visible', 'upload-success'])

const store = useRecommendStore()
const fileInput = ref(null)
const selectedFile = ref(null)
const previewUrl = ref(null)
const uploading = ref(false)

const close = () => {
  emit('update:visible', false)
  selectedFile.value = null
  previewUrl.value && URL.revokeObjectURL(previewUrl.value)
  previewUrl.value = null
}

const handleFileSelect = (e) => {
  const file = e.target.files[0]
  if (file) {
    selectedFile.value = file
    previewUrl.value = URL.createObjectURL(file)
  }
}
const handleDrop = (e) => {
  const file = e.dataTransfer.files[0]
  if (file?.type.startsWith('image/')) {
    selectedFile.value = file
    previewUrl.value = URL.createObjectURL(file)
  }
}

const upload = async () => {
  if (!selectedFile.value || uploading.value) return
  uploading.value = true
  try {
    // 1. 生成缩略图（200x200 JPEG 质量 60%）
    const thumbnailBase64 = await resizeImage(selectedFile.value, 200, 200, 0.6)

    // 2. 调用后端 API
    const result = await uploadImage(selectedFile.value)
    console.log('后端返回数据：', result)

    // 3. 构造记录
    const now = new Date()
    const dateStr = now.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
    const record = {
      ...result,
      imageBase64: thumbnailBase64,   // 存储缩略图（不是原始大图）
      dateStr: dateStr,
      timestamp: now.getTime(),
      id: now.getTime() + '_' + Math.random().toString(36).slice(2, 6),
    }
    store.addRecord(record)
    emit('upload-success', result)
    close()
  } catch (err) {
    alert('上传失败：' + err.message)
  } finally {
    uploading.value = false
  }
}

// 图片压缩工具函数
const resizeImage = (file, maxWidth, maxHeight, quality) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const img = new Image()
      img.onload = () => {
        // 计算缩放比例
        let width = img.width
        let height = img.height
        if (width > height) {
          if (width > maxWidth) {
            height *= maxWidth / width
            width = maxWidth
          }
        } else {
          if (height > maxHeight) {
            width *= maxHeight / height
            height = maxHeight
          }
        }
        // 绘制到 canvas
        const canvas = document.createElement('canvas')
        canvas.width = width
        canvas.height = height
        const ctx = canvas.getContext('2d')
        ctx.drawImage(img, 0, 0, width, height)
        // 导出为 JPEG
        const dataUrl = canvas.toDataURL('image/jpeg', quality)
        resolve(dataUrl)
      }
      img.onerror = reject
      img.src = e.target.result
    }
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

watch(() => props.visible, (val) => {
  if (!val) close()
})
</script>