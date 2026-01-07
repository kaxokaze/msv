import os
import PyInstaller.__main__

PyInstaller.__main__.run([
    '--distpath=%s' % "./release",
    '--name=%s' % "Mass Site Visitor",
    '--onefile',
    '--clean',
    '--windowed',
    '--noconsole',
    '--noconfirm',
    '--icon=%s' % os.path.join('assets', 'icon.ico'),
    os.path.join('obfuscated', 'siteVisitor.pyw'),
])
