# My config:

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

keys = [
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
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
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
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    # restart Qtile:
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show run"), desc="Using rofi instead"),
    # Custom keys
    # brightness
    # Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    # Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
    # volume
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("amixer sset Master 5%-"),
        desc="Lower Volume by 5%",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("amixer sset Master 5%+"),
        desc="Raise Volume by 5%",
    ),
    # language
    Key([mod], "F1", lazy.spawn("setxkbmap us"), desc="Change to US layout"),
    Key([mod], "F2", lazy.spawn("setxkbmap ro std"), desc="Change to RO-STD layout"),
    # launch browser
    Key([mod], "i", lazy.spawn("firefox")),
    # fullscreen
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    # switch to last visited group (kinda lika alt+tab)
    Key([mod], "Tab", lazy.screen.toggle_group()),
]  # this shit ']' is important

groups = [
    Group("1", spawn=("code")),
    Group("2", spawn=("alacritty")),
    Group("3", spawn=("firefox")),
    Group("4", spawn=("chromium --new-window https://www.youtube.com")),
    Group("5")
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
        border_focus="#ADD8E6", 
        border_normal="#000000", 
        border_width=2, 
        name="",
        margin=2),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    # layout.Floating(name="~"),
]

widget_defaults = dict(
    font="Font Awesome 6 Free,Font Awesome 6 Free Regular",
    fontsize=14,
    padding=2,
)
extension_defaults = widget_defaults.copy()


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                # widget.Wttr(location={'Bucharest, Romania': 'wttr'}, foreground='#11111b', background='#f5e0dc'),
                widget.KeyboardLayout(
                    configured_keyboards=["us", "ro"],
                    foreground="#11111b",
                    background="#f5e0dc",
                ),
                widget.Net(
                    interface="enp2s0",
                    foreground="#11111b",
                    background="#cba6f7",
                    width=180,
                    format="NET:{down:6.2f}{down_suffix:<2}↓↑{up:6.2f}{up_suffix:<2}",
                ),
                widget.CPU(foreground="#11111b", background="#eba0ac", width=140),
                widget.Memory(
                    fmt="Mem: {}", foreground="#11111b", background="#fab387", width=170
                ),
                widget.DF(
                    fmt="Spc:{}",
                    format="{uf}{m}/{r:.2f}{m}/{r:.0f}%",
                    partition="/",
                    visible_on_warn=False,
                    foreground="#11111b",
                    background="#74c7ec",
                ),
                widget.Volume(
                    fmt="Vol: {}", foreground="#11111b", background="#f38ba8"
                ),
                widget.Clock(
                    format="%Y-%m-%d %a %I:%M %p",
                    foreground="#11111b",
                    background="#a6e3a1",
                ),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
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
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),
    ],
    border_normal="#000000",
    border_focus="#ADD8E6",
    border_width=4,
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True


auto_minimize = True

wl_input_rules = None

wmname = "LG3D"
