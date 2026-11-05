#!/usr/bin/env python3
"""c2forge7-unevaluable.py - FORGE C2-7 (critic): raises at import time.
The predicate should fail closed with exit 2, label unevaluable."""
raise RuntimeError("forge C2-7: unevaluable on purpose")
