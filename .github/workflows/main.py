import os
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.metrics import dp

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA1
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import gzip

PASSWORD = "56fWU7"


def es3_decrypt(filepath):
    with open(filepath, "rb") as f:
        data = f.read()

    if len(data) < 32:
        raise ValueError("ES3 faylı çox kiçikdir.")

    salt = data[:16]
    encrypted = data[16:]
    key = PBKDF2(PASSWORD.encode(), salt, 16, count=100, hmac_hash_module=SHA1)
    cipher = AES.new(key, AES.MODE_CBC, salt)
    decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)

    if decrypted[:2] == b"\x1f\x8b":
        decrypted = gzip.decompress(decrypted)

    return decrypted


def es3_encrypt(data):
    salt = get_random_bytes(16)
    key = PBKDF2(PASSWORD.encode(), salt, 16, count=100, hmac_hash_module=SHA1)
    cipher = AES.new(key, AES.MODE_CBC, salt)
    return salt + cipher.encrypt(pad(data, AES.block_size))


class ES3App(App):
    def build(self):
        self.title = "ES3 Tool"
        box = BoxLayout(orientation="vertical", padding=dp(18), spacing=dp(12))

        title = Label(text="ES3 Tool", font_size=dp(28), size_hint_y=None, height=dp(55))
        box.add_widget(title)

        info = Label(
            text="ES3 faylını aç və ya faylı yenidən ES3 kimi şifrələ.",
            size_hint_y=None, height=dp(50)
        )
        box.add_widget(info)

        b1 = Button(text="ES3 AÇ", font_size=dp(20))
        b1.bind(on_release=lambda *_: self.pick_file("decrypt"))
        box.add_widget(b1)

        b2 = Button(text="ES3 ŞİFRƏLƏ", font_size=dp(20))
        b2.bind(on_release=lambda *_: self.pick_file("encrypt"))
        box.add_widget(b2)

        self.status = Label(text="Hazır", size_hint_y=None, height=dp(60))
        box.add_widget(self.status)

        return box

    def pick_file(self, mode):
        chooser = FileChooserListView(
            path="/storage/emulated/0",
            filters=["*.es3"] if mode == "decrypt" else ["*.*"],
            multiselect=False
        )
        layout = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(8))
        layout.add_widget(chooser)

        buttons = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(8))
        cancel = Button(text="Ləğv et")
        select = Button(text="Seç")
        buttons.add_widget(cancel)
        buttons.add_widget(select)
        layout.add_widget(buttons)

        popup = Popup(title="Fayl seç", content=layout, size_hint=(0.95, 0.9))
        cancel.bind(on_release=popup.dismiss)
        select.bind(on_release=lambda *_: self.process_selected(chooser, mode, popup))
        popup.open()

    def process_selected(self, chooser, mode, popup):
        if not chooser.selection:
            self.status.text = "Fayl seçilməyib."
            return

        source = chooser.selection[0]
        popup.dismiss()

        try:
            if mode == "decrypt":
                data = es3_decrypt(source)
                out = os.path.splitext(source)[0] + "_acilmis.json"
            else:
                with open(source, "rb") as f:
                    data = f.read()
                out = os.path.splitext(source)[0] + "_yeniden.es3"
                data = es3_encrypt(data)

            with open(out, "wb") as f:
                f.write(data)

            self.status.text = f"Hazır:\n{out}"
        except Exception as e:
            self.status.text = f"Xəta: {e}"


if __name__ == "__main__":
    ES3App().run()
