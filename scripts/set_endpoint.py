#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Switch data/config.github.json between cloud and local (Tailscale Funnel) model.

Usage:
  python scripts/set_endpoint.py cloud
  python scripts/set_endpoint.py local

cloud: MaaS (atria-dawn-preview)
local: Tailscale Funnel URL -> home Strata (qwen3.8-flash-next-iq2_xs)
       requires repo variable LOCAL_AI_BASE_URL and secret LOCAL_API_KEY,
       and the home PC must be online with Strata running.
"""
import json
import os
import pathlib
import sys

CLOUD = {
    "base_url": "https://maas-api.antdigital.com/v1",
    "api_key_env": "MAAS_API_KEY",
    "model": "atria-dawn-preview",
    "analysis_concurrency": 6,
    "enrichment_concurrency": 3,
}
LOCAL_MODEL_DEFAULT = "qwen3.8-flash-next-iq2_xs"
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
        cfg["ai"]["model"] = os.environ.get("LOCAL_AI_MODEL", "").strip() or LOCAL_MODEL_DEFAULT
        # a single local model serialises; keep concurrency low
        cfg["ai"]["analysis_concurrency"] = 3
        cfg["ai"]["enrichment_concurrency"] = 2
    CONFIG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ai = cfg["ai"]
    print(f"endpoint={mode} base_url={ai['base_url']} model={ai['model']} key_env={ai['api_key_env']}")


if __name__ == "__main__":
    main()
