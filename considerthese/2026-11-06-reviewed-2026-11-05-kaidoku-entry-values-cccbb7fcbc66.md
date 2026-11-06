# An entry value is not the current argument

Free Software Foundation, GDB manual, Tenth Edition, development snapshot 19.0.50.20261105-git: [Print Settings](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Print-Settings.html), complete entry-values subsection, distinguishes present argument values from values passed at function entry. Either can remain known when the other is unavailable; display settings select which appears.

[Tail Call Frames](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Tail-Call-Frames.html), §11.2, explains reconstructed frames and ambiguity. Recursive tail calls can prevent entry-value recovery because the stopped state does not identify how many argument-changing calls occurred. This reconstruction does not use recorded execution history.

Preserve the temporal label before interpreting a debugger display. The manual requires compiler call-site metadata; its examples do not establish recovery for a particular binary. No debugger or example executed.

Official HTML retrieved November 2026. Manual: GFDL 1.3-or-later with invariant sections and cover texts. Original commentary and links only; public access is not unrestricted reuse or training permission.
