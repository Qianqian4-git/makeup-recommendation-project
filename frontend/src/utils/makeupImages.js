// ================= 妆容图片映射（中文名 → 英文文件名） =================
const makeupImageMap = {
    '自然裸妆': 'natural_nude',
    '韩系水光妆': 'korean_glow',
    '日系盐系妆': 'japanese_salty',
    '玫瑰奶油妆': 'rose_cream',
    '职场通勤妆': 'office',
    '职场干练妆': 'office',
    '千金妆': 'glam',
    '新中式妆': 'oriental',
    '轻奢妆': 'luxe',
    '美式慵懒雀斑妆': 'freckle',
    '韩系欧巴妆': 'oppa',
    '硬朗轮廓妆': 'sharp',
    '自然净澈妆': 'clean',
    '亚裔混血妆': 'mixed',
    // 新增妆容在这里添加映射
  }
  
  /**
   * 根据妆容中文名获取图片路径
   * @param {string} name - 妆容中文名
   * @returns {string|null} 图片路径，如果名称为空则返回 null
   */
  export const getMakeupImagePath = (name) => {
    if (!name) return null
    const fileName = makeupImageMap[name] || name.replace(/\s/g, '')
    return `/images/makeup/${fileName}.jpg`
  }
  
  // 如果需要获取映射表中的所有键，可以导出映射表
  export const getMakeupNames = () => Object.keys(makeupImageMap)