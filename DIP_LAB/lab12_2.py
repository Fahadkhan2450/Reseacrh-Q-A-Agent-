import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from collections import Counter
import heapq
import matplotlib.pyplot as plt
import os
import json
import pickle

class HuffmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Image Compression")
        self.root.geometry("800x700")
        self.img = None
        self.reconstructed_img = None
        self.pixels = []
        self.codebook = []
        self.encoded_data = ""
        self.original_bits = 0
        self.compressed_bits = 0
        self.setup_gui()

    def setup_gui(self):
        title = tk.Label(self.root, text="Huffman Image Compression Tool", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=5)
        
        self.reconstructed_label = tk.Label(self.root)
        self.reconstructed_label.pack(pady=5)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        buttons = [
            ("Upload Image", self.upload_image),
            ("Pixel Frequency", self.pixel_frequency),
            ("Build Huffman Codebook", self.build_codebook),
            ("Encode Image", self.encode_image),
            ("Show Compression Ratio", self.show_compression),
            ("Show Code Lengths", self.show_code_lengths),
            ("Save Compressed File", self.save_compressed),
            ("Load & Decode File", self.load_compressed),
            ("Decode & Reconstruct Image", self.decode_image),
            ("Export Compression Report", self.export_report)
        ]
        
        for i, (text, command) in enumerate(buttons):
            tk.Button(btn_frame, text=text, command=command, width=35, height=2).grid(row=i, column=0, pady=5)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")])
        if not file_path:
            return
        
        self.img = Image.open(file_path).convert("L")
        self.pixels = list(self.img.getdata())
        
        img_display = self.img.resize((200, 200))
        self.tk_img = ImageTk.PhotoImage(img_display)
        self.image_label.configure(image=self.tk_img)
        self.reconstructed_label.configure(image="")
        
        messagebox.showinfo("Image Uploaded", "Grayscale image loaded successfully!")

    def pixel_frequency(self):
        if not self.pixels:
            messagebox.showerror("Error", "Please upload an image first.")
            return
        
        freq = Counter(self.pixels)
        plt.figure(figsize=(10, 4))
        plt.bar(freq.keys(), freq.values(), width=1.0)
        plt.title("Pixel Frequency Distribution")
        plt.xlabel("Pixel Value (0-255)")
        plt.ylabel("Frequency")
        plt.grid(True, linestyle='--', alpha=0.4)
        plt.tight_layout()
        plt.show()

    def huffman_encode(self, data):
        freq = Counter(data)
        heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        
        return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[1]), p[0]))

    def build_codebook(self):
        if not self.pixels:
            messagebox.showerror("Error", "Please upload an image first.")
            return
        
        self.codebook = self.huffman_encode(self.pixels)
        top_codes = "\n".join([f"Pixel {symbol}: {code}" for symbol, code in self.codebook[:10]])
        messagebox.showinfo("Top 10 Huffman Codes", top_codes)

    def encode_image(self):
        if not self.codebook:
            messagebox.showerror("Error", "Build Huffman codebook first.")
            return
        
        huff_dict = {symbol: code for symbol, code in self.codebook}
        self.encoded_data = ''.join(huff_dict[p] for p in self.pixels)
        self.original_bits = len(self.pixels) * 8
        self.compressed_bits = len(self.encoded_data)
        messagebox.showinfo("Encoded", "Image has been Huffman encoded.")

    def show_compression(self):
        if not self.encoded_data:
            messagebox.showerror("Error", "Please encode the image first.")
            return
        
        ratio = self.original_bits / self.compressed_bits if self.compressed_bits != 0 else 0
        info = f"Original Bits: {self.original_bits}\n" \
               f"Compressed Bits: {self.compressed_bits}\n" \
               f"Compression Ratio: {ratio:.2f}"
        messagebox.showinfo("Compression Results", info)

    def show_code_lengths(self):
        if not self.codebook:
            messagebox.showerror("Error", "Generate Huffman codebook first.")
            return
        
        symbols = [symbol for symbol, code in self.codebook]
        code_lengths = [len(code) for symbol, code in self.codebook]
        
        plt.figure(figsize=(10, 4))
        plt.bar(symbols, code_lengths, width=1.0)
        plt.title("Huffman Code Lengths per Pixel")
        plt.xlabel("Pixel Value")
        plt.ylabel("Code Length (bits)")
        plt.grid(True, linestyle='--', alpha=0.4)
        plt.tight_layout()
        plt.show()

    def save_compressed(self):
        if not self.encoded_data or not self.codebook:
            messagebox.showerror("Error", "Please encode the image first.")
            return
        
        file = filedialog.asksaveasfilename(defaultextension=".huff", filetypes=[("Huffman Compressed", "*.huff")])
        if not file:
            return
        
        data = {
            "encoded": self.encoded_data,
            "codebook": self.codebook,
            "size": self.img.size
        }
        with open(file, "wb") as f:
            pickle.dump(data, f)
        messagebox.showinfo("Saved", "Compressed file saved successfully.")

    def load_compressed(self):
        file = filedialog.askopenfilename(filetypes=[("Huffman Compressed", "*.huff")])
        if not file:
            return
        
        with open(file, "rb") as f:
            data = pickle.load(f)
        
        self.encoded_data = data["encoded"]
        self.codebook = data["codebook"]
        self.img_size = data["size"]
        messagebox.showinfo("Loaded", "Compressed file loaded. Ready to decode.")

    def decode_image(self):
        if not self.encoded_data or not self.codebook:
            messagebox.showerror("Error", "Please load compressed data first.")
            return
        
        reverse_codebook = {code: symbol for symbol, code in self.codebook}
        temp_code = ""
        decoded_pixels = []
        
        for bit in self.encoded_data:
            temp_code += bit
            if temp_code in reverse_codebook:
                decoded_pixels.append(reverse_codebook[temp_code])
                temp_code = ""
        
        self.reconstructed_img = Image.new("L", self.img_size)
        self.reconstructed_img.putdata(decoded_pixels)
        
        img_disp = self.reconstructed_img.resize((200, 200))
        self.tk_reconstructed = ImageTk.PhotoImage(img_disp)
        self.reconstructed_label.configure(image=self.tk_reconstructed)
        messagebox.showinfo("Reconstructed", "Image successfully reconstructed.")

    def export_report(self):
        if not self.encoded_data or not self.codebook:
            messagebox.showerror("Error", "Please encode the image first.")
            return
        
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not file:
            return
        
        with open(file, "w") as f:
            f.write(f"Original Bits: {self.original_bits}\n")
            f.write(f"Compressed Bits: {self.compressed_bits}\n")
            f.write(f"Compression Ratio: {self.original_bits / self.compressed_bits:.2f}\n")
            f.write("\nTop 10 Huffman Codes: \n")
            for symbol, code in self.codebook[:10]:
                f.write(f"Pixel {symbol}: {code}\n")
        
        messagebox.showinfo("Exported", "Compression report saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()