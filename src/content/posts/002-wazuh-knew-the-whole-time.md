---
title: "wazuh knew the whole time"
description: "I investigated my own fake Windows incident and discovered the SIEM had the evidence the entire time. Very helpful."
publishedAt: 2026-08-09
caseNumber: "002"
status: "solved"
tags: ["wazuh", "sysmon", "incident-response"]
featured: true
readTime: "9 minutes"
---

### aka: the logs were there. nobody bothered to tell me.

after the first lab worked, i was briefly impressed with myself.

this lasted maybe five minutes.

then i realized my incredible SOC experience consisted of:

1. intentionally generate one event
2. wait for the alert i specifically designed to catch it
3. act surprised when it happens

basically solving a mystery where i wrote the answer key first.

so i wanted something messier.

an actual chain of endpoint activity where i would have to correlate multiple events instead of staring at one giant red alert like a toddler who found a shape.

i created a controlled Windows incident involving PowerShell, discovery commands, file creation, DNS activity, network connections, and a persistence-related registry change.

then i investigated it.

yes, i created the incident myself.

no, this is not cheating.

it's called a lab because “lying to your own computer and then interrogating it” sounds less employable.

## PowerShell starts reproducing

Wazuh gave me an initial alert from rule **92027**.

`powershell.exe` had spawned another `powershell.exe`.

the child ran:

```powershell
Write-Output 'PROJECT2-INITIAL-EXECUTION'; whoami; hostname
```

basically:

hello.

who am i.

where am i.

very normal questions to ask if you're either malware or somebody waking up after a terrible night.

the activity gave me process execution plus user and hostname discovery.

good starting point.

but one event doesn't tell you much.

so i kept going.

## 4,954 files because Windows hates me personally

i knew the lab had created:

`project2-stage.ps1`

inside the user's Temp directory.

Sysmon Event ID 11 records file creation.

so i searched file-creation telemetry.

**4,954 events.**

great.

apparently Windows spends all day generating files like a small child with construction paper.

somewhere inside 4,954 events was the one file i actually cared about.

so i filtered them down.

eventually:

`project2-stage.ps1`

there.

Wazuh had surfaced it as a level-15 alert.

now the timeline had:

PowerShell execution  
→ discovery  
→ script creation

then the networking activity started.

## PowerShell apparently needed internet access too

Sysmon Event ID 22 showed DNS queries to:

`example.com`

Event ID 3 showed a PowerShell-associated network connection.

`example.com` was intentional because this was a safe lab and i enjoy not explaining accidental malware traffic to my ISP.

then Event ID 13 showed:

`Project2LabTest`

written under the current user's Run key.

Run keys can execute programs when users log in.

normal software uses them.

malware also uses them.

the registry doesn't know whether you're evil. it just does what you tell it, which honestly is probably why computers keep ending up like this.

so the activity chain was now:

execution  
→ discovery  
→ script creation  
→ DNS  
→ network connection  
→ persistence-related registry change

nice.

then i checked Wazuh.

some of it wasn't there.

## what do you mean there's no alert

process creation?

yes.

file creation?

yes.

DNS?

no.

network connection?

no.

registry change?

no.

cool.

Sysmon had the events locally.

so i assumed something between Sysmon and Wazuh was broken.

again.

because apparently i had developed trust issues with my own SIEM.

i checked the raw events.

they existed.

i checked whether Wazuh decoded them.

it did.

i checked whether Wazuh had matching base rules.

it did.

so now i had reached the extremely annoying technical state of:

**everything works except the thing i can see.**

then i checked the rule levels.

Event ID 3:

rule `61605`

**level 0**

Event ID 13:

rule `61615`

**level 0**

Event ID 22:

rule `61650`

**level 0**

oh.

so Wazuh knew.

Wazuh had always known.

it just didn't think this information deserved to interrupt me.

thank you.

## what level 0 meant

this changed the entire problem.

the events were not missing.

telemetry collection worked.

decoding worked.

the base rules existed.

but these generic rules were level 0, meaning those events did not become normal analyst-visible alerts on their own.

so this wasn't:

> telemetry failure

it was:

> detection coverage

which is significantly less dramatic but significantly more important.

the data was there.

the logic deciding what should become an alert was the issue.

basically the security camera recorded everything correctly, but nobody had configured it to yell when something interesting happened.

excellent.

love systems.

## timeline

once i stopped accusing Wazuh of deleting evidence, the incident lined up pretty cleanly.

**20:39:49**  
PowerShell child process plus user/hostname discovery.

**20:43:05**  
DNS query to `example.com`.

**20:44:25**  
another DNS query.

**20:57:59**  
`project2-stage.ps1` created.

**20:59:27**  
DNS again.

**20:59:28**  
PowerShell network connection.

**21:00:46**  
Run-key registry value created.

and suddenly the logs stopped looking like random computer debris and started looking like behavior.

which is basically the entire appeal of incident response.

one event is boring.

seven related events are gossip.

## normal tools can still look bad

another thing this lab reinforced:

PowerShell isn't malicious.

DNS isn't malicious.

Run keys aren't automatically malicious.

even `example.com` obviously isn't malicious.

the important part is how the activities relate.

PowerShell spawning PowerShell, running discovery, dropping a script into Temp, generating network traffic, and modifying a persistence-related registry location?

that's different.

security analysis is mostly refusing to scream “malware” every time you see something vaguely suspicious.

which is harder than you'd think if you've spent enough time on LinkedIn.

## final result

i correlated Sysmon Event IDs:

**1, 3, 11, 13, and 22**

filtered **4,954 file-creation events** down to one relevant artifact, and reconstructed the activity timeline.

but the useful finding was that some events existed perfectly fine in the telemetry and simply weren't being surfaced as visible alerts.

so the lesson was:

**seeing something and alerting on something are not the same thing.**

which would've been nice for Wazuh to mention before i started accusing the pipeline of being broken.

whatever.

**CASE 002: CLOSED**

Wazuh knew the entire time.

really healthy communication style.
