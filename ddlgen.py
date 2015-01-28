#!/usr/bin/env python

import commands
import sys

user = sys.argv[1]
password = sys.argv[2]
db = sys.argv[3]

def execute(command):
    return commands.getoutput('echo "%s" | mysql %s' % (command, " ".join(sys.argv[1:]))).split("\n")

def discard(rows):
    discarded = False
    new_rows = []
    for row in rows:
        if discarded:
            new_rows.append(row)
        else:
            if row.startswith("********"):
                discarded = True
    return new_rows

for table in execute("SHOW TABLES")[1:]:
    res = discard(execute("SHOW CREATE TABLE \`%s\` \G" % table))
    if len(res) >= 2:
        if res[0].strip().startswith("View"):
            rows = res[1].split(":", 1)[-1].replace(",", ",\n").split("\n")
            cols = ["\t" + row.strip() + "," for row in rows]
        else:
            cols = ["\t" + row.strip() for row in res[1:]]

        print table
        print "\n".join(cols)
        print "-" * 10
