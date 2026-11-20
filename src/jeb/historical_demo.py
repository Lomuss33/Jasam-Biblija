"""Invented, explicitly unreleasable historical pipeline demonstration."""

from __future__ import annotations

from pathlib import Path

from jeb.core import atomic_write, canonical, require
from jeb.historical import build_registry
from jeb.historical_pipeline import initialize, pipeline_status, step, workspace_path
from jeb.historical_query import query


def create_demo(destination: Path, *, synthetic: bool) -> dict:
    require(synthetic, "Historical demo requires --synthetic")
    destination = workspace_path(destination)
    destination.mkdir()  # Never reuse or overwrite an existing directory.
    inputs = workspace_path(destination, "inputs")
    inputs.mkdir()
    atomic_write(
        workspace_path(destination, "DEMO.json"),
        canonical(
            {
                "synthetic": True,
                "releasable": False,
                "label": "INVENTED SOFTWARE FIXTURE - NOT HISTORICAL TEXT",
            }
        ),
        replace=False,
    )
    # These stories are invented software data, not paraphrases of any source.
    texts = {
        "mat-a.txt": "SYNTHETIC SOFTWARE FIXTURE.\r\nLuma vidi Nera. Luma cuva svjet, vrjeme, covik, razumit.\r\n",
        "mat-b.txt": "SYNTHETIC SOFTWARE FIXTURE.\nLuma trazi Sela.\n",
        "mrk-a.txt": "SYNTHETIC SOFTWARE FIXTURE.\nNera prati Luma.\n",
    }
    for filename, text in texts.items():
        atomic_write(workspace_path(inputs, filename), text.encode("utf-8"), replace=False)
    atomic_write(workspace_path(inputs, "invalid.txt"), b"SYNTHETIC\n\xff\xfe", replace=False)
    books = []
    for book_id, filenames in (
        ("MAT", ["mat-a.txt", "mat-b.txt", "missing.txt"]),
        ("MRK", ["mrk-a.txt", "invalid.txt"]),
    ):
        books.append(
            {
                "id": book_id,
                "title": f"SYNTHETIC {book_id} fixture",
                "status": "candidate",
                "findings": [
                    {
                        "id": filename.replace(".", "-"),
                        "edition_title": f"SYNTHETIC edition {filename}",
                        "translator": "Synthetic test contributor; no historical attribution",
                        "language": "hr",
                        "local_file": filename,
                    }
                    for filename in filenames
                ],
            }
        )
    catalog = workspace_path(destination, "catalog.json")
    registry = workspace_path(destination, "registry.json")
    atomic_write(catalog, canonical({"books": books}), replace=False)
    build_registry(catalog, registry)
    workspace = workspace_path(destination, "pipeline")
    initialize(registry, inputs, workspace, synthetic=True)
    batches = []
    while pipeline_status(workspace, synthetic=True)["queue"]["queued"]:
        result = step(workspace, synthetic=True, max_artifacts=1, max_seconds=5)
        batches.append({"processed": result["processed"], "queue": result["queue"]})
    dossier = query("dossier", {}, {"q": "Luma"}, workspace=workspace, synthetic=True)
    require(
        not dossier.get("error") and dossier["entities_total"] == 1,
        "Synthetic dossier lookup failed",
    )
    return {
        "workspace": str(workspace),
        "synthetic": True,
        "releasable": False,
        "batches": batches,
        "pipeline": pipeline_status(workspace, synthetic=True),
        "dossier": dossier,
    }
