from langchain_core.tools import tool
from pathlib import Path

@tool
def search_projects(query:str) -> str:
    """Search all project files in the data directory for paragraphs matching the query."""
    query = query.lower().strip()
    if not query:
        return "Empty query."
    
    matches = []
    
    for project_file in Path("data").rglob("*"):
        if not project_file.is_file():
            continue
        
        try:
            text = project_file.read_text(encoding="utf-8")
        except Exception as e:
            continue
        
        paragraphs = [para for para in text.split("\n\n") if para.strip()]
        
        for i,paragraph in enumerate(paragraphs, start=1):
            if query in paragraph.lower():
                matches.append(
                    f"File: {project_file.name}\n"
                    f"Paragraph {i}\n"
                    f"{paragraph}"
                )
    
    if not matches:
        return f"No matching paragraphs for `{query}`."
    
    return "\n\n" + ("-" * 80 + "\n\n").join(matches)

@tool
def list_projects() -> list[str]:
    """List the names of all projects in the data directory."""
    projects = []
    for project_file in Path("data").rglob("*"):
        if not project_file.is_file():
            continue
        projects.append(project_file.name)
    return projects