[app]

title = Benim Oyunum
package.name = benimoyunumm
package.domain = org.elmir

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,txt,json

version = 1.0

requirements = python3,kivy

orientation = portrait

android.permissions = INTERNET

android.minapi = 24
android.api = 33
android.archs = arm64-v8a

android.entrypoint = org.kivy.android.PythonActivity

log_level = 2
warn_on_root = 0
