# PyPass-SAB 🐍
<div align="center">
    <br>
    <img src="https://img.shields.io/badge/Python-3.10-blue.svg">
    <img src="https://img.shields.io/github/languages/code-size/GuillaumeMCK/PyPass-SAB">
    <img src="https://img.shields.io/badge/Platform-Windows-blue.svg">
    <a href="https://github.com/GuillaumeMCK/PyPass-SAB/releases">
        <img src="https://img.shields.io/github/downloads/GuillaumeMCK/PyPass-SAB/total">
    </a>
</div>
<br/>

> PyPass-SAB is a patcher write in python that allows you to bypass the **100 days remaining limit** 
> of StartAllBack this is NOT a keygen. <br/>
> *Why did I make this?*<br/>
> Because it's bored to reinstall StartAllBack every 100 days and I don't trust 
> the "cracks" found on 🇷🇺 forums. 🤷‍♂ <br/>
> <br/>
<div align="center">
    <img src="https://raw.githubusercontent.com/GuillaumeMCK/PyPass-SAB/main/.assets/banner.png" width="500">
</div>
<br>

## What does it do?
- Check the hash of `StartAllBackX64.dll` to make sure that the file is the correct one.
- Make a backup of `StartAllBackX64.dll` in the same folder named `StartAllBackX64.bak`.
- Stop all instances of `Explorer.exe`
- Patch `StartAllBackX64.dll`
- Start explorer.exe
- That's all!

## The patch
### Before
<details>
  <summary>Show</summary>
    <img src="https://raw.githubusercontent.com/GuillaumeMCK/PyPass-SAB/main/.assets/original.png" width="600">
</details>

### After
<details>
  <summary>Show</summary>
    <img src="https://raw.githubusercontent.com/GuillaumeMCK/PyPass-SAB/main/.assets/patched.png" width="600">
</details>
<br/>

*NOTE: The patch was created with ghidra*
## How to launch it?
**From release page** : <br/>
Download the latest [release](https://github.com/GuillaumeMCK/PyPass-SAB/releases), unzip it and launch the file "main.exe"
<br><br/>
**From sources** : <br/>
Follow the instructions below <br/>
```batch
git clone https://github.com/GuillaumeMCK/PyPass-SAB.git
cd PyPass-SAB
pip install -r requirements.txt
py main.py
```

## Build
To build the project run 
```batch
cd PyPass-SAB
py setup.py build
```


## Disclaimer
I AM NOT RESPONSIBLE FOR ANY DAMAGE CAUSED OR ANY ILLEGAL USAGE OF THIS SCRIPT.
USE IT AT YOUR OWN RISK.
