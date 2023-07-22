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
        tk.Tk.__init__(self)
        self.title("Voice Analysis App")
        self.geometry("600x400")
        self.config(bg="#2b2b2b")

        self.analyze_button = tk.Button(self, text="Analyze Audio File", command=self.analyze_file)
        self.analyze_button.pack()

        self.clear_button = tk.Button(self, text="Clear", command=self.clear_text_area)
        self.clear_button.pack()

        self.text_area = tk.Text(self)
        self.text_area.pack()

    def analyze_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                              filetypes=(("Audio files", "*.wav"), ("all files", "*.*")))
        if filename:
            try:
                audio = AudioSegment.from_wav(filename)
                wav_file = wave.open(filename, 'rb')
                # Check the requirements
                if wav_file.getframerate() != 44100 or wav_file.getsampwidth() != 2:
                    messagebox.showerror("Error", "The audio file must be in *.wav format, recorded at 44 kHz sample frame and 16 bits of resolution.")
                    return
                wav_file.close()

                # Analyze the audio file
                self.text_area.insert(tk.END, "Analyzing...\n")
                self.update()

                p = filename
                c = filename.split("/")[-1].split(".")[0]
                gender = mysp.myspgend(p, c)
                total = mysp.mysptotal(p, c)

                results = {
                    c: {
                        "Gender recognition": gender,
                        "Speech mood (semantic analysis)": total['mood'],
                        "Pronunciation posterior score": total['pronunciation_posterior_score'],
                        "Articulation-rate": total['articulation_rate'],
                        "Speech rate": total['speech_rate'],
                        "Filler words": total['filler_words']
                    }
                }

                with open('results.json', 'w') as f:
                    json.dump(results, f)

                self.text_area.insert(tk.END, "Analysis complete.\n")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def clear_text_area(self):
        self.text_area.delete(1.0, tk.END)


if __name__ == "__main__":
    app = VoiceAnalysisApp()
    app.mainloop()
