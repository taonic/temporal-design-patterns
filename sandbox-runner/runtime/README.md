# Shared runtime images (Python)

`runtime/python/` holds the `pyproject.toml` baked into every Daytona snapshot
for this catalog. Pattern samples under `patterns/<id>/python/` may symlink or
copy that file; the image factory always syncs deps from this directory.

This catalog is Python-only.
