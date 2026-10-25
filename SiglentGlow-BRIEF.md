# SiglentGlow — firmware brief for Claude Code

**Owner:** Gareth Cooke · **Written:** 2026-10-25 · **Hardware design lives in:** `C:\Development\3DPrinting\SiglentTower` (wiring sheet `parts/wiring/wiring-4-connections.png`)

## 1. Goal

Write the firmware and on-device web UI for **SiglentGlow**, the backlight controller in Gareth's Siglent bench-instrument tower. It drives two short WS2812B strips and two 5 mm WS2812 "sill" pixels from a Seeed **XIAO ESP32-S3**. Build it as a sibling of **MorayGlow**, with the same architecture, the same shared libraries and the same conventions, so the two projects look and behave like one family.

Create the project at **`C:\Development\Projects\SiglentGlow`**, beside `MorayGlow`, `IguanaPlatform` and `IguanaCommon`. Read these before writing anything:

- `C:\Development\Projects\MorayGlow\CLAUDE.md` and `README.md`: architecture, conventions, build commands, library rules
- `MorayGlow\MorayServer\` (`src/main.cpp`, `src/webserver.cpp`, `src/mqtt.cpp`, `include/state.h`, `include/config.h`, `platformio.ini`, `data/`, `test/`): the template to mirror
- `C:\Development\Projects\IguanaPlatform\` (`EspProvision`, `EspDevice`, `EspMqttBase`, `EspLogger`, `data/`, `scripts/gen_build_info.py`)
- `C:\Development\Projects\IguanaCommon\IguanaLib\` (`ButtonStatus`, `TwoStateValue`)

**Do not modify IguanaPlatform, IguanaCommon or MorayGlow.** If something in them blocks you, stop and say what and why.

## 2. Hardware (fixed — design the firmware to this)

| Item | Detail |
|---|---|
| MCU | Seeed XIAO ESP32-S3 (`board = seeed_xiao_esp32s3`) |
| Bus 1 data | **D0 = GPIO1** → 74AHCT125 level shifter → 330 Ω → sill pixel 1 → sill pixel 2 → left strip. **17 LEDs**: indices 0–1 sill, 2–16 left strip |
| Bus 2 data | **D1 = GPIO2** → 74AHCT125 → 330 Ω → right strip. **15 LEDs** |
| Button | **D4 = GPIO5**, momentary to GND, `INPUT_PULLUP` (the same pin as MorayGlow) |
| LEDs | WS2812B, colour order **GRB**, 5 V |
| Power | 5 V from one USB port on the bench power strip; the LEDs are fed directly, and the XIAO's 5V pin is fed through a Schottky diode. Current budget for all LEDs: **1500 mA** |
| Avoid | GPIO3 (ESP32-S3 strapping pin), and GPIO0, GPIO45 and GPIO46, as MorayGlow does |

The strip length may change later (the backlight might go to a denser strip). Put every LED count in **one place** (`config.h`), and derive the bus split and index ranges from those constants.

## 3. Behaviour

### 3.1 Light state
- State is **on/off, colour (`#rrggbb`) and brightness (0–255)**. Static colour only: no effects, no cycle mode.
- The **strips and both sill pixels** show the state's colour at the state's brightness, and are all dark when off.
- **Restore the last state on boot**: persist on, colour and brightness in NVS (Preferences, a namespace of its own), and write at most once, 5 s after the last change, to spare the flash. First boot defaults: on, `#ffffff`, brightness 128.
- **Current limit**: cap the total draw at 1500 mA at 5 V with the LED library's power limiter (FastLED: `setMaxPowerInVoltsAndMilliamps(5, 1500)`), applied on top of the user's brightness.

### 3.2 Sill pixels as a status light ("both")
The sill pixels follow the strips (3.1) **except** when one of these takes over, highest priority first:
1. **Factory-reset countdown**: the button has been held for ≥ 1 s. The sill pixels blink red, getting faster from 800 ms to 80 ms per half-cycle as the hold approaches 5 s (as MorayGlow's status LED does). At 5 s they flash red 5 times, all LEDs go dark, then `Provision.factoryReset()`.
2. **Setup (AP) mode**: the sill pixels pulse amber slowly (about a 2 s breathing cycle). The strips stay dark.
3. **Boot**: two white blinks of the sill pixels (200 ms on / 200 ms off) before the state is applied, matching MorayGlow's boot blink.

### 3.3 Button (D4)
- **Short press** (released before 1 s): toggle on/off. Apply the change, broadcast it over the WebSocket, publish to MQTT, and schedule the NVS save.
- **Hold ≥ 1 s**: the reset countdown in 3.2. Releasing before 5 s cancels it and changes nothing.
- Debounce with `ButtonStatus`, as MorayGlow does.

### 3.4 Provisioning, network and OTA
Use **IguanaPlatform `EspProvision`**, exactly as MorayGlow's `setup()` does:
`Provision.begin("siglentglow", "SiglentGlow", cfg)` with `apPassword = "siglentglow"`, `nvsNamespace = "siglentglow"`, `otaPassword = OTA_PASSWORD` (`"password"` first-boot default), `friendlyHostname = "siglentglow"` (→ `http://siglentglow.local`), `serviceType = "siglentglow"`. Station routes and MQTT setup go in `Provision.onStation(...)`. `Provision.loop()` runs in `loop()`.

### 3.5 REST + WebSocket (mirror MorayGlow's `webserver.cpp`)
| Method | Path | Body | Response |
|---|---|---|---|
| GET | `/api/state` | — | `{"on":bool,"color":"#rrggbb","brightness":0-255}` |
| POST | `/api/power` | `{"on":bool}` | state JSON |
| POST | `/api/color` | `{"color":"#rrggbb"}` | state JSON (400 if not a valid hex colour) |
| POST | `/api/brightness` | `{"brightness":0-255}` | state JSON (400 if missing or out of range) |
| WS | `/ws` | — | push the state JSON to every client on any change, and to a new client on connect |

Every state change from any source (REST, WS, MQTT, button) goes through one path, e.g. `applyLedState()` → `broadcastState()` → `Mqtt.publishState()` → schedule the NVS save. The network-setting and device-info routes come from EspProvision's common endpoints; don't duplicate them.

### 3.6 MQTT / Home Assistant
- Subclass `EspMqttBase` as `MqttLight`, as MorayGlow does.
- **Broker host and port from NVS**: `Provision.getMqttHost(MQTT_HOST)` / `getMqttPort(MQTT_PORT)`, with user and password from `getMqttUser()` / `getMqttPass()`, all settable on `/settings.html`. **If the host is empty, don't start MQTT at all** (no 5-second reconnect loop to nowhere).
- Topics: `<device-id>/state` and `<device-id>/command`; discovery at `homeassistant/light/<device-id>/config` (retained), republished on every reconnect.
- Discovery: JSON schema, `supported_color_modes: ["rgb"]`, **`brightness: true`**, `brightness_scale: 255`, `device` block with name `SiglentGlow`, model `XIAO ESP32-S3`, manufacturer `IguanaWare`.
- Command payload (HA JSON schema): `{"state":"ON"|"OFF","color":{"r","g","b"},"brightness":N}`, with any key optional.
- **State payload must be HA-compliant**, which differs from the REST JSON: `{"state":"ON","color_mode":"rgb","brightness":N,"color":{"r":..,"g":..,"b":..}}`, retained. *(MorayGlow publishes its REST-style `{"on":..}` on the state topic, which HA's JSON schema doesn't read. Don't copy that, and don't fix MorayGlow either: just mention it in your final summary.)*

### 3.7 Web UI (`data/`, LittleFS, no build step)
- `index.html` + `js/app.js` + `js/siglent.js` (a UMD utility module like `moray.js`): the power button, MorayGlow's LED-strip colour picker, and a **brightness slider** (sending at most every 200 ms while dragging), with a status line and the light/dark theme toggle. Links to `settings.html` and `setup.html`.
- `setup.html` and `settings.html`: take them from IguanaPlatform's `data/` / MorayGlow's `data/`. **Reconcile the stylesheet path**: IguanaPlatform's pages link `/style.css`, while MorayGlow's link `css/style.css`. Use one stylesheet that every page links correctly.
- Title and heading: "SiglentGlow". There's only one device, so leave out `devices.html`.

### 3.8 LED driver
- Use **FastLED** (or NeoPixelBus if FastLED misbehaves on this core) on the ESP32-S3's **RMT** peripheral, with **two outputs**: one `CRGB` array of `LEDS_BUS1 + LEDS_BUS2` and two `addLeds` calls on GPIO1 and GPIO2.
- Pick a library version that builds against the Arduino core the `espressif32` platform in MorayGlow's `platformio.ini` resolves to. Pin the version in `lib_deps`.
- WS2812 timing must not glitch while Wi-Fi is busy (web page open, MQTT traffic). RMT handles that, but say so in the summary if you saw otherwise.

## 4. Project layout (mirror MorayGlow)

```
SiglentGlow/
├── CLAUDE.md              # adapted from MorayGlow's: build commands, architecture, pins, API, MQTT
├── README.md              # short: what it is, hardware, how to flash, how to set it up
├── .gitignore             # as MorayGlow's
└── SiglentServer/
    ├── platformio.ini     # envs: xiao_esp32s3, xiao_esp32s3_ota (upload_port siglentglow.local), native
    │                      # lib_extra_dirs = ../../IguanaCommon and ../.. ; extra_scripts = ../../IguanaPlatform/scripts/gen_build_info.py
    ├── include/           # config.h (pins, LED counts, current limit, MQTT fallback, OTA default), state.h, mqtt.h, webserver.h, leds.h
    ├── src/               # main.cpp, leds.cpp, mqtt.cpp, webserver.cpp
    ├── data/              # web UI (3.7)
    └── test/test_state.cpp
```

`state.h` stays **header-only with `inline` functions and `#ifndef ARDUINO` guards** so it compiles natively: `stateToJson(on, color, brightness)`, `haStateToJson(...)`, `rgbToHex`, `hexToRgb`, `isValidHexColor`, `parseMqttCommand(payload, on, color, brightness)` (it updates only the keys present, clamps brightness to 0–255, and returns false on bad JSON).

## 5. Acceptance — done when

1. `pio run -e xiao_esp32s3` builds with no errors and no new warnings in project code.
2. `pio test -e native` passes, covering every function in `state.h`: valid and invalid colours, brightness clamping, partial MQTT commands, bad JSON, and the HA state payload shape.
3. `pio run -e xiao_esp32s3 -t buildfs` builds the LittleFS image.
4. The code reads like MorayGlow: same file split, naming and comment style, and library rules from MorayGlow's CLAUDE.md (ArduinoJson v7 `JsonDocument`, `setBufferSize(512)`, POST bodies in `onBody`, async Wi-Fi scan).
5. A git repo is initialised with one commit, its message in MorayGlow's style (a subject line, then a bullet body).
6. Your final summary lists: what you built, any deviations from this brief and why, the MorayGlow HA-state-topic note (3.6), and the flashing steps for Gareth as a numbered list (USB flash, uploadfs, join `SiglentGlow-XXXXXX` / password `siglentglow`, pick Wi-Fi, open `siglentglow.local`, set the MQTT host on `/settings.html`).

Use the PlatformIO path from MorayGlow's CLAUDE.md (`& "$env:USERPROFILE\.platformio\penv\Scripts\pio.exe"`). No hardware is needed for 1–5: Gareth will flash and bench-test it himself on the breadboard.

## 6. Out of scope

Effects, presets, segments as separate lights, sound reactivity, `devices.html` / peer discovery, and any change to the shared libraries.
