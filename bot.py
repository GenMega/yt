import json
import time
import requests

# 1. Define headers with a genuine Android WebView User-Agent
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-A536B Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36",
    "sec-ch-ua-platform": '"Android"',
    "x-requested-with": "XMLHttpRequest",
    "sec-ch-ua": (
        '"Android WebView";v="155", "Chromium";v="155", "Not(A:Brand";v="24"'
    ),
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua-mobile": "?1",
    "origin": "https://payup.video",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://payup.video/tasks/videoExtYT/",
    "accept-language": "en-IN,en-US;q=0.9,en;q=0.8",
    "priority": "u=1, i",
}

COOKIES = {
    "partner": "710",
    "source": "partner",
    "_ga": "GA1.1.1751980776.1792427586",
    "_ym_uid": "1792427587147522510",
    "_ym_d": "1792427587",
    "_ym_isad": "2",
    "hash": "b34a7cc0d1a712053e13113d6716096c",
    "signed": "1",
    "vignette": "1",
    "newUser": "2",
    "PHPSESSID": "j40fkl04e266c4ds36e81cjbbi",
    "_ga_5JGWQMNX26": "GS2.1.s1792427585$o1$g1$t1792427870$j59$l0$h0",
}


def run_bot():
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.update(COOKIES)

    print(
        "\n"
        + "=" * 60
        + "\n🚀 PAYUP.VIDEO AUTO-TASK BOT STARTED SUCCESSFULLY\n"
        + "=" * 60
    )

    loop_count = 1
    start_time = time.time()
    MAX_RUNTIME_SECONDS = 4.5 * 3600  # Exit gracefully after 4.5 hours for cron rotation

    while True:
        # Check if we are approaching the GitHub Actions restart window
        if time.time() - start_time > MAX_RUNTIME_SECONDS:
            print(
                "\n[⏰ TIME LIMIT REACHED] Gracefully exiting script to allow GitHub Actions cron restart."
            )
            break

        try:
            print(f"\n┌──────────────────────────────────────────────┐")
            print(f"│ 🔄 Starting Task Loop #{loop_count:<19} │")
            print(f"└──────────────────────────────────────────────┘")

            # STEP 1: Get Task Details
            print("[*] Requesting task from getExtYT.php...")
            get_url = "https://payup.video/tasks/control/getExtYT.php"
            get_body = "type=video&mac=0"

            response = session.post(get_url, data=get_body, timeout=15)
            res_json = response.json()

            if res_json.get("status") != "ok":
                error_msg = res_json.get(
                    "message", "No tasks available / restrictions"
                )
                print(f"[-] Server notice: {error_msg}")
                print("[*] Waiting 10 seconds before checking for new tasks...")
                time.sleep(10)
                continue

            task_data = res_json.get("data", {})
            task_id = task_data.get("id")
            yt_id = task_data.get("ytId", "N/A")
            balance = task_data.get("balance", "0.00")

            if not task_id:
                print("[-] Task ID not found in response. Retrying in 5 seconds...")
                time.sleep(5)
                continue

            print(f"[+] Task Acquired!")
            print(f"    ├── Task ID  : {task_id}")
            print(f"    ├── YouTube ID: {yt_id}")
            print(f"    └── Balance  : {balance}")

            # STEP 2: Start the Task
            print(f"[*] Initializing task via start.php...")
            start_url = "https://payup.video/tasks/control/start.php"

            start_body = (
                f"TaskId={task_id}"
                "&fin%5BvideoCard%5D%5Bvendor%5D=ARM"
                "&fin%5BvideoCard%5D%5Brenderer%5D=Mali-G68"
                "&fin%5BviewPort%5D%5Bh%5D=660"
                "&fin%5BviewPort%5D%5Bw%5D=384"
                "&fin%5BviewPort%5D%5BhM%5D=832"
                "&fin%5BviewPort%5D%5BwM%5D=384"
                "&fin%5Bplatform%5D=Linux%2Baarch64"
                "&fin%5Bdpr%5D=2.8125"
                "&fin%5Bmulti%5D%5Bspeakers%5D=1"
                "&fin%5Bmulti%5D%5Bmicros%5D=1"
                "&fin%5Bmulti%5D%5Bwebcams%5D=1"
                "&fin%5Bmulti%5D%5Bdevices%5D=1"
                "&fin%5Bori%5D%5Balpha%5D=124"
                "&fin%5Bori%5D%5Bbeta%5D=122.7"
                "&fin%5Bori%5D%5Bgamma%5D=-76.80000000000001"
                "&fin%5Bori%5D%5Bis%5D=1"
                "&fin%5Bv%5D=2.6"
                "&fin%5Bcl%5D%5Bx%5D=0"
                "&fin%5Bcl%5D%5By%5D=0"
                "&fin%5BwebDef%5D=false"
                "&fin%5BnavName%5D=Navigator"
                "&fin%5Btouch%5D=true"
                "&fin%5Bc%5D=155"
                "&fin%5Bmemory%5D=4"
                "&fin%5Bconcur%5D=8"
                "&fin%5Ben%5D%5Bar%5D="
                "&fin%5Ben%5D%5Bb%5D=155"
                "&fin%5Ben%5D%5Bm%5D="
                "&fin%5Ben%5D%5Bp%5D=Android"
                "&fin%5Ben%5D%5Bpv%5D="
                "&fin%5Bbat%5D%5Bcharging%5D=0"
                "&fin%5Bbat%5D%5Blvl%5D=0.23"
            )

            session.post(start_url, data=start_body, timeout=15)
            print(f"[+] Task successfully started!")

            # STEP 3: 15-Second Countdown Timer
            print("[*] Running countdown timer...")
            for remaining in range(15, 0, -1):
                print(f"⏱️  Time Remaining: {remaining:2d} seconds...", end="\r")
                time.sleep(1)
            print("⏱️  Countdown finished!                                 ")

            # STEP 4: Check Task Status / Completion
            print("[*] Verifying task completion via checkExtYT.php...")
            check_url = "https://payup.video/captcha/control/checkExtYT.php"
            check_body = "refreshTask=0"

            check_response = session.post(check_url, data=check_body, timeout=15)
            print(f"[+] Verification Response: {check_response.text.strip()}")

            print(f"✅ Loop #{loop_count} completed successfully!\n")
            loop_count += 1

            time.sleep(3)

        except requests.exceptions.RequestException as re:
            print(f"\n[⚠️ NETWORK ERROR]: {re}")
            print("[🔄 AUTO-RESTART] Reconnecting in 10 seconds...")
            time.sleep(10)
        except (KeyError, ValueError, json.JSONDecodeError) as je:
            print(f"\n[⚠️ PARSING ERROR]: Failed to interpret server response ({je})")
            print("[🔄 AUTO-RESTART] Restarting loop in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"\n[⚠️ UNEXPECTED ERROR]: {e}")
            print("[🔄 AUTO-RESTART] Recovering in 10 seconds...")
            time.sleep(10)


if __name__ == "__main__":
    run_bot()
