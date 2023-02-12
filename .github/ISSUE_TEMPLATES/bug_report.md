## Description

A clear and concise description of the bug.

## Steps to Reproduce

1. Step 1
2. Step 2
3. Step 3

You can paste here the part of your Robot Framework code that is causing the error.

## Expected Behavior

What you expected to happen.

## Actual Behavior

What actually happened.

## Environment

- OS: [e.g. Windows 10, macOS Big Sur]
- Library version: [e.g. 3.0]
- Python version: [e.g. 3.9.1]

## Additional Context

You can add logs of your Robot Framework code.

Running with `--loglevel DEBUG` helps provide additional information.
If you think the issue might be related to x3270, you can open your connection with the extra arguments `-trace -tracefile Path/To/Your/File.txt`.

```robot
@{extra_args}=    Create List    -trace    -tracefile ${CURDIR}/trace.txt
Open Connection    myhost.com    extra_args=${extra_args}
```

Make sure your logs do **not** contain any sensitive information such as passwords, etc.
