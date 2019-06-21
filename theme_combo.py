import sublime
import sublime_plugin

class SaveComboCommand(sublime_plugin.WindowCommand):
    def run(self):
        # Theme Combo: Save current combo
        def save_combo(combo_name):
            # Load the user preferences
            user_settings = sublime.load_settings('Preferences.sublime-settings')
            # Get the user combos
            theme_combos = user_settings.get("theme_combos")

            # Build a new combo
            combo = {}
            # With the current theme
            combo["theme"] = user_settings.get("theme")
            # And the current color scheme
            combo["color_scheme"] = user_settings.get("color_scheme")

            # Add or update the combo
            theme_combos[combo_name] = combo
            # Update the user preferences
            user_settings.set("theme_combos", theme_combos)
            # Save the user preferences
            sublime.save_settings("Preferences.sublime-settings")

        # Show a prompt asking for a name
        self.window.show_input_panel("Combo name:", "", save_combo, None, None)

class LoadComboCommand(sublime_plugin.WindowCommand):
    # Theme Combo: Load combo
    def run(self):
        # List of available combos
        combos = {}

        # Load package settings
        res = sublime.load_resource("Packages/ThemeCombo/Preferences.sublime-settings")
        default_settings = sublime.decode_value(res)

        # Populate default combos
        for combo_name in default_settings["theme_combos"]:
            combos[combo_name] = default_settings["theme_combos"][combo_name]

        # Load user preferences
        user_settings = sublime.load_settings('Preferences.sublime-settings')

        # Populate user combos
        if user_settings.has("theme_combos"):
            user_combos = user_settings.get("theme_combos", [])

            for combo_name in user_combos:
                combos[combo_name] = user_combos[combo_name]

        # Create a list of combo names
        options = list(combos.keys())

        def on_done(index):
            # If a combo was selected...
            if index >= 0:
                # Get the theme and color scheme
                combo_name = options[index]
                combo = combos.get(combo_name);
                theme = combo["theme"]
                color_scheme = combo["color_scheme"]

                # Load the user preferences
                user_settings = sublime.load_settings('Preferences.sublime-settings')
                # Update the theme
                user_settings.set("theme", theme)
                # Update the color scheme
                user_settings.set("color_scheme", color_scheme)
                # Save the user preferences
                sublime.save_settings('Preferences.sublime-settings')

        # Display the quick panel with a list of available combos
        self.window.show_quick_panel(options, on_done)
