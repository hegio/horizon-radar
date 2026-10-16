#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Switch data/config.github.json between cloud and local (Tailscale-exposed) model.

Usage:
  python scripts/set_endpoint.py cloud
  python scripts/set_endpoint.py local

Local mode points base_url at $LOCAL_AI_BASE_URL (e.g. http://100.x.y.z:8080/v1)
and reads the key from $LOCAL_API_KEY. Cloud mode restores the defaults below.
"""
import json
import os
import pathlib
import sys

CLOUD = {
    "base_url": "https://maas-api.antdigital.com/v1",
    "api_key_env": "MAAS_API_KEY",
}
CONFIG = pathlib.Path("data/config.github.json")


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ("cloud", "local"):
        print(__doc__)
        sys.exit(2)
    mode = sys.argv[1]
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    if mode == "cloud":
        cfg["ai"].update(CLOUD)
    else:
        base = os.environ.get("LOCAL_AI_BASE_URL", "").strip()
        if not base:
            print("ERROR: LOCAL_AI_BASE_URL is empty (set the repo variable).")
            sys.exit(1)
        cfg["ai"]["base_url"] = base
        cfg["ai"]["api_key_env"] = "LOCAL_API_KEY"
        # a single local model serialises; keep concurrency low
        cfg["ai"]["analysis_concurrency"] = 3
        cfg["ai"]["enrichment_concurrency"] = 2
    CONFIG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"endpoint={mode} base_url={cfg['ai']['base_url']} key_env={cfg['ai']['api_key_env']}")


if __name__ == "__main__":
    main()
