---
title: "the hacker forgot how cron works"
description: "A Linux compromise involving credential theft, persistence, exfiltration, and an attacker who apparently skipped the cron documentation."
publishedAt: 2026-08-10
caseNumber: "003"
status: "solved"
tags: ["linux", "dfir", "hack-the-box"]
featured: true
readTime: "10 minutes"
---

### aka: finally somebody else fucked up the computer

by this point i had done two Windows investigations.

there was one obvious problem.

**i caused both of them.**

i knew why PowerShell ran.

i knew why the file appeared.

i knew why the registry changed.

there's only so much “investigation” you can do when the suspect is you and you remember doing it.

so i wanted something where i didn't already know the ending.

give me a machine that's already ruined.

don't tell me what happened.

let me figure it out from whatever embarrassing evidence everybody left behind.

this is how i ended up doing Hack The Box's **LuckyShot** Linux DFIR Sherlock.

the situation was basically:

company files are missing or modified.

here's the forensic evidence.

figure out what happened.

finally.

somebody else's problem.

my job was to answer things like:

- how did the attacker get in?
- what account did they use?
- what did they do after access?
- did anything get stolen?
- did they establish persistence?

basically reconstruct the night after everybody else already left.

fine.

i'm extremely nosy.

## first theory: wrong

i started by checking removable media.

maybe somebody plugged in a USB drive and copied the files.

simple.

obvious.

very CSI: Cyber.

the USB inventory showed VMware virtual devices and normal Linux root hubs.

nothing supporting removable-media exfiltration.

cool.

theory dead.

this is actually one of the better parts of forensics.

you can have whatever theory you want.

the computer does not care.

if the evidence doesn't support it, shut up and find another one.

## somebody tried every username on earth

next i looked at SSH authentication activity.

source IP:

`192.168.161.198`

and this person was trying usernames like:

`administrator`

`admin`

`default`

`ubuntu`

`root`

this is less “elite hacker” and more “guy trying every bathroom door in a restaurant.”

fail.

fail.

fail.

then:

`Accepted password for administrator`

there we go.

successful SSH access.

the exact timestamp in `auth.log` was:

`2025-02-10 19:39:03.232692 +02:00`

another login summary suggested the first success was closer to 19:41.

the raw authentication log showed an earlier event.

so the raw log won.

because summaries are helpful until they're wrong.

then they're just confident.

## bash history immediately starts tattling

after login, the attacker started doing reconnaissance.

system details.

accounts.

privileges.

normal post-compromise questions:

where am i?

who am i?

what am i allowed to ruin?

then they moved into credential access.

LaZagne was cloned and executed.

another Linux credential-recovery tool was downloaded.

then i found files named:

`Passwords_Backup.txt`

and:

`Server_Credentials.txt`

extremely subtle.

you might as well name the folder `STOLEN SHIT`.

those files were transferred out over SCP to:

`192.168.161.198`

the same IP associated with the SSH activity.

so yes.

credential data was exfiltrated.

not ideal.

## sys_monitor.sh, which sounds completely trustworthy

then i found:

`sys_monitor.sh`

any malicious file named something like “system monitor” is already annoying because it's basically wearing a little fake employee badge.

the script was tied to:

`systemd-networkm.service`

the legitimate Linux service is:

`systemd-networkd`

notice anything?

they changed **one letter**.

honestly, rude.

the service launched:

`/tmp/sys_monitor.sh`

as **root**.

and it was configured to restart.

so at this point the attacker had moved beyond:

> i know your password

into:

> i have furniture here now

## apparently they wanted every possible way back in

then i found an SSH authorized key.

its comment:

`kali@kali`

which is useful as context.

it is not attribution.

if i put `barackobama@whitehouse` in an SSH key comment, i unfortunately do not become Barack Obama.

then there was a new user:

`Regev`

added to:

`sudo`

and:

`adm`

so now the attacker had created another privileged account.

because apparently root-level persistence wasn't enough.

always good to diversify your portfolio.

at this stage:

- unauthorized SSH access
- credential recovery
- credential exfiltration
- malicious script
- systemd persistence
- attacker SSH key
- new privileged account

very restrained behavior.

## root's shell configuration was also ruined

root's `.bashrc` and `.profile` contained Ncat listener commands.

ports:

`7575`

and:

`9000`

that meant network listeners had been **configured** to launch under certain shell-startup conditions.

configured.

important word.

i had evidence the commands existed.

i did **not** have runtime evidence proving both listeners were actively running when the forensic snapshot was collected.

this is the part of forensic reporting where you have to become extremely annoying about language.

you can't say:

> they definitely ran

just because:

> they were configured to run

evidence doesn't care what would probably happen.

**configured ≠ observed.**

i hate it too.

## then cron completely humiliated the attacker

eventually i found:

`/etc/cron.d/syscheck`

the cron file was designed to fetch a payload, reverse it, Base64-decode it, and pipe it into Bash.

which is the sort of command sequence that usually indicates your afternoon is about to get worse.

so i checked syslog to see whether cron actually executed it.

response:

**bad minute**

...

they wrote the cron schedule wrong.

i'm sorry.

you brute-forced your way into a Linux machine.

dumped credentials.

stole files.

installed a root systemd service.

added an SSH key.

created a privileged account.

modified root shell startup files.

then lost to cron syntax.

imagine robbing a bank successfully and then getting trapped in the parking garage because you can't validate your ticket.

awful.

## unfortunately, this distinction matters

the funny part is that this changed how the finding had to be reported.

the malicious cron file existed.

the attacker clearly intended it as persistence.

but syslog showed cron rejected it.

therefore:

**attempted cron persistence:** yes.

**successful cron persistence:** no.

meanwhile the systemd persistence had stronger evidence of actual execution.

so they don't get described the same way.

you have to distinguish between:

**observed**

**configured**

and:

**attempted**

because apparently “the attacker obviously wanted this to happen” is not a forensic artifact.

## what happened

the evidence supported this sequence:

someone at `192.168.161.198` repeatedly attempted SSH logins.

eventually they successfully authenticated as `administrator`.

they performed system and privilege discovery.

they ran credential-recovery tooling.

they exfiltrated credential files with SCP.

they executed `sys_monitor.sh`.

they established root-level persistence through a deceptive systemd service.

they added an SSH authorized key.

they created privileged user `Regev`.

they modified root's shell configuration with Ncat listener commands.

and they attempted to establish additional persistence through cron.

attempted.

because they couldn't write cron syntax.

## final result

this was the first investigation where i genuinely didn't know what happened before i started.

and that made the process way more interesting.

every artifact changed the story.

the USB theory died.

the raw authentication log corrected the initial timeline.

bash history exposed credential activity.

systemd showed successful persistence.

shell configuration showed additional access mechanisms.

cron showed intent and then immediately showed failure.

which is basically what DFIR is:

somebody does a bunch of stupid things to a computer.

then you arrive later and determine **exactly which stupid things can actually be proven.**

**CASE 003: CLOSED**

attacker got root.

cron still told them to fuck off.
