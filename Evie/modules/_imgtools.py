from Evie import tbot
from Evie.events import register
from PIL import Image, ImageDraw, ImageFont
import os

@register(pattern="^/logo ?(.*)")
async def lg(event):
 try:
    fk = await event.reply("Processing.....")
    text = event.pattern_match.group(1)
    if not text:
        await event.edit("`Please Give Me A Valid Input.`")
        return
    img = Image.open("./Evie/function/black_blank_image.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./Evie/function/Fonts/Streamster.ttf", 220)
    image_widthz, image_heightz = img.size
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    draw.text(
        ((image_widthz - w) / 2, (image_heightz - h) / 2),
        text,
        font=font,
        fill=(255, 255, 0),
    )
    file_name = "LogoBy@Evie.png"
    img.save(file_name, "png")
    if event.reply_to_msg_id:
        await tbot.send_file(
            event.chat_id,
            file=file_name,
            caption="By_MissEvie_Robot",
            reply_to=event.message.id
        )
    else:
        await tbot.send_file(
            event.chat_id, file=file_name, caption="By_MissEvie_Robot"
        )
    if os.path.exists(file_name):
        os.remove(file_name)
 except Exception as e:
   await event.reply(f"{e}")
