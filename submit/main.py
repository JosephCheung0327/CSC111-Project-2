"""
This is the main file to run the Destiny app.
"""

import ui

if __name__ == '__main__':
    home_image_path = "destiny_home_page.png"  # The path to the PNG image for home page
    app = ui.DestinyApp(home_image_path)
    app.run()
