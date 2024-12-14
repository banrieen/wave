import gettext

# Set the local directory
appname = 'spary'
localedir = './locales'



# create the translation file 
# xgettext -d base -o spray/locales/en/spray.pot spray/report2ppt.py
# Translate message
print(_("Hello World"))
# Set up Gettext
locale = input("Please enter the preferred locale (en, fr, lv):")

appname = 'lokalise'
localedir = './locales'

translations = gettext.translation(appname, localedir, fallback=True, languages=[locale.strip()])

translations.install()

print(_("Learn Python i18n"))