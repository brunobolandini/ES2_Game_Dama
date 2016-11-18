#!C:\Python27\python
def printboard():
    ct = "<br>"
    s = ""
    print "<table>"
    print "<tbody>"
    for n in range(8):
        print "<tr>"
        for x in range(8):
            if n % 2:
                s = "a" if x % 2 else "b"
            else:
                s = "b" if x % 2 else "a"
            print "<td class=%s>" % s
            print ct
            print "</td>"
        print "</tr>"
    print "</tbody>"
    print "</table>"


def header():
    print "<!DOCTYPE html>"
    print "<HTML>"
    print "<head>"
    print "<meta content=\"text/html; charset=UTF-8\" http-equiv=\"content-type\">"
    print "<title>Checkers EX2</title>"
    print "<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">"
    print "</head>"


def main():
    header()
    print "<body>"
    printboard()
    print "</body>"
    print "</HTML>"


main()