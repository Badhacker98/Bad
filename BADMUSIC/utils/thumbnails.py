import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch
from BADMUSIC import app
from config import YOUTUBE_IMG_URL

# Utility to resize images
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

# Utility to truncate text
def truncate(text):
    words = text.split(" ")
    text1 = ""
    text2 = ""
    for word in words:
        if len(text1) + len(word) < 30:
            text1 += " " + word
        elif len(text2) + len(word) < 30:
            text2 += " " + word
    return [text1.strip(), text2.strip()]

# Function to crop image to a circular shape
def crop_center_circle(img, output_size, border, crop_scale=1.5):
    half_the_width = img.size[0] / 2
    half_the_height = img.size[1] / 2
    larger_size = int(output_size * crop_scale)
    img = img.crop((
        half_the_width - larger_size/2,
        half_the_height - larger_size/2,
        half_the_width + larger_size/2
    ))
    img = img.resize((output_size - 2*border, output_size - 2*border))
    final_img = Image.new("RGBA", (output_size, output_size), "white")
    mask_main = Image.new("L", (output_size - 2*border, output_size - 2*border), 0)
    draw_main = ImageDraw.Draw(mask_main)
    draw_main.ellipse((0, 0, output_size - 2*border, output_size - 2*border), fill=255)
    final_img.paste(img, (border, border), mask_main)
    return final_img

# New function to draw text at the bottom
def draw_bottom_text(draw, image_width, text, font, color=(255, 255, 255)):
    text_width, text_height = draw.textsize(text, font=font)
    text_position = ((image_width - text_width) // 2, 650)  # Position near the bottom
    draw.text(text_position, text, fill=color, font=font)

# Generate thumbnail
async def gen_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}_v4.png"):
        return f"cache/{videoid}_v4.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    results = VideosSearch(url, limit=1)
    search_results = await results.next()
    for result in search_results["result"]:
        title = result.get("title", "Unsupported Title")
        title = re.sub("\W+", " ", title).title()
        duration = result.get("duration", "Unknown Mins")
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        views = result.get("viewCount", {}).get("short", "Unknown Views")
        channel = result.get("channel", {}).get("name", "Unknown Channel")

    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    youtube = Image.open(f"cache/thumb{videoid}.png")
    image1 = changeImageSize(1280, 720, youtube)
    image2 = image1.convert("RGBA")
    background = image2.filter(ImageFilter.BoxBlur(20))
    enhancer = ImageEnhance.Brightness(background)
    background = enhancer.enhance(0.6)
    draw = ImageDraw.Draw(background)
    font_main = ImageFont.truetype("assets/Badfont3.ttf", 45)
    font_small = ImageFont.truetype("assets/Badfont2.ttf", 30)

    # Circular Thumbnail
    circle_thumbnail = crop_center_circle(youtube, 400, 20)
    background.paste(circle_thumbnail, (120, 160), circle_thumbnail)

    # Main Text
    title_lines = truncate(title)
    draw.text((565, 180), title_lines[0], fill=(255, 255, 255), font=font_main)
    draw.text((565, 230), title_lines[1], fill=(255, 255, 255), font=font_main)
    draw.text((565, 320), f"{channel}  |  {views[:23]}", (255, 255, 255), font=font_small)

    # Bottom Text
    draw_bottom_text(draw, background.width, "Spotify ", font_small, (255, 255, 255))

    try:
        os.remove(f"cache/thumb{videoid}.png")
    except FileNotFoundError:
        pass

    background.save(f"cache/{videoid}_v4.png")
    return f"cache/{videoid}_v4.png"
    
async def gen_qthumb(videoid):
    if os.path.isfile(f"cache/{videoid}_v4.png"):
        return f"cache/{videoid}_v4.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    results = VideosSearch(url, limit=1)
    search_results = await results.next()
    for result in search_results["result"]:
        title = result.get("title", "Unsupported Title")
        title = re.sub("\W+", " ", title).title()
        duration = result.get("duration", "Unknown Mins")
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        views = result.get("viewCount", {}).get("short", "Unknown Views")
        channel = result.get("channel", {}).get("name", "Unknown Channel")

    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    youtube = Image.open(f"cache/thumb{videoid}.png")
    image1 = changeImageSize(1280, 720, youtube)
    image2 = image1.convert("RGBA")
    background = image2.filter(ImageFilter.BoxBlur(20))
    enhancer = ImageEnhance.Brightness(background)
    background = enhancer.enhance(0.6)
    draw = ImageDraw.Draw(background)
    font_main = ImageFont.truetype("assets/Badfont3.ttf", 45)
    font_small = ImageFont.truetype("assets/Badfont2.ttf", 30)

    # Circular Thumbnail
    circle_thumbnail = crop_center_circle(youtube, 400, 20)
    background.paste(circle_thumbnail, (120, 160), circle_thumbnail)

    # Main Text
    title_lines = truncate(title)
    draw.text((565, 180), title_lines[0], fill=(255, 255, 255), font=font_main)
    draw.text((565, 230), title_lines[1], fill=(255, 255, 255), font=font_main)
    draw.text((565, 320), f"{channel}  |  {views[:23]}", (255, 255, 255), font=font_small)

    # Bottom Text
    draw_bottom_text(draw, background.width, "Spotify ", font_small, (255, 255, 255))

    try:
        os.remove(f"cache/thumb{videoid}.png")
    except FileNotFoundError:
        pass

    background.save(f"cache/{videoid}_v4.png")
    return f"cache/{videoid}_v4.png"
