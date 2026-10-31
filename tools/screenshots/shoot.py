"""Drives Hanuchi through a few screens and saves each one as a PNG.

Runs inside the screenshot container (see run.sh): shoot.py APP OUTDIR
"""
import importlib.machinery
import importlib.util
import io
import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, GLib, Graphene, Gtk
from PIL import Image, ImageDraw, ImageFilter

SCALE = 2          # HiDPI shots, sharp on GitHub
RADIUS = 12        # Adwaita window corner radius
SHADOW = 24        # blur of the drop shadow, in logical px


def load_app(path):
    loader = importlib.machinery.SourceFileLoader("hanuchi", path)
    spec = importlib.util.spec_from_loader("hanuchi", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def grab(widget):
    """Render a toplevel to a PIL image at SCALE."""
    w, h = widget.get_width(), widget.get_height()
    snap = Gtk.Snapshot()
    snap.scale(SCALE, SCALE)
    Gtk.WidgetPaintable.new(widget).snapshot(snap, w, h)
    rect = Graphene.Rect().init(0, 0, w * SCALE, h * SCALE)
    tex = widget.get_native().get_renderer().render_texture(snap.to_node(), rect)
    data = tex.save_to_png_bytes().get_data()
    return Image.open(io.BytesIO(data)).convert("RGBA")


def frame(img):
    """Round the corners and drop a soft shadow, like a window on a desktop."""
    r, pad = RADIUS * SCALE, SHADOW * SCALE
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *img.size), r, fill=255)
    img.putalpha(mask)

    w, h = img.size
    out = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    shadow = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (pad, pad + pad // 4, pad + w, pad + h + pad // 4), r, fill=(0, 0, 0, 90))
    out.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(pad / 2.5)))
    out.alpha_composite(img, (pad, pad))
    return out


def with_dialog(win_img, dlg_img):
    """Put a dialog over its dimmed parent, the way libadwaita shows it in-window."""
    out = win_img.copy()
    out.alpha_composite(Image.new("RGBA", out.size, (0, 0, 0, 70)))
    # The floating dialog's surface carries a faint margin around the card;
    # keep only the card itself.
    alpha = dlg_img.getchannel("A").point(lambda a: a if a > 200 else 0)
    dlg_img.putalpha(alpha)
    x = (out.width - dlg_img.width) // 2
    y = (out.height - dlg_img.height) // 2
    out.alpha_composite(dlg_img, (x, y))
    return out


def main():
    app_path, outdir = sys.argv[1], sys.argv[2]
    hanuchi = load_app(app_path)
    style = Adw.StyleManager.get_default()

    class App(hanuchi.HanuchiApp):
        def do_activate(self):
            win = hanuchi.HanuchiWindow(self)
            win.present()
            steps = []

            def save(img, name):
                frame(img).save(f"{outdir}/{name}.png")
                print("saved", name, flush=True)

            def select(i):
                win.list_box.select_row(win.list_box.get_row_at_index(i))

            def dialogs():
                return [t for t in Gtk.Window.list_toplevels() if t is not win and t.get_mapped()]

            def shot_network():
                select(0)

            def shot_network_save():
                save(grab(win), "network")
                win.go_dashboard()

            def shot_dashboard():
                save(grab(win), "dashboard")
                win.network_dialog("join")

            def shot_join():
                ds = dialogs()
                img = grab(win)
                if ds:
                    img = with_dialog(img, grab(ds[0]))
                save(img, "join")
                for d in ds:
                    d.close()
                style.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
                select(1)

            def shot_dark():
                save(grab(win), "dark")
                self.quit()

            steps = [shot_network, shot_network_save, shot_dashboard, shot_join, shot_dark]

            def run_next():
                steps.pop(0)()
                return bool(steps)
            # Give the first refresh time to land, then one step every 1.5 s.
            GLib.timeout_add(3000, lambda: GLib.timeout_add(1500, run_next) and False)

    App().run([])


if __name__ == "__main__":
    main()
