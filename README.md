# FirstFruits-yt-thumb-gen
A aimple Python script to generate a Youtube thumbnail with the settings used in First Fruits Bible Study.

Uses `Pillow` to generate images and text elements. For development of a built-in HTTP server that allows for quick submittal of background image and text inputs, `multipart` is needed.

Use PIP to install required dependencies.
- `pip install -r requirements.txt`

Usage:
1. `python cli.py [<image-name>.png]`
2. If image filename is omitted or the filename provided is not a valid image, you'll be prompted for an image.
3. Enter the Bible passage for the episode.
4. Choose either 1 or 2-line title (vertically centering passage and title lines based on this check).
5. Enter the title text for each line.
6. Verify the date (YYYY-MM-DD format).
7. The image is generated in the output folder with formatting applied.

Notes:
- Output images are saved as /output/YYYY-MM-DD.png depending on the confirmed or manually entered.
- It is useful to keep initial background images out of the /output folder to avoid overwriting. If the webserver is being used, input backgrounds will be automatically stored in /web.
- If the output filename is identical to the input background (including path), the background file will be renamed.
- The background image will be expanded to Youtube's required 1280x720, overflowing those boundaries depending on its aspect ratio before it is cropped to size.
- Text settings including fonts, sizes, color, stroke thickness and color, and drop shadow blur and distance values are stored in dictionaries in the thumb_gen.py script. These may be moved to a config file later on.