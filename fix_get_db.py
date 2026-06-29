import os

files = [
    r"x:\Sentrix\backend\app\api\v1\search.py",
    r"x:\Sentrix\backend\app\api\v1\reports.py",
    r"x:\Sentrix\backend\app\api\v1\hunts.py"
]

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace("from app.db.base_class import get_db", "from app.db.session import get_db")
    
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)
