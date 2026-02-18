> [!WARNING]
> ## Archived
> This project is archived and no longer maintained.
>
> Appier is no longer in active use, so this scaffold has been retired. It remains available as a reference but will not receive updates or bug fixes.

<div align="center">
  <img src="logo.png" alt="appier_scaffold" width="512"/>

  [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
  [![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

  **🏗️ Starter scaffold for Appier web apps with authentication baked in 🐝**

</div>

---

## Overview

**The Pain:** Starting a new Appier web app means wiring up authentication from scratch — signup, signin, password recovery, account models, templates, and a scheduler — every single time.

**The Solution:** `appier_scaffold` is a ready-to-run starter project that bundles all of that boilerplate into a single clone-and-go scaffold.

**The Result:** Skip the repetitive setup and jump straight into building your app logic.

## Features

- **Authentication out of the box** — signup, signin, password recovery, and reset flows included
- **Account model** — base account model with extension points
- **Template set** — pre-built HTML templates for all auth pages (signin, signup, recover, reset, error pages)
- **Scheduler integration** — background task scheduler wired into the app
- **Configuration-driven** — `appier.json` for server, email, and app settings
- **Netius server** — configured to run with the Netius async HTTP server

## Project Structure

```
src/
  controllers/       # Request handlers (base + account)
  models/            # Data models (base + account)
  templates/         # HTML templates for auth flows
  static/            # Static assets (CSS, JS, libs)
  appier.json        # App configuration
  scheduler.py       # Background scheduler
  test.py            # App entry point
```

## Quick Start

```bash
git clone https://github.com/tsilva/appier_scaffold.git
cd appier_scaffold
pip install appier netius
python src/test.py
```

The app starts on `http://localhost:8080` by default.

Configure `src/appier.json` to set your app name, email (SMTP), and server settings before deploying.

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.
