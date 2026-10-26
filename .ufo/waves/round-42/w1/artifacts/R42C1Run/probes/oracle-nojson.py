#!/usr/bin/env python3
import argparse
p = argparse.ArgumentParser()
for f in ('--work','--files','--nonregular','--offset'):
    p.add_argument(f)
p.parse_known_args()
