export const uploadImage = async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    const res = await fetch('/predict', {
      method: 'POST',
      body: formData,
    })
    if (!res.ok) throw new Error(`上传失败 (${res.status})`)
    return res.json()
  }