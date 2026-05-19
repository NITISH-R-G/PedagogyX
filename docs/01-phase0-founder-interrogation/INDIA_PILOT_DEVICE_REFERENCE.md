# India Pilot Device Reference (D-DEV)

**Status:** Research draft — **not** founder-confirmed SKUs  
**Last updated:** 2026-05-19  
**Source:** Public vendor pages, India education IFPD market summaries, GeM-oriented listings  
**Purpose:** Set **minimum client spec tiers** until a pilot partner names exact models on site.

Founder answer: **“IDK — search the internet.”** Use this doc for architecture and RFC-0002; replace with **confirmed OEM + model** when the first pilot school is named.

---

## How to use this document

| Tier | Meaning |
|------|---------|
| **Reference profile** | Abstract spec (RAM, SoC class) — see [PRODUCTION_CLIENT_SPEC.md](../05-architecture/PRODUCTION_CLIENT_SPEC.md) |
| **Likely OEM** | Brands commonly sold into Indian K-12 / higher-ed — validate on physical hardware |
| **Pilot action** | Record `make`, `model`, `Android version`, `RAM`, `storage` from **Settings → About** on day 0 |

---

## Interactive flat panels / smartboards (Windows or Android onboard)

Most Indian “smart classrooms” use **65–86″ interactive flat panels (IFPs)** with built-in Android and optional OPS/Windows PC.

### India-focused manufacturers / brands

| Brand | Notes | Typical sizes | OS (typical) |
|-------|-------|---------------|--------------|
| **ViewSonic** ViewBoard | Widely cited as strong IFPD share in India; education line (e.g. IN6501 class) | 65–86″ | Android 13+ on panel |
| **BenQ** Board | Google EDLA-certified education boards; EZWrite / InstaShare | 65–86″ | Android on panel |
| **Samsung** Flip / Flip Pro | Business/education interactive displays in India | 75–85″ | Android 14 (newer Flip Pro) |
| **LG** CreateBoard (TR3DK series) | Common in institutional quotes; DMS (ConnectedCare) | 75–86″ | Android 13 |
| **Newline** | EDLA-oriented; verify local support in your state | 65–86″ | Android |
| **Teachmint** (IFP) | India-based; Bengaluru; X2 Neo / Plus / Pro series | 65–86″ | Android 14 (marketing) |
| **Promark** | India smart board vendor (multiple PRO series) | 65–98″ | Android 8–13 |
| **DeltaView** | India AI digital board vendor | Varies | Android |
| **Edutech Solutions** | EDLA-certified panels (marketing) | 65–86″ | Android 16 (vendor claim) |
| **Studynlearn / Smartschool** | Noida-based IFP + content bundles | 65″+ | Android |

**Price context (public listings, not PedagogyX quotes):** many 65–75″ IFPs cluster roughly **₹73k–₹2.5L** depending on brand, OPS PC, and warranty — use for **hardware planning only**, not customer budget (see D-10).

### Windows smartboard profile (attached PC or OPS)

Many installs pair the panel with a **low-end OPS/mini-PC** (Celeron N5105-class, 4 GB RAM). PedagogyX **Windows client** targets:

- **Windows 10/11** on OPS or teacher PC driving HDMI
- Screen capture via desktop duplication (see PRODUCTION_CLIENT_SPEC)

---

## Android tablets / classroom handhelds (India)

Used for student devices, teacher tablets, or **companion capture** (camera relay). Not always the primary board.

| Brand / provider | Notes | Typical form |
|------------------|-------|--------------|
| **Prabhaktech** | Education tablets 7–10″, MDM, India institutional focus | Android |
| **RDP** | Make-in-India tablets; GeM listings; 8–10″ Essential series | Android |
| **Acer** Chromebook Tab 510 | **Chrome OS** (not Android) — only if school standardizes Chrome tablets | ChromeOS |
| **Generic GeM / state scheme tablets** | Often 7–10″, 2–4 GB RAM — treat as **Android B** profile | Android |

**COSMIQ** and similar vendors often sell **panels + software ecosystem**; tablet may be secondary.

---

## Recommended minimum spec tiers (PedagogyX v1)

Until OEM is confirmed, **certify the client against profiles**, not brand names:

| Profile | Smartboard / panel | Android tablet |
|---------|-------------------|----------------|
| **A (target)** | IFP + OPS: Celeron N5105+, **4 GB RAM**, 64 GB storage; or panel SoC with **4 GB+** | **4 GB RAM**, Android 10+, hardware H.264 |
| **B (minimum)** | **4 GB RAM**, screen + mic only (defer extra cam) | **2–3 GB RAM**, screen + mic only |
| **Below minimum** | < 4 GB RAM or no H.264 encode | Defer cam; short sessions only |

---

## Pilot checklist (fill on site)

```text
Site name:
Contact (principal / IT):

Panel brand/model:
Panel Android version (if built-in):
OPS PC model (if any):
OPS RAM/CPU/Windows version:

Teacher tablet/phone (if used):
Student devices (if any):

Upload: Mbps sustained (speed test):
WAN outages per week (estimate):
```

---

## References (public web, 2026)

- ViewSonic India ViewBoard: https://www.viewsonic.com/in/products/viewboard/
- BenQ India education boards: https://www.benq.com/en-in/education/benq-board-interactive-displays.html
- Samsung India Flip Pro: https://www.samsung.com/in/business/smart-signage/interactive-display/
- LG India CreateBoard: https://www.lg.com/in/business/information-display/digital-signage/interactive/
- Teachmint IFP (vendor): https://teachmintxinteractiveflatpanel.com/
- Promark smart boards: https://promark.co.in/smart-boards/
- RDP education tablets: https://www.rdp.in/corporate/tablets

**Disclaimer:** PedagogyX does not endorse any vendor; list is for **compatibility planning** only.
