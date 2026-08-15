"""
Auto-generate high-quality Vietnamese UI sprites for all 66 files in translation/sprites.
Uses Pillow with Segoe UI / Arial / Times New Roman bold fonts, smooth anti-aliasing, and drop-shadow / outer-glow.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SPRITES_DIR = r"e:\MGWT.v1.1.2\translation\sprites"

# Translations dictionary
SPRITE_TEXTS = {
    # Main menu labels
    "Label_NewGame@ZhHans.png": "Chơi mới",
    "Label_LoadGame@ZhHans.png": "Tải game",
    "Label_Options@ZhHans.png": "Cài đặt",
    "Label_Gallery@ZhHans.png": "Phòng tranh",
    "Label_Exit@ZhHans.png": "Thoát",
    "Label_WitchBook@ZhHans.png": "Sổ Tay Phù Thủy",

    # In-game menu buttons
    "MenuButton_Save_Normal@ZhHans.png": "Lưu",
    "MenuButton_Save_Highlighted@ZhHans.png": "Lưu",
    "MenuButton_Load_Normal@ZhHans.png": "Tải",
    "MenuButton_Load_Highlighted@ZhHans.png": "Tải",
    "MenuButton_Log_Normal@ZhHans.png": "Nhật ký",
    "MenuButton_Log_Highlighted@ZhHans.png": "Nhật ký",
    "MenuButton_Options_Normal@ZhHans.png": "Cài đặt",
    "MenuButton_Options_Highlighted@ZhHans.png": "Cài đặt",
    "MenuButton_Title_Normal@ZhHans.png": "Về Menu",
    "MenuButton_Title_Highlighted@ZhHans.png": "Về Menu",

    # Titles
    "OptionsTitle@ZhHans.png": "Cài đặt",
    "SaveTitle@ZhHans.png": "Lưu game",
    "LoadTitle@ZhHans.png": "Tải game",
    "BookTitle@ZhHans.png": "Sổ Tay Phù Thủy",
    "TitleBase@ZhHans.png": "Bắt đầu",
    "PresentButtonBody@ZhHans.png": "Xuất trình",

    # Tabs
    "TabLabel_Audio_Active@ZhHans.png": "Âm thanh",
    "TabLabel_Audio_Inactive@ZhHans.png": "Âm thanh",
    "TabLabel_Graphics_Active@ZhHans.png": "Đồ họa",
    "TabLabel_Graphics_Inactive@ZhHans.png": "Đồ họa",
    "TabLabel_Message_Active@ZhHans.png": "Thông điệp",
    "TabLabel_Message_Inactive@ZhHans.png": "Thông điệp",
    "TabLabel_Map_Active@ZhHans.png": "Bản đồ",
    "TabLabel_Map_Inactive@ZhHans.png": "Bản đồ",
    "TabLabel_Profile_Active@ZhHans.png": "Hồ sơ",
    "TabLabel_Profile_Inactive@ZhHans.png": "Hồ sơ",
    "TabLabel_Rule_Active@ZhHans.png": "Quy tắc",
    "TabLabel_Rule_Inactive@ZhHans.png": "Quy tắc",
    "TabLabel_Clue_Active@ZhHans.png": "Manh mối",
    "TabLabel_Clue_Inactive@ZhHans.png": "Manh mối",
    "TabLabel_Note_Active@ZhHans.png": "Ghi chú",
    "TabLabel_Note_Inactive@ZhHans.png": "Ghi chú",

    # Trial debate emotions
    "Agreement@ZhHans.png": "ĐỒNG TÌNH",
    "Doubt@ZhHans.png": "NGHI VẤN",
    "Objection@ZhHans.png": "PHẢN BIỆN",
    "Perjury@ZhHans.png": "KHAI MAN",

    # Magic
    "Magic_Blue@ZhHans.png": "Ma pháp",
    "Magic_Gray@ZhHans.png": "Ma pháp",
    "Magic_Orange@ZhHans.png": "Ma pháp",
    "Magic_Pink@ZhHans.png": "Ma pháp",
    "Magic_Purple@ZhHans.png": "Ma pháp",
    "Magic_Yellow@ZhHans.png": "Ma pháp",

    # Debate Text Begin / End
    "Debate_Text_Begin_1_Normal@ZhHans.png": "Bắt đầu",
    "Debate_Text_Begin_1_White@ZhHans.png": "Bắt đầu",
    "Debate_Text_Begin_2_Normal@ZhHans.png": "Tranh luận",
    "Debate_Text_Begin_2_White@ZhHans.png": "Tranh luận",
    "Debate_Text_Begin_3_Normal@ZhHans.png": "Bắt đầu",
    "Debate_Text_Begin_3_White@ZhHans.png": "Bắt đầu",
    "Debate_Text_Begin_4_Normal@ZhHans.png": "Tranh luận",
    "Debate_Text_Begin_4_White@ZhHans.png": "Tranh luận",
    "Debate_Text_End_1_Normal@ZhHans.png": "Kết thúc",
    "Debate_Text_End_1_White@ZhHans.png": "Kết thúc",
    "Debate_Text_End_2_Normal@ZhHans.png": "Tranh luận",
    "Debate_Text_End_2_White@ZhHans.png": "Tranh luận",
    "Debate_Text_End_3_Normal@ZhHans.png": "Kết thúc",
    "Debate_Text_End_3_White@ZhHans.png": "Kết thúc",
    "Debate_Text_End_4_Normal@ZhHans.png": "Tranh luận",
    "Debate_Text_End_4_White@ZhHans.png": "Tranh luận",
}

FONT_PATH_SANS = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_PATH_SERIF = r"C:\Windows\Fonts\timesbd.ttf"
FONT_PATH_ARIAL = r"C:\Windows\Fonts\arialbd.ttf"

def render_vietnamese_sprites():
    count = 0
    for filename, text in SPRITE_TEXTS.items():
        filepath = os.path.join(SPRITES_DIR, filename)
        if not os.path.exists(filepath):
            continue
            
        orig = Image.open(filepath).convert("RGBA")
        w, h = orig.size
        
        # Create a blank RGBA image of the same size
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Determine appropriate font size
        font_path = FONT_PATH_SERIF if any(k in filename for k in ["Title", "Agreement", "Objection", "Perjury", "Doubt", "Magic", "Debate"]) else FONT_PATH_SANS
        
        # Find max font size that fits in width & height (with margin)
        target_w = int(w * 0.85)
        target_h = int(h * 0.80)
        
        font_size = 40
        font = ImageFont.truetype(font_path, font_size)
        while font_size > 8:
            bbox = draw.textbbox((0, 0), text, font=font)
            bw = bbox[2] - bbox[0]
            bh = bbox[3] - bbox[1]
            if bw <= target_w and bh <= target_h:
                break
            font_size -= 1
            font = ImageFont.truetype(font_path, font_size)
            
        bbox = draw.textbbox((0, 0), text, font=font)
        bw = bbox[2] - bbox[0]
        bh = bbox[3] - bbox[1]
        
        x = (w - bw) // 2 - bbox[0]
        y = (h - bh) // 2 - bbox[1]
        
        # Determine text color and shadow style
        if "White" in filename:
            fill_color = (255, 255, 255, 255)
            shadow_color = (0, 0, 0, 180)
        elif "Highlighted" in filename:
            fill_color = (255, 240, 200, 255)
            shadow_color = (80, 20, 20, 200)
        elif "Inactive" in filename:
            fill_color = (180, 180, 180, 220)
            shadow_color = (0, 0, 0, 150)
        elif "Active" in filename:
            fill_color = (255, 255, 255, 255)
            shadow_color = (40, 40, 40, 200)
        elif "Magic" in filename:
            fill_color = (255, 255, 240, 255)
            shadow_color = (20, 10, 30, 220)
        else:
            fill_color = (255, 255, 255, 255)
            shadow_color = (0, 0, 0, 200)
            
        # Draw shadow / outline
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1), (-2, -2), (2, 2)]:
            draw.text((x + dx, y + dy), text, font=font, fill=shadow_color)
            
        # Draw main text
        draw.text((x, y), text, font=font, fill=fill_color)
        
        # Save back
        img.save(filepath, "PNG")
        count += 1
        print(f"[RENDERED] {filename} -> '{text}' (size {w}x{h}, font {font_size})")

    print(f"\n[SUCCESS] Rendered {count} Vietnamese sprites into {SPRITES_DIR}!")

if __name__ == "__main__":
    render_vietnamese_sprites()
