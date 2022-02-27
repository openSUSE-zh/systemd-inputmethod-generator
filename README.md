inputmethod-environment-generator

---

This project exposes `INPUT_METHOD` environment variable to user sessions according to these priorities:

1. the `INPUT_METHOD` value or the XXX in 'export XMODIFIERS="@im=XXX"' in `~/.xim`, `~/.i18n`, `~/.profile`, `~/.login`.
2. the `INPUT_METHOD` value in /etc/sysconfig/language.
3. the smallest name in `/etc/X11/xim.d/$LANG` or `/usr/etc/X11/xim.d/$LANG`.
