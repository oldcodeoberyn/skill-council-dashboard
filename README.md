# skill-council-dashboard

This is a reusable **Hermes Agent & OpenClaw** skill for automating interactions and data querying on the **Council Dashboard V2** (`https://council-dashboard-v2.pages.dev/`).

## Installation

To import this skill into your Hermes Agent or OpenClaw instance:

```bash
hermes skill install https://github.com/oldcodeoberyn/skill-council-dashboard
```

Or clone it manually into your skills directory:
```bash
git clone https://github.com/oldcodeoberyn/skill-council-dashboard.git ~/.hermes/skills/productivity/council-dashboard
```

## Features

- **Automated Login**: Securely logs into the dashboard with your region and credentials.
- **Roster Export**: Fetches complete member lists (including custom numbers, WeChat IDs, and registration statuses).
- **Activity Metrics Tracking**: Retrieves WeChat group activity statistics.
- **Funnel Analytics**: Inspects enrollment, training coverage, and exam standard indicators.
- **Ready-to-run Script**: Run exports with a single shell command without writing any code.

## Quick Start (Built-in Script)

Install required dependencies:
```bash
pip install playwright
playwright install chromium
```

Run the built-in python script directly from the skill directory:
```bash
python scripts/export_roster.py --region "成都" --username "李捷" --password "123456" --output roster_chengdu.md
```

Options:
- `--region`: Region name (e.g., `成都`).
- `--username`: Your login name.
- `--password`: Your login password.
- `--format`: Output format, either `markdown` (default) or `json`.
- `--output`: Output file path (defaults to `roster_export.md`).

## Configuration

When using this skill, replace the placeholder credentials inside the SKILL.md file or provide them as parameters to your execution scripts:
- `<YOUR_REGION>`: E.g., `成都`
- `<YOUR_USERNAME_OR_ID>`: E.g., `李捷`
- `<YOUR_PASSWORD>`: E.g., `123456`

## Repository Structure

```
.
├── SKILL.md               # The official Hermes Agent Skill file
├── README.md              # Installation and usage instructions
└── scripts/
    └── export_roster.py   # Executable Playwright python script
```

## License

MIT License.
