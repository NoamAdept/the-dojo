# Whispered Variables

`orient-environment` · Yellow Belt

**Goal:** Open the prepared lab shell, find the two environment variables that each hold half of the flag, join them in order, and submit the result.

Type in the challenge folder. The last line shows the flag:

```bash
printf '%s\n' 'printenv | grep "^LAB_"' 'printf "%s\n" "${LAB_FLAG_PART1}${LAB_FLAG_PART2}"' | ./lab_shell.sh
```

Paste the flag in the flag box and press **Submit**.
