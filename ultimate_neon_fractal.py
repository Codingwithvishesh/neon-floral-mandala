
import cv2
import numpy as np
import math

# ==================================================
# ULTIMATE NEON FRACTAL FLOWER
# ==================================================

WIDTH = 1024
HEIGHT = 768
FPS = 30
DURATION = 12

OUTPUT = "ultimate_neon_fractal.mp4"

TOTAL_FRAMES = FPS * DURATION
CX = WIDTH // 2
CY = HEIGHT // 2
SCALE = HEIGHT * 0.47

LAYERS = 100
SAMPLES = 2400
REVEAL_SECONDS = 7.0


# ==================================================
# NEON COLOR FUNCTION
# ==================================================

def neon_color(hue, saturation=1.0, value=1.0):
    hsv = np.uint8([[
        [
            int(hue) % 180,
            int(np.clip(saturation, 0, 1) * 255),
            int(np.clip(value, 0, 1) * 255)
        ]
    ]])

    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0, 0]

    return tuple(int(channel) for channel in bgr)


# ==================================================
# CREATE MATHEMATICAL FLOWER CURVES
# ==================================================

def create_curves():
    theta = np.linspace(
        0,
        2 * math.pi,
        SAMPLES,
        endpoint=True
    )

    curves = []

    for i in range(LAYERS):
        fraction = i / (LAYERS - 1)

        layer_scale = 0.13 + 0.87 * fraction

        radius = SCALE * layer_scale

        petal = np.abs(np.cos(2 * theta))

        radial = (
            0.15
            + 0.85 * np.power(petal, 0.68)
        )

        ripple = (
            1.0
            + 0.035 * np.sin(18 * theta + i * 0.12)
            + 0.015 * np.sin(43 * theta - i * 0.08)
            + 0.008 * np.cos(71 * theta + i * 0.04)
        )

        angle = (
            theta
            + 0.025 * np.sin(4 * theta + i * 0.03)
        )

        r = radius * radial * ripple

        x = CX + r * np.cos(angle)
        y = CY + r * np.sin(angle)

        points = np.column_stack((x, y))
        points = points.astype(np.int32)

        curves.append((points, fraction, i))

    return curves


CURVES = create_curves()


# ==================================================
# DRAW PART OF A CURVE
# ==================================================

def draw_curve(canvas, points, color, thickness=1,
               fraction=1.0):

    count = int(len(points) * fraction)
    count = max(2, min(count, len(points)))

    visible_points = points[:count].reshape(-1, 1, 2)

    cv2.polylines(
        canvas,
        [visible_points],
        False,
        color,
        thickness,
        cv2.LINE_AA
    )


# ==================================================
# BACKGROUND
# ==================================================

def create_background():
    background = np.zeros(
        (HEIGHT, WIDTH, 3),
        dtype=np.uint8
    )

    background[:] = (1, 0, 3)

    rng = np.random.default_rng(42)

    star_x = rng.integers(0, WIDTH, 250)
    star_y = rng.integers(0, HEIGHT, 250)
    star_brightness = rng.integers(3, 17, 250)

    for x, y, brightness in zip(
        star_x, star_y, star_brightness
    ):
        background[y, x] = (
            int(brightness),
            int(brightness // 2),
            int(brightness)
        )

    return background


BACKGROUND = create_background()


# ==================================================
# RENDER ONE FRAME
# ==================================================

def render_frame(frame_number):

    time_seconds = frame_number / FPS

    progress = min(
        1.0,
        time_seconds / REVEAL_SECONDS
    )

    glow = np.zeros(
        (HEIGHT, WIDTH, 3),
        dtype=np.uint8
    )

    sharp = np.zeros_like(glow)

    # Reveal curves progressively from the center outward.
    active_layers = max(
        1,
        min(LAYERS, int(progress * LAYERS) + 1)
    )

    for i in range(active_layers):

        points, layer_fraction, index = CURVES[i]

        hue = (
            116
            + 30 * layer_fraction
            + 4 * math.sin(
                time_seconds * 0.7 + i * 0.1
            )
        ) % 180

        color = neon_color(hue)

        # Progressively trace the newest curve.
        if i == active_layers - 1 and progress < 1.0:
            reveal_fraction = (
                progress * LAYERS
            ) % 1.0

            reveal_fraction = max(
                0.04,
                reveal_fraction
            )
        else:
            reveal_fraction = 1.0

        thickness = 3 if i % 8 == 0 else 2

        draw_curve(
            glow,
            points,
            color,
            thickness,
            reveal_fraction
        )

        # Thin highlights create detailed filaments.
        if i % 2 == 0:
            highlight = neon_color(
                hue + 5,
                0.6,
                1.0
            )

            draw_curve(
                sharp,
                points,
                highlight,
                1,
                reveal_fraction
            )

    # ==================================================
    # OUTER ENERGY FILAMENTS
    # ==================================================

    if progress > 0.25:

        wisp_progress = min(
            1.0,
            (progress - 0.25) / 0.5
        )

        for side in range(4):

            base_angle = side * math.pi / 2

            for j in range(36):

                start_radius = SCALE * (
                    0.35 + j * 0.006
                )

                end_radius = SCALE * (
                    0.67 + j * 0.009
                )

                f = np.linspace(
                    0.0,
                    wisp_progress,
                    120
                )

                radius = (
                    start_radius
                    + (end_radius - start_radius) * f
                )

                angle = (
                    base_angle
                    + 0.025 * np.sin(
                        f * 13 + j * 0.3
                    )
                )

                x = CX + radius * np.cos(angle)
                y = CY + radius * np.sin(angle)

                points = np.column_stack(
                    (x, y)
                ).astype(np.int32)

                color = neon_color(
                    125 + j * 0.8 + time_seconds
                )

                cv2.polylines(
                    glow,
                    [points.reshape(-1, 1, 2)],
                    False,
                    color,
                    1,
                    cv2.LINE_AA
                )

    # ==================================================
    # CINEMATIC GLOW
    # ==================================================

    broad_glow = cv2.GaussianBlur(
        glow,
        (0, 0),
        17
    )

    tight_glow = cv2.GaussianBlur(
        glow,
        (0, 0),
        5
    )

    frame = cv2.addWeighted(
        BACKGROUND,
        1.0,
        broad_glow,
        0.75,
        0
    )

    frame = cv2.addWeighted(
        frame,
        1.0,
        tight_glow,
        0.90,
        0
    )

    frame = cv2.addWeighted(
        frame,
        1.0,
        glow,
        0.80,
        0
    )

    frame = cv2.addWeighted(
        frame,
        1.0,
        sharp,
        1.0,
        0
    )

    # ==================================================
    # GLOWING CENTER
    # ==================================================

    pulse = 3 + int(
        2 * (
            0.5
            + 0.5 * math.sin(time_seconds * 4)
        )
    )

    center_color = neon_color(
        125 + time_seconds * 3,
        0.45,
        1.0
    )

    cv2.circle(
        frame,
        (CX, CY),
        pulse + 5,
        center_color,
        1,
        cv2.LINE_AA
    )

    cv2.circle(
        frame,
        (CX, CY),
        2,
        (255, 245, 255),
        -1,
        cv2.LINE_AA
    )

    # ==================================================
    # PROGRESS BAR
    # ==================================================

    bar_y = HEIGHT - 20

    cv2.rectangle(
        frame,
        (20, bar_y),
        (WIDTH - 20, bar_y + 2),
        (20, 15, 28),
        -1
    )

    fill_x = 20 + int(
        (WIDTH - 40) * progress
    )

    cv2.rectangle(
        frame,
        (20, bar_y),
        (fill_x, bar_y + 2),
        neon_color(125 + time_seconds * 2),
        -1
    )

    return frame


# ==================================================
# MAIN VIDEO RENDERER
# ==================================================

def main():

    print("=" * 45)
    print("ULTIMATE NEON FRACTAL FLOWER")
    print("=" * 45)

    print(f"Resolution: {WIDTH} x {HEIGHT}")
    print(f"FPS: {FPS}")
    print(f"Duration: {DURATION} seconds")
    print("Step-by-step reveal enabled.")
    print("Rendering started...")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        OUTPUT,
        fourcc,
        FPS,
        (WIDTH, HEIGHT)
    )

    if not writer.isOpened():
        raise RuntimeError(
            "Video writer could not open. "
            "Check OpenCV installation and folder permissions."
        )

    try:

        for frame_number in range(TOTAL_FRAMES):

            frame = render_frame(frame_number)

            writer.write(frame)

            if frame_number % FPS == 0:

                percentage = int(
                    frame_number / TOTAL_FRAMES * 100
                )

                print(
                    f"Rendering progress: {percentage}%"
                )

    finally:
        writer.release()

    print()
    print("RENDER COMPLETE!")
    print(f"Video saved as: {OUTPUT}")


if __name__ == "__main__":
    main()
