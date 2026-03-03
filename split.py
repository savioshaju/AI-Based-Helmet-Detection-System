import os
import random
import shutil

# Paths
image_dir = "images"
label_dir = "labels"

base_output = "dataset"

train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1

images = [f for f in os.listdir(image_dir) if f.endswith((".jpg", ".png"))]
random.shuffle(images)

total = len(images)
train_end = int(total * train_ratio)
val_end = train_end + int(total * val_ratio)

splits = {
    "train": images[:train_end],
    "valid": images[train_end:val_end],
    "test": images[val_end:]
}

for split in splits:
    os.makedirs(f"{base_output}/{split}/images", exist_ok=True)
    os.makedirs(f"{base_output}/{split}/labels", exist_ok=True)

    for img in splits[split]:
        label = img.rsplit(".", 1)[0] + ".txt"

        shutil.copy(os.path.join(image_dir, img),
                    f"{base_output}/{split}/images/{img}")

        if os.path.exists(os.path.join(label_dir, label)):
            shutil.copy(os.path.join(label_dir, label),
                        f"{base_output}/{split}/labels/{label}")

print("Dataset split complete.")