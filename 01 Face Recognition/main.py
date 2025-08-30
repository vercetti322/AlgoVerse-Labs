from manim import *

# Face Recognition : mesh based architecture
ASSET = "D:\\AlgoVerse-Labs\\01 Face Recognition\\assets"
FONT = "Roboto"
TEXT_COLOR = "#383838"
LOGO_GREEN = "#62b6aa" 


# defaults for reel
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.background_color = WHITE

class Introduction(Scene):
    def construct(self):
        ronaldo = ImageMobject(ASSET + "\\ronaldo.png")
        ronaldo.scale_to_fit_width(config.frame_width)
        self.play(GrowFromCenter(ronaldo))
        self.wait(4)
