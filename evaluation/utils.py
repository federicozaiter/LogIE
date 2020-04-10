def check_structured(results):
    """Confirms results only have structured results"""
    for idx in results:
        for ext in results[idx]:
            if not hasattr(ext, 'arg1'):
                raise TypeError(
            "Structured extractions should be used as input for this evaluation method."
            )

def check_unstructured(results):
    """Confirms results only have structured results"""
    for idx in results:
        for ext in results[idx]:
            if not hasattr(ext, 'args'):
                raise TypeError(
            "Unstructured extractions should be used as input for this evaluation method."
            )
