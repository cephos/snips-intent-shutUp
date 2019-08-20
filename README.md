# Snips shutUp TTS action
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)]

This is a Snips action written in Python and is compatible with `snips-skill-server`.
It stops the tts-service as soon as it gets the shutUp-Intent (For example by saying "Snips, sei still!") so the Read Text or answer of an action is cancelled.
To stop the service it has to be run with elevated privileges (root).

## Skill Setup
### Prerequisites

You'll need to add the ShutUp skill in german in your assistant. It's available on [Snips' console](https://console.snips.ai)

### SAM (preferred)
To install the action on your device, you can use [Sam](https://snips.gitbook.io/getting-started/installation)

`sam install action -g https://github.com/snipsco/snips-skill-weather-tts.git`

### Manually

Copy it manually to the device to the folder `/var/lib/snips/skills/`
You'll need `snips-skill-server` installed on the pi

`sudo apt-get install snips-skill-server`

Stop snips-skill-server & generate the virtual environment
```
sudo systemctl stop snips-skill-server
cd /var/lib/snips/skills/snips-skill-weather-tts/
sh setup.sh
sudo systemctl start snips-skill-server
```

## How to trigger

`Hey Snips`

`Sei still!`

## Logs
Show snips-skill-server logs with sam:

`sam service log snips-skill-server`

Or on the device:

`journalctl -f -u snips-skill-server`

Check general platform logs:

`sam watch`

Or on the device:

`snips-watch`
