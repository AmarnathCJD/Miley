from Evie import tbot
from Evie.events import register
from PIL import Image, ImageDraw, ImageFont
import os, random

@register(pattern="^/logo ?(.*)")
async def lg(event):
 fk = await event.reply("Processing.....")
 try:
    arg = event.pattern_match.group(1)
    if not arg:
        await fk.edit("`Please Give Me A Valid Input.`")
        return
    if "|" in arg:
       text, cust= arg.split("|")
       text = text.strip()
       cust = cust.strip()
       op = cust.split(" ", 2)
       if len(op) == 3:
         color = op[0]
         stroke = op[1]
         width = int(op[2])
       elif len(op) == 2:
         color = op[0]
         stroke = op[1]
         width = 10
       elif len(op) == 1:
         color = op[0]
         stroke = 'black'
         width = 10
    else:
       text = arg
       color = (255, 255, 0)
       stroke = 'black'
       width = 7
    img = Image.open("./Evie/function/black_blank_image.jpg")
    draw = ImageDraw.Draw(img)
    if len(text) < 7:
       font = ImageFont.truetype("./Evie/function/Fonts/Streamster.ttf", 450)
    else:
       font = ImageFont.truetype("./Evie/function/Fonts/vermin_vibes.ttf", 300)
    image_widthz, image_heightz = img.size
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    draw.text(
        ((image_widthz - w) / 2, (image_heightz - h) / 2),
        text,
        font=font,
        fill=color,
    )
    x = (image_widthz - w) / 2
    y = (image_heightz - h) / 2
    draw.text(
        (x, y), text, font=font, fill=color, stroke_width=width, stroke_fill=stroke
    )
    file_name = "LogoBy@Evie.png"
    img.save(file_name, "png")
    await fk.delete()
    async with tbot.action(event.chat_id, 'photo'):
      if event.reply_to_msg_id:
        await tbot.send_file(
            event.chat_id,
            file=file_name,
            caption="MissEvie_Robot",
            force_document=True,
            reply_to=event.message.id
        )
      else:
        await tbot.send_file(
            event.chat_id, file=file_name, caption="MissEvie_Robot", force_document=True
        )
    if os.path.exists(file_name):
        os.remove(file_name)
 except Exception as e:
   await fk.edit(f"{e}")


