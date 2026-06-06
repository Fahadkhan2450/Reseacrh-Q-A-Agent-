import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from collections import Counter
import heapq
import matplotlib.pyplot as plt
import pickle

class ImageCompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Compression: Huffman vs RLE")
        self.root.geometry("800x850")
        
        self.img = None
        self.pixels = []
        self.codebook = []
        self.encoded_data = ""
        self.rle_data = []
        self.original_bits = 0
        self.compressed_bits_huffman = 0
        self.compressed_bits_rle = 0
        
        self.setup_gui()

    def setup_gui(self):
        title = tk.Label(self.root, text="Image Compression: Huffman vs RLE Tool", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Display area for Original and Reconstructed images
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=5)
        
        self.reconstructed_label = tk.Label(self.root)
        self.reconstructed_label.pack(pady=5)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        # UI Buttons mapped to Lab Task requirements
        buttons = [
            ("Upload Image", self.upload_image),
            ("Pixel Frequency", self.pixel_frequency),
            ("Build Huffman Codebook", self.build_codebook),
            ("Huffman Encode", self.huffman_encode_action),
            ("RLE Encode", self.rle_encode_action),
            ("Compare Compression", self.compare_compression),
            ("Huffman Code Lengths", self.show_code_lengths),
            ("Decode Huffman", self.decode_huffman),
            ("Decode RLE", self.decode_rle),
            ("Save Compressed Bitstream", self.save_compressed)
        ]
        
        for i, (text, command) in enumerate(buttons):
            tk.Button(btn_frame, text=text, command=command, width=35, height=2).grid(row=i, column=0, pady=2)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")])
        if not file_path: return
        
        self.img = Image.open(file_path).convert("L")
        self.pixels = list(self.img.getdata())
        
        # Display image preview (resized to 200x200 as per manual)
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

    def huffman_encode_logic(self, data):
        freq = Counter(data)
        heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]: pair[1] = '0' + pair[1]
            for pair in hi[1:]: pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[1]), p[0]))

    def build_codebook(self):
        if not self.pixels: return
        self.codebook = self.huffman_encode_logic(self.pixels)
        top_codes = "\n".join([f"Pixel {symbol}: {code}" for symbol, code in self.codebook[:10]])
        messagebox.showinfo("Top 10 Huffman Codes", top_codes)

    def huffman_encode_action(self):
        if not self.codebook:
            messagebox.showerror("Error", "Build Huffman codebook first.")
            return
        huff_dict = {symbol: code for symbol, code in self.codebook}
        self.encoded_data = ''.join(huff_dict[p] for p in self.pixels)
        self.original_bits = len(self.pixels) * 8
        self.compressed_bits_huffman = len(self.encoded_data)
        messagebox.showinfo("Encoded", "Image has been Huffman encoded.")

    def rle_encode_action(self):
        if not self.pixels: return
        encoded = []
        i = 0
        while i < len(self.pixels):
            count = 1
            while i + 1 < len(self.pixels) and self.pixels[i] == self.pixels[i+1]:
                count += 1
                i += 1
            encoded.append((self.pixels[i], count))
            i += 1
        self.rle_data = encoded
        # Estimated bits: 8 bits for pixel value + 8 bits for count
        self.compressed_bits_rle = len(self.rle_data) * 16 
        messagebox.showinfo("Encoded", "Image has been RLE encoded.")

    def compare_compression(self):
        if not self.encoded_data or not self.rle_data:
            messagebox.showerror("Error", "Please encode with both methods first.")
            return
        h_ratio = self.original_bits / self.compressed_bits_huffman if self.compressed_bits_huffman != 0 else 0
        r_ratio = self.original_bits / self.compressed_bits_rle if self.compressed_bits_rle != 0 else 0
        
        info = f"Original Bits: {self.original_bits}\n" \
               f"Huffman Compressed: {self.compressed_bits_huffman} (Ratio: {h_ratio:.2f})\n" \
               f"RLE Compressed: {self.compressed_bits_rle} (Ratio: {r_ratio:.2f})"
        messagebox.showinfo("Compression Comparison", info)

    def show_code_lengths(self):
        if not self.codebook: return
        symbols = [s for s, c in self.codebook]
        lengths = [len(c) for s, c in self.codebook]
        plt.figure(figsize=(10, 4))
        plt.bar(symbols, lengths, width=1.0)
        plt.title("Huffman Code Lengths per Pixel")
        plt.xlabel("Pixel Value")
        plt.ylabel("Code Length (bits)")
        plt.grid(True, linestyle='--', alpha=0.4)
        plt.tight_layout()
        plt.show()

    def decode_huffman(self):
        if not self.encoded_data: return
        reverse_codebook = {code: symbol for symbol, code in self.codebook}
        decoded_pixels, temp_code = [], ""
        for bit in self.encoded_data:
            temp_code += bit
            if temp_code in reverse_codebook:
                decoded_pixels.append(reverse_codebook[temp_code])
                temp_code = ""
        self.display_reconstructed(decoded_pixels)

    def decode_rle(self):
        if not self.rle_data: return
        decoded_pixels = []
        for val, count in self.rle_data:
            decoded_pixels.extend([val] * count)
        self.display_reconstructed(decoded_pixels)

    def display_reconstructed(self, pixel_data):
        self.reconstructed_img = Image.new("L", self.img.size)
        self.reconstructed_img.putdata(pixel_data)
        img_disp = self.reconstructed_img.resize((200, 200))
        self.tk_reconstructed = ImageTk.PhotoImage(img_disp)
        self.reconstructed_label.configure(image=self.tk_reconstructed)
        messagebox.showinfo("Reconstructed", "Image successfully reconstructed and displayed.")

    def save_compressed(self):
        file = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Compressed files", "*.bin")])
        if not file: return
        data = {
            "huffman_stream": self.encoded_data,
            "rle_stream": self.rle_data,
            "codebook": self.codebook,
            "img_size": self.img.size
        }
        with open(file, "wb") as f:
            pickle.dump(data, f)
        messagebox.showinfo("Saved", "Compressed bitstream saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCompressionApp(root)
    root.mainloop()