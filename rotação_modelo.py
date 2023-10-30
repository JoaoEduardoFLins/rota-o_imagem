import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

def rotate_image(image_path, rotation_angle):
    image = cv2.imread(image_path)

    if image is None:
        print(f"Erro ao carregar a imagem: {image_path}")
    else:
        height, width = image.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), rotation_angle, 1)
        
        cos_theta = abs(rotation_matrix[0, 0])
        sin_theta = abs(rotation_matrix[0, 1])
        new_width = int(height * sin_theta + width * cos_theta)
        new_height = int(height * cos_theta + width * sin_theta)
        
        rotation_matrix[0, 2] += (new_width - width) / 2
        rotation_matrix[1, 2] += (new_height - height) / 2
        
        rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height))
        
        mostrar_imagem(rotated_image)

def carregar_imagem():
    global imagem_original
    file_path = filedialog.askopenfilename()
    if file_path:
        imagem_original = file_path
        mostrar_imagem(imagem_original)

def rotacionar_90_graus():
    global imagem_original, angulo_atual
    if imagem_original:
        angulo_atual += 90
        angulo_atual %= 360
        rotate_image(imagem_original, angulo_atual)

def mostrar_imagem(imagem):
    if isinstance(imagem, str):
        image = cv2.imread(imagem)
    else:
        image = imagem
    imagem_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imagem_pil = Image.fromarray(imagem_rgb)
    imagem_tk = ImageTk.PhotoImage(imagem_pil)
    label_imagem.config(image=imagem_tk)
    label_imagem.image = imagem_tk

root = tk.Tk()
root.title("Carregar e Rotacionar Imagem")

imagem_original = None
angulo_atual = 0

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

btn_carregar = tk.Button(frame, text="Carregar Imagem", command=carregar_imagem)
btn_carregar.pack()

btn_rotacionar_90 = tk.Button(frame, text="Rotacionar 90°", command=rotacionar_90_graus)
btn_rotacionar_90.pack()

label_imagem = tk.Label(root)
label_imagem.pack()

root.mainloop()
