---
title: "windows is a snitch"
description: "I wanted SOC experience and apparently the solution was creating more problems for myself with several computers."
publishedAt: 2026-08-08
caseNumber: "001"
status: "solved"
tags: ["sysmon", "wazuh", "siem"]
featured: true
readTime: "8 minutes"
---

### aka: i was bored so i gave myself an IT problem

i was bored.

which is usually how bad decisions start, except this one was technically career development so everybody has to pretend it was productive.

i needed cybersecurity portfolio projects.

i already had Security+, which is cool if your career goal is explaining what a firewall is to somebody's uncle.

i wanted actual SOC experience.

small problem:

i did not work in a SOC.

so i decided to build one at home.

because apparently when normal people are unemployed and bored they watch Netflix, and when i do it i install enterprise security software on random computers in my bedroom.

whatever.

i had:

- a Windows PC
- a MacBook
- an Ubuntu VM
- the internet
- no reason to believe this would go smoothly

the goal was pretty simple.

i wanted to understand what actually happens between:

**Windows does something weird**

and:

**some exhausted analyst gets an alert about it**

because cybersecurity courses love saying things like *endpoint telemetry gets ingested into the SIEM.*

great.

that sentence means nothing to me unless i can watch it happen.

so the plan was:

Windows does something  
↓  
Sysmon records it  
↓  
Wazuh gets it  
↓  
Wazuh decides whether it cares  
↓  
i stare at a dashboard and become employable somehow

easy.

the first thing that happened was Ubuntu wouldn't start.

of course.

## apparently turning the computer on was part of the lab

my Wazuh manager was running inside an Ubuntu ARM64 virtual machine on my MacBook through UTM.

or at least it was supposed to be.

the VM refused to launch because something was holding onto its EFI variables file.

i had no idea what that meant.

which is fine because computers usually explain problems in the linguistic style of a ransom note.

eventually i found an old QEMU process still running from the previous session.

it was basically squatting in the VM after everybody else had gone home.

killed it.

Ubuntu started.

amazing.

twenty-first century cybersecurity professional successfully turns computer on.

## then the computers refused to acknowledge each other

i installed the Wazuh agent on Windows.

manager running.

agent installed.

dashboard open.

status:

**never connected**

really cool.

so now i had to figure out whether the agent was broken, Wazuh was broken, Windows was broken, the network was broken, or i was broken.

i checked connectivity.

Wazuh normally uses TCP 1514 for agent communication and 1515 for enrollment.

could Windows reach them?

no.

finally, an actual answer.

because:

> Wazuh doesn't work

is useless.

but:

> Windows can't reach TCP 1514 and 1515

is specific enough that you can actually do something besides stare at it.

the VM networking wasn't giving the physical Windows machine a usable route to the manager.

so i changed the UTM networking and forwarded the Wazuh traffic.

tested it again.

1514 worked.

1515 worked.

great.

fixed.

## no actually

the agent still wasn't connecting correctly.

awesome.

this is where i learned that **being able to reach a server and being authenticated to that server are completely separate problems**, which feels obvious after somebody tells you.

Windows could reach Wazuh.

Wazuh just didn't recognize the agent correctly.

there was an old disconnected agent registration left over from an earlier setup.

so i removed it and enrolled the endpoint again.

then the manager returned:

`Valid key received`

and the agent finally logged:

`Connected to the server`

there.

they know each other now.

congratulations to everyone involved.

## installing corporate spyware on myself

next was Sysmon.

Sysmon gives Windows much more detailed event logging around things like:

- process creation
- network connections
- file creation
- registry changes

basically Windows already records things, but Sysmon records them like it's collecting evidence for a custody hearing.

perfect.

i wanted the entire path working:

Windows  
→ Sysmon  
→ Wazuh agent  
→ Wazuh manager  
→ detection rule  
→ alert

then i wanted to write a rule myself.

because otherwise i was basically just installing software and congratulating myself for following directions.

## making Wazuh care

i created custom XML rule:

`100100`

it targeted Sysmon Event ID 1.

Event ID 1 records process creation.

so the test was extremely sophisticated:

run something.

if everything works, Sysmon sees the process, Wazuh receives the event, my rule matches it, and an alert appears.

i triggered activity.

opened Wazuh.

**rule 100100**

**level 10**

there it was.

finally.

an alert i intentionally caused, detected by a system i intentionally configured, on a computer i own.

basically i had spent several hours setting a trap for myself and then successfully stepped in it.

but it worked.

## the part that was actually useful

the most useful thing i learned wasn't really Wazuh.

it was troubleshooting without becoming stupid.

at the beginning, every problem felt like:

> why doesn't this work

which is basically not a question.

eventually it became:

is Ubuntu running?

can Windows reach the manager?

are 1514 and 1515 reachable?

is the agent enrolled?

is Sysmon generating events?

is Wazuh receiving them?

does my rule match?

each question gives you something you can actually test.

and every test kills off another possibility.

very boring.

very effective.

unfortunately this is how most useful things work.

## final result

by the end i had:

- Windows 10 generating Sysmon telemetry
- a Wazuh agent sending it to Ubuntu ARM64
- working communication over TCP 1514/1515
- a properly enrolled endpoint
- custom rule `100100`
- a level-10 alert triggered from Sysmon Event ID 1

so technically i got what i wanted.

SOC experience.

just without coworkers, money, or health insurance.

**CASE 001: CLOSED**

Windows is a snitch.

finally somebody in this house is useful.
