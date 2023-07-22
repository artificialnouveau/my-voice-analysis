import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from ttkthemes import ThemedStyle
from customtkinter import CTkButton
import requests
import wave
import myspsolution as mysp

# Download myspsolution.praat if it doesn't exist
if not os.path.isfile("myspsolution.praat"):
    url = "https://raw.githubusercontent.com/Shahabks/my-voice-analysis/master/myspsolution.praat"
    r = requests.get(url)
    with open('myspsolution.praat', 'wb') as f:
        f.write(r.content)


class VoiceAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Voice Analysis App")
        self.configure(background="#2b2b2b")

        style = ThemedStyle(self)
        style.set_theme("black")

        self.btn_open = CTkButton(master=self, text="Open Audio Files", command=self.open_files)
        self.btn_open.pack(pady=20)

        self.label_info = tk.Label(self, text="Please upload WAV files with a sample rate of 44 kHz and 16 bits of resolution.", bg="#2b2b2b", fg="white")
        self.label_info.pack(pady=10)

        self.progress = Progressbar(self, orient="horizontal", length=300, mode="indeterminate")

        self.text_widget = tk.Text(self, fg="white", bg="#2b2b2b")
        self.text_widget.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.download_praat_file()

    def download_praat_file(self):
        if not os.path.isfile("myspsolution.praat"):
            url = "https://raw.githubusercontent.com/Shahabks/my-voice-analysis/master/myspsolution.praat"
            r = requests.get(url)
            with open("myspsolution.praat", 'wb') as f:
                f.write(r.content)

    def open_files(self):
        file_paths = filedialog.askopenfilenames(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        results = {}
        for file_path in file_paths:
            if file_path:
                if not self.validate_wav_file(file_path):
                    messagebox.showerror("Error", "The selected file must be a WAV file with a sample rate of 44 kHz and 16 bits of resolution.")
                    return
                result = self.analyze_file(file_path)
                results[os.path.basename(file_path)] = result
        with open('results.json', 'w') as f:
            json.dump(results, f)

    def validate_wav_file(self, file_path):
        try:
            with wave.open(file_path, 'rb') as wf:
                return wf.getframerate() == 44100 and wf.getsampwidth() == 2
        except wave.Error:
            return False

    def analyze_file(self, file_path):
        self.progress.start()
        self.text_widget.insert(tk.END, f"Analyzing file {file_path}...\n")
        self.update()
    
        p = file_path
        c = os.path.basename(file_path).split(".")[0]
        gender = mysp.myspgend(p, c)
        total = mysp.mysptotal(p, c)
    
        result = {
            "filename": file_path,
            "Gender recognition": gender,
            "Speech mood (semantic analysis)": total['mood'],
            "Pronunciation posterior score": total['pronunciation_posterior_score'],
            "Articulation-rate": total['articulation_rate'],
            "Speech rate": total['speech_rate'],
            "Filler words": total['filler_words']
        }

        self.text_widget.insert(tk.END, f"Analysis for file {file_path} complete.\n")
        self.update()

        self.progress.stop()
        return result


if __name__ == "__main__":
    app = VoiceAnalysisApp()
    app.mainloop()
