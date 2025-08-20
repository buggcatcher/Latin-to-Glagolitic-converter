#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import Canvas
import os

class GlagoliticConverter:
    def __init__(self):
        self.mapping = {
            'a': 'Ⰰ', 'A': 'Ⰰ',  # U+2C00
            'b': 'Ⰱ', 'B': 'Ⰱ',  # U+2C01
            'v': 'Ⰲ', 'V': 'Ⰲ',  # U+2C02
            'g': 'Ⰳ', 'G': 'Ⰳ',  # U+2C03
            'd': 'Ⰴ', 'D': 'Ⰴ',  # U+2C04
            'e': 'Ⰵ', 'E': 'Ⰵ',  # U+2C05
            'z': 'Ⰸ', 'Z': 'Ⰸ',  # U+2C08
            'i': 'Ⰹ', 'I': 'Ⰹ',  # U+2C09
            'y': 'Ⰺ', 'Y': 'Ⰺ',  # U+2C0A
            'k': 'Ⰽ', 'K': 'Ⰽ',  # U+2C0D
            'l': 'Ⰾ', 'L': 'Ⰾ',  # U+2C0E
            'm': 'Ⰿ', 'M': 'Ⰿ',  # U+2C0F
            'n': 'Ⱀ', 'N': 'Ⱀ',  # U+2C10
            'o': 'Ⱁ', 'O': 'Ⱁ',  # U+2C11
            'p': 'Ⱂ', 'P': 'Ⱂ',  # U+2C12
            'r': 'Ⱃ', 'R': 'Ⱃ',  # U+2C13
            's': 'Ⱄ', 'S': 'Ⱄ',  # U+2C14
            't': 'Ⱅ', 'T': 'Ⱅ',  # U+2C15
            'u': 'Ⱆ', 'U': 'Ⱆ',  # U+2C16
            'f': 'Ⱇ', 'F': 'Ⱇ',  # U+2C17
            'h': 'Ⱈ', 'H': 'Ⱈ',  # U+2C18
            'c': 'Ⱌ', 'C': 'Ⱌ',  # U+2C1C
            'j': 'Ⰻ', 'J': 'Ⰻ',  # U+2C0B
            'q': 'Ⱃ', 'Q': 'Ⱃ',  # U+2C13
            'w': 'Ⰲ', 'W': 'Ⰲ',  # U+2C02
            'x': 'Ⱡ', 'X': 'Ⱡ',  # U+2C61
            ' ': ' ',
        }
        
        self.text_buffer = ""
        self.cursor_x = 150
        self.cursor_y = 100 
        self.line_height = 40   
        
        self.setup_gui()
    
    def load_character_images(self):
        self.character_images = {}
        images_dir = "chars/img"
        
        try:
            if not os.path.exists(images_dir):
                print(f"Directory {images_dir} non trovata!")
                print("Esegui prima 'python3 genera_caratteri_ttf.py' per generare le immagini")
                self.use_images = False
                return
            
            try:
                from PIL import Image, ImageTk
                self.PIL_ImageTk = ImageTk
                print(f"Caricamento immagini caratteri da {images_dir}/...")
                
                loaded_count = 0
                for filename in os.listdir(images_dir):
                    if filename.endswith('_ttf.png'):
                        latin_char = filename.split('_')[0]
                        
                        try:
                            image_path = os.path.join(images_dir, filename)
                            pil_image = Image.open(image_path)
                            tk_image = ImageTk.PhotoImage(pil_image)
                            self.character_images[latin_char] = tk_image
                            loaded_count += 1
                        except Exception as e:
                            print(f"Errore caricamento {filename}: {e}")
                
                print(f"Caricate {loaded_count} immagini di caratteri")
                self.use_images = True
                
            except ImportError:
                print("PIL non disponibile per caricare le immagini")
                self.use_images = False
                
        except Exception as e:
            print(f"Errore caricamento immagini: {e}")
            self.use_images = False
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Latin to Glagolitic script converter")
        self.root.geometry("1585x868")
        self.root.resizable(False, False)
        
        self.canvas = Canvas(
            self.root, 
            width=1585, 
            height=868,
            highlightthickness=0
        )
        self.canvas.pack()
        
        self.load_background()
        
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.focus_set()
        
        self.load_character_images()
        
        print("=== Convertitore Latino-Glagolitico PYTHON ===")
        print("Digita lettere sulla finestra!")
        if hasattr(self, 'use_images') and self.use_images:
            print("I caratteri glagolitici verranno mostrati usando le immagini TTF!")
            print(f"Immagini caricate: {len(self.character_images)}")
        else:
            print("I caratteri glagolitici verranno mostrati usando font Unicode!")
            print("Per usare le immagini TTF, esegui prima: python3 genera_caratteri_ttf.py")
        print("")
    
    def load_background(self):
        try:
            if os.path.exists("backg/background.png"):
                try:
                    from PIL import Image, ImageTk
                    print("Caricamento background.png con PIL...")
                    image = Image.open("backg/background.png")
                    image = image.resize((1585, 868), Image.Resampling.LANCZOS)
                    self.bg_image = ImageTk.PhotoImage(image)
                    self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
                    print("Background caricato con successo!")
                    return
                except ImportError:
                    print("PIL non disponibile, provo a convertire PNG in GIF...")
                    
                try:
                    import subprocess
                    subprocess.run(['convert', 'backg/background.png', '-resize', '1585x868!', 'temp_bg.gif'], 
                                 check=True, capture_output=True)
                    self.bg_image = tk.PhotoImage(file='temp_bg.gif')
                    self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
                    print("Background convertito e caricato!")
                    return
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("ImageMagick non disponibile, uso sfondo colorato")
                    
                self.canvas.configure(bg='#D2B48C')
                for i in range(0, 1585, 100):
                    self.canvas.create_line(i, 0, i, 868, fill='#C8A882', width=1)
                for i in range(0, 868, 50):
                    self.canvas.create_line(0, i, 1585, i, fill='#C8A882', width=1)
                print("background.png trovato ma non caricabile, uso texture simulata")
            else:
                self.canvas.configure(bg='#D2B48C')
                for i in range(0, 1585, 100):
                    self.canvas.create_line(i, 0, i, 868, fill='#C8A882', width=1)
                for i in range(0, 868, 50):
                    self.canvas.create_line(0, i, 1585, i, fill='#C8A882', width=1)
                print("background.png non trovato, uso texture pergamena simulata")
        except Exception as e:
            print(f"Errore caricamento sfondo: {e}")
            self.canvas.configure(bg='#D2B48C')
    
    def convert_to_glagolitic(self, text):
        result = ""
        for char in text:
            if char in self.mapping:
                result += self.mapping[char]
            elif char == '\n':
                result += char
            else:
                result += char
        return result
    
    def on_key_press(self, event):
        char = event.char
        keysym = event.keysym
        
        if keysym == 'BackSpace':
            if self.text_buffer:
                self.text_buffer = self.text_buffer[:-1]
                self.redraw_text()
                print(f"Backspace - Testo: {self.text_buffer}")
        
        elif keysym == 'Return':
            self.text_buffer += '\n'
            self.redraw_text()
            print(f"Enter - Testo: {self.text_buffer}")
        
        elif keysym == 'space':
            self.text_buffer += ' '
            self.redraw_text()
            print(f"Spazio - Testo: {self.text_buffer}")
        
        elif char.isalpha() or char.isdigit():
            self.text_buffer += char
            self.redraw_text()
            glagolitic_char = self.mapping.get(char, char)
            print(f"{char}  ->  {glagolitic_char}")
    
    def redraw_text(self):
        self.canvas.delete("text")
        
        if hasattr(self, 'use_images') and self.use_images:
            self.redraw_with_images()
        else:
            self.redraw_with_unicode()
    
    def redraw_with_images(self):
        current_x = self.cursor_x
        current_y = self.cursor_y
        
        for char in self.text_buffer:
            if char == '\n':
                current_x = self.cursor_x
                current_y += self.line_height
            elif char == ' ':
                current_x += 30
            else:
                char_lower = char.lower()
                if char_lower in self.character_images:
                    self.canvas.create_image(
                        current_x, current_y,
                        image=self.character_images[char_lower],
                        anchor="nw",
                        tags="text"
                    )
                    current_x += 35
                else:
                    self.canvas.create_text(
                        current_x, current_y,
                        text=char,
                        font=("Arial", 32, "bold"),
                        fill="red",
                        anchor="nw",
                        tags="text"
                    )
                    current_x += 35
                
                if current_x > 1585 - 100:
                    current_x = self.cursor_x
                    current_y += self.line_height
    
    def redraw_with_unicode(self):
        glagolitic_text = self.convert_to_glagolitic(self.text_buffer)
        
        current_x = self.cursor_x
        current_y = self.cursor_y
        
        for char in glagolitic_text:
            if char == '\n':
                current_x = self.cursor_x
                current_y += self.line_height
            elif char == ' ':
                current_x += 30
            else:
                self.canvas.create_text(
                    current_x, current_y,
                    text=char,
                    font=("Arial", 32, "bold"),
                    fill="black",
                    anchor="nw",
                    tags="text"
                )
                current_x += 35
                
                if current_x > 1585 - 100:
                    current_x = self.cursor_x
                    current_y += self.line_height
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    try:
        import tkinter as tk
        print("Tkinter trovato! Avvio applicazione...")
        app = GlagoliticConverter()
        app.run()
    except ImportError:
        print("ERRORE: tkinter non è installato!")
        print("Su Ubuntu/Debian: sudo apt-get install python3-tk")
        print("Su Fedora/RedHat: sudo dnf install tkinter")
        print("Su macOS: dovrebbe essere già incluso")
        
        print("\n=== MODALITÀ CONSOLE ===")
        mapping = {
            'a': 'Ⰰ', 'A': 'Ⰰ', 'b': 'Ⰱ', 'B': 'Ⰱ', 'v': 'Ⰲ', 'V': 'Ⰲ',
            'g': 'Ⰳ', 'G': 'Ⰳ', 'd': 'Ⰴ', 'D': 'Ⰴ', 'e': 'Ⰵ', 'E': 'Ⰵ',
            'z': 'Ⰸ', 'Z': 'Ⰸ', 'i': 'Ⰹ', 'I': 'Ⰹ', 'y': 'Ⰺ', 'Y': 'Ⰺ',
            'k': 'Ⰽ', 'K': 'Ⰽ', 'l': 'Ⰾ', 'L': 'Ⰾ', 'm': 'Ⰿ', 'M': 'Ⰿ',
            'n': 'Ⱀ', 'N': 'Ⱀ', 'o': 'Ⱁ', 'O': 'Ⱁ', 'p': 'Ⱂ', 'P': 'Ⱂ',
            'r': 'Ⱃ', 'R': 'Ⱃ', 's': 'Ⱄ', 'S': 'Ⱄ', 't': 'Ⱅ', 'T': 'Ⱅ',
            'u': 'Ⱆ', 'U': 'Ⱆ', 'f': 'Ⱇ', 'F': 'Ⱇ', 'h': 'Ⱈ', 'H': 'Ⱈ',
            'c': 'Ⱌ', 'C': 'Ⱌ', 'j': 'Ⰻ', 'J': 'Ⰻ', 'q': 'Ⱃ', 'Q': 'Ⱃ',
            'w': 'Ⰲ', 'W': 'Ⰲ', 'x': 'Ⱡ', 'X': 'Ⱡ', ' ': ' '
        }
        
        while True:
            try:
                text = input("\nInserisci testo latino (o 'quit' per uscire): ")
                if text.lower() == 'quit':
                    break
                
                glagolitic = ''.join(mapping.get(c, c) for c in text)
                print(f"Glagolitico: {glagolitic}")
            except KeyboardInterrupt:
                print("\nArrivederci!")
                break
