#!/usr/bin/env python3
import os, shutil, argparse, json, datetime

def safe_move_or_copy(src_path, target_dir, filename, copy=False):
    """
    搬移或複製檔案，如果目標已存在則自動加編號避免覆蓋。
    """
    base, ext = os.path.splitext(filename)
    target = os.path.join(target_dir, filename)
    counter = 1
    while os.path.exists(target):
        new_name = f"{base}_{counter}{ext}"
        target = os.path.join(target_dir, new_name)
        counter += 1
    if copy:
        shutil.copy2(src_path, target)
    else:
        shutil.move(src_path, target)
    return target

def organize_by_extension(src, copy=False, dry_run=False):
    undo_log = []
    for filename in os.listdir(src):
        path = os.path.join(src, filename)
        if os.path.isfile(path):
            ext = os.path.splitext(filename)[1][1:].lower() or "noext"
            target_dir = os.path.join(src, ext.upper())
            if dry_run:
                target = os.path.join(target_dir, filename)
                print(f"[DRY-RUN] {path} -> {target}")
            else:
                os.makedirs(target_dir, exist_ok=True)
                target = safe_move_or_copy(path, target_dir, filename, copy)
            undo_log.append({"original": path, "moved": target})
    return undo_log

def organize_by_date(src, copy=False, dry_run=False):
    undo_log = []
    for filename in os.listdir(src):
        path = os.path.join(src, filename)
        if os.path.isfile(path):
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            target_dir = os.path.join(src, str(mtime.year), f"{mtime.month:02d}")
            if dry_run:
                target = os.path.join(target_dir, filename)
                print(f"[DRY-RUN] {path} -> {target}")
            else:
                os.makedirs(target_dir, exist_ok=True)
                target = safe_move_or_copy(path, target_dir, filename, copy)
            undo_log.append({"original": path, "moved": target})
    return undo_log

def main():
    parser = argparse.ArgumentParser(description="Organize files by extension or date.")
    parser.add_argument("--src", required=True, help="Source folder path")
    parser.add_argument("--mode", choices=["ext", "date"], default="ext", help="Organize mode: ext/date")
    parser.add_argument("--copy", action="store_true", help="Copy instead of move")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving")
    parser.add_argument("--undo", help="Undo from log.json")
    args = parser.parse_args()

    if args.undo:
        with open(args.undo, "r") as f:
            undo_log = json.load(f)
        for entry in undo_log:
            original, moved = entry["original"], entry["moved"]
            if os.path.exists(moved):
                if os.path.exists(original):
                    print(f"⚠️ Skip restoring {original}, already exists.")
                    continue
                os.makedirs(os.path.dirname(original), exist_ok=True)
                shutil.move(moved, original)
        print("Undo completed.")
        return

    if args.mode == "ext":
        undo_log = organize_by_extension(args.src, args.copy, args.dry_run)
    else:
        undo_log = organize_by_date(args.src, args.copy, args.dry_run)

    if not args.dry_run:
        log_file = os.path.join(args.src, f"undo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(log_file, "w") as f:
            json.dump(undo_log, f, indent=2)
        print(f"Undo log saved: {log_file}")
    else:
        print("Dry run completed. No files were moved.")

if __name__ == "__main__":
    main()
