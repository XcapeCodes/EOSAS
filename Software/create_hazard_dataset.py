import shutil
from pathlib import Path

SOURCE_BASE = Path("data/existing/SkinDisease")
DEST_BASE = Path("data/hazard_dataset")

hazard_map = {
    "Low_Hazard": [
        "Unknown_Normal"
    ],
    "Medium_Hazard": [
        "Acne",
        "Eczema",
        "Rosacea",
        "Tinea",
        "Warts",
        "Moles",
        "Vitiligo",
        "Candidiasis",
        "Infestations_Bites",
        "Sun_Sunlight_Damage"
    ],
    "High_Hazard": [
        "SkinCancer",
        "Vasculitis",
        "Lupus",
        "Bullous",
        "Actinic_Keratosis",
        "DrugEruption",
        "Vascular_Tumors",
        "Benign_tumors",
        "Psoriasis",
        "Lichen",
        "Seborrh_Keratoses"
    ]
}

def copy_images(split):
    source_split = SOURCE_BASE / split
    dest_split = DEST_BASE / split

    for hazard_class, original_classes in hazard_map.items():
        dest_folder = dest_split / hazard_class
        dest_folder.mkdir(parents=True, exist_ok=True)

        for original_class in original_classes:
            source_folder = source_split / original_class

            if not source_folder.exists():
                print("Missing:", source_folder)
                continue

            for img_file in source_folder.iterdir():
                if img_file.is_file():
                    new_name = f"{original_class}_{img_file.name}"
                    shutil.copy2(img_file, dest_folder / new_name)

    print(f"Finished {split}")

copy_images("train")
copy_images("test")

print("Hazard dataset created.")
