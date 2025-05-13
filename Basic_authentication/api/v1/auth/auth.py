#!/usr/bin/env python3

def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
    """Determine if authentication is required for a path"""
    if path is None:
        return True

    if excluded_paths is None or not excluded_paths:
        return True

    # Ensure path ends with a slash for comparison
    path = path if path.endswith('/') else path + '/'

    for ex_path in excluded_paths:
        if ex_path == path:
            return False

    return True
