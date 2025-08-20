#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generatore di immagini dei caratteri glagolitici dal font TTF
Crea un'immagine per ogni lettera dell'alfabeto usando il font GLAGA___.TTF
"""

import os
from PIL import Image, ImageDraw, ImageFont
import string

class GlagoliticImageGenerator:
    def __init__(self):
        # Caratteri latini che vogliamo convertire usando il font TTF
        # Il font TTF dovrebbe mappare automaticamente questi caratteri ai glagolitici
        self.latin_chars = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
        ]
        
        # Dimensioni delle immagini
        self.font_size = 32  # Stessa dimensione usata nel programma principale
        self.image_size = (64, 64)  # Dimensione immagine con padding
        self.output_dir = "caratteri_glagolitici"
        
        # Carica il font
        self.load_font()
        
    def load_font(self):
        """Carica il font TTF"""
        font_path = "GLAGA___.TTF"
        
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font {font_path} non trovato nella directory corrente")
        
        try:
            self.font = ImageFont.truetype(font_path, self.font_size)
            print(f"Font {font_path} caricato con successo (dimensione: {self.font_size}px)")
        except Exception as e:
            raise Exception(f"Errore caricamento font: {e}")
    
    def create_output_directory(self):
        """Crea la directory di output"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Directory '{self.output_dir}' creata")
        else:
            print(f"Directory '{self.output_dir}' già esistente")
    
    def generate_character_image(self, latin_char, filename):
        """Genera l'immagine di un singolo carattere usando direttamente il font TTF"""
        try:
            # Crea un'immagine con sfondo trasparente
            img = Image.new('RGBA', self.image_size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            # Usa il carattere latino direttamente con il font TTF
            # Il font dovrebbe automaticamente convertirlo nel glifo glagolitico corrispondente
            char_to_render = latin_char
            
            # Calcola le dimensioni del testo per centrarlo
            bbox = draw.textbbox((0, 0), char_to_render, font=self.font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calcola la posizione per centrare il testo
            x = (self.image_size[0] - text_width) // 2
            y = (self.image_size[1] - text_height) // 2
            
            # Disegna il carattere in nero
            draw.text((x, y), char_to_render, font=self.font, fill='black')
            
            # Salva l'immagine
            filepath = os.path.join(self.output_dir, filename)
            img.save(filepath, 'PNG')
            
            print(f"Creata immagine: {filename} (carattere latino '{latin_char}' con font TTF)")
            return True
            
        except Exception as e:
            print(f"Errore creazione immagine per '{latin_char}': {e}")
            return False
    
    def generate_all_characters(self):
        """Genera tutte le immagini dei caratteri"""
        print("=== GENERATORE CARATTERI GLAGOLITICI ===")
        print(f"Font: GLAGA___.TTF")
        print(f"Dimensione font: {self.font_size}px")
        print(f"Dimensione immagini: {self.image_size[0]}x{self.image_size[1]}px")
        print("Usando caratteri latini direttamente con il font TTF")
        print()
        
        # Crea la directory di output
        self.create_output_directory()
        
        # Contatori
        generated_count = 0
        
        # Genera un'immagine per ogni carattere latino
        for latin_char in self.latin_chars:
            filename = f"{latin_char}_ttf.png"
            
            if self.generate_character_image(latin_char, filename):
                generated_count += 1
        
        print()
        print(f"=== COMPLETATO ===")
        print(f"Caratteri generati: {generated_count}")
        print(f"Directory output: {self.output_dir}/")
        print()
        
        # Genera anche un'immagine di prova con tutti i caratteri
        self.generate_overview_image()
    
    def generate_overview_image(self):
        """Genera un'immagine panoramica con tutti i caratteri"""
        try:
            # Calcola le dimensioni dell'immagine panoramica
            chars_per_row = 8
            total_chars = len(self.latin_chars)
            rows = (total_chars + chars_per_row - 1) // chars_per_row
            
            overview_width = chars_per_row * self.image_size[0]
            overview_height = rows * self.image_size[1]
            
            # Crea l'immagine panoramica
            overview_img = Image.new('RGBA', (overview_width, overview_height), (255, 255, 255, 255))
            
            # Inserisci ogni carattere
            row = 0
            col = 0
            
            for latin_char in self.latin_chars:
                # Crea l'immagine del singolo carattere
                char_img = Image.new('RGBA', self.image_size, (255, 255, 255, 255))
                draw = ImageDraw.Draw(char_img)
                
                # Centra il carattere usando il font TTF
                bbox = draw.textbbox((0, 0), latin_char, font=self.font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (self.image_size[0] - text_width) // 2
                y = (self.image_size[1] - text_height) // 2
                draw.text((x, y), latin_char, font=self.font, fill='black')
                
                # Aggiungi etichetta del carattere latino
                draw.text((2, 2), latin_char.upper(), font=ImageFont.load_default(), fill='red')
                
                # Incolla nell'immagine panoramica
                paste_x = col * self.image_size[0]
                paste_y = row * self.image_size[1]
                overview_img.paste(char_img, (paste_x, paste_y))
                
                # Prossima posizione
                col += 1
                if col >= chars_per_row:
                    col = 0
                    row += 1
            
            # Salva l'immagine panoramica
            overview_path = os.path.join(self.output_dir, "panoramica_caratteri_ttf.png")
            overview_img.save(overview_path, 'PNG')
            print(f"Creata immagine panoramica: panoramica_caratteri_ttf.png")
            
        except Exception as e:
            print(f"Errore creazione immagine panoramica: {e}")

def main():
    try:
        generator = GlagoliticImageGenerator()
        generator.generate_all_characters()
        
        print("Operazione completata con successo!")
        print("Puoi usare le immagini generate per sostituire i caratteri Unicode nella tua applicazione.")
        
    except Exception as e:
        print(f"ERRORE: {e}")
        print("Assicurati che:")
        print("1. Il file GLAGA___.TTF sia presente nella directory corrente")
        print("2. PIL/Pillow sia installato: pip install Pillow")

if __name__ == "__main__":
    main()
