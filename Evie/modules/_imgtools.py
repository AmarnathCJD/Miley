from Evie import tbot
from Evie.events import register
from PIL import Image, ImageDraw, ImageFont


@register(pattern="^/logo ?(.*)")
async def lg(event):
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
    file_name = "LogoBy@MeisNub.png"
    await client.send_chat_action(message.chat.id, "upload_photo")
    img.save(file_name, "png")
    if message.reply_to_message:
        await client.send_photo(
            message.chat.id,
            photo=file_name,
            caption="Made Using FridayUserBot",
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_photo(
            message.chat.id, photo=file_name, caption="Made Using FridayUserBot"
        )
    await client.send_chat_action(message.chat.id, "cancel")
    await event.delete()
    if os.path.exists(file_name):
        os.remove(file_name)
