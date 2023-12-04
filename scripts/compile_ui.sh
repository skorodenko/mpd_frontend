SRC="./soloviy/frontend/ui/templates"
DST="./soloviy/frontend/ui"

pyside6-rcc $SRC/icons.qrc -o $DST/icons_rc.py
pyside6-uic --from-imports -o $DST/ui_init_wizard.py $SRC/init_wizard.ui
pyside6-uic --from-imports -o $DST/ui_main_window.py $SRC/main_window.ui
pyside6-uic --from-imports -o $DST/ui_playlist_tile.py $SRC/playlist_tile.ui
pyside6-uic --from-imports -o $DST/ui_settings.py $SRC/settings.ui
