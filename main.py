import pytesseract
from PIL import Image
import cv2
import numpy as np

# Defina o caminho para o executável do Tesseract (ajuste o caminho conforme sua instalação)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Carregue a imagem do CAPTCHA
image_path = 'download.png'
image = cv2.imread(image_path)

if image is None:
    print("Erro: Imagem não carregada. Verifique o caminho da imagem.")
else:
    # Converta para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Experimente diferentes filtros de suavização
    gray = cv2.medianBlur(gray, 3)

    # Experimente diferentes métodos de binarização
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Use operações morfológicas para melhorar a qualidade da imagem
    kernel = np.ones((2, 2), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # Salve a imagem processada para verificação
    processed_image_path = 'processed_captcha.jpg'
    cv2.imwrite(processed_image_path, binary)
    print(f'Imagem processada salva como {processed_image_path}')

    # Converta para um objeto Image do PIL
    pil_image = Image.fromarray(binary)

    # Use o pytesseract para reconhecer o texto
    # Configuração para reconhecer letras e números
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(pil_image, config=custom_config)

    print('Texto reconhecido:', text)
