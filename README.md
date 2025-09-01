Python 自動整理檔案小工具

這是一個使用 Python 撰寫的小工具，幫你快速整理電腦資料夾，讓檔案分類更有效率。

✨ 功能特色

📂 依副檔名自動分類：自動建立 PDF/、JPG/、TXT/ 等資料夾

🗓 依修改日期分類：自動建立 /2025/08/ 這類日期資料夾

🔍 Dry-run 預覽模式：先模擬搬移，不會誤動檔案

↩️ Undo 還原功能：一鍵回復到整理前狀態

🚚 搬移 / 複製模式：可選擇是移動檔案還是僅複製備份

🖥 跨平台：Windows / macOS / Linux 皆可使用 (需安裝 Python 3)

🚀 使用方法
# 依副檔名分類
python organize_files.py --src ~/Downloads --mode ext

# 依日期分類
python organize_files.py --src ~/Downloads --mode date

# Dry-run 預覽 (不會真的移動)
python organize_files.py --src ~/Downloads --mode ext --dry-run

# Undo (回復到整理前)
python organize_files.py --undo undo_20250831_214935.json