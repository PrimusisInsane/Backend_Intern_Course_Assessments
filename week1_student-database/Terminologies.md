# Python

Python is a programming language, high-level, general purpose, designed to be understandable to humans used in many fields like web development, automation, data science, machine learning, and scripting.

Runs code by converting your source code into bytecode and Python Virtual Machine executes the bytecode. It is interpreted language.

Run in terminal as:

```bash
main.py
```

---

###### Required Tools

Learners like me use VS Code, Git, GitHub, pip, venv, and ofcourse Python to learn the software.

```bash
python --version
```

Checks the version of python in the terminal

```bash
python main.py
```

starts up python code called main.py

---

###### Input and Output

Input means receiving data from user, and output displays the result.

Input() always returns string.

So need coversion on input to prevent errors.

```python
int(input())   # for integer

float(input()) # for floats

bool(value)    # for value True or False

list('abc')    # string to list of characters
```

---

###### Operators

Arithemetic Operators like `+`, `-`, `*`, `/`, `//`, `%`, `**` are used that perform various operations on values to produce a result.

---

###### Conditional Statements

Decision Making - program behaves differently depending on user input, stored data, or system state.

For e.g.

```python
if
elif
else
```

Nested Condition - if statement inside another if statement.

Caution - too much nesting makes code hard to read.

---

###### Loops and Repetition

Loops are when codes needs to repeat. Without loops, it will be long and repetitive. Used for reading files, processing lists and training machine learning codes.

For e.g.

* for Loop - iterate over a sequence or repeat a known number of times
* while Loop - when number of repetitions in not known in advance
* break and continue - either breaks a loop completely or continue skips the current iteration and moves to the next one

---

###### Strings

String is sequence of characters, text data such as names, messages, emails, URLs and password.

* Indexing and Slicing - Indexing starts at 0, negative indexes start from the end.
* String are immutable, you cannot change one character inside the same string object. Python Instead Creates a new string.
* f-Strings are the modern and readable way to insert variables into text.

---

###### Lists, Tuples, Set and Dictionaries

* A list is mutable collection, used to store many values and process them together.
* Tuples is used for fixed data such as coordinates, RGB color values and constant records.
* Set stores unique values, useful for removing duplicates and checking membership efficiently.
* Dictionaries stores key-value pairs, important Python data structures because of APIs, JSON and database records often lookin like dictionaries.

---

###### Function

Reusable block of code that makes code cleaner, reusable, and easier to test.

---

###### Parameters and Arguments

Parameter is the variable written in function definition.

An argument is the actual value passed to the function when calling it.

---

###### List Comprehension

It is a concise way to create a list from an iterable. It is common in data processing and clean Python code.

---

###### Lambda Functions

It is a small anonymous function. Useful for short operations, for eg. map - transforms each item and filter - keeps items that match a condition.

---

##### Some Error Terminologies

| Error            | Meaning                                  |
| ---------------- | ---------------------------------------- |
| SyntaxError      | Wrong Code grammar                       |
| NameError        | Variable or function name is not defined |
| TypeError        | Wrong data type operation                |
| ValueError       | Correct type but invalid value           |
| IndexError       | List index does not exist                |
| KeyError         | Dictrionary key does not exist           |
| IndentationError | Indentation is wrong                     |

* Use these on try....except method to bypass error and run the code
* Use IDE built in debugger like VS Code debugger for learning about the error and bugs
* Test small parts before executing big piles of codes
* Check datatype using `type()`

---

###### File Handling

It is needed as variables disappear when the programs stops running. Python can create and read and write upon this said files to store data permanently. it helps you save user notes, read configuration values, datasets, logs etc.

---

###### Object-Oriented Programming

(OOP) organizes code around objects. An object combines data and behaviour. It also matches real world thinking.

For e.g. Student's got attributes and actions, a bank account has balance and operations and a car has speed and methods.

---

###### 4 pillars of OOP

* Encapsulation - Keep Data and related methods together
* Inheritance - Reuse features from another class
* Polymorphism - Same method name can behave differently
* Abstraction - Hide complex details and expose simple interface

---

###### APIs and JSON

API allows apps to communicate with each other and JSON common data format used by APIs, helping information from backend to fronend or vice versa.

---

###### Database Theory

Four operations of databases (CRUD)

* Create : add new data
* Read : view data
* Update : change existing data
* Delete : remove data

---

###### SQLite

Simple built-in database. Excellent for beginners.

---

##### Python for Web Development

###### Backend Theory

Python on Web Development is used on the backend. The backend receives requests, validates data, talks to databases, applies logic, and returns responses to the frontend.

Common Web Frameworks are Django, FastAPI, and Flask.

* Django is good for full web applications.
* FastAPI is excellent for APIs and AI/ML services.
* Flask is lightweight and flexible.
