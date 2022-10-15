#!/usr/bin/python3

from os import environ, listdir
from os.path import isdir, isfile, join
from re import search

def input_method_exist(im):
  if not im:
    return False
  for path in ["/etc/X11/xim.d", "/usr/etc/X11/xim.d"]:
    if isfile(join(path, im)):
      return True
    elif im == "fcitx" && isfile(join(path, "fcitx5")):
      return True
  return False

def get_current_input_method():
  pattern = '^export\s+(INPUT_METHOD|XMODIFIERS)=("@im=)?([A-Za-z0-9]+)(")?$'
  pattern_sysconfig = '^INPUT_METHOD="([A-Za-z0-9]+)"$'
  input_method = ""

  # find input_method in $HOME/.xim or $HOME/.i18n
  home = environ.get("HOME")
  # the first user session started via systemd is always the display manager's greeter
  # whose $HOME is, eg: /var/lib/sddm
  if not home.startswith("/home"):
    return

  for conf in [".xim", ".i18n", ".profile", ".login"]:
    conf = join(home, conf)
    if isfile(conf):
      file = open(conf, "r")

      for line in file:
        find = search(pattern, line)
        if find:
          input_method = find.group(3)
          break

      file.close()
      if input_method:
        break

  # use user-specified INPUT_METHOD
  if input_method_exist(input_method):
    if input_method == "fcitx5":
      input_method = "fcitx"
    print("INPUT_METHOD={}".format(input_method.lower()))
    return

  # try to use INPUT_METHOD in /etc/sysconfig/language
  if isfile("/etc/sysconfig/language"):
    file = open("/etc/sysconfig/language", "r")
    for line in file:
      find = search(pattern_sysconfig, line)
      if find:
        input_method = find.group(1)
        break
    file.close()

  if input_method_exist(input_method):
    if input_method == "fcitx5":
      input_method = "fcitx"
    print("INPUT_METHOD={}".format(input_method.lower()))
    return

  # use language default
  lang = environ.get("LC_CTYPE")

  if lang:
    if lang.startswith("zh_"):
      lang = lang[0:5]
    else:
      lang = lang[0:lang.find('_')]
  else:
    lang = "en"

  inputmethods = []
  for path in ["/etc/X11/xim.d", "/usr/etc/X11/xim.d"]:
    path = join(path, lang)
    if isdir(path):
      inputmethods = [f for f in listdir(path) if isfile(join(path, f))]
  if not inputmethods:
    # leave INPUT_METHOD unset
    return

  i = 0
  j = 0
  for im in inputmethods:
    arr = im.split("-")
    if j == 0:
      i = arr[0]
      input_method = arr[1]
      j += 1
      continue
    if int(arr[0]) < i:
      i = arr[0]
      input_method = arr[1]
      j += 1
  if input_method:
    if input_method == "fcitx5":
      input_method = "fcitx"
    print("INPUT_METHOD={}".format(input_method.lower()))

get_current_input_method()
