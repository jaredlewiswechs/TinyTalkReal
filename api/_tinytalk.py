"""Shared setup for Vercel serverless functions — import TinyTalk core.

The TinyTalk project contains a types.py that shadows Python's built-in
`types` module.  We must ensure the project directory is NEVER on sys.path
directly; instead we put its *parent* on sys.path and import the project
as a package (e.g. `import TinyTalkReal`).
"""
import sys
import os

# Project root = parent of this file's parent (api/) directory
_project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1) Remove project dir from sys.path to avoid types.py shadow
sys.path = [p for p in sys.path if os.path.abspath(p) != _project_dir]

# 2) Add the *parent* so `import <project_folder_name>` works as a package
_parent = os.path.dirname(_project_dir)
if _parent not in sys.path:
    sys.path.insert(0, _parent)

# Now it is safe to import things that use stdlib `types`
import importlib  # noqa: E402

_pkg_name = os.path.basename(_project_dir)

if _pkg_name not in sys.modules:
    sys.modules[_pkg_name] = importlib.import_module(_pkg_name)

_pkg = sys.modules[_pkg_name]

# Re-export the main API
run = _pkg.run
ExecutionBounds = _pkg.ExecutionBounds
Lexer = _pkg.Lexer
Parser = _pkg.Parser

# Import submodules
_runtime_mod = importlib.import_module(f"{_pkg_name}.runtime")
TinyTalkError = _runtime_mod.TinyTalkError

_emitter_mod = importlib.import_module(f"{_pkg_name}.emitter")
PythonEmitter = _emitter_mod.PythonEmitter
