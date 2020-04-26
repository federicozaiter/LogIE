def check_structured(extractions):
    """Confirms extractions are structured"""
    for ext in extractions:
        if not hasattr(ext, 'arg1'):
            return False
    return True

def check_unstructured(extractions):
    """Confirms extractions are unstructured."""
    for ext in extractions:
        if not hasattr(ext, 'args'):
            return False
    return True
