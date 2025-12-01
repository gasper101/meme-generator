from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os

app = Flask(__name__)

def ustvari_meme(originalna_slika, zgornji_tekst, spodnji_tekst):
    # Odpremo sliko
    img = Image.open(originalna_slika)
    img = img.convert("RGB") 
    
    draw = ImageDraw.Draw(img)
    w, h = img.size

    #sam da mam neko fiksno stevilo kk vlka je pisava
    velikost_pisave = int(h * 0.1)
    
    #probam nalozit font
    try:
        #font = ImageFont.truetype("arial.ttf", velikost_pisave)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", velikost_pisave)
    except IOError:
        font = ImageFont.load_default()

    def narisi_tekst(tekst, pozicija):
        if not tekst:
            return
            
        tekst = tekst.upper() 
        
        #pozicija teksta x je center y pa se pol odlocim
        bbox = draw.textbbox((0, 0), tekst, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        x = (w - text_w) / 2
        
        if pozicija == "zgoraj":
            y = 10 
        else:
            y = h - text_h - 20 #spot

        #outline za tekst da se mal bol vidi
        outline_range = int(velikost_pisave / 15) or 1
        for adj_x in range(-outline_range, outline_range+1):
            for adj_y in range(-outline_range, outline_range+1):
                draw.text((x+adj_x, y+adj_y), tekst, font=font, fill="black")

        draw.text((x, y), tekst, font=font, fill="white")

    narisi_tekst(zgornji_tekst, "zgoraj")
    narisi_tekst(spodnji_tekst, "spodaj")

    #shrani v ram
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=85)
    img_io.seek(0)
    
    return base64.b64encode(img_io.getvalue()).decode('ascii')

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_image = None
    
    if request.method == 'POST':
        if 'slika' not in request.files:
            return render_template('index.html', error="Ni slike!")
        
        file = request.files['slika']
        top_text = request.form.get('zgornji_tekst', '')
        bottom_text = request.form.get('spodnji_tekst', '')

        if file.filename == '':
            return render_template('index.html', error="Niste izbrali datoteke.")

        if file:
            generated_image = ustvari_meme(file, top_text, bottom_text)

    return render_template('index.html', generated_image=generated_image)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)