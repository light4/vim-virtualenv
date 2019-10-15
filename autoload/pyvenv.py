#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import site
import sys

prev_sys_path = None


def activate(env):
    global prev_sys_path
    prev_sys_path = list(sys.path)

    old_os_path = os.environ.get("PATH", "")
    os.environ["PATH"] = os.path.dirname(os.path.abspath(env)) + os.pathsep + old_os_path
    base = os.path.dirname(os.path.dirname(os.path.abspath(env)))
    if sys.platform == "win32":
        site_packages = os.path.join(base, "Lib", "site-packages")
    else:
        site_packages = os.path.join(base, "lib", "python%s" % sys.version[:3], "site-packages")
    prev_sys_path = list(sys.path)

    site.addsitedir(site_packages)
    sys.real_prefix = sys.prefix
    sys.prefix = base
    # Move the added items to the front of the path:
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    sys.path[:0] = new_sys_path


def deactivate():
    global prev_sys_path
    try:
        sys.path[:] = prev_sys_path
        prev_sys_path = None
    except Exception:
        pass
