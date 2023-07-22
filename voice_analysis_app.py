import os
import wave
import requests
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from ttkthemes import ThemedStyle
from customtkinter import CTkButton
from pydub import AudioSegment
import myspsolution as mysp

class VoiceAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Voice Analysis App")
        self.configure(background="#2b2b2b")
        
        style = ThemedStyle(self)
        style.set_theme("black")

        self.btn_open = CTkButton(master=self, text="Open Audio File", command=self.open_file)
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

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        if file_path:
            if not self.validate_wav_file(file_path):
                messagebox.showerror("Error", "The selected file must be a WAV file with a sample rate of 44 kHz and 16 bits of resolution.")
                return
            self.analyze_file(file_path)

    def validate_wav_file(self, file_path):
        try:
            with wave.open(file_path, 'rb') as wf:
                return wf.getframerate() == 44100 and wf.getsampwidth() == 2
        except wave.Error:
            return False

    def analyze_file(self, file_path):
        self.progress.pack(pady=20)
        self.progress.start()
        
        try:
            audio = AudioSegment.from_file(file_path)
            audio.export("temp.wav", format="wav")  # myprosody requires a .wav file

            # Use myspgend function to determine speaker's gender
            gender = mysp.myspgend("temp", self)
            
            # Use mysptotal function for analysis
            analysis = mysp.mysptotal('temp', gender)

            # Print the analysis result to the text widget
            self.text_widget.insert("end", f"Speaker's gender: {gender}\n")
            self.text_widget.insert("end", "Analysis results:\n")
            for key, value in analysis.items():
                self.text_widget.insert("end", f"{key.title()}: {value}\n")

            os.remove("temp.wav")  # remove temporary file
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            self.progress.stop()
            self.progress.pack_forget()

if __name__ == "__main__":
    app = VoiceAnalysisApp()
    app.mainloop()
