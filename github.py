#!/usr/bin/env python
import argparse
import os
import sys

import requests

URL = "https://api.github.com/repos/{}/{}/stargazers?per_page=100&page={}"


def colors(string, color):
    """Make things colorfull
    Arguments:
        string {str} -- String to apply colors on
        color {int} -- value of color to apply
    """
    return "\033[{}m{}\033[0m".format(color, string)


def fetch(username, reponame, fresh=False):
    """Fetch all the stargazers and put them in a file
    Arguments:
        username {str} -- Github Username
        reponame {str} -- repositoryof the user to check.
    """
    users = []
    cnt = 1
    stars = True
    filename = "{}-{}.md".format(username, reponame)

    while stars:
        url = URL.format(username, reponame, cnt)
        response = requests.get(url).json()
        if response:
            for i in response:
                users.append(i["login"])
            cnt += 1
        else:
            stars = False

    if fresh:
        with open(filename, "w") as f:
            for i in users:
                f.write(i)
                f.write("\n")

    return filename, users


def compare(filepath, users):
    """Compare two file to find out the missing stargazers
    Arguments:
        filepath {str} -- path to file storing
    """
    if os.path.isfile(filepath):
        with open(filepath) as f:
            data = f.read().splitlines()
    else:
        print(colors("[!] File not found"))
    traitor = set(data).difference(users)

    return traitor


def main(username, reponame, path=None, fresh=False, check=False):
    """Main man
    Arguments:
        username {str} -- Github Username
        reponame {str} -- repository name
    Keyword Arguments:
        path {str} -- Path to the file storing all the username (default: {None})
        fresh {bool} -- Record all the stargazers (default: {False})
        check {bool} -- Find the traitor (default: {False})
    """

    print(colors("\n[~] Grabbing all the stargazers for: {}/{}".format(username, reponame), 93))

    if fresh:
        filename, users = fetch(username, reponame, fresh=True)
        print(colors("\n[+] stargazers stored in: {}".format(filename), 92))
    elif check:
        filename, users = fetch(username, reponame)
        traitor = compare(path, users)
        if traitor:
            print(colors("\n[+] The damn traitor is: {}".format(traitor), 94))
        else:
            print(colors("\n[+] No body double crossed you my man!! ", 93))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Name of the owner of the repository")
    parser.add_argument("reponame", help="Name of the repository")
    parser.add_argument("-f", "--fresh", help="Record all the stargazers", action="store_true")
    parser.add_argument("-c", "--check", help="find the traitor")
    args = parser.parse_args()

    if args.fresh and args.check:
        print(colors("\n[!] Don't get smart with me", 93))
        sys.exit(1)
    elif args.fresh:
        main(args.username, args.reponame, fresh=True)
    elif args.check:
        main(args.username, args.reponame, args.check, check=True)
    else:
        print(colors("\n[!] No Operation Selected!! ", 91))
        sys.exit(1)
