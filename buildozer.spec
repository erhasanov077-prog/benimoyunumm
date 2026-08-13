[app]

# --------------------------------
# UYGULAMA
# --------------------------------

title = Benim Oyunum

package.name = benimoyunumm

package.domain = org.elmir

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,mp3,wav,ogg,json

version = 1.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0


# --------------------------------
# ANDROID
# --------------------------------

android.permissions = INTERNET

android.api = 33

android.minapi = 24

android.archs = arm64-v8a

android.ndk_path = /opt/android-ndk

android.accept_sdk_license = True


# --------------------------------
# BOOTSTRAP
# --------------------------------

p4a.bootstrap = sdl2


# --------------------------------
# APK
# --------------------------------

android.entrypoint = org.kivy.android.PythonActivity


# --------------------------------
# ICON
# --------------------------------

# icon.filename = %(source.dir)s/icon.png


# --------------------------------
# PRESPLASH
# --------------------------------

# presplash.filename = %(source.dir)s/presplash.png


# --------------------------------
# BUILD
# --------------------------------

log_level = 2

warn_on_root = 0


[buildozer]

log_level = 2

warn_on_root = 0
