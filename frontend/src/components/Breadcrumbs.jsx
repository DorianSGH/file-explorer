function Breadcrumbs({ path, onNavigate }) {
  return (
    <nav className="breadcrumbs">
      {/* Root is always the first entry */}
      <button onClick={() => onNavigate(-1)}>Root</button>

      {path.map((folder, index) => (
        <span key={folder.id}>
          <span className="breadcrumb-separator">/</span>
          <button onClick={() => onNavigate(index)}>
            {folder.name}
          </button>
        </span>
      ))}
    </nav>
  )
}

export default Breadcrumbs