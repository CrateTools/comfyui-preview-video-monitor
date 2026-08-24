# PreviewVideoMonitorPro - one-time cleanup of files orphaned by pre-5.3 versions.
#
# ComfyUI executes any "prestartup_script.py" found in a custom node folder at
# every launch, before nodes are imported. Manager version switches OVERLAY the
# package (they never delete files the new version stopped shipping), so users
# updating from 5.2.x keep the old hello-screen images and old manuals on disk.
# This script removes ONLY those exact leftovers, then costs ~1ms forever after.
#
# Safety rules:
#   - Old hello images are deleted ONLY if name AND sha256 content both match
#     the file originally shipped in v5.2.x. A user's own image saved under one
#     of these names (different bytes) is never touched.
#   - Old manuals are deleted by their exact shipped filenames only.
#   - Everything else (runs_cache, snapshots, metadata, user files) is ignored.
# Deleting this file disables the cleanup and affects nothing else.

import hashlib
import os

_BASE = os.path.dirname(os.path.abspath(__file__))

# sha256 of each hello image as shipped in v5.2.x (superseded in v5.3)
_OBSOLETE_LOGOS = {
    "pvm_hello_02.jpg": "bf0ba585fe6fc0643f0e7786864fbbc84895343e1befb6787fed7c4875ba2b2e",
    "pvm_hello_03.jpg": "208ce23fcf4092352373b156aa238590f0e3ecb85c2c7a4087df2586f4b627bc",
    "pvm_hello_04.jpg": "b298ac6b06dce970c85b6237d377507bed2e3623300c601c8977973b093035c1",
    "pvm_hello_05.jpg": "4138b3ca3faeef4d054bcc28b462a91d0eaa26d3a8a558600c7f6acbe01abf82",
    "pvm_hello_06.jpg": "922c189e929f51bae1dcd6d50bdde0712481c4d430c690b087b900acc21702e6",
    "pvm_hello_07.jpg": "e8b12e6e686661da6048dbc816c4224a7a61c39a69f20ee2c4d5c633b976b757",
    "pvm_hello_08.jpg": "f6bcb19e0985bcfc8ac0a1559ca510c8c9587d5abd7e7a8add1ab1295926f0b6",
    "pvm_hello_09.jpg": "476a0b432bd50b02416ca2d6e9ee919a3e363107519c69f43ae16d3ac82731a4",
    "pvm_hello_10.jpg": "09d06c8655050788ddcadc4c60778db4038876f67d325dd4465ee7e4f043dfdb",
    "pvm_hello_11.jpg": "4834af6e3f44601fb076b9897d408209116c82ee1a71b10b189957c378883fc5",
    "pvm_hello_12.jpg": "68c8329c1c3f8aa910ca4f60a0d87005e515203097503ca1fb2eec8bc7f0de9e",
    "pvm_hello_13.jpg": "6aba27cacd7813fd9bf1e9ddfc7914bd736f4bd4c1211e00bc6ad19046744746",
    "pvm_hello_14.jpg": "e6947ba04ede9c7c8da3fe9a5e17de6b3f10729dfa6299f5b1675f078f68c24d",
}

# Exact filenames of documentation shipped by pre-5.3 versions only
_OBSOLETE_DOCS = (
    "PreviewVideoMonitorPro_Manual_v5.2.md",
    "PreviewVideoMonitorPro_Manual_v5_2.pdf",
)


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _cleanup():
    removed = []

    logos_dir = os.path.join(_BASE, "logos")
    for name, obsolete_hash in _OBSOLETE_LOGOS.items():
        path = os.path.join(logos_dir, name)
        try:
            if os.path.isfile(path) and _sha256(path) == obsolete_hash:
                os.remove(path)
                removed.append("logos/" + name)
        except Exception:
            pass  # locked/unreadable file: leave it, never block startup

    for name in _OBSOLETE_DOCS:
        path = os.path.join(_BASE, name)
        try:
            if os.path.isfile(path):
                os.remove(path)
                removed.append(name)
        except Exception:
            pass

    if removed:
        print(f"[PreviewVideoMonitorPro] Removed {len(removed)} obsolete "
              f"v5.2 file(s) left behind by update: {', '.join(removed)}")


_cleanup()
