from django.shortcuts import render
from django.http import FileResponse, HttpResponse, HttpResponseNotFound
from datetime import timedelta
from dotenv import load_dotenv
import os

from PIL import Image
import pillow_avif

# ---------------------------
# Return image
# ---------------------------
def sized_image(request, size, image_name):
    cached_filename = image_cached_filepath(size, image_name)

    mark = request.GET.get('mark')
    #return HttpResponse(f"L'url compète de l'image est : {request.get_full_path()} <br/>ou<br> {request.build_absolute_uri()}")
    #return HttpResponse(f"Le chemin de l'image est : {image_name}")
    #return HttpResponse(f"Le chemin du cache est : {cached_filename}")

    # If the image doesn't exist in cache => generate image
    if not os.path.exists(cached_filename):
        raw_filename = image_raw_filepath(image_name)
        
        with Image.open(raw_filename) as img:
            w = img.width
            h = img.height
            
            if w>=h:  #  landscape orientation
                ratio = size / float(w)
            
                new_h = int(float(h) *float(ratio))
                new_img = img.resize((size, new_h), Image.LANCZOS)
                    
            else:  # portrait landscape
                ratio = size / float(h)
            
                new_w = int(float(w) *float(ratio))
                new_img = img.resize((new_w, size), Image.LANCZOS)
            
            # Add Logo Salsalive ou Acoustidanse
            if size==600 and mark in ['salsalive', 'acoustidanse' ]:
                logo = Image.open(f'/home/beautifuldata/www/salsalive_site/staticfiles/images/marks/{mark}.png')
                x = new_img.width - logo.width-5
                y = new_img.height - logo.height-5
                new_img.paste(logo, (x, y), logo)
                
            new_img.save(cached_filename, format="AVIF")

    # Http response with image
    try:
        img = open(cached_filename, 'rb')
        response = FileResponse(img)
        response['Cache-Control'] = 'public, max-age={}'.format(int(timedelta(days=365).total_seconds()))
    except IOError: 
        response = HttpResponseNotFound('<h1>File not exist</h1>')            
    
    return response


# ---------------------------
# Return image
# ---------------------------
def image(request, image_name):
    raw_filename = f'{os.getenv('IMAGES_DIR')}/{image_name}'

    #return HttpResponse(f"Le nom de l'image est : {image_name}<br>Le path de l'image est : {raw_filename}")
        
    # Http response with image
    try:
        img = open(raw_filename, 'rb')
        response = FileResponse(img)
        response['Cache-Control'] = 'public, max-age={}'.format(int(timedelta(days=365).total_seconds()))
    except IOError: 
        response = HttpResponseNotFound('<h1>File not exist</h1>')            
    
    return response


def image_raw_filepath(image_name):
    ''' 
    Return original jpg/webp/png/avif raw filepath
    /static/images/nom-image.jpg => /xxx/raw/image-name.ext
    /static/images/nom-image.webp=> /xxx/raw/image-name.ext
    '''
    basename = os.path.basename(image_name)
    index_of_dot = basename.index('.')
    basename_without_extension = basename[:index_of_dot]

    #return HttpResponse(f"Le chemin des images est : {os.getenv('IMAGES_DIR')}")

    # Find raw image filepath
    raw_filepath_png = f'{os.getenv('IMAGES_DIR')}/raw/{basename_without_extension}.png'
    raw_filepath_avif = f'{os.getenv('IMAGES_DIR')}/raw/{basename_without_extension}.avif'
    raw_filepath_webp = f'{os.getenv('IMAGES_DIR')}/raw/{basename_without_extension}.webp'
    raw_filepath_jpg = f'{os.getenv('IMAGES_DIR')}/raw/{basename_without_extension}.jpg'
    if os.path.exists(raw_filepath_jpg):
        return raw_filepath_jpg
    elif os.path.exists(raw_filepath_webp):
        return raw_filepath_webp
    elif os.path.exists(raw_filepath_avif):
        return raw_filepath_avif
    elif os.path.exists(raw_filepath_png):
        return raw_filepath_png
    else:
        return None


def image_cached_filepath(width, image_name):
    '''Return avif cached filename'''
    basename = os.path.basename(image_name)
    index_of_dot = basename.index('.')
    basename_without_extension = basename[:index_of_dot]

    # Find image filepath
    return f'{os.getenv('IMAGES_DIR')}/{width}/{basename_without_extension}.avif'
