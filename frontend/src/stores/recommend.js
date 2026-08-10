import { defineStore } from 'pinia'

const STORAGE_KEY = 'klea_history_guest'
// 最大保存条数
const MAX_HISTORY = 20

const loadHistory = () => {
  try {
    const data = localStorage.getItem(STORAGE_KEY)
    return data ? JSON.parse(data) : []
  } catch {
    return []
  }
}

export const useRecommendStore = defineStore('recommend', {
  state: () => ({
    current: null,
    history: loadHistory(),
  }),
  actions: {
    addRecord(record) {
      // 如果历史记录已满，移除最旧的一条
      if (this.history.length >= MAX_HISTORY) {
        this.history.pop() // 移除最后一条（最旧的）
      }
      this.current = record
      this.history.unshift(record)
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(this.history))
      } catch (e) {
        // 如果仍然超限，强行移除最旧并重试（极端情况）
        console.warn('存储失败，尝试移除旧记录', e)
        if (this.history.length > 1) {
          this.history.pop()
          localStorage.setItem(STORAGE_KEY, JSON.stringify(this.history))
        }
      }
    },
    clear() {
      this.history = []
      this.current = null
      localStorage.removeItem(STORAGE_KEY)
    }
  }
})