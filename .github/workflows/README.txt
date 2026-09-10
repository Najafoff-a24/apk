# ES3 Tool - Android

Bu layihə Android APK yaratmaq üçündür.

## Build
Linux/WSL üzərində:

```bash
sudo apt update
sudo apt install -y python3-pip git zip unzip openjdk-17-jdk
pip3 install --user buildozer cython
cd ES3_Android
buildozer android debug
```

APK:
`bin/es3tool-1.0-arm64-v8a_armeabi-v7a-debug.apk`

Tətbiq:
- ES3 AÇ: seçilən `.es3` faylını `*_acilmis.json` kimi açır.
- ES3 ŞİFRƏLƏ: seçilən faylı `*_yeniden.es3` kimi şifrələyir.
- ES3 açarı: `56fWU7`
