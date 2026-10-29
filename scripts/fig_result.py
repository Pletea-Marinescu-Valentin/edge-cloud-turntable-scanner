"""Fig. 4: the test object and its textured model.

The two photographs in data/photos are the team's own images: the Parkside PSSA 4 B2 cordless screwdriver on
the AprilTag disc inside the cell, and a render of the textured model produced by the pipeline. They are raster
by nature; this script only brings them to a common height, strips their metadata and writes the JPEG files
that main.tex places side by side.
"""

from PIL import Image

import style

HEIGHT_PX = 800          # about 360 dpi at the printed height of the figure
SOURCES = {
    "fig_result_photo.jpg": "screwdriver_real.jpg",
    "fig_result_model.jpg": "screwdriver_model.jpg",
}


def main():
    style.FIGS.mkdir(parents=True, exist_ok=True)
    for out_name, src_name in SOURCES.items():
        with Image.open(style.DATA / "photos" / src_name) as im:
            im = im.convert("RGB")
            width = round(im.width * HEIGHT_PX / im.height)
            im = im.resize((width, HEIGHT_PX), Image.Resampling.LANCZOS)
            clean = Image.new("RGB", im.size)          # copy pixels only: no EXIF or other metadata
            clean.paste(im)
            out = style.FIGS / out_name
            clean.save(out, "JPEG", quality=90, optimize=True, progressive=False)
            print(f"wrote {out.relative_to(style.ROOT)} ({width}x{HEIGHT_PX})")


if __name__ == "__main__":
    main()
