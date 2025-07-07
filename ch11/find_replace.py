#!/usr/bin/python3
import source
import replacements

def find_replace_router(source, replacements):
    count = 1
    while count < 2:
        count += 1
        for line in source.splitlines():
            for key in replacements.keys():
                if key in line:
                    #line = re.sub(str(key), str(replacements[key]), line)
                    line = line.replace(str(key), str(replacements[key]))
                else:
                    continue
            else:
                print(line)

find_replace_router(source.r1, replacements.replacements)
