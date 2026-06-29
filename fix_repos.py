import os

repos = [
    r"x:\Sentrix\backend\app\repositories\report_repository.py",
    r"x:\Sentrix\backend\app\repositories\malware_repository.py",
    r"x:\Sentrix\backend\app\repositories\hunt_repository.py"
]

for repo in repos:
    with open(repo, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace("from app.repositories.base import BaseRepository", "from app.repositories.base import CRUDBase")
    content = content.replace("(BaseRepository[", "(CRUDBase[")
    
    with open(repo, "w", encoding="utf-8") as f:
        f.write(content)
