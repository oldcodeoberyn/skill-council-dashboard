import asyncio
import json
import argparse
import sys
from playwright.async_api import async_playwright

async def export_roster(region, username, password, output_format, output_path):
    print(f"[*] Launching browser for {region} (User: {username})...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # 1. Log in
            print("[*] Navigating to login page...")
            await page.goto("https://council-dashboard-v2.pages.dev/login")
            await page.select_option("#region", value=region)
            await page.fill("#identifier", username)
            await page.fill("#pwd", password)
            await page.click("button[type='submit']")
            await page.wait_for_timeout(3000)
            
            if "login" in page.url:
                print("[!] Login failed. Please check your credentials and region.")
                return False
            
            print("[+] Login successful! Navigating to council dashboard...")
            await page.goto("https://council-dashboard-v2.pages.dev/council")
            await page.wait_for_timeout(3000)
            
            # 2. Call admin roster API
            print("[*] Querying member roster API...")
            api_url = f"https://council-dashboard-v2.pages.dev/api/admin/members?region={region}&summary=1&count=1&limit=200"
            response_json = await page.evaluate(f"""
                async () => {{
                    const response = await fetch("{api_url}");
                    return await response.json();
                }}
            """)
            
            if not response_json.get("ok"):
                print("[!] API call failed:", response_json)
                return False
                
            members = response_json.get("members", [])
            print(f"[+] Retrieved {len(members)} members successfully.")
            
            # 3. Format & Export
            if output_format == "json":
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(members, f, ensure_ascii=False, indent=2)
                print(f"[+] Exported JSON to {output_path}")
            else:
                # Markdown format
                lines = [
                    f"# Council Member Roster - {region}",
                    f"Total Members: {len(members)}\n",
                    "| No | Code | Name | Join Time | Growth Total | WeChat |",
                    "| :--- | :--- | :--- | :--- | :--- | :--- |"
                ]
                # Sort descending by member number
                sorted_m = sorted(members, key=lambda x: x.get("member_no", 0) if x.get("member_no") else 9999, reverse=True)
                for m in sorted_m:
                    no = m.get("member_no", "N/A")
                    code = m.get("member_code", "N/A")
                    name = m.get("name", "N/A")
                    jt = m.get("join_time", "N/A") or "N/A"
                    gt = m.get("growth_total", 0)
                    wc = m.get("wechat", "N/A")
                    lines.append(f"| {no} | {code} | {name} | {jt} | {gt} | {wc} |")
                
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))
                print(f"[+] Exported Markdown Table to {output_path}")
                
            return True
        except Exception as e:
            print("[!] Exception occurred:", e)
            return False
        finally:
            await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Council Dashboard Roster")
    parser.add_argument("--region", required=True, help="Region name (e.g. 成都)")
    parser.add_argument("--username", required=True, help="Username")
    parser.add_argument("--password", required=True, help="Password")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"], help="Output format")
    parser.add_argument("--output", default="roster_export.md", help="Output file path")
    args = parser.parse_args()
    
    success = asyncio.run(export_roster(args.region, args.username, args.password, args.format, args.output))
    sys.exit(0 if success else 1)
