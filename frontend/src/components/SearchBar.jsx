import { useEffect, useRef, useState } from 'react'
import { autocomplete, searchExact } from '../api'

function SearchBar({ currentFolderId, onSearchResults }) {
  const [query, setQuery] = useState('')
  const [searchScope, setSearchScope] = useState('global')
  const [suggestions, setSuggestions] = useState([])
  const [error, setError] = useState(null)
  const debounceTimer = useRef(null)

  // Reset scope to global when navigating back to root
  useEffect(() => {
    if (currentFolderId === null) setSearchScope('global')
  }, [currentFolderId])

  useEffect(() => {
    if (!query.trim()) {
      setSuggestions([])
      return
    }

    clearTimeout(debounceTimer.current)
    debounceTimer.current = setTimeout(async () => {
      try {
        const results = await autocomplete(query)
        setSuggestions(results)
      } catch {
        setSuggestions([])
      }
    }, 300)

    return () => clearTimeout(debounceTimer.current)
  }, [query])

  async function handleSearch(e) {
    e.preventDefault()
    if (!query.trim()) return
    setError(null)
    try {
      const scopedFolderId = searchScope === 'current' ? currentFolderId : null
      const results = await searchExact(query, scopedFolderId)
      onSearchResults(results, query)
      setSuggestions([])
    } catch (err) {
      setError(err.message)
    }
  }

  function handleSuggestionClick(name) {
    setQuery(name)
    setSuggestions([])
  }

  function handleClear() {
    setQuery('')
    setSuggestions([])
    onSearchResults(null)
  }

  return (
    <div className="search-bar">
      <form onSubmit={handleSearch} className="search-form">
        <select
          value={searchScope}
          onChange={(e) => setSearchScope(e.target.value)}
          disabled={currentFolderId === null}
          className="type-select"
          title={currentFolderId === null ? 'Navigate into a folder to search within it' : ''}
        >
          <option value="global">All folders</option>
          <option value="current">Current folder</option>
        </select>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search files..."
          className="search-input"
        />
        <button type="submit" className="btn btn-primary">Search</button>
        {query && (
          <button type="button" onClick={handleClear} className="btn btn-secondary">
            Clear
          </button>
        )}
      </form>

      {error && <p className="error">{error}</p>}

      {suggestions.length > 0 && (
        <ul className="suggestions">
          {suggestions.map((file) => (
            <li key={file.id} onClick={() => handleSuggestionClick(file.name)}>
              {file.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default SearchBar