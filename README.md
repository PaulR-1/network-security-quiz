# Network and security reviewers

Exam review quizzes, plus a Cisco command notebook. Each saved command becomes its own folder.

## Run it

From this folder:

```bash
python3 server.py
```

Then open [Cisco command practice](http://127.0.0.1:43127/cisco%20Command%20Practice/) or the [reviewer home page](http://127.0.0.1:43127/).

Python 3 is the only requirement. The server does not install packages. With the server running, each command is saved as a folder on disk.

On the published site, the same page saves the command in this browser only (`localStorage`, key `cisco-command-practice-v1`). Those notes are not written into the git repository. Another browser, another device, or clearing site data removes them. Search still runs from the browser.

Newest commands are listed first. Edit command changes the title. On disk, that rewrites `command.txt` and leaves the folder name as it was.

## Cisco command practice

The page lives in `cisco Command Practice/`.

1. Type an IOS command and press Enter.
2. A description box pops up. Write what the command does and press Enter.
3. The app creates a folder at `cisco Command Practice/commands/<command>/` with `command.txt` and `description.txt`.
4. **Search the net for more descriptions** looks up public Q&A and Wikipedia, then saves the extra notes in that same folder.

Entering a command that already has a folder adds another description file there.

Delete removes one description and leaves the folder. Delete folder removes that command and every description in it. On disk, that deletes the description file or the whole command folder.

The quiz pages are static HTML. A folder on disk is written only while `server.py` is running. The published page keeps the same notes in the browser.
