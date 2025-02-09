
from __future__ import annotations
from typing import Iterable

from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes


class CustomTheme(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.rose,
        secondary_hue: colors.Color | str = colors.amber,
        neutral_hue: colors.Color | str = colors.gray,
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_md,
        text_size: sizes.Size | str = sizes.text_lg,
        font: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("Quicksand"),
            "ui-sans-serif",
            "sans-serif",
        ),
        font_mono: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("IBM Plex Mono"),
            "ui-monospace",
            "monospace",
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        super().set(
            # 🌅 **New Elegant Background**
            body_background_fill="""
                radial-gradient(circle at top left, *primary_200, *secondary_100),
                linear-gradient(120deg, *primary_300, *secondary_200)
            """,
            body_background_fill_dark="""
                radial-gradient(circle at bottom right, *primary_800, *secondary_600),
                linear-gradient(120deg, *primary_900, *secondary_700)
            """,

            # 🔘 Dark Grey Buttons with Hover Effect
            button_primary_background_fill="#4A4A4A",
            button_primary_background_fill_hover="#6A6A6A",
            button_primary_text_color="white",
            button_primary_background_fill_dark="#3A3A3A",
            button_primary_shadow="0px 4px 12px rgba(0,0,0,0.3)",

            # 🖱️ Other UI Elements
            slider_color="*secondary_300",
            slider_color_dark="*secondary_600",
            block_title_text_weight="600",
            block_border_width="3px",
            block_shadow="*shadow_drop_lg",
            button_large_padding="32px",
        )