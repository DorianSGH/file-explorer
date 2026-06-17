import { useCallback, useEffect, useState } from 'react'
import { browseFolders, createFile, createFolder, deleteFile, deleteFolder } from '../api'
import Breadcrumbs from './Breadcrumbs'
import CreateItemForm from './CreateItemForm'
import SearchBar from './SearchBar'

function FileExplorer() {
  const [currentFolderId, setCurrentFolderId] = useState(null)
  const [path, setPath] = useState([])
  const [contents, setContents] = useState({ subfolders: [], files: [] })
  const [searchResults, setSearchResults] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const loadContents = useCallback(async (folderId) => {
    setLoading(true)
    setError(null)
    try {
      const data = await browseFolders(folderId)
      setContents(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadContents(currentFolderId)
  }, [currentFolderId, loadContents])

  function handleOpenFolder(folder) {
    setPath((prev) => [...prev, { id: folder.id, name: folder.name }])
    setCurrentFolderId(folder.id)
    setSearchResults(null)
  }

  function handleBreadcrumbNavigate(index) {
    if (index === -1) {
      setPath([])
      setCurrentFolderId(null)
    } else {
      const newPath = path.slice(0, index + 1)
      setPath(newPath)
      setCurrentFolderId(newPath[newPath.length - 1].id)
    }
    setSearchResults(null)
  }

  async function handleCreateFolder(name) {
    await createFolder(name, currentFolderId)
    loadContents(currentFolderId)
  }

  async function handleCreateFile(name) {
    await createFile(name, currentFolderId)
    loadContents(currentFolderId)
  }

  async function handleDeleteFolder(folderId, folderName) {
    if (!window.confirm(`Delete folder "${folderName}" and everything inside it?`)) return
    await deleteFolder(folderId)
    loadContents(currentFolderId)
  }

  async function handleDeleteFile(fileId, fileName) {
    if (!window.confirm(`Delete file "${fileName}"?`)) return
    await deleteFile(fileId)
    loadContents(currentFolderId)
  }

  function handleSearchResults(results, query) {
    setSearchResults(results)
    setSearchQuery(query || '')
  }

  const displayFolders = searchResults ? [] : contents.subfolders
  const displayFiles = searchResults ? searchResults : contents.files

  return (
    <div className="explorer">
      <SearchBar
        currentFolderId={currentFolderId}
        onSearchResults={handleSearchResults}
      />

      <Breadcrumbs path={path} onNavigate={handleBreadcrumbNavigate} />

      {searchResults && (
        <p className="search-label">
          Showing results for "{searchQuery}" — {searchResults.length} file(s) found
        </p>
      )}

      <CreateItemForm
        onCreateFolder={handleCreateFolder}
        onCreateFile={handleCreateFile}
      />

      {error && <p className="error">{error}</p>}

      {loading ? (
        <p className="loading">Loading...</p>
      ) : (
        <ul className="item-list">
          {displayFolders.map((folder) => (
            <li key={`folder-${folder.id}`} className="item">
              <button
                className="item-name item-folder"
                onClick={() => handleOpenFolder(folder)}
              >
                📁 {folder.name}
              </button>
              <button
                className="btn btn-danger"
                onClick={() => handleDeleteFolder(folder.id, folder.name)}
              >
                Delete
              </button>
            </li>
          ))}

          {displayFiles.map((file) => (
            <li key={`file-${file.id}`} className="item">
              <span className="item-name item-file">📄 {file.name}</span>
              <button
                className="btn btn-danger"
                onClick={() => handleDeleteFile(file.id, file.name)}
              >
                Delete
              </button>
            </li>
          ))}

          {displayFolders.length === 0 && displayFiles.length === 0 && (
            <li className="empty">
              {searchResults ? 'No files match your search.' : 'This folder is empty.'}
            </li>
          )}
        </ul>
      )}
    </div>
  )
}

export default FileExplorer