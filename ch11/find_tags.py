#!/usr/bin/python3

import re
import source

tags = re.compile(r'(\[\[.*?\]\])')
found_tags = tags.findall(source.r1)
unique_tags = list(set(found_tags))

print(unique_tags)
