# Syllabus

Created by: Isaac Simms
Created time: August 26, 2026 10:21 PM
Last edited by: Isaac Simms
Last updated time: August 26, 2026 10:22 PM

# Course Syllabus

# CS 425: Distributed Systems

Click this link for a [PDF version](https://courses.grainger.illinois.edu/cs425/fa2026/intro.FA26.pdf) of the syllabus.

(**NOTE**: **It is highly recommended that you download the PDF version and read it thoroughly. That pdf contains all the relevant information)**

## Course Description

Cloud computing systems today, whether open-source or used inside companies, are built using a common set of core techniques, algorithms, and design philosophies – all centered around distributed systems. Learn about such fundamental distributed computing "concepts" for cloud computing.

Some of these concepts include: clouds, MapReduce, key-value/NoSQL stores, classical distributed algorithms, widely-used distributed algorithms, scalability, trending areas, and much, much more!

Know how these systems work from the inside out. Get your hands dirty using these concepts with provided homework exercises. In the programming assignments, implement some of these concepts in template code (programs) provided in the C++ programming language. Prior experience with C++ is required.

The course also features interviews with leading researchers and managers, from both industry and academia.

Both DS3 (3cr) and DS4 (4cr) students have the same material, with the difference that the DS4 students do the 2 Programming Assignments, but the DS3 students do not do the 2 Programming Assignments.

## Main Textbook (Recommended, not Required)

Coulouris, G., Dollimore, J., Kindberg, T., & Blair, G. (2011). *Distributed systems: Concepts and design* (5th edition). Addison-Wesley. ISBN: 0132143011.

We will refer to chapter, section, and problem numbers ONLY in the fifth edition. If you use an older edition, correct interpretation/translation of these numbers is solely the students’ responsibility (no excuses).

## Course Schedule

| **Week** | **Duration** | **Topics** | Readings |
| --- | --- | --- | --- |
| 1 | 8/24 - 8/30 | Course Orientation, Basic Computer Science Fundamentals |  |
| 2 | 8/31 - 9/6 | **Course Part 1 Begins**: Introduction to Clouds, Clouds Are Distributed Systems, MapReduce, Interview with Sumeet Singh | Relevant parts of Chapter 1 |
| 3 | 9/7 - 9/13 | Gossip, Membership, Grids, Interview with William Gropp | Section 18.4 (Relevant Parts), Section 15.1 and relevant parts of Section 2.4.2, Further readings (papers): [Gossip-style FD](http://dl.acm.org/citation.cfm?id=1659238), [SWIM](http://ieeexplore.ieee.org/document/1028914/?reload=true&arnumber=1028914) |
| 4 | 9/14 - 9/20 | P2P Systems, Interview: Blue Waters Supercomputer | [Paper - "Gnutella Protocol Specification"](https://courses.engr.illinois.edu/cs425/fa2017/gnutella_protocol_0.4.pdf), [Paper - "Chord"](http://dl.acm.org/citation.cfm?id=383071) (Sections 1-4, 6-7) |
| 5 | 9/21 - 9/27 | Key-Value Stores, Time and Ordering, Interview with Marcos Aguilera | [Cassandra 2.0 Documentation at datastax.com](http://docs.datastax.com/en/cassandra/2.0/), [Cassandra 2.0 Paper](http://www.datastax.com/documentation/articles/cassandra/cassandrathenandnow.html), [Cassandra 3.0 Documentation](http://docs.datastax.com/en/cassandra/3.0/) (may differ from material being discussed), [Cassandra NoSQL Presentation](http://www.slideshare.net/Eweaver/cassandra-presentation-at-nosql), [Cassandra 1.0 documentation at datastax.com](http://www.odbms.org/wp-content/uploads/2013/11/cassandra10.pdf), [Cassandra Apache wiki](http://wiki.apache.org/cassandra/ArchitectureOverview), [HBase](http://hbase.apache.org/book/), [MongoDB](http://www.mongodb.org/), Sections 14.1-14.4 |
| 6 | 9/28 - 10/4 | Classical Distributed Algorithms

 | Section 14.5, Section 15.4, Paper "Impossibility of Distributed Consensus" (sections 1-3 only) and Section 15.5.2, Section 17.3.1, 21.5.2 (Paxos sections) |
| 7 | 10/5 - 10/11 | Midterm Exam
(covers syllabus weeks 1-5) | 
Exam window is 10/9 through 10/11 |
| 8 | 10/12 - 10/18 | HW 3 |  |
| 9 | 10/19 - 10/25 | **Course Part 2 Begins:** Classical Distributed Algorithms Continued | Section 15.3, Section 15.2 |
| 10 | 10/26 - 11/1 | Concurrency Control, Replication Control | Section 4.3, Relevant parts of Chapter 5, Section 16.{1, 2, 4},  17.{1, 2, 3, 5}; Sections 18.1 - 18.3, 18.5 |
| 11 | 11/23 - 11/8 | Stream Processing, Distributed Graph Processing, Structure of Networks, Scheduling, Storm Demo | [Storm](http://storm-project.net/), [Pregel](http://dl.acm.org/citation.cfm?id=1807184), ([Optional: Spark Streaming](http://www.eecs.berkeley.edu/Pubs/TechRpts/2012/EECS-2012-259.pdf)) |
| 12 | 11/9 - 11/15 | Distributed File Systems, Distributed Shared Memory, Sensor Networks, Interview with Brighten Godfrey | Chapter 12 (relevant parts), Sections 6.5 (relevant parts). Optional: Chap 6 from Tanenbaum, Distributed Systems: principles and paradigms |
| 13 | 11/167 - 11/22 | Security, Datacenter Outage Studies, Interview with Paul Kwiat | See links on slides |
| 14 | 11/23 - 11/29 | Fall Break |  |
| 15 | 11/30 - 12/6 | information for final exam |  |
| 16 | 12/7 - 12/13 | Final Exam (covers entire course) | Final exam window: 12/11 to 12/13 |

MOOC - CS 425 Content Mapping

| MOOC | CS 425 |
| --- | --- |
| Cloud Computing Concepts Part 1 | Week 1 to Week 6 |
| Cloud Computing Concepts Part 2 | Week 9 to Week 14 |

## Assignment Deadlines

For all assignment deadlines, please refer to the Course Deadlines, Late Policy, and Academic Calendar page.

## Elements of This Course

- **About the Course:** This 4-credit hour course is **16** weeks long. The first week basic computer science fundamentals is a good starting point. It is recommended that you pass the prerequisite quiz to make sure that you meet the prerequisite to take this course. The course is composed of two parts, Part 1 and Part 2. Each course part is further divided into 5 weeks of content. The two course parts are exactly the same as the MOOC version of the course: Cloud Computing Concepts Part 1 and 2. Besides the two parts, this course has additional homeworks and exams that are not included in the MOOC. For details about each component of the course, see the course component description below.
- **Lecture Videos:** In this course, content will be presented as lecture videos. Each week's content is broken into several lessons that contain a number of lecture videos. Each lecture video is no longer than 30 minutes. You may stream lecture videos for playback within the browser by clicking on their titles, or you may download the lecture videos and watch them offline. You can also download each lecture PowerPoint by clicking the **Resources** tab in each lecture video. NOTE: You may notice that the PowerPoint slides for the lecture videos will have numbering that's inconsistent with the corresponding week. That is because the course is combined from the Cloud Computing Concepts Part 1 and Part 2 MOOCs.
- **In-Video Questions:** Some lecture videos contain in-video questions. These questions are low stake, designed to help enhance your understanding of concepts in the lecture videos. In-video questions are not a graded component of this course.
- **Supplementary Readings:** Some weeks may have supplementary readings. The supplementary readings can be accessed via the weekly overview page.
- **Quizzes:** Each part of the course has 5 weekly quizzes. The quizzes are designed to help you better understand and apply the knowledge you learned from the lecture videos. You have unlimited attempts for each quiz. The number of questions in the weekly quizzes varies. The highest attempt score is recorded as the score of the quiz. Each quiz will be graded on a pass/fail basis (cutoff is 70% of points on that quiz).
- **Coursera Final Quizzes:** There are Coursera final quizzes, one at the end of each course part. You have only two attempts on each Coursera final quiz. Each Coursera final quiz has 30 questions. The grade of a Coursera final quiz will be the highest score from the two attempts. Each final quiz evaluates your overall understanding and application of each course part.
- **Homework (or HW):** There are 4 homework sets. The homework release date and due date can be found on the Course Deadlines, Late Policy, and Academic Calendar page. **Your homework solution submissions are required to be typed and uploaded to Gradescope** (you may use any of your favorite word processors). We will not accept handwritten solutions. Figures and equations (if any) may be drawn by hand. All homework must be done individually.
- **Programming Assignments:** There are a total of 2 programming assignments (or MP = Machine Programs), 1 in each part of the course.
- **Exams:** There are 2 written exams in the course. The midterm exam covers content from Week 1 to Week 5. The final exam covers all content in the entire course. Both exams are **timed** **exams proctored via ProctorU**.

## Grading Distribution and Scale

### Grading Distribution

Your final grade will be calculated based on the activities listed in the table below. Your official final course grade will be listed in [Enterprise](https://apps.uillinois.edu/selfservice/). The course grade you see displayed in Coursera may not match your official final course grade.

| Assignment | DS3 points | DS3 percents | DS4 points | DS4 percents |
| --- | --- | --- | --- | --- |
| Weekly Quizzes | 0.25 pts per question x
127 questions = 31.75 pts | 20.92% | 31.75 pts | 16.14% |
| Final Quizzes | 0.25 pts per question  x
60 questions = 15 pts | 9.89% | 15 pts | 7.62% |
| Programming Assignments 
(only for DS4) | n/a |  | 22.5 pts x
2 MP = 45 pts | 22.87% |
| Homework | 10 pts per HW x best 3/4 HWs
= 30 pts | 19.77% | 30 pts | 15.25% |
| Exams | 25 pts for midterm +
50 pts for final exam
= 75 pts | 49.42% | 75 pts | 38.12% |
| Total | 151.75 max for DS3 | 100% | 196.75 max for DS4 | 100% |

### Grading Scale

The grading scale will be curved after all students' coursework is graded at the end of the course. Final grades are assigned (curved) separately for all MCS-DS students. In other words you are not competing directly with on-campus students for your grades. Use everyone's knowledge and help (within the bounds of academic integrity) to do the best that you can!

**NOTE**: You will notice that the point value of assignments in Coursera are different from the Grading Distribution table above (e.g., Programming Assignments are worth 90 points each in Coursera, but they are actually worth 22.5 points each for this course); the grades for assignments in Coursera will be scaled down when calculating the final grade for this course.

### View Grades

You can view your grade on each assignment by clicking the **Assignments** tab on the left menu bar. H**W and Midterm Exam grades will be posted only on Canvas.**

### Student Code and Policies

A student at the University of Illinois at the Urbana‑Champaign campus is a member of a University community of which all members have at least the rights and responsibilities common to all citizens, free from institutional censorship; affiliation with the University as a student does not diminish the rights or responsibilities held by a student or any other community member as a citizen of larger communities of the state, the nation, and the world. See the [University of Illinois Student Code](http://studentcode.illinois.edu/index.html) for more information.

### Academic Integrity

All students are expected to abide by [the campus regulations on academic integrity found in the Student Code of Conduct](http://admin.illinois.edu/policy/code/article1_part4_1-401.html). These standards will be enforced and infractions of these rules will not be tolerated in this course. Sharing, copying, or providing any part of a homework solution or code is an infraction of the University’s rules on academic integrity. We will be actively looking for violations of this policy in homework and project submissions. Any violation will be punished as severely as possible with sanctions and penalties typically ranging from a failing grade on this assignment up to a failing grade in the course, including a letter of the offending infraction kept in the student's permanent university record.

Again, a good rule of thumb: *Keep every typed word and piece of code your own*. If you think you are operating in a gray area, you probably are. If you would like clarification on specifics, please contact the course staff.

### Disability Accommodations

Students with learning, physical, or other disabilities requiring assistance should contact the instructor as soon as possible. If you’re unsure if this applies to you or think it may, please contact the instructor and [Disability Resources and Educational Services (DRES)](http://disability.illinois.edu/) as soon as possible. You can contact DRES at 1207 S. Oak Street, Champaign, via phone at (217) 333-1970, or via email at [disability@illinois.edu](mailto:disability@illinois.edu).