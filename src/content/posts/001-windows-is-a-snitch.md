---
title: "Windows Is a Snitch"
description: "I installed Sysmon to make Windows report on itself. It responded by producing an amount of telemetry best described as vindictive."
publishedAt: 2026-08-01
caseNumber: "001"
status: "solved"
tags: ["sysmon", "wazuh", "siem"]
featured: true
readTime: "7 minutes"
aiGrade: "B-"
---

I thought installing Sysmon would take twenty minutes.

This was my first mistake.

## Mission brief

The objective was simple: install Sysmon on a Windows endpoint, ship the logs into Wazuh, and prove that I could see meaningful endpoint activity inside the SIEM.

My original plan:

1. Install Sysmon.
2. Connect the agent.
3. Observe logs.
4. Become employable.

The computer had other plans.

## The part where nothing talks to anything

The Wazuh agent installed successfully, which was encouraging for approximately six minutes. Then it sat there in the dashboard looking spiritually absent.

> AI confidently told me the service was running, which was technically true and operationally useless.

The actual problem was **[replace this with your real root cause]**.

```powershell
Get-Service WazuhSvc
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -MaxEvents 10
```

## Evidence

Add your screenshots here using normal Markdown:

```md
![Wazuh dashboard showing the connected endpoint](/images/case-001/wazuh-dashboard.png)
```

## AI report card

**Correct:** It helped me remember which Windows event channel Sysmon uses.

**Incorrect:** It suggested a configuration path that did not exist on my system.

**Human fix:** I checked the actual service configuration and verified each step instead of treating generated text as documentation.

## What I learned

The useful lesson was not merely “how to install Sysmon.” It was that a running service, a connected agent, and visible telemetry are three separate states—and checking only one of them is how you lose an afternoon.

The less useful lesson was that XML can sense fear.
