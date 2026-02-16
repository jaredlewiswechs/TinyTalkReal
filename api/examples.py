"""Vercel serverless function: GET /api/examples — return example programs."""

import sys, os, json
from pathlib import Path
from http.server import BaseHTTPRequestHandler

# Fix path so the package is importable
_api_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_api_dir)
sys.path = [p for p in sys.path if os.path.abspath(p) != _project_root]
sys.path.insert(0, os.path.dirname(_project_root))
import importlib as _il
if 'realTinyTalk' not in sys.modules:
    sys.modules['realTinyTalk'] = _il.import_module(os.path.basename(_project_root))


def _get_examples():
    examples = [
        {
            'name': '\U0001f44b Hello World',
            'code': '// Welcome to realTinyTalk!\n// The friendliest programming language\n\nshow("Hello World!")\n\n// Space-separated args - no commas needed!\nlet name = "Newton"\nshow("Welcome" name "to realTinyTalk!")\n\n// Property magic - no parentheses needed!\nshow("Uppercase:" name.upcase)\nshow("Length:" name.len)\nshow("Reversed:" name.reversed)',
        },
        {
            'name': '\U0001f4d6 Tutorial: Basics',
            'code': '// TUTORIAL 1: The Basics\n\n// Variables with \'let\'\nlet greeting = "Hello"\nlet number = 42\nlet pi = 3.14159\n\nshow("greeting:" greeting)\nshow("number:" number)\nshow("pi:" pi)\n\n// Math just works\nshow("")\nshow("=== Math ===")\nlet sum = 2 + 3\nlet product = 10 * 4\nlet power = 2 ** 8\nshow("2 + 3 =" sum)\nshow("10 * 4 =" product)\nshow("2 ** 8 =" power)\n\n// Strings\nshow("")\nshow("=== Strings ===")\nlet name = "Alice"\nshow("Hello" name "!")\nshow("Length:" name.len)\nshow("Uppercase:" name.upcase)\nshow("Reversed:" name.reversed)',
        },
        {
            'name': '\U0001f4d6 Tutorial: Functions',
            'code': '// TUTORIAL 2: Functions\n\n// LAW = pure function (no side effects)\nlaw square(x)\n    reply x * x\nend\n\nlaw greet(name)\n    reply "Hello " + name + "!"\nend\n\nshow("square(5) =" square(5))\nshow(greet("World"))\n\n// Functions can call functions\nlaw sum_of_squares(a, b)\n    reply square(a) + square(b)\nend\n\nshow("sum_of_squares(3, 4) =" sum_of_squares(3, 4))\n\n// Recursion works too\nlaw factorial(n)\n    if n <= 1 { reply 1 }\n    reply n * factorial(n - 1)\nend\n\nshow("")\nshow("=== Factorials ===")\nfor i in range(1, 8) {\n    show(i.str + "! =" factorial(i))\n}',
        },
        {
            'name': '\U0001f4d6 Tutorial: Collections',
            'code': '// TUTORIAL 3: Lists & Maps\n\nlet fruits = ["apple", "banana", "cherry"]\nshow("Fruits:" fruits)\nshow("First:" fruits.first)\nshow("Last:" fruits.last)\nshow("Length:" fruits.len)\n\nshow("")\nshow("=== Each fruit ===")\nfor fruit in fruits {\n    show("-" fruit)\n}\n\n// Maps (like dictionaries)\nlet person = {\n    "name": "Alice",\n    "age": 30,\n    "city": "NYC"\n}\n\nshow("")\nshow("=== Person ===")\nshow("Name:" person.name)\nshow("Age:" person.age)\nshow("City:" person.city)\n\nperson.country = "USA"\nshow("Country:" person.country)',
        },
        {
            'name': '\U0001f4d6 Tutorial: Control Flow',
            'code': '// TUTORIAL 4: Control Flow\n\nlet age = 25\n\nif age >= 18 {\n    show("You are an adult")\n} else {\n    show("You are a minor")\n}\n\nshow("")\nshow("=== Countdown ===")\nfor i in range(5, 0, -1) {\n    show(i)\n}\nshow("Liftoff!")\n\nshow("")\nshow("=== Doubling ===")\nlet x = 1\nwhile x < 100 {\n    show(x)\n    x = x * 2\n}\n\nshow("")\nshow("=== Skip evens, stop at 7 ===")\nfor i in range(10) {\n    if i % 2 == 0 { continue }\n    if i > 7 { break }\n    show(i)\n}',
        },
        {
            'name': '\U0001f529 Property Magic',
            'code': '// Property conversions - no parentheses needed!\n\nlet num = 42\nlet text = "3.14"\n\nshow("=== Type Conversions ===")\nshow("num.str:" num.str)\nshow("text.float:" text.float)\nshow("text.int:" text.int)\nshow("num.type:" num.type)\n\nshow("")\nshow("=== String Properties ===")\nlet msg = "  hello world  "\nshow("original:" msg)\nshow("trimmed:" msg.trim)\nshow("upcase:" msg.upcase)\nshow("lowcase:" msg.lowcase)\nshow("len:" msg.len)\nshow("reversed:" msg.reversed)\n\nshow("")\nshow("=== List Properties ===")\nlet items = [1, 2, 3, 4, 5]\nshow("items:" items)\nshow("first:" items.first)\nshow("last:" items.last)\nshow("empty:" items.empty)\nshow("len:" items.len)',
        },
        {
            'name': '\U0001f4dc when (Constants)',
            'code': '// WHEN - Declares immutable facts\n\nwhen PI = 3.14159\nwhen GRAVITY = 9.81\nwhen APP_NAME = "MyApp"\n\nshow("PI:" PI)\nshow("Gravity:" GRAVITY)\nshow("App:" APP_NAME)\n\nlaw circle_area(radius)\n    reply PI * radius * radius\nend\n\nshow("")\nshow("=== Circle Areas ===")\nfor r in range(1, 6) {\n    show("radius" r "-> area" circle_area(r))\n}',
        },
        {
            'name': '\U0001f528 forge (Actions)',
            'code': '// FORGE - Actions that can change state\n\nforge greet(name)\n    show("Hello" name "!")\n    reply "greeted"\nend\n\nforge countdown(n)\n    while n > 0 {\n        show(n)\n        n = n - 1\n    }\n    show("Liftoff!")\nend\n\ngreet("World")\nshow("")\ncountdown(5)',
        },
        {
            'name': '\u2696\ufe0f law/reply/end (classic)',
            'code': '// Classic function syntax (still works!)\n\nlaw square(x)\n    reply x * x\nend\n\nlaw factorial(n)\n    if n <= 1 { reply 1 }\n    reply n * factorial(n - 1)\nend\n\nlaw is_even(n)\n    reply n % 2 == 0\nend\n\nshow("square(5):" square(5))\nshow("factorial(6):" factorial(6))\nshow("is_even(4):" is_even(4))\nshow("is_even(7):" is_even(7))',
        },
        {
            'name': '\U0001f522 Fibonacci',
            'code': '// Fibonacci - clean and simple\n\nlaw fib(n)\n    if n <= 1 { reply n }\n    reply fib(n - 1) + fib(n - 2)\nend\n\nshow("=== Fibonacci Sequence ===")\nfor i in range(12) {\n    show("fib(" i.str ") =" fib(i))\n}',
        },
        {
            'name': '\U0001f3af FizzBuzz',
            'code': '// The classic interview question\n\nlaw fizzbuzz(n)\n    if n % 15 == 0 { reply "FizzBuzz" }\n    if n % 3 == 0 { reply "Fizz" }\n    if n % 5 == 0 { reply "Buzz" }\n    reply n\nend\n\nshow("=== FizzBuzz 1-20 ===")\nfor i in range(1, 21) {\n    show(fizzbuzz(i))\n}',
        },
        {
            'name': '\U0001f50d Prime Numbers',
            'code': '// Find prime numbers\n\nlaw is_prime(n)\n    if n < 2 { reply false }\n    for i in range(2, n) {\n        if n % i == 0 { reply false }\n    }\n    reply true\nend\n\nshow("=== Primes up to 50 ===")\nlet primes = []\nfor n in range(2, 51) {\n    if is_prime(n) {\n        primes = primes + [n]\n    }\n}\nshow(primes)\nshow("")\nshow("Found" primes.len "primes")',
        },
        {
            'name': '\U0001f4ca Quicksort',
            'code': '// Quicksort algorithm\n\nlaw quicksort(arr)\n    if arr.len <= 1 { reply arr }\n    \n    let pivot = arr[0]\n    let less = []\n    let greater = []\n    \n    for i in range(1, arr.len) {\n        if arr[i] < pivot {\n            less = less + [arr[i]]\n        } else {\n            greater = greater + [arr[i]]\n        }\n    }\n    \n    reply quicksort(less) + [pivot] + quicksort(greater)\nend\n\nlet unsorted = [64, 34, 25, 12, 22, 11, 90]\nshow("Unsorted:" unsorted)\nshow("Sorted:" quicksort(unsorted))',
        },
        {
            'name': '\U0001f517 Step Chains (NEW!)',
            'code': '// dplyr-style data manipulation\n// Chain operations with _underscore steps!\n\nlet numbers = [5, 2, 8, 1, 9, 3, 7, 4, 6]\nshow("Numbers:" numbers)\n\nlet top3 = numbers _sort _reverse _take(3)\nshow("Top 3:" top3)\n\nlaw is_even(x)\n    reply x % 2 == 0\nend\n\nlet evens = numbers _filter(is_even)\nshow("Evens:" evens)\nshow("Even count:" numbers _filter(is_even) _count)\n\nshow("Sum:" numbers _sum)\nshow("Average:" numbers _avg)\nshow("Min:" numbers _min)\nshow("Max:" numbers _max)\n\nlaw doubled(x)\n    reply x * 2\nend\n\nshow("Doubled:" numbers _map(doubled))\n\nshow("")\nshow("=== Complex Chain ===")\nlaw big(x)\n    reply x > 3\nend\n\nlet result = numbers _filter(big) _sort _take(3)\nshow("filter(>3) + sort + take(3):" result)',
        },
        {
            'name': '\U0001f4ac Natural Comparisons',
            'code': '// Natural language comparisons!\n// is, isnt, has, hasnt, isin, islike\n\nlet name = "Alice"\nlet numbers = [1, 2, 3, 4, 5]\nlet text = "Hello World"\n\nshow("=== is / isnt ===")\nshow("name is Alice:" (name is "Alice"))\nshow("name isnt Bob:" (name isnt "Bob"))\nshow("5 is 5:" (5 is 5))\nshow("5 isnt 6:" (5 isnt 6))\n\nshow("")\nshow("=== has / hasnt ===")\nshow("numbers has 3:" (numbers has 3))\nshow("numbers hasnt 99:" (numbers hasnt 99))\nshow("text has World:" (text has "World"))\nshow("text hasnt Goodbye:" (text hasnt "Goodbye"))\n\nshow("")\nshow("=== isin ===")\nshow("3 isin numbers:" (3 isin numbers))\nshow("99 isin numbers:" (99 isin numbers))\n\nshow("")\nshow("=== islike (wildcards) ===")\nshow("Alice islike A*:" ("Alice" islike "A*"))\nshow("Alice islike *ice:" ("Alice" islike "*ice"))\nshow("Alice islike Al?ce:" ("Alice" islike "Al?ce"))\nshow("Bob islike A*:" ("Bob" islike "A*"))',
        },
        {
            'name': '\u2728 String Properties',
            'code': '// String properties - no parentheses needed!\n\nlet msg = "  Hello World  "\n\nshow("=== String Properties ===")\nshow("original:" msg)\nshow("trimmed:" msg.trim)\nshow("upcase:" msg.upcase)\nshow("lowcase:" msg.lowcase)\nshow("reversed:" msg.reversed)\nshow("len:" msg.len)\n\nshow("")\nshow("=== Split Operations ===")\nlet sentence = "the quick brown fox"\nshow("words:" sentence.words)\nshow("chars:" sentence.chars)\n\nshow("")\nshow("=== String + Steps ===")\nlet words = sentence.words\nshow("first 2 words:" words _take(2))\nshow("sorted words:" words _sort)\nshow("unique chars:" sentence.chars _unique _sort)',
        },
        {
            'name': '\U0001f3d7\ufe0f Blueprints (OOP)',
            'code': '// Blueprints = Classes in realTinyTalk\n\nblueprint Counter\n    field value\n    \n    forge inc()\n        self.value = self.value + 1\n        reply self.value\n    end\n    \n    forge add(n)\n        self.value = self.value + n\n        reply self.value\n    end\n    \n    forge reset()\n        self.value = 0\n        reply self.value\n    end\nend\n\nlet c = Counter(0)\nshow("Initial:" c.value)\nshow("After inc():" c.inc())\nshow("After inc():" c.inc())\nshow("After add(10):" c.add(10))\nshow("After reset():" c.reset())\n\nlet increment = c.inc\nshow("Calling bound method:" increment())\nshow("Again:" increment())',
        },
        {
            'name': '\U0001f504 Higher-Order Functions',
            'code': '// Pass functions to other functions!\n\nlet numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n\nlaw doubled(x)\n    reply x * 2\nend\n\nlaw squared(x)\n    reply x * x\nend\n\nlaw is_even(x)\n    reply x % 2 == 0\nend\n\nlaw is_odd(x)\n    reply x % 2 == 1\nend\n\nlaw greater_than_5(x)\n    reply x > 5\nend\n\nshow("=== Transform with _map ===")\nshow("Numbers:" numbers)\nshow("Doubled:" numbers _map(doubled))\nshow("Squared:" numbers _map(squared))\n\nshow("")\nshow("=== Filter with predicates ===")\nshow("Evens:" numbers _filter(is_even))\nshow("Odds:" numbers _filter(is_odd))\n\nshow("")\nshow("=== Chain them! ===")\nlet result = numbers _filter(is_odd) _map(squared) _sum\nshow("Sum of squared odds:" result)\nshow("Big doubled top 3:" numbers _filter(greater_than_5) _map(doubled) _take(3))\n\nshow("")\nshow("=== Functions are values ===")\nlaw apply_twice(func, x)\n    reply func(func(x))\nend\n\nshow("apply_twice(doubled, 3):" apply_twice(doubled, 3))\nshow("apply_twice(squared, 2):" apply_twice(squared, 2))',
        },
    ]

    # Also include .tt files from the repository root
    repo_root = Path(_project_root)
    existing_names = {e['name'] for e in examples}
    for sample_path in sorted(repo_root.glob('*.tt')):
        display_name = f"\U0001f4c4 {sample_path.stem.replace('_', ' ').title()}"
        if display_name in existing_names:
            continue
        try:
            code = sample_path.read_text(encoding='utf-8')
        except Exception:
            continue
        examples.append({'name': display_name, 'code': code})
        existing_names.add(display_name)

    return examples


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        resp = json.dumps(_get_examples())
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(resp.encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
