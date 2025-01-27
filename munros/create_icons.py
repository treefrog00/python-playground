from pathlib import Path
from PIL import Image
import httpx
import io
import math

# Base URL for the marker icons
MARKER_BASE_URL = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-{}.png"

# List of available colors
MARKER_COLORS = ['green', 'blue', 'red', 'black', 'violet', 'orange']

# Dictionary of marker URLs for different colors
marker_icons = {color: MARKER_BASE_URL.format(color) for color in MARKER_COLORS}

# List of rotation degrees

ROTATION_DEGREES = [0, 35, 70]

def download_and_rotate_images():
    output_dir = Path('rotated_markers')
    output_dir.mkdir(exist_ok=True)

    with httpx.Client() as client:
        for color, url in marker_icons.items():
            # Download the image
            response = client.get(url)
            image_data = response.content

            # Create rotations for each degree in the list
            for degree in ROTATION_DEGREES:
                # Create a new image object for each rotation
                img = Image.open(io.BytesIO(image_data))

                if degree:
                    width, height = img.size
                    if degree == 70:
                        # changing the centre stops expand
                        # from working, which requires
                        # a bunch of trigonometry instead
                        #rotation_center = (width // 2, height)
                        #rotation_center = (width // 2, height // 2)
                        #img = img.rotate(-degree, center=rotation_center, expand=True, resample=Image.BICUBIC)
                        img = img.rotate(-degree,
                        expand=True, resample=Image.BICUBIC)
                    else:
                        img = img.rotate(-degree, expand=True, resample=Image.BICUBIC)

                output_path = output_dir / f'marker-icon-{color}-r{degree}.png'
                img.save(output_path, optimize=True, quality=95)

if __name__ == '__main__':
    download_and_rotate_images()
