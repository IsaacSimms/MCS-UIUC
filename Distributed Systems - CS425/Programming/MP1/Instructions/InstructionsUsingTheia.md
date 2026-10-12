# Using Theia IDE on Coursera Labs

**Course:** CS 425 / Cloud Computing Concepts

Theia is an open-source IDE (similar to VS Code) used for some programming assignments. It runs in the browser for coding, compiling, and submitting.

Assignments with a Theia lab typically have **two separate items** on the course week page:
1. A Programming Assignment item (instructions, submission token generator, submission history/grades).
2. A Lab launcher item (to open the Theia IDE workspace).

Copy the submission token from the first item into the Theia IDE when ready to submit.

---

## Submission Token and Grading Page

- Contains assignment instructions, a **submission token** generator, and the **My Submissions** tab.
- The My Submissions tab shows pending autograding jobs and past results.
- Generate a fresh token for each resubmission (tokens expire).

---

## “Ungraded” Lab Launcher Page

- Labeled “Ungraded Lab.” This only means the Coursera Labs workspace is not directly wired to the autograder.
- You still submit from the lab using a script + token.
- Sometimes the launcher is integrated into the submission results page (no manual token needed).
- Click the launch button to open the workspace.

---

## Setting Up Your Workspace

1. On first entry the workspace may look empty. Click the **Open Workspace** link.
2. In the panel that opens, select the `lab-workspace` directory inside the `theia` home folder, then click **Open**.
   - **Critical:** Always use `lab-workspace` as the working directory. Only this folder is automatically saved to the cloud between sessions.
3. Open the file explorer (upper-left icon that looks like two sheets of paper) to see files.
4. Click a file (e.g., `MP1Node.cpp`) to open it for editing.
5. Open a terminal: **Terminal → New Terminal**.

---

## Compiling and Testing

### Compile
```bash
make clean && make
```
- Use View → Problems for a high-level error overview.
- The make terminal output is the most detailed source of compiler messages.

## Test
Mark the tester script executable, then run it. Names vary by assignment; check any README.
MP1 example:
```Bash
chmod +x ./Tester.sh
./Tester.sh
```

MP2 example:
```Bash
chmod +x ./KVStoreTester.sh
./KVStoreTester.sh
```

These scripts are for local testing only; they do not produce a grade.

## Submitting for a Grade

1. Obtain a current submission token from the Programming Assignment page (generate a new one if resubmitting).
2. In the Theia terminal run:
```Bash
python3 ./submit.py
```
3. Enter the email address you use for Coursera.
4. Paste the submission token when prompted.
5. Follow any additional prompts the script presents.
6. Return to the Programming Assignment page and open the My Submissions tab to monitor results.

The submission script may also work on your own Linux machine if you prefer to develop offline. See backup instructions below.

## Backing Up Your Files
Work inside ~/lab-workspace (i.e., /home/theia/lab-workspace) so files are auto-saved to the cloud every few minutes.
To download a local copy:
```Bash
cd ~/lab-workspace
make clean
zip -r backup.zip *
```
Right-click backup.zip in the file explorer and choose Download.

Importing Code Files
Preferred methods:

Right-click empty space in the file explorer → Upload Files.
Drag-and-drop files from your local file manager into the Theia file list.

## Fallback method:
```Bash
mkdir ~/lab-workspace/upload
```
Select the new upload folder, then use File → Upload Files. Move the uploaded files to their proper locations afterward.