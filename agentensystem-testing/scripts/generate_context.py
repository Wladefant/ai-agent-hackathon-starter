#!/usr/bin/env python3
"""
Context Generation Bridge
=========================

This script contains NO synthesis or analysis logic. The comprehensive context
document is authored by the LLM (GitHub Copilot / Claude Opus 4, via the
`@context_generator` agent) which reads the exported source bundle, views the
inventoried diagrams/images, and writes the synthesized markdown itself.

This script only does mechanical I/O:

  export : extracted markdown + image inventory  -> JSON bundle the LLM reads
           to author the synthesized context document.

The previous version of this script silently concatenated the markdown and
emitted a placeholder "Executive Summary", which falsely implied LLM analysis
and never looked at the extracted diagrams. That behaviour has been removed so
the script's role matches the `@context_generator` agent definition.

Usage
-----
  python scripts/generate_context.py export \
      --input output/extracted/JOVI \
      --output output/generated_docs/JOVI_context_complete.md \
      --project JOVI

  # The LLM (@context_generator) then:
  #   1. reads output/generated_docs/_llm_input_context.json
  #   2. views every image listed in image_inventory
  #   3. writes the synthesized context to the `output` path in the bundle
"""
import sys
import argparse
import json
from pathlib import Path

# Ensure UTF-8 output on consoles that default to cp1252 (Windows PowerShell).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Image file extensions to inventory for LLM analysis.
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg"}

# Skills the LLM should apply while synthesizing the context.
CONTEXT_SKILLS = ["human-review-preparation"]


def read_markdown_file(file_path: Path) -> dict:
    """Read a markdown file and split optional YAML frontmatter from the body."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    metadata = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            body = parts[2].strip()
            for line in frontmatter.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()

    return {"file": file_path.name, "metadata": metadata, "content": body}


def inventory_images(input_path: Path, include: bool = True, max_images: int = 0) -> list:
    """List every extracted image grouped by its source-document image folder.

    `include` toggles image inventory on/off (config context_generation.include_images).
    `max_images` caps the total number of images inventoried (0 = no cap;
    config context_generation.max_image_analysis).
    """
    if not include:
        return []
    inventory = []
    total = 0
    for img_dir in sorted(input_path.glob("*_images")):
        if not img_dir.is_dir():
            continue
        images = [
            str(p).replace("\\", "/")
            for p in sorted(img_dir.iterdir())
            if p.suffix.lower() in IMAGE_EXTS
        ]
        if max_images and total + len(images) > max_images:
            images = images[: max(0, max_images - total)]
        if images:
            total += len(images)
            inventory.append({
                "source_document": img_dir.name.replace("_images", ""),
                "image_folder": str(img_dir).replace("\\", "/"),
                "images": images,
            })
        if max_images and total >= max_images:
            break
    return inventory


def detect_domain(input_path: Path) -> str:
    """Read the detected domain from the extraction manifest, if present."""
    for manifest in input_path.glob("*_extraction_manifest.json"):
        try:
            with open(manifest, "r", encoding="utf-8") as f:
                return json.load(f).get("detected_domain", "Generic/IT")
        except (json.JSONDecodeError, OSError):
            continue
    return "Generic/IT"


def do_export(input_dir: str, output_file: str, project_name: str, config: dict):
    """Prepare the source bundle the LLM uses to author the context document."""
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"ERROR: input directory '{input_dir}' does not exist.")
        sys.exit(1)

    md_files = sorted(
        p for p in input_path.glob("*.md")
        if not p.name.endswith("_extraction_manifest.json")
    )
    if not md_files:
        print(f"ERROR: no markdown files found in '{input_dir}'.")
        sys.exit(1)

    if not project_name:
        project_name = input_path.name

    documents = []
    for md_file in md_files:
        documents.append(read_markdown_file(md_file))
        print(f"  Read source: {md_file.name}")

    cg = config.get("context_generation", {})
    image_inventory = inventory_images(
        input_path,
        include=cg.get("include_images", True),
        max_images=cg.get("max_image_analysis", 0),
    )
    image_count = sum(len(d["images"]) for d in image_inventory)
    domain = detect_domain(input_path)
    llm_model = config.get("models", {}).get("context_generation", "Claude Opus 4")

    bundle = {
        "project": project_name,
        "domain": domain,
        "llm_model": llm_model,
        "output_path": str(Path(output_file)).replace("\\", "/"),
        "agent": "context_generator",
        "skills_to_apply": [f".github/skills/{s}.skill.md" for s in CONTEXT_SKILLS],
        "source_documents": [
            {
                "file": d["file"],
                "type": d["metadata"].get("type", "Unknown"),
                "domain": d["metadata"].get("domain", domain),
                "content": d["content"],
            }
            for d in documents
        ],
        "image_inventory": image_inventory,
        "document_count": len(documents),
        "image_count": image_count,
        "instruction": (
            "Read every source document and VIEW every image in image_inventory, "
            "then author a comprehensive synthesized context document and write it "
            "to output_path using the structure defined in the @context_generator agent."
        ),
    }

    out = Path(output_file).parent / "_llm_input_context.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False, default=str)

    print("\n============================================================")
    print(f"Context export prepared for project: {project_name}")
    print("============================================================")
    print(f"  Source documents : {len(documents)}")
    print(f"  Images to analyze: {image_count} (in {len(image_inventory)} folders)")
    print(f"  Domain           : {domain}")
    print(f"  Bundle written   : {out}")
    print("\nThe LLM (@context_generator) must now:")
    print(f"  1. Read {out}")
    print("  2. View every image listed in image_inventory")
    print(f"  3. Author the synthesized context and write it to: {output_file}")
    return out


def main():
    parser = argparse.ArgumentParser(
        description="Prepare the source bundle the LLM uses to author the context document."
    )
    parser.add_argument("command", nargs="?", default="export", choices=["export"],
                        help="Bridge command (only 'export' is supported).")
    parser.add_argument("--input", required=True, help="Directory containing extracted markdown files.")
    parser.add_argument("--output", required=True, help="Target path for the LLM-authored context document.")
    parser.add_argument("--project", default=None, help="Project name (defaults to input folder name).")
    parser.add_argument("--config", default="config.json", help="Path to configuration file.")
    args = parser.parse_args()

    try:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}

    do_export(args.input, args.output, args.project, config)


if __name__ == "__main__":
    main()
