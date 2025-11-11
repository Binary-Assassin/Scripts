# Fuzzing Guide — Sequential (PowerShell + ffuf)

> Minimal, reliable instructions.

## Prerequisites

* **PowerShell 7+** (pwsh) for running the provided scripts. Install via `winget install --id Microsoft.PowerShell -e` or download MSI from the PowerShell releases.
* **ffuf** (native `ffuf.exe`) in PATH, or WSL with ffuf installed.
* `ips.txt` — list of targets (format below).
* `wordlist.txt` — newline-separated list of paths to fuzz (no leading `/`).
* Permission to test targets.

---

## Provided commands

Run the sequential ffuf runner (explicit pwsh path, recommended if pwsh not on PATH):

```powershell
& "C:\Program Files\PowerShell\7\pwsh.exe" -NoProfile -ExecutionPolicy Bypass .\Fuzz-Sequential-FFUF.ps1 -IpsFile .\ips.txt -Wordlist .\wordlist.txt -OutDir .\results -Threads 40 -TimeoutSec 10
```

Or (if `pwsh` is available in PATH):

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass .\Fuzz-Sequential-FFUF.ps1 -IpsFile .\ips.txt -Wordlist .\wordlist.txt -OutDir .\results -Threads 40 -TimeoutSec 10
```

---

## `ips.txt` format (one entry per line)

Acceptable entries (comments and blank lines supported):

```
# plain host or IP
192.168.1.10
example.com

# or with scheme (script respects explicit scheme)
http://10.0.0.5
https://web.example.org:8443

# comments/blank lines ignored (lines starting with #)
```

> If scheme is omitted, scripts default to `http://` unless you run HTTPS detection.

---

## Output

* Per-host JSON (raw ffuf output) and per-host `.txt` files containing lines of the form:

```
<URL>\t<STATUS>\t<LENGTH>
```

* Output directory defaults to `./results` (or the path you pass via `-OutputDir` / `-OutDir`).

---

## Key takeaways

* Start small: test with a short wordlist and low thread counts to avoid noisy traffic.
* Increase `-Threads` for ffuf if you need higher throughput, but monitor target stability.
* Always obtain authorization before testing.

---

## Troubleshooting

* If `pwsh` not found after install, either open a new terminal session or run the explicit path:
  `"C:\Program Files\PowerShell\7\pwsh.exe"`.
* If `ffuf` not found: download `ffuf.exe` to a PATH directory or use WSL (`sudo apt install ffuf`) and run the script with WSL-compatible options.

---

## Next steps tbd (optional)

* Integrate a pre-scan (nmap/masscan) to filter hosts with ports 80/443 open before fuzzing.
* Add logging/centralized storage for results if you scale beyond dozens of hosts.

*End of file.*
