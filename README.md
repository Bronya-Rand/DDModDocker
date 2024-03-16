# Doki Doki Mod Docker

<p align="center">
    <img src=".github/assets/DDMDLogo.png" alt="DDMD Logo" width=160> 
</p>
Doki Doki Mod Docker is a Ren'Py application designed to streamline the management and play of multiple Doki Doki Literature Club (DDLC) mods. It effectively 'containerizes' mods, allowing them to run independently within a single copy of Ren'Py/DDLC.

> [!IMPORTANT]
> This project is currently in alpha. You may encounter bugs or compatibility issues with certain mods. To report mod incompatibility, report it either in [Issues](https://github.com/Bronya-Rand/DDModDocker/issues).

> [!NOTE]
> This project is unaffiliated with Team Salvato. See [BUILDING.md](BUILDING.md) on how to build Mod Docker with fixes for Pull Requests. Credits for DDMD can be seen by looking at [CREDITS.md](CREDITS.md).

## Features

- **Ren'Py 8 Mod Compatibility:** Seamlessly run mods built on the Ren'Py 8 engine!
- **Mod Installation:** Easily install new mods directly within Mod Docker.
- **Multiple Mod Storage:** Manage as many mods you want to play within a single app!
- **Separate Saves:** Maintain independent save data for each mod (and copies of said mod)!
- **Custom Background:** Personalize the Mod Docker interface with a custom background image (instructions below).
- **[Beta] Auto `scripts.rpa` Removal:** Streamlines the experience for select mods that require the removal of `scripts.rpa`.
- **[Alpha] Auto MAS Template Fixes:** Ensures compatibility for mods built with the Monika After Story template (rather than the Bronya Rand 2.0 Template).

**Custom Background Instructions**
1. Place a 16:9 image into Mod Docker's `game` directory.
2. Name the image `docker_custom_image`.

## Installation
> [!IMPORTANT]
> **For macOS Users:** These steps require you to access the directory within the Mod Docker app. Right-click the Mod Docker app, select *Show Package Contents*, then navigate to `Contents/Resources/autorun`.

1. Download the latest version of Mod Docker [here](https://github.com/Bronya-Rand/DDModDocker/releases).
2. Extract Mod Docker to a location of your choice.
> [!CAUTION] 
> Avoid installing directly over DDLC
3. Download DDLC's PC ZIP from [ddlc.moe](https://ddlc.moe) and extract the ZIP file.
4. Locate the *DDLC-X.X.X-pc/game* folder and copy the following files to Mod Docker's `game` folder:
   - `audio.rpa`
   - `fonts.rpa`
   - `images.rpa`
5. Create a `mods` folder within Mod Docker's `game` folder.
6. Inside the `mods` folder, create a subfolder for each mod you wish to install
> [!TIP]
> Suggested Mod Folder Naming Scheme: Mod's Full Name or Acronym
7. Copy the `game` folder from the desired mod into its respective subfolder within the `mods` folder.
> [!IMPORTANT]
> If the mod lacks a `game` folder, create one inside the mod's subfolder and place all mod files (RPAs, RPYCs, etc.) within.
8. Launch Mod Docker using `DDMD.exe` (Windows), `DDMD` (macOS), or `DDMD.sh` (Linux).
9. Press F9 to access the Mod Docker menu. Select your mod and click *Select*.
10. Restart the game and relaunch Mod Docker.

## Why Mod Docker?

- Effortless Mod Management
  > Play multiple DDLC mods within a single application! Eliminate the hassle and disk space consumption of separate game copies or complex manual installations.
- Streamlined Play Experience
  > Enjoy mods (or multiple copies of the same mod) as if they have been freshly installed!
- Developed with Players and Modders in Mind
  > Mod Docker prioritizes ease of use, recognizing the passion both players and mod creators have for the DDLC community. Its design aims to elevate the modding experience for everyone.

## What inspired Mod Docker?

Mod Docker draws inspiration from the earlier vision of the Doki Doki Mod Launcher (DDML), conceived in 2018. While limitations existed in DDML's initial implementation, Mod Docker revisits that core concept, refining it for practicality and ease of use.  It draws on the modularity principles of [Docker](https://docker.com) to create a streamlined solution that aligns with standard modding practices.

## How does a 'mod container' work?

<p align="center">
    <img src=".github/assets/Containerization.png" alt="A diagram of how mod container works"> 
</p>

Think of a mod container as a self-contained space within Mod Docker. It houses all the necessary files for a specific mod, including RPAs, RPYC/RPY's, and folders like mod_assets. When you select a mod, Mod Docker loads only the files from its dedicated container.

## Comparing Mod Docker to Other Mod Launchers/Managers

Mod Docker takes a unique approach to mod management compared to other mod managers/launchers. Here's a breakdown of key differences:

<p align="center">
    <img src=".github/assets/CompareThree.png" alt="A diagram comparing Mod Docker to Doki Doki Mod Launcher/Mod Manager and Standard Installs"> 
</p>

### Mod Docker
- Self-Contained Mods: Each mod runs in its own dedicated folder, ensuring complete isolation and conflicts.
- Custom Ren'Py Engine: Utilizes a specialized Ren'Py build (6 (SE), 7 and 8) to enable seamless mod loading.
- Base Game Independence: Functions without external programs or the base game itself (aside from essential RPAs).

### Doki Doki Mod Launcher/Doki Doki Mod Manager
- Centralized Mod Storage: Mods reside within a single directory.
- External Dependencies: Relies on a custom Ren'Py SDK (DDML) or a separate program (DDMM) for execution.
- Shared Save Data: Multiple mod copies can access each other's save data.
- Ren'Py 8 Limitations: DDML has no Ren'Py 8 support and DDMM has incompatibility issues with Ren'Py 8 mods.
- Base Game Reliance: Requires the base game (and mod dependencies) for mod execution.

### Standard Install
- Manual Process: Involves manually adding mod files to the game directory.
- Base Game Reliance: Requires the base game for mod execution.

Copyright © 2022-2024 Azariel Del Carmen (Bronya-Rand). All rights reserved. Licensed under GNU AGPL-3.0. See [LICENSE](LICENSE) for more information.
