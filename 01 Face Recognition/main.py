from manim import *
import numpy as np
import json

# Face Recognition : mesh based architecture
ASSET = "D:\\AlgoVerse-Labs\\01 Face Recognition\\assets"
TEXT_COLOR = "#383838"
ARROW_GREEN = "#62b6aa" 

# defaults for reel
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.background_color = "#efd6ac"

def save_dots(dots, filename="dots.json"):
    data = []
    for dot in dots:
        data.append({
            "pos": dot.get_center().tolist(),   # [x, y, z]
            "radius": dot.radius,
            "color": str(dot.color)  # convert to string like '#00FF00'
        })
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_dots(filename="dots.json"):
    with open(filename, "r") as f:
        data = json.load(f)

    dots = VGroup()
    for d in data:
        pos = np.array(d["pos"])
        radius = d.get("radius", 0.07)
        color = d.get("color")  # default green if missing
        dots.add(Dot(pos, radius=radius, color=color))
    
    return dots

class Introduction(Scene):
    def construct(self):
        # ronaldo pic
        ronaldo = ImageMobject(ASSET + "\\ronaldo.png")
        ronaldo.scale_to_fit_width(config.frame_width * 0.9)
        ronaldo.shift(DOWN * 14)

        # line 1
        line_1 = Text("How does your iPhone", font="Roboto").scale_to_fit_width(config.frame_width * 0.8)
        line_1.set_color(TEXT_COLOR).shift(UP * 10.15)
        line_1.set_opacity(0)
        
        # First part: "Recognize"
        part1 = Text("Recognize", font="Anton", color=ARROW_GREEN)

        # Second part: "you?"
        part2 = Text("you?", font="Anton", color=TEXT_COLOR).next_to(part1, RIGHT, buff=0.1)
        VGroup(part1, part2).move_to(ORIGIN).shift(UP * 9).scale_to_fit_width(config.frame_width * 0.8)
    
        self.add(line_1, part1, part2)

        # animation
        self.play(
            AnimationGroup(
                line_1.animate.shift(DOWN * 5).set_opacity(1),
                VGroup(part1, part2).animate.shift(DOWN * 5).set_opacity(1),
                lag_ratio=0.8
            ),
            ronaldo.animate.shift(UP * 10.5),
            run_time=1.75
        )

        self.wait(0.5)

        # pointing to ronaldo's face and saying ronaldo
        pointer = VGroup(
            Line(start=ORIGIN, end=ORIGIN + RIGHT * 0.4),
            Line(start=ORIGIN + UP * 0.4 + LEFT * 0.3, end=ORIGIN),
            Dot(point=ORIGIN + RIGHT * 0.4)
        ).scale(2.4).shift(LEFT * 2.5 + DOWN * 1.5).set_color(TEXT_COLOR)

        cr7 = Text("CR7", font="Anton", color=ARROW_GREEN).next_to(pointer[1], UP, buff=0.1)
        cr7.shift(LEFT * 0.4)

        self.play(Write(pointer), run_time=0.75)
        self.play(FadeIn(cr7))

        self.wait(4)

        # fadeout texts
        self.play(
            FadeOut(VGroup(pointer, line_1, part1, part2, cr7)),
            run_time=0.4
        )

        self.wait(4)

class MeshScene(MovingCameraScene):
    def construct(self):
        # prepare scene
        ronaldo = ImageMobject(ASSET + "\\ronaldo.png")
        ronaldo.scale_to_fit_width(config.frame_width * 0.9)
        ronaldo.shift(DOWN * 4.5)
        self.add(ronaldo)

        self.wait(4)

        # bring iphone above
        iphone = ImageMobject(ASSET + "\\iphone.png").scale(0.8)
        iphone.shift(UP * 14)
        self.play(iphone.animate.shift(DOWN * 9), run_time=1.2)

        # move camera to phone's top
        self.play(self.camera.frame.animate.scale(0.4).move_to(iphone.get_top() + DOWN * 0.4))

        # point the camera
        pointer = VGroup(
            Line(start=ORIGIN, end=ORIGIN + RIGHT * 0.4),
            Line(start=ORIGIN + UP * 0.45 + LEFT * 0.35, end=ORIGIN + DOWN * 0.01 + RIGHT * 0.01),
            Dot(point=ORIGIN + RIGHT * 0.4)
        ).shift(UP * 6.85 + LEFT * 0.4).scale(0.7).set_color(TEXT_COLOR)

        ir = Text("IR Camera", font="Anton", color=ARROW_GREEN).next_to(pointer[1], UP, buff=0.04)
        ir.scale(0.4).shift(DOWN * 0.12)

        self.play(Write(pointer), run_time=0.7)

        self.play(FadeIn(ir), run_time=0.7)

        self.wait(1)

        self.play(FadeOut(pointer, ir), run_time=0.6)

        self.wait(2)

        # go back
        self.play(self.camera.frame.animate.scale(2.5).move_to(ORIGIN))
        self.wait(2)

        # saved dots
        dots = load_dots()
        self.play(*[GrowFromCenter(x) for x in dots], lag_ratio=0.2, run_time=1.24)

        self.wait(0.7)

        # go over each and connect each
        k = 5
        lines = VGroup()
        for i, dot1 in enumerate(dots):
            distances = []
            for j, dot2 in enumerate(dots):
                if i != j:
                    dist = np.linalg.norm(dot1.get_center() - dot2.get_center())
                    distances.append((dist, dot2))
            # sort by distance and take k closest
            distances.sort(key=lambda x: x[0])
            for _, neighbor in distances[:k]:
                line = Line(dot1.get_center(), neighbor.get_center(), color=ARROW_GREEN)
                line.set_stroke(width=2.5)
                lines.add(line)

        # animate all lines in one go
        self.play(Write(lines), run_time=2)
        self.wait(2)

        # remove ronaldo
        self.play(FadeOut(ronaldo), run_time=0.7)
        self.wait(2)

        # scale down and bring it to phone
        self.play(
            VGroup(dots, lines).animate.scale(0.7).move_to(ORIGIN),
            FadeOut(iphone),
            run_time=0.7
        )

        mesh = VGroup(dots, lines)

        # pointer to explain
        pointer = VGroup(
            Line(start=ORIGIN, end=ORIGIN + RIGHT * 0.4),
            Line(start=ORIGIN + UP * 0.45 + LEFT * 0.35, end=ORIGIN + DOWN * 0.01 + RIGHT * 0.01),
            Dot(point=ORIGIN + RIGHT * 0.4)
        ).move_to(mesh.get_center() + UP * 2.8 + LEFT * 0.6).scale(2.4).set_color(TEXT_COLOR)

        self.play(Write(pointer))

        coords = Text("x, y, z", font="Anton", color=TEXT_COLOR).next_to(pointer[1], UP, buff=0.04)
        self.play(FadeIn(coords), run_time=0.7)

        self.wait(2)

        self.play(FadeOut(coords), FadeOut(pointer), run_time=0.4)

        self.wait(4)


class FacePrint(MovingCameraScene):
    def construct(self):
        # setting the scene
        dots = load_dots()
        k = 5
        lines = VGroup()
        for i, dot1 in enumerate(dots):
            distances = []
            for j, dot2 in enumerate(dots):
                if i != j:
                    dist = np.linalg.norm(dot1.get_center() - dot2.get_center())
                    distances.append((dist, dot2))
            # sort by distance and take k closest
            distances.sort(key=lambda x: x[0])
            for _, neighbor in distances[:k]:
                line = Line(dot1.get_center(), neighbor.get_center(), color=ARROW_GREEN)
                line.set_stroke(width=2.5)
                lines.add(line)
        
        mesh = VGroup(dots, lines).scale(0.7).move_to(ORIGIN)
        self.add(mesh)
        
        self.wait(2)

        # make it small and put above
        self.play(mesh.animate.shift(UP * 3.85).scale(0.6), run_time=0.7)

        # new dots 
        dot_vector = VGroup(*[Dot(radius=0.14, color=TEXT_COLOR) for _ in range(len(dots))])
        dot_vector.arrange(RIGHT, buff=0.3).move_to(ORIGIN + DOWN * 0.2)

        # animate
        dot_copy = dots.copy()
        self.add(dot_copy)

        self.play(
            ReplacementTransform(dot_copy, dot_vector),
            run_time=0.8
        )

        # go to center of first dot and convert it into 3 dots
        self.play(
            self.camera.frame.animate.scale(0.08).move_to(dot_vector[0].get_center())
        )

        self.wait(0.4)

        # break all the dots
        grps = VGroup()
        for dot in dot_vector:
            grp = VGroup(
                Dot(radius=0.05, color=ARROW_GREEN),
                Dot(radius=0.05, color=ARROW_GREEN),
                Dot(radius=0.05, color=ARROW_GREEN),
            )
            grp.arrange(RIGHT, buff=0.03).move_to(dot)
            grps.add(grp)
            
        self.play(ReplacementTransform(dot_vector, grps), run_time=0.7)

        self.wait(0.8)

        self.play(
            self.camera.frame.animate.scale(12.5).move_to(ORIGIN)
        )
        self.wait(0.4)

        # brace on the dot_vector
        grp_brace = Brace(grps, buff=0.14, direction=DOWN).set_color(TEXT_COLOR)
        self.play(GrowFromCenter(grp_brace), run_time=0.6)

        brace_label = Text("Flattened Input", color=TEXT_COLOR, font="Anton")
        brace_label.scale(0.7).next_to(grp_brace, DOWN, buff=0.2)
        self.play(FadeIn(brace_label), run_time=0.4)

        self.wait(0.7)

        # remove mesh and and push the grps, grp_brace and brace_label up
        self.play(
            FadeOut(mesh),
            VGroup(grps, grp_brace, brace_label).animate.shift(UP * 4),
            run_time=0.7
        )

        self.wait(0.3)

        # remove grp_brace and brace_label
        self.play(
            FadeOut(VGroup(grp_brace, brace_label)),
            run_time=0.4
        )

        # make network below it
        input_layer = VGroup(*[Dot(radius=0.34, color=TEXT_COLOR) for _ in range(2)]).arrange(DOWN, buff=0.7)
        hidden_layer = VGroup(*[Dot(radius=0.34, color=TEXT_COLOR) for _ in range(3)]).arrange(DOWN, buff=0.7)
        output_layer = VGroup(Dot(radius=0.34, color=TEXT_COLOR))

        # position layers side by side
        hidden_layer.next_to(input_layer, RIGHT, buff=1)
        output_layer.next_to(hidden_layer, RIGHT, buff=1)

        # --- Connections ---
        connections = VGroup()

        # connect input → hidden
        for in_node in input_layer:
            for hid_node in hidden_layer:
                connections.add(Line(in_node.get_center(), hid_node.get_center(), stroke_color=TEXT_COLOR, stroke_width=3))

        # connect hidden → output
        for hid_node in hidden_layer:
            for out_node in output_layer:
                connections.add(Line(hid_node.get_center(), out_node.get_center(), stroke_color=TEXT_COLOR, stroke_width=3))

        # --- Group everything ---
        network = VGroup(connections, input_layer, hidden_layer, output_layer)
        network.move_to(ORIGIN + UP * 0.2)

        self.play(GrowFromCenter(network), run_time=0.8)

        self.wait(0.8)

        # go from grps to first input_layer, and make dots ARROW_GREEN
        grps_copy = grps.copy()
        self.play(
            Transform(grps_copy, input_layer),
            *[Indicate(dot, color=ARROW_GREEN) for dot in input_layer],
            run_time=0.7
        )

        self.wait(0.2)

        self.play(
            *[Indicate(dot, color=ARROW_GREEN) for dot in hidden_layer],
            run_time=0.4
        )

        self.wait(0.2)

        self.play(
            *[Indicate(dot, color=ARROW_GREEN) for dot in output_layer],
            run_time=0.4
        )

        self.wait(0.2)

        # faceprint vector
        faceprint = VGroup(*[Dot(radius=0.3, color=ARROW_GREEN) for _ in range(7)])
        faceprint.arrange(RIGHT, buff=0.3).move_to(ORIGIN + DOWN * 3)

        self.play(
            Transform(output_layer.copy(), faceprint),
            run_time=0.4
        )

        # brace on the dot_vector
        faceprint_brace = Brace(faceprint, buff=0.14, direction=DOWN).set_color(TEXT_COLOR)
        self.play(GrowFromCenter(faceprint_brace), run_time=0.6)

        brace_label = Text("Faceprint Vector", color=TEXT_COLOR, font="Anton")
        brace_label.scale(0.7).next_to(faceprint_brace, DOWN, buff=0.2)
        self.play(FadeIn(brace_label), run_time=0.4)

        self.wait(0.8)
        self.play(FadeOut(VGroup(brace_label, grps_copy, faceprint_brace, network, grps)), run_time=0.3)

        self.wait(4)

class Unlock(MovingCameraScene):
    def construct(self):
        # prepare scene
        faceprint = VGroup(*[Dot(radius=0.3, color=ARROW_GREEN) for _ in range(7)])
        faceprint.arrange(RIGHT, buff=0.3).move_to(ORIGIN + DOWN * 3)
        self.add(faceprint)

        self.wait(2)

        # bring iphone above
        iphone = ImageMobject(ASSET + "\\iphone.png").scale(0.8)
        iphone.shift(UP * 10)
        self.play(iphone.animate.shift(DOWN * 8), run_time=0.9)
        self.wait(0.7)

        # bring faceprint to iphone
        self.play(
            faceprint.animate.move_to(iphone.get_center()).set_opacity(0).scale(0.04),
            run_time=1.2
        )

        self.wait(0.2)

        # make phone larger
        self.play(
            iphone.animate.scale(2.4),
            run_time=0.4
        )

        self.wait(0.2)

        # have ronaldo appear
        ronaldo = ImageMobject(ASSET + "\\ronaldo2.png")
        ronaldo.scale_to_fit_width(iphone.width * 0.37)
        ronaldo.shift(DOWN * 0.52 + RIGHT * 0.02)        
        self.play(FadeIn(ronaldo), run_time=0.6)
        self.wait(0.2)

        # face mesh
        dots = load_dots()
        k = 5
        lines = VGroup()
        for i, dot1 in enumerate(dots):
            distances = []
            for j, dot2 in enumerate(dots):
                if i != j:
                    dist = np.linalg.norm(dot1.get_center() - dot2.get_center())
                    distances.append((dist, dot2))
            # sort by distance and take k closest
            distances.sort(key=lambda x: x[0])
            for _, neighbor in distances[:k]:
                line = Line(dot1.get_center(), neighbor.get_center(), color=ARROW_GREEN)
                line.set_stroke(width=2.5)
                lines.add(line)
        
        mesh = VGroup(dots, lines).scale(0.42).shift(UP * 3.3)
        self.play(Create(mesh), run_time=0.7)
        
        self.wait(0.4)

        # copy of mesh to above
        faceprint = VGroup(*[Dot(radius=0.3, color=TEXT_COLOR) for _ in range(7)])
        faceprint.arrange(RIGHT, buff=0.3).scale(0.5).shift(UP * 2.9)
        self.play(ReplacementTransform(mesh.copy(), faceprint), run_time=0.7)

        self.wait(0.7)

        # bring original faceprint
        id = VGroup(*[Dot(radius=0.3, color=ARROW_GREEN) for _ in range(7)])
        id.arrange(RIGHT, buff=0.3).scale(0.5).shift(UP * 4.3)
        self.play(Create(id), run_time=0.7)
        
        self.wait(0.4)

        # circumscribe
        self.play(Circumscribe(VGroup(id, faceprint), color=PURE_RED), run_time=0.7)
        self.play(Circumscribe(VGroup(id, faceprint), color=PURE_RED), run_time=0.7)
        self.play(FadeOut(id, faceprint), run_time=0.4)

        self.wait(0.4)

        # Diplay CR7
        cr7 = Text("CR7 Confirmed", color=ARROW_GREEN, font="ANTON")
        cr7.scale_to_fit_width(id.width).shift(UP * 3.4)
        self.play(Write(cr7), run_time=0.9)

        self.wait(0.8)

        # fadeout everything
        to_fade = Group(cr7, ronaldo, mesh)
        self.play(FadeOut(to_fade), run_time=0.8)
        
        self.wait(0.3)

        # outro
        arrow = ImageMobject(ASSET + "\\arrow.png").scale(0.7).shift(UP * 2.4)
        self.play(GrowFromCenter(arrow), run_time=0.7)

        text = Text("@algoverselabs", font="Roboto", color=TEXT_COLOR)
        text.shift(UP * 0.24).scale(0.65)
        self.play(Write(text), run_time=0.7)
        self.wait(0.2)

        text_relative = text.get_center() - iphone.get_center()
        arrow_relative = arrow.get_center() - iphone.get_center()

        self.play(
            text.animate.move_to(ORIGIN + text_relative),
            arrow.animate.move_to(ORIGIN + arrow_relative),
            iphone.animate.move_to(ORIGIN),
            run_time=0.8
        )

        self.wait(4)