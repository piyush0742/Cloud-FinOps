import subprocess
import requests
import sys

# ========================
# CONFIG
# ========================

NAMESPACE = "auth-ns"

SERVICES = [
    "order-service",
    "payment-service",
    "auth-service"
]

CONTAINER_NAME = None  # set if needed
AI_API_URL = "http://127.0.0.1:8000/summarize"

TAIL_LINES = "50"
SINCE_TIME = "5m"

# ========================
# HELPERS
# ========================

def get_pod_name(service):
    """
    Find pod for a given service
    """
    cmd = [
        "kubectl", "get", "pods",
        "-n", NAMESPACE,
        "--no-headers"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Failed to get pods for {service}")
        return None

    for line in result.stdout.splitlines():
        if service in line:
            return line.split()[0]

    return None


def get_logs(pod):
    """
    Fetch logs from pod
    """
    cmd = [
        "kubectl", "logs", pod,
        "-n", NAMESPACE,
        "--tail", TAIL_LINES,
        "--since", SINCE_TIME
    ]

    if CONTAINER_NAME:
        cmd.extend(["-c", CONTAINER_NAME])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Failed to fetch logs for pod {pod}")
        return None

    if not result.stdout.strip():
        return None

    return result.stdout


def send_to_ai(service, logs):
    """
    Send logs to AI
    """
    response = requests.post(
        AI_API_URL,
        json={
            "service": service,
            "logs": logs
        },
        timeout=30
    )

    if response.status_code != 200:
        print(f"❌ AI error for {service}")
        print(response.text)
        return None

    return response.json()

# ========================
# MAIN
# ========================

def main():
    print("\n🚀 Feeding Kubernetes logs to AI\n")

    for service in SERVICES:
        print(f"🔍 Processing service: {service}")

        pod = get_pod_name(service)
        if not pod:
            print(f"⚠️ No pod found for {service}\n")
            continue

        print(f"✅ Pod found: {pod}")

        logs = get_logs(pod)
        if not logs:
            print(f"⚠️ No logs found for {service}\n")
            continue

        print("📥 Logs fetched, sending to AI...")

        result = send_to_ai(service, logs)
        if not result:
            continue

        print(f"\n🧠 AI Summary for {service}:")
        print(result.get("summary", "No summary returned"))
        print("-" * 60)

    print("\n✅ Done processing all services\n")


if __name__ == "__main__":
    main()
