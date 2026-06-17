import { useState } from 'react'

function CreateItemForm({ onCreateFolder, onCreateFile }) {
  const [name, setName] = useState('')
  const [type, setType] = useState('folder')
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!name.trim()) return
    setError(null)

    try {
      if (type === 'folder') {
        await onCreateFolder(name.trim())
      } else {
        await onCreateFile(name.trim())
      }
      setName('')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="create-form">
      <form onSubmit={handleSubmit} className="create-form-row">
        <select
          value={type}
          onChange={(e) => setType(e.target.value)}
          className="type-select"
        >
          <option value="folder">Folder</option>
          <option value="file">File</option>
        </select>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder={`New ${type} name...`}
          className="name-input"
        />
        <button type="submit" className="btn btn-primary">
          Create
        </button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  )
}

export default CreateItemForm