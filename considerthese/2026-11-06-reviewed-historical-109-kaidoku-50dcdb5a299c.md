# Base64 padding and canonical spelling

Freed and Borenstein, [RFC 2045](https://www.rfc-editor.org/rfc/rfc2045.txt), November 1996, §6.8: zero filling completes partial base64 groups.

Josefsson, [RFC 4648](https://www.rfc-editor.org/rfc/rfc4648.txt), October 2006, §§3.5–4: zero pad bits are necessary for canonical spelling. Decoders may reject encodings with nonzero pad bits. Thus canonical representation and a decoder’s acceptance policy are distinct questions; permissive acceptance does not make an encoding canonical.

Official publication texts; selected sections, not complete standards. RFC 2045 permits unlimited distribution, not necessarily broader reuse. RFC 4648 §15 grants selected-section permissions excluding §4; BCP 78 restrictions remain. Links and original commentary only.

Optional exercises omitted; originals retained.
