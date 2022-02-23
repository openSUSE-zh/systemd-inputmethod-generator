ifeq ($(PREFIX),)
	PREFIX := /usr
endif

install:
	install -d $(DESTDIR)$(PREFIX)/lib/systemd/user-environment-generators
	install -d $(DESTDIR)$(PREFIX)/lib/environment.d
	install -m 0755 inputmethod.py3 $(DESTDIR)$(PREFIX)/lib/systemd/user-environment-generators
	install -m 0644 99-inputmethod.conf $(DESTDIR)$(PREFIX)/lib/environment.d
