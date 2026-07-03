---
name: council-dashboard
description: "Use when you need to automate queries, fetch member rosters, or analyze activity data on the Council Dashboard V2."
version: 1.0.1
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [council, dashboard, automation, playwright, api, roster]
    related_skills: [cost-optimized-automation]
---

# Council Dashboard V2 Automation

## Overview
This skill provides structured recipes, API mappings, and an executable script for automating user-level and manager-level tasks on the Council Dashboard V2 (`https://council-dashboard-v2.pages.dev/`). It details the login mechanism, session management, and specific API endpoints for querying member rosters, WeChat community activity, growth logs, and dashboard overview metrics.

## When to Use
- When you need to retrieve member lists, rosters, or verify registration status for a region.
- When you need to extract WeChat active engagement data or growth logs.
- When you need to analyze the recruitment funnel, training coverages, or test results on the dashboard.

### Don't use for:
- Standard public articles unless they require authenticated access.

---

## Executing the Built-in Automation Script

The skill includes a ready-to-run automation script `scripts/export_roster.py` which can export a region's member list directly to a Markdown table or JSON file.

### Usage:
```bash
python scripts/export_roster.py --region <REGION> --username <USERNAME> --password <PASSWORD> [--format markdown|json] [--output <FILE_PATH>]
```

### Examples:
1. Export Chengdu region roster as a Markdown table (default):
   ```bash
   python scripts/export_roster.py --region "成都" --username "李捷" --password "123456" --output roster_chengdu.md
   ```
2. Export as raw JSON:
   ```bash
   python scripts/export_roster.py --region "成都" --username "李捷" --password "123456" --format json --output roster.json
   ```

---

## API Reference

### 1. Authentication
* **Endpoint**: `POST https://council-dashboard-v2.pages.dev/api/login`
* **Content-Type**: `application/json`
* **Payload**:
  ```json
  {
    "region": "<YOUR_REGION>",
    "identifier": "<YOUR_USERNAME_OR_ID>",
    "pwd": "<YOUR_PASSWORD>"
  }
  ```

### 2. Council Dashboard Overview
* **Endpoint**: `GET https://council-dashboard-v2.pages.dev/api/dashboard`
* **Query Parameters**:
  * `region`: Region name (e.g., `成都`)
  * `ptype`: Statistical period (`all`, `week`, `month`)
  * `include_region_summary`: `1`
  * `_t`: `{timestamp}`

### 3. Member Roster (Detailed / Admin)
* **Endpoint**: `GET https://council-dashboard-v2.pages.dev/api/admin/members`
* **Query Parameters**:
  * `region`: Region name (e.g., `成都`)
  * `summary`: `1`
  * `count`: `1` (return total count)
  * `sort`: Sort field (e.g., `join_time`, `growth_total`, `member_no`)
  * `dir`: Order (`desc` or `asc`)
  * `limit`: Max records to return (e.g., `100`)
  * `offset`: Pagination offset (e.g., `0`)

### 4. WeChat Community Activity
* **Endpoint**: `GET https://council-dashboard-v2.pages.dev/api/admin/wechat_activity`
* **Query Parameters**:
  * `region`: Region name
  * `period_type`: Filtering period (`week`, `month`)
  * `limit`: Max records (e.g., `80`)

### 5. Growth Scores & Rankings
* **Endpoint**: `GET https://council-dashboard-v2.pages.dev/api/admin/growth_log`
* **Query Parameters**:
  * `region`: Region name
  * `period`: Filter period (`week`, `month`, `all`)
  * `view`: View type (`rank` or `detail`)

---

## Common Pitfalls

1. **Permission / Scope Constraints**:
   Logged-in accounts (like those with `regional_council` scope) can only query their own assigned region. Passing other regions to the query parameters will still return data bound to their assigned region.

2. **Sequential工号 vs Join Time**:
   Some newly registered members may have an empty `join_time` field. They can be identified by their sequential member codes (`TM000...`) or `member_no` being larger than prior established entries.

3. **Session Timing**:
   Ensure `await page.goto(".../council")` is executed prior to calling the API internally, as it sets up necessary localized storage and context routing.

## Verification Checklist

- [ ] Authenticated successfully and redirected from `/login` to `/member` or `/council`.
- [ ] API calls return `{"ok": true}` status block.
- [ ] List limit is large enough to cover the region's roster (e.g. `limit=100`).
