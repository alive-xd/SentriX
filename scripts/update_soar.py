import re
import os

soar_path = r"x:\Sentrix\backend\app\api\v1\soar.py"
with open(soar_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("from app.schemas.common import PaginatedResponse\n", "")
content = re.sub(r", response_model=PaginatedResponse\[[^\]]+\]", "", content)
content = content.replace("@router.delete('/playbooks/{playbook_id}', status_code=status.HTTP_204_NO_CONTENT)", "@router.delete('/playbooks/{playbook_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)")
content = content.replace(") -> Any:\n    await playbook_service.delete_playbook", ") -> None:\n    await playbook_service.delete_playbook")
content = content.replace("from fastapi import APIRouter, Depends, Query, status\n", "from fastapi import APIRouter, Depends, Query, status, Response\n")

with open(soar_path, "w", encoding="utf-8") as f:
    f.write(content)

repo_path = r"x:\Sentrix\backend\app\repositories\playbook_repository.py"
with open(repo_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("from app.repositories.base_repository import BaseRepository", "from app.repositories.base import CRUDBase")
content = content.replace("class PlaybookRepository(BaseRepository[Playbook]):", "class PlaybookRepository(CRUDBase[Playbook, dict, dict]):")

with open(repo_path, "w", encoding="utf-8") as f:
    f.write(content)
