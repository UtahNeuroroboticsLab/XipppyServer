#!/bin/sh
# Checks XipppyServer.py's logging without hardware. The script blocks in the
# `while True: xp._open()` retry loop with no NIP attached, and everything
# hardware/socket-bound sits after that loop - so timing out there is fine, the
# logging has already run by then.
set -e
LOG=/var/rppl/storage/logs/XipppyServerLog.log

timeout 5 python XipppyServer.py || true   # spins in the xipppy retry loop; expected
timeout 5 python XipppyServer.py || true   # second run = restart case

echo '===== log ====='
cat "$LOG"
echo '==============='

test "$(grep -c '^### XipppyServer start' "$LOG")" -eq 2   # appended, not clobbered
grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3} \[INFO\] XipppyServer: Started' "$LOG"
grep -q 'feedbackdecode.initSS:' "$LOG"    # per-module name via propagation
grep -q 'XipppyServer: waiting on xipppy' "$LOG"

rm -rf /var/rppl/storage                   # missing storage root must be fatal
if python XipppyServer.py 2>/dev/null; then echo 'FAIL: no raise on missing RootDir'; exit 1; fi

echo OK
