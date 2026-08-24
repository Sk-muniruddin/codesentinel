from codesentinel.diff_parser import parse_git_diff


def test_parse_added_line():
    diff = """\
diff --git a/sample.py b/sample.py
index 1234567..abcdefg 100644
--- a/sample.py
+++ b/sample.py
@@ -1,2 +1,4 @@
 def hello():
     return "hello"
+def goodbye():
+    return "bye"
"""

    changes = parse_git_diff(diff)

    assert len(changes) == 2

    assert changes[0].file == "sample.py"
    assert changes[0].line == 3
    assert changes[0].change_type == "added"
    assert changes[0].content == "def goodbye():"

    assert changes[1].file == "sample.py"
    assert changes[1].line == 4
    assert changes[1].change_type == "added"
    assert changes[1].content == '    return "bye"'


def test_parse_correct_line_number():
    diff = """\
diff --git a/sample.py b/sample.py
index 1234567..abcdefg 100644
--- a/sample.py
+++ b/sample.py
@@ -1,6 +1,8 @@
 def first():
     return 1


 def second():
     return 2


+def third():
+    return 3
"""

    changes = parse_git_diff(diff)

    assert len(changes) == 2

    assert changes[0].file == "sample.py"
    assert changes[0].line == 9
    assert changes[0].change_type == "added"
    assert changes[0].content == "def third():"

    assert changes[1].file == "sample.py"
    assert changes[1].line == 10
    assert changes[1].change_type == "added"
    assert changes[1].content == "    return 3"


def test_ignore_git_metadata():
    diff = """\
diff --git a/sample.py b/sample.py
index 1234567..abcdefg 100644
--- a/sample.py
+++ b/sample.py
@@ -1,1 +1,2 @@
 def hello():
+    return "hello"
\\ No newline at end of file
"""

    changes = parse_git_diff(diff)

    assert len(changes) == 1
    assert changes[0].content == '    return "hello"'


def test_ignore_blank_added_lines():
    diff = """\
diff --git a/sample.py b/sample.py
index 1234567..abcdefg 100644
--- a/sample.py
+++ b/sample.py
@@ -1,1 +1,3 @@
 def hello():
+
+    return "hello"
"""

    changes = parse_git_diff(diff)

    assert len(changes) == 1
    assert changes[0].content == '    return "hello"'


def test_ignore_identical_delete_add_pair():
    diff = """\
diff --git a/sample.py b/sample.py
index 1234567..abcdefg 100644
--- a/sample.py
+++ b/sample.py
@@ -1,1 +1,1 @@
-    return 0
+    return 0
"""

    changes = parse_git_diff(diff)

    assert changes == []


def test_parse_modified_line():
    diff = """\
diff --git a/sample.py b/sample.py
index 1234567..abcdefg 100644
--- a/sample.py
+++ b/sample.py
@@ -1,2 +1,2 @@
 def get_user():
-    return user.name
+    return user.username
"""

    changes = parse_git_diff(diff)

    assert len(changes) == 2

    assert changes[0].file == "sample.py"
    assert changes[0].line == 2
    assert changes[0].change_type == "added"
    assert changes[0].content == "    return user.username"

    assert changes[1].file == "sample.py"
    assert changes[1].change_type == "deleted"
    assert changes[1].content == "    return user.name"


def test_parse_deleted_line():
    diff = """\
diff --git a/sample.py b/sample.py
index 1234567..abcdefg 100644
--- a/sample.py
+++ b/sample.py
@@ -1,3 +1,2 @@
 def get_user():
-    return user.name
     return user.username
"""

    changes = parse_git_diff(diff)

    assert len(changes) == 1

    assert changes[0].file == "sample.py"
    assert changes[0].change_type == "deleted"
    assert changes[0].content == "    return user.name"