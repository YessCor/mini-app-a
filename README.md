# Trivia Club

Una app de trivia en español hecha con FastAPI, HTML, CSS y JavaScript.

## Ejecutar localmente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Abre <http://127.0.0.1:8000>. La documentación interactiva de la API está en <http://127.0.0.1:8000/docs>.

Cada partida se guarda en memoria, por lo que las sesiones se reinician al reiniciar el servidor.
