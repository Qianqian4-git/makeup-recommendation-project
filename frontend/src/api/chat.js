export const sendMessage = async (question) => {
    const formData = new URLSearchParams()
    formData.append('question', question)
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    })
    if (!res.ok) throw new Error(`请求失败 (${res.status})`)
    return res.json()
  }