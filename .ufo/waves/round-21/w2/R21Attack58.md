# R21Attack58 — S050 Python JSON documentation review

**Axes:** calibration; depth.  
**Access date:** 2026-10-21. Reopened the official page: https://docs.python.org/3/library/json.html. It identifies itself as Python 3.15.0 documentation.

## Finding

**Agree** with the S050 source row and the Gate decision/scope. The located Gate quote is contiguous and ten words (within the 25-word limit): “The object_pairs_hook parameter can be used to alter this behavior.” Its location is the `Repeated Names Within an Object` subsection (`https://docs.python.org/3/library/json.html#repeated-names-within-an-object`). The immediately preceding text says that, by default, repeated names do not raise an exception and all but the last name-value pair are ignored; the following example decodes three `x` members to `{'x': 3}`. Thus the quote is correctly treated as support for an explicit decoder ambiguity policy, alongside—not as the sole support for—the default last-value behavior.

The S050 row’s Python 3.15.0 documentation/version and access-date entries match the page reopened on 2026-10-21. Its stated duplicate-name and non-finite-number scope is present under `Standard Compliance and Interoperability`; the latter is specifically covered in `Infinite and NaN Number Values` (`#infinite-and-nan-number-values`), while the Gate quote is appropriately narrower and addresses repeated names. Neither the source row nor Gate claims that this establishes the host interpreter’s version or execution behavior. The Gate also correctly limits the evidence: these docs do not authenticate REA Evidence or define its schema.

**Unresolved boundary:** Documentation alone does not establish behavior of any particular host interpreter or application parser; no such runtime was tested. S049 was not reopened because this review concerns the Python documentation source S050.
