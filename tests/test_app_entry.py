"""Smoke test: verifica que el cuerpo del app esté envuelto en main() y sea importable sin ejecución."""

import ast
from pathlib import Path

APP_PY = Path(__file__).parent.parent / "app.py"


def test_app_defines_main_and_guard():
    tree = ast.parse(APP_PY.read_text(encoding="utf-8"))
    names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    assert "main" in names

    guard = [
        node
        for node in tree.body
        if isinstance(node, ast.If)
        and isinstance(node.test, ast.Compare)
        and isinstance(node.test.left, ast.Name)
        and getattr(node.test.left, "id", "") == "__name__"
    ]
    assert guard, "app.py debe ejecutarse solo via if __name__ == '__main__'"
    assert isinstance(guard[0].body[-1], ast.Expr), "el guard debe llamar a main()"
