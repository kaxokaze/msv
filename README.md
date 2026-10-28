# Mass Site Visitor
This is the source code for a somewhat popular traffic generating bot, which I actively maintained and sold between 2016-2023. I share this as a legacy for a program that ended up gathering over a thousand users over time. This source code is shared for educational purposes, I no longer intend to make any profits from MSV, as I am focused on other things currently.


## Development setup

The application currently uses legacy Selenium 3 WebDriver APIs and bundled browser drivers. For a local development environment, create a virtual environment and install dependencies from `requirements.txt`:

```powershell
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the GUI from the repository root on Windows:

```powershell
python siteVisitor.pyw
```

Notes:
- Run only against websites you own or are explicitly authorized to test.
- A modern Selenium 4 migration and cross-platform driver discovery are not yet implemented.
- The legacy bundled browser drivers and browser integrations may not work with current browser releases.
- The repository does not yet include an automated test suite for the GUI or browser integration.
