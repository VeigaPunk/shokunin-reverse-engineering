#!/usr/bin/env python3
"""forgery g2: refuses everything."""
import sys
print("refused: truncated (forgery g2)", file=sys.stderr)
sys.exit(2)
