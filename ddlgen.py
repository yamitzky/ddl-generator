#!/usr/bin/env python

import commands
import sys

user = sys.argv[1]
password = sys.argv[2]
db = sys.argv[3]

def execute(command):
    return commands.getoutput('echo "%s" | mysql -u %s --password=%s %s' % (command, user, password, db)).split("\n")

for table in execute("SHOW TABLES")[1:]:
    res = execute("SHOW CREATE TABLE \`%s\` \G" % table)
    if len(res) >= 3:
        if res[2].strip().startswith("View"):
            rows = res[3].split(":", 1)[-1].replace(",", ",\n").split("\n")
            cols = ["\t" + row.strip() + "," for row in rows]
        else:
            cols = ["\t" + row.strip() for row in res[3:]]

        print table
        print "\n".join(cols)
        print "-" * 10
