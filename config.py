# Dependencies:
# python-psutil
# alsa-utils
# rofi
# nitrogen
# picom

# Standard imports
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# Custom imports
from check_internet_widget import check_connectivity

import subprocess


@hook.subscribe.startup_once
def autostart():
    # Set the wallpaper using nitrogen
    subprocess.Popen(
        [
            "nitrogen",
            "--set-zoom-fill",
            "/home/feralsmurf/Downloads/Wallpapers/forestx.jpg",
        ]
    )
    # Start picom
    subprocess.Popen(["picom"])


# Maximize all apps running in the background
@lazy.group.function
def maximize_all(group):
    for win in group.windows:
        if win.minimized:
            win.toggle_minimize()


mod = "mod4"
terminal = guess_terminal()

keys = [
    # Show all active Window
    Key([mod], "o", lazy.spawn("rofi -show window")),
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show run"), desc="rofi"),
    Key([mod], "d", lazy.spawn("rofi -show window"), desc="rofi show running windows"),
    # Max all
    Key(
        [mod, "shift"],
        "m",
        maximize_all,
        desc="Unminimize all windows in current group",
    ),
    # Max/Min
    Key([mod], "m", lazy.window.toggle_maximize(), desc="Toggle maximize"),
    Key([mod], "n", lazy.window.toggle_minimize(), desc="Toggle minimize"),
    ############
    # Language #
    ############
    Key([mod], "F1", lazy.spawn("setxkbmap us"), desc="Change to US layout"),
    Key([mod], "F2", lazy.spawn("setxkbmap ro std"), desc="Change to RO-STD layout"),
    ##############
    # Media keys #
    ##############
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("amixer -q sset Master 5%-"),
        desc="Lower Volume by 5%",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("amixer -q sset Master 5%+"),
        desc="Raise Volume by 5%",
    ),
]

groups = [Group(i) for i in "123456789"]

groups = [
    Group("1", label="1 dev"),
    Group("2", label="2 www", spawn=["chromium"]),
    Group("3", label="3 term", spawn=["alacritty -e fish -c 'wttr; exec fish'"]),
    Group("4", label="4 files"),
    Group(
        "5",
        label="5 docs",
    ),
    Group("6", label="6 media"),
    Group(
        "7",
        label="7 misc",
    ),
]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

layouts = [
    layout.Columns(
        border_focus="#74c7ec",
        border_normal="#1e1e2e",
        border_width=2,
        margin=4,
        name="",
    ),
]

widget_defaults = dict(
    font="DejaVu Nerd Font Bold",
    fontsize=14,
    padding=2,
    foreground="#cdd6f4",
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(
                    this_current_screen_border="#a6e3a1",
                    highlight_method="line",
                    background="#1e1e2e",
                    highlight_color="#1e1e2e",
                    foreground="#cdd6f4",
                    active="#cdd6f4",
                ),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#f38ba8", "#ffffff"),
                    },
                    nae_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                widget.TextBox(fmt="bg{}"),  # shows some text after Systray
                widget.Clipboard(fmt="Yanked!"),
                widget.KeyboardLayout(
                    fmt="🎹 {}",
                    configured_keyboards=["us", "ro"],
                    display_map={"us": "std"},
                ),
                widget.GenPollText(func=check_connectivity, update_interval=10),
                widget.OpenWeather(
                    location="Bucharest",
                    format="~{temp:.0f}°, {pressure}hPa, {wind_speed:.0f}km/h, {humidity}%H, {weather}",
                    fmt="🏙️ {} ",
                    app_key="0ec6327bcee56539cbf468aaffd0bb79",
                    update_interval=60,
                ),
                widget.DF(
                    partition="/home",
                    format="{uf}{m} free ",
                    fmt="💾 {}",
                    visible_on_warn=False,
                ),
                widget.Memory(
                    fmt="🐏 {} ",
                    measure_mem="G",
                    format="{MemUsed:.0f}{mm}|{MemTotal:.0f}{mm}",
                ),
                widget.CPU(
                    fmt="🧠 {} ",
                    format="{freq_current}GHz|{load_percent:.0f}%",
                    width=105,
                ),
                # widget.ThermalSensor(
                #     fmt="🔥 {}", format="{temp:.0f}{unit}", tag_sensor="Package id 0"
                # ),
                widget.Volume(fmt="📢 {} "),
                widget.Clock(format="%Y.%m.%d %a %I:%M", fmt="⏳️ {} "),
            ],
            24,
            background="#1e1e2e",
        ),
    ),
]

mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_focus="#a6e3a1",
    border_normal="#1e1e2e",
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True

wl_input_rules = None

wmname = "LG3D"
