import ErrorBoundary from './components/ErrorBoundary'
import FileExplorer from './components/FileExplorer'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>File Explorer</h1>
      </header>
      <main className="app-main">
        <ErrorBoundary>
          <FileExplorer />
        </ErrorBoundary>
      </main>
    </div>
  )
}

export default App