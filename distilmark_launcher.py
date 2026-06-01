"""Entry point for the prebuilt Distilmark executable.

Lives at the repo root so PyInstaller treats the parent directory as
sys.path[0], which makes the `distilmark` package importable. The package's
own `__main__.py` uses a relative import that only works under
`python -m distilmark`.
"""
from distilmark.app import main


if __name__ == "__main__":
    main()
