import asyncio
import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch

# Helper Functions
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

def truncate(text):
    words = text.split(" ")
    text1, text2 = "", ""
    for word in words:
        if len(text1) + len(word) < 30:
            text1 += " " + word
        elif len(text2) + len(word) < 30:
            text2 += " " + word
    return [text1.strip(), text2.strip()]

def crop_center_circle(img, output_size, border, crop_scale=1.5):
    half_width = img.size[0] / 2
    half_height = img.size[1] / 2
    larger_size = int(output_size * crop_scale)
    img = img.crop((
        half_width - larger_size / 2,
        half_height - larger_size / 2,
        half_width + larger_size / 2,
        half_height + larger_size / 2
    ))
    img = img.resize((output_size - 2 * border, output_size - 2 * border))
    final_img = Image.new("RGBA", (output_size, output_size), "white")
    mask_main = Image.new("L", (output_size - 2 * border, output_size - 2 * border), 0)
    draw_main = ImageDraw.Draw(mask_main)
    draw_main.ellipse((0, 0, output_size - 2 * border, output_size - 2 * border), fill=255)
    final_img.paste(img, (border, border), mask_main)
    return final_img

def draw_progress_bar(draw, x, y, width, height, progress, bg_color="white", fill_color="red"):
    draw.rectangle([x, y, x + width, y + height], fill=bg_color)  # Background
    draw.rectangle([x, y, x + int(width * progress), y + height], fill=fill_color)  # Progress

# Thumbnail Generator
async def gen_thumb(vidid, current_position, total_duration):
    try:
        # Fetch video metadata
        url = f"https://www.youtube.com/watch?v={vidid}"
        results = VideosSearch(url, limit=1)
        result = (await results.next())["result"][0]

        title = re.sub("\W+", " ", result.get("title", "Unsupported Title")).title()
        duration = result.get("duration", "Unknown Mins")
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        views = result.get("viewCount", {}).get("short", "Unknown Views")
        channel = result.get("channel", {}).get("name", "Unknown Channel")

        # Download thumbnail
        os.makedirs("cache", exist_ok=True)
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    thumbnail_path = f"cache/thumb{vidid}.png"
                    async with aiofiles.open(thumbnail_path, mode="wb") as f:
                        await f.write(await resp.read())

        # Open and process thumbnail
        youtube = Image.open(thumbnail_path)
        image1 = changeImageSize(1280, 720, youtube)
        background = image1.convert("RGBA").filter(ImageFilter.BoxBlur(20))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        draw = ImageDraw.Draw(background)

        # Fonts
        font_title = ImageFont.truetype("assets/Bad/font3.ttf", 45)
        font_text = ImageFont.truetype("assets/Bad/font2.ttf", 30)

        # Circular thumbnail
        circle_thumbnail = crop_center_circle(youtube, 400, 20)
        background.paste(circle_thumbnail, (120, 160), circle_thumbnail)

        # Title and Info
        title_lines = truncate(title)
        draw.text((565, 180), title_lines[0], fill=(255, 255, 255), font=font_title)
        draw.text((565, 230), title_lines[1], fill=(255, 255, 255), font=font_title)
        draw.text((565, 320), f"{channel}  |  {views[:23]}", fill=(255, 255, 255), font=font_text)

        # Progress Bar
        progress = current_position / total_duration if total_duration > 0 else 0
        draw_progress_bar(draw, 565, 380, 580, 10, progress, bg_color="white", fill_color="red")

        # Current Time and Duration
        current_time_text = f"{int(current_position // 60):02}:{int(current_position % 60):02}"
        draw.text((565, 400), current_time_text, fill=(255, 255, 255), font=font_text)
        draw.text((1145, 400), duration, fill=(255, 255, 255), font=font_text)

        # Save and return
        thumb_path = f"cache/{vidid}_v4_{int(current_position)}.png"
        background.save(thumb_path)
        return thumb_path
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return None

# Real-Time Thumbnail Regeneration
async def regenerate_thumbnails(vidid, total_duration):
    current_position = 0
    while current_position <= total_duration:
        print(f"Generating thumbnail for position: {current_position}")
        thumbnail_path = await gen_thumb(vidid, current_position, total_duration)
        if thumbnail_path:
            print(f"Thumbnail saved at {thumbnail_path}")
        else:
            print("Failed to generate thumbnail.")
        await asyncio.sleep(10)  # Update every 10 seconds
        current_position += 10

# Test the function
# asyncio.run(regenerate_thumbnails("your_video_id", total_duration_in_seconds))

async def gen_qthumb(vidid, current_position, total_duration):
    try:
        # Fetch video metadata
        url = f"https://www.youtube.com/watch?v={vidid}"
        results = VideosSearch(url, limit=1)
        result = (await results.next())["result"][0]

        title = re.sub("\W+", " ", result.get("title", "Unsupported Title")).title()
        duration = result.get("duration", "Unknown Mins")
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        views = result.get("viewCount", {}).get("short", "Unknown Views")
        channel = result.get("channel", {}).get("name", "Unknown Channel")

        # Download thumbnail
        os.makedirs("cache", exist_ok=True)
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    thumbnail_path = f"cache/thumb{vidid}.png"
                    async with aiofiles.open(thumbnail_path, mode="wb") as f:
                        await f.write(await resp.read())

        # Open and process thumbnail
        youtube = Image.open(thumbnail_path)
        image1 = changeImageSize(1280, 720, youtube)
        background = image1.convert("RGBA").filter(ImageFilter.BoxBlur(20))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        draw = ImageDraw.Draw(background)

        # Fonts
        font_title = ImageFont.truetype("assets/Bad/font3.ttf", 45)
        font_text = ImageFont.truetype("assets/Bad/font2.ttf", 30)

        # Circular thumbnail
        circle_thumbnail = crop_center_circle(youtube, 400, 20)
        background.paste(circle_thumbnail, (120, 160), circle_thumbnail)

        # Title and Info
        title_lines = truncate(title)
        draw.text((565, 180), title_lines[0], fill=(255, 255, 255), font=font_title)
        draw.text((565, 230), title_lines[1], fill=(255, 255, 255), font=font_title)
        draw.text((565, 320), f"{channel}  |  {views[:23]}", fill=(255, 255, 255), font=font_text)

        # Progress Bar
        progress = current_position / total_duration if total_duration > 0 else 0
        draw_progress_bar(draw, 565, 380, 580, 10, progress, bg_color="white", fill_color="red")

        # Current Time and Duration
        current_time_text = f"{int(current_position // 60):02}:{int(current_position % 60):02}"
        draw.text((565, 400), current_time_text, fill=(255, 255, 255), font=font_text)
        draw.text((1145, 400), duration, fill=(255, 255, 255), font=font_text)

        # Save and return
        thumb_path = f"cache/{vidid}_v4_{int(current_position)}.png"
        background.save(thumb_path)
        return thumb_path
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return None

# Real-Time Thumbnail Regeneration
async def regenerate_thumbnails(vidid, total_duration):
    current_position = 0
    while current_position <= total_duration:
        print(f"Generating thumbnail for position: {current_position}")
        thumbnail_path = await gen_thumb(vidid, current_position, total_duration)
        if thumbnail_path:
            print(f"Thumbnail saved at {thumbnail_path}")
        else:
            print("Failed to generate thumbnail.")
        await asyncio.sleep(10)  # Update every 10 seconds
        current_position += 10

# Test the function
# asyncio.run(regenerate_thumbnails("your_video_id", total_duration_in_seconds))
