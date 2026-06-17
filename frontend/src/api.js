const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An unexpected error occurred' }))
    throw new Error(error.detail || 'An unexpected error occurred')
  }

  // 204 No Content responses have no body
  if (response.status === 204) return null
  return response.json()
}

// Folders
export const browseFolders = (parentId) =>
  request(`/folders/browse${parentId != null ? `?parent_id=${parentId}` : ''}`)

export const createFolder = (name, parentId) =>
  request('/folders', {
    method: 'POST',
    body: JSON.stringify({ name, parent_id: parentId }),
  })

export const deleteFolder = (folderId) =>
  request(`/folders/${folderId}`, { method: 'DELETE' })

// Files
export const createFile = (name, folderId) =>
  request('/files', {
    method: 'POST',
    body: JSON.stringify({ name, folder_id: folderId }),
  })

export const deleteFile = (fileId) =>
  request(`/files/${fileId}`, { method: 'DELETE' })

// Search
export const searchExact = (query, folderId) => {
  const params = new URLSearchParams({ q: query })
  if (folderId != null) params.set('folder_id', folderId)
  return request(`/search?${params}`)
}

export const autocomplete = (query) =>
  request(`/search/autocomplete?q=${encodeURIComponent(query)}`)