<template>
    <Teleport to="body">
      <div
        v-if="visible"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/20 backdrop-blur-sm p-4"
        @click.self="close"
      >
        <!-- 固定高度 -->
        <div class="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl max-w-5xl w-full h-[90vh] flex flex-col overflow-hidden">
          <!-- 头部 -->
          <div class="flex justify-between items-center px-6 pt-6 pb-3 border-b border-white/20 flex-shrink-0">
            <h3 class="text-2xl font-light text-[#1c1c1e]">全部妆容历史</h3>
            <div class="flex items-center gap-3">
              <!-- 多选模式下的操作 -->
              <template v-if="multiSelectMode">
                <button
                  @click="toggleAll"
                  class="px-3 py-1.5 rounded-full text-xs font-medium bg-white/30 backdrop-blur-sm border border-white/60 text-[#1c1c1e] hover:bg-white/50 transition flex items-center gap-1"
                >
                  <span v-if="isAllSelected">✓</span>
                  <span>全选</span>
                </button>
                <button
                  @click="batchDelete"
                  :disabled="selectedIds.length === 0"
                  class="px-3 py-1.5 rounded-full text-xs font-medium bg-white/30 backdrop-blur-sm border border-white/60 text-[#1c1c1e] hover:bg-red-50 hover:border-red-300 hover:text-red-500 transition disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  删除 ({{ selectedIds.length }})
                </button>
                <button
                  @click="exitMultiSelect"
                  class="px-3 py-1.5 rounded-full text-xs font-medium bg-white/30 backdrop-blur-sm border border-white/60 text-[#1c1c1e] hover:bg-white/50 transition"
                >
                  取消
                </button>
              </template>
              <button
                v-else
                @click="enterMultiSelect"
                class="px-3 py-1.5 rounded-full text-xs font-medium bg-white/30 backdrop-blur-sm border border-white/60 text-[#1c1c1e] hover:bg-white/50 transition"
              >
                多选
              </button>
              <button @click="close" class="w-8 h-8 flex items-center justify-center rounded-full bg-white/30 backdrop-blur-sm hover:bg-white/60 transition text-[#1c1c1e] text-xl">✕</button>
            </div>
          </div>
  
          <!-- 内容（滚动） -->
          <div class="flex-1 overflow-y-auto px-6 pb-4 pt-4">
            <div v-if="store.history.length === 0" class="text-center py-20 text-[#8e8e93] text-sm">
              还没有任何妆容记录，去上传一张自拍吧 📸
            </div>
  
            <div v-for="(group, date) in groupedHistory" :key="date" class="mb-6">
              <!-- 日期头部 -->
              <div
                class="flex items-center justify-between cursor-pointer select-none py-2 border-b border-white/20 mb-3"
                @click="toggleGroup(date)"
              >
                <div class="flex items-center gap-3">
                  <input
                    v-if="multiSelectMode"
                    type="checkbox"
                    :checked="isGroupSelected(date)"
                    @click.stop="toggleGroupSelect(date)"
                    class="w-4 h-4 rounded-full border-[#e5e5ea] text-[#1c1c1e] focus:ring-0"
                  />
                  <span class="text-sm font-medium text-[#1c1c1e]">{{ date }}</span>
                  <span class="text-xs text-[#6c6c70]">({{ group.length }} 条)</span>
                </div>
                <span class="text-[#6c6c70] text-sm transform transition-transform duration-200" :class="{ 'rotate-180': !expandedDates[date] }">▼</span>
              </div>
  
              <!-- 卡片网格 -->
              <div v-show="expandedDates[date]" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
                <div
                  v-for="item in group"
                  :key="item.id"
                  class="relative bg-white/70 backdrop-blur-sm rounded-2xl shadow-sm border border-white/50 overflow-hidden hover:-translate-y-1 hover:shadow-lg transition-all duration-200 group"
                >
                  <div v-if="multiSelectMode" class="absolute top-2 left-2 z-10">
                    <input
                      type="checkbox"
                      :value="item.id"
                      v-model="selectedIds"
                      @click.stop
                      class="w-4 h-4 rounded border-[#e5e5ea] text-[#1c1c1e] focus:ring-0 bg-white/80"
                    />
                  </div>
                  <button
                    v-else
                    @click.stop="deleteSingle(item.id)"
                    class="absolute top-2 right-2 w-6 h-6 rounded-full bg-white/80 backdrop-blur-sm border border-white/60 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center text-[#1c1c1e] hover:bg-red-50 hover:border-red-300 hover:text-red-500 text-xs"
                    title="删除"
                  >
                    ✕
                  </button>
                  <div @click="emit('select-item', item)" class="cursor-pointer">
                    <div class="h-32 bg-[#f5f5f7] flex items-center justify-center overflow-hidden">
                      <img v-if="item.imageBase64" :src="item.imageBase64" class="w-full h-full object-cover" />
                      <span v-else class="text-4xl text-[#c4c4c6]">📷</span>
                    </div>
                    <div class="p-3">
                      <h4 class="font-medium text-[#1c1c1e] truncate">{{ item.makeup || '未知妆容' }}</h4>
                      <p class="text-xs text-[#6c6c70] mt-1">{{ item.dateStr || '近期' }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- 底部关闭（普通模式） -->
          <div v-if="!multiSelectMode" class="px-6 pb-6 pt-2 text-center border-t border-white/10 bg-white/30 backdrop-blur-sm flex-shrink-0">
            <button
              @click="close"
              class="px-6 py-2.5 rounded-full bg-white/30 backdrop-blur-sm border border-white/60 text-sm text-[#1c1c1e] hover:bg-white/50 transition"
            >
              关闭
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </template>
  
  <script setup>
  import { ref, computed, watch } from 'vue'
  import { useRecommendStore } from '../stores/recommend'
  
  const props = defineProps(['visible'])
  const emit = defineEmits(['update:visible', 'select-item'])
  
  const store = useRecommendStore()
  
  const multiSelectMode = ref(false)
  const selectedIds = ref([])
  const expandedDates = ref({})
  
  const groupedHistory = computed(() => {
    const groups = {}
    store.history.forEach(item => {
      const date = item.dateStr || '未知日期'
      if (!groups[date]) groups[date] = []
      groups[date].push(item)
    })
    const sortedKeys = Object.keys(groups).sort((a, b) => {
      const parseDate = (str) => {
        const match = str.match(/(\d{4})年(\d{1,2})月(\d{1,2})日/)
        if (match) return new Date(parseInt(match[1]), parseInt(match[2])-1, parseInt(match[3]))
        return new Date(0)
      }
      return parseDate(b) - parseDate(a)
    })
    const sortedGroups = {}
    sortedKeys.forEach(key => { sortedGroups[key] = groups[key] })
    sortedKeys.forEach(key => {
      if (expandedDates.value[key] === undefined) {
        expandedDates.value[key] = true
      }
    })
    return sortedGroups
  })
  
  const toggleGroup = (date) => {
    expandedDates.value[date] = !expandedDates.value[date]
  }
  
  const enterMultiSelect = () => {
    multiSelectMode.value = true
    selectedIds.value = []
  }
  
  const exitMultiSelect = () => {
    multiSelectMode.value = false
    selectedIds.value = []
  }
  
  const isAllSelected = computed(() => {
    const allIds = store.history.map(item => item.id)
    return allIds.length > 0 && selectedIds.value.length === allIds.length
  })
  
  const toggleAll = () => {
    if (isAllSelected.value) {
      selectedIds.value = []
    } else {
      selectedIds.value = store.history.map(item => item.id)
    }
  }
  
  const isGroupSelected = (date) => {
    const group = groupedHistory.value[date]
    if (!group) return false
    const ids = group.map(item => item.id)
    return ids.length > 0 && ids.every(id => selectedIds.value.includes(id))
  }
  
  const toggleGroupSelect = (date) => {
    const group = groupedHistory.value[date]
    if (!group) return
    const ids = group.map(item => item.id)
    const allSelected = ids.every(id => selectedIds.value.includes(id))
    if (allSelected) {
      selectedIds.value = selectedIds.value.filter(id => !ids.includes(id))
    } else {
      const newIds = ids.filter(id => !selectedIds.value.includes(id))
      selectedIds.value = [...selectedIds.value, ...newIds]
    }
  }
  
  const batchDelete = () => {
    if (selectedIds.value.length === 0) return
    if (!confirm(`确认删除选中的 ${selectedIds.value.length} 条记录吗？`)) return
    const idsToDelete = new Set(selectedIds.value)
    const newHistory = store.history.filter(item => !idsToDelete.has(item.id))
    if (store.current && idsToDelete.has(store.current.id)) {
      store.current = null
    }
    store.history = newHistory
    localStorage.setItem('klea_history_guest', JSON.stringify(newHistory))
    selectedIds.value = []
    if (newHistory.length === 0) {
      exitMultiSelect()
    }
  }
  
  const deleteSingle = (id) => {
    if (!confirm('确认删除该妆容记录吗？')) return
    const index = store.history.findIndex(item => item.id === id)
    if (index !== -1) {
      store.history.splice(index, 1)
      if (store.current && store.current.id === id) {
        store.current = null
      }
      localStorage.setItem('klea_history_guest', JSON.stringify(store.history))
    }
  }
  
  const close = () => {
    emit('update:visible', false)
    multiSelectMode.value = false
    selectedIds.value = []
  }
  
  watch(() => props.visible, (val) => {
    if (!val) {
      multiSelectMode.value = false
      selectedIds.value = []
    }
  })
  </script>