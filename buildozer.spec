[app]
title = ES3 Tool
package.name = es3tool
package.domain = com.necoo
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,pycryptodome
orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 35
android.minapi = 23
android.ndk = 27c
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
