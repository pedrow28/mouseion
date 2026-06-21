#!/bin/bash
set -euo pipefail

# ─── Config ───────────────────────────────────────
PROJECT_DIR="/home/user/projects/iof-mg-engine"
VENV_PYTHON="/home/user/.hermes/hermes-agent/venv/bin/python3"
SCRIPT="${PROJECT_DIR}/iof_mg_briefing.py"
LOG_FILE="${PROJECT_DIR}/logs/cron.log"
BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
CHAT_ID="7537593368"
# ──────────────────────────────────────────────────

TODAY=$(date +%Y-%m-%d)

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Run the Python script, capturing both stdout and stderr
if "$VENV_PYTHON" "$SCRIPT" --no-vault --date "$TODAY" >> "$LOG_FILE" 2>&1; then
    STATUS="✅"
    MSG="Briefing IOF-MG Saúde de *${TODAY}* processado com sucesso."
    EXIT_CODE=0
else
    STATUS="❌"
    MSG="Briefing IOF-MG Saúde de *${TODAY}* **FALHOU**."
    EXIT_CODE=1
    # Append last 20 lines of log to the message
    LAST_LINES=$(tail -n 20 "$LOG_FILE" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
    MSG="${MSG}%0A%0A\`\`\`%0A${LAST_LINES}%0A\`\`\`"
fi

# Always notify on Telegram (success or failure)
if [[ -n "$BOT_TOKEN" ]]; then
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d "chat_id=${CHAT_ID}" \
        -d "parse_mode=Markdown" \
        -d "text=${STATUS} ${MSG}" > /dev/null || true
fi

echo "${STATUS} Briefing IOF-MG Saúde de ${TODAY} finalizado."
exit "$EXIT_CODE"
