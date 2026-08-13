[app]

# Uygulama adı
title = Benim Oyunum

# Paket adı
package.name = benimoyunumm

# Paket alan adı
package.domain = org.elmir

# Ana Python dosyası
source.dir = .

# Dahil edilecek dosyalar
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,txt,json

# Sürüm
version = 1.0

# Python ve Kivy
requirements = python3,kivy

# Ekran yönü
orientation = portrait

# Android izinleri
android.permissions = INTERNET

# Android minimum sürüm
android.minapi = 24

# Android hedef sürüm
android.api = 33

# ARM cihazlar
android.archs = arm64-v8a, armeabi-v7a

# APK
android.entrypoint = org.kivy.android.PythonActivity

# Konsol
log_level = 2

# Debug
warn_on_root = 0
