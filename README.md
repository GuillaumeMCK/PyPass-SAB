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
> of StartAllBack. This patcher is compatible with versions between **v3.5.5** and **v3.5.7**. <br/>
> <br/>
<div align="center">
    <img src="https://raw.githubusercontent.com/GuillaumeMCK/PyPass-SAB/main/.assets/banner.png" width="500">
</div>
<br>

## Why did I make this?
Because it's bored to reinstall StartAllBack every 100 days and I don't trust
the "cracks" on the internet 🤷‍♂.<br/>
I also wanted to make a patcher by myself, so I made this one.
But if you want to support the developer of StartAllBack you can buy it on [this website](https://www.startallback.com/).

## What does it do?

- Check the hash of `StartAllBackX64.dll` to make sure that the file is the correct one.
- Make a backup of `StartAllBackX64.dll` in the same folder named `StartAllBackX64.bak`.
- Stop all instances of `Explorer.exe`
- Patch `StartAllBackX64.dll`
- Start explorer.exe
- That's all!

## The patch

<details>
  <summary>Ordinal_101 Function</summary>

```asm
                      *************************************************************
                      *                                                             
                      *   FUNCTION                                                  
                      *************************************************************
                      undefined8  __fastcall  Ordinal_101 (void )
      undefined8        RAX:8          <RETURN>
                      0x2164  101  
                      Ordinal_101                                     XREF[4]:     Entry Point (*) ,  180027af9 (c) , 
                                                                                   18008a9bc (*) ,  1800920fc (*)   
180002164  b8  00  00      MOV        EAX ,0x0
           00  00
180002169  c3              RET
```
</details>

<details>
  <summary>Ordinal_102 Function</summary>

```asm
                      *************************************************************
                      *                                                             
                      *   FUNCTION                                                  
                      *************************************************************
                      undefined8  __fastcall  Ordinal_102 (undefined8 *  param_1 )
      undefined8        RAX:8          <RETURN>
      undefined8 *      RCX:8          param_1
                      0x1f68  102  
                      Ordinal_102                                     XREF[4]:     Entry Point (*) ,  180027aeb (c) , 
                                                                                   18008a9c0 (*) ,  1800920e4 (*)   
180001f68  48  c7  01      MOV        qword ptr [param_1 ],0x1
           01  00  00 
           00
180001f6f  b8  01  00      MOV        EAX ,0x1
           00  00
180001f74  c3              RET
```
</details>

> **Note**: The patch will not change the expiration date of the software.

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

To build the project

```batch
cd PyPass-SAB
py setup.py build
```

## Disclaimer
> **Warning**:
> I AM NOT RESPONSIBLE FOR ANY DAMAGE CAUSED OR ANY ILLEGAL USAGE OF THIS SCRIPT.
> USE IT AT YOUR OWN RISK.
