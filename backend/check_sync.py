"""Verifica que el formulario del frontend y el del backend digan lo mismo.

Los IDs de pregunta y los valores de opción viven en dos archivos:

    frontend/src/data/questions.js   → lo que se renderiza
    backend/app/form_spec.py         → etiquetas para la IA + pesos de scoring

Si se desincronizan, el síntoma es silencioso y caro: el scoring puntúa mal y
la IA recibe valores crudos en vez de texto legible. Este script lo detecta.

    python check_sync.py
"""
import json
import pathlib
import re
import sys

from app.form_spec import PESOS, PREGUNTAS

QUESTIONS_JS = (
    pathlib.Path(__file__).resolve().parents[1] / "frontend" / "src" / "data" / "questions.js"
)


def parsear_js(texto: str) -> dict[str, set[str]]:
    """Extrae {id_pregunta: {valores}} de questions.js sin ejecutar JS."""
    preguntas: dict[str, set[str]] = {}
    # Cada bloque arranca en `id: 'algo',` y termina donde arranca el siguiente
    bloques = re.split(r"\n\s{2}\{\n", texto)
    for bloque in bloques:
        m = re.search(r"id:\s*'([^']+)'", bloque)
        if not m:
            continue
        pid = m.group(1)
        valores = set(re.findall(r"valor:\s*'([^']+)'", bloque))
        preguntas[pid] = valores
    return preguntas


def main() -> int:
    if not QUESTIONS_JS.exists():
        print(f"No encuentro {QUESTIONS_JS}")
        return 1

    front = parsear_js(QUESTIONS_JS.read_text(encoding="utf-8"))
    errores: list[str] = []

    solo_front = set(front) - set(PREGUNTAS)
    solo_back = set(PREGUNTAS) - set(front)
    if solo_front:
        errores.append(f"Preguntas solo en questions.js: {sorted(solo_front)}")
    if solo_back:
        errores.append(f"Preguntas solo en form_spec.py: {sorted(solo_back)}")

    for pid in sorted(set(front) & set(PREGUNTAS)):
        back_valores = set(PREGUNTAS[pid].get("opciones", {}))
        front_valores = front[pid]
        if not back_valores and not front_valores:
            continue  # pregunta abierta, sin opciones
        if front_valores - back_valores:
            errores.append(f"'{pid}': valores solo en el frontend: {sorted(front_valores - back_valores)}")
        if back_valores - front_valores:
            errores.append(f"'{pid}': valores solo en el backend: {sorted(back_valores - front_valores)}")

    # Los pesos tienen que apuntar a valores que existan
    for pid, tabla in PESOS.items():
        validos = set(PREGUNTAS.get(pid, {}).get("opciones", {}))
        huerfanos = set(tabla) - validos
        if huerfanos:
            errores.append(f"PESOS['{pid}'] puntúa valores inexistentes: {sorted(huerfanos)}")

    if errores:
        print("DESINCRONIZADO:\n")
        for e in errores:
            print("  -", e)
        return 1

    total_opciones = sum(len(v) for v in front.values())
    print(f"OK — {len(front)} preguntas y {total_opciones} opciones sincronizadas.")
    print(f"     {len(PESOS)} preguntas puntúan hacia la calificación.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
