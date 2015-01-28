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
    if "View" in res[1]:
        rows = res[2].split(":", 1)[-1].split(",")
        cols = ["\t" + row + "," for row in rows]
    else:
        cols = ["\t" + row.strip() for row in res[3:-1]]

    print table
    print "\n".join(cols)
    print "-" * 10
