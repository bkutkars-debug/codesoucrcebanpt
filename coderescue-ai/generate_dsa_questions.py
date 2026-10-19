import json
import os

questions = [
    # ==================== 50 EASY QUESTIONS ====================
    {
        "id": 1,
        "title": "Two Sum",
        "difficulty": "Easy",
        "category": "Arrays & Hashing",
        "companies": ["Google", "Amazon", "Meta", "Microsoft"],
        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0, 1]", "explanation": "nums[0] + nums[1] == 9, so return [0, 1]."},
            {"input": "nums = [3,2,4], target = 6", "output": "[1, 2]", "explanation": "nums[1] + nums[2] == 6, so return [1, 2]."}
        ],
        "constraints": ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "-10^9 <= target <= 10^9", "Only one valid answer exists."],
        "starterCode": "def two_sum(nums: list[int], target: int) -> list[int]:\n    # Write your solution here\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []\n",
        "entryFunction": "two_sum",
        "testCases": [
            {"input": {"nums": [2, 7, 11, 15], "target": 9}, "expected": [0, 1]},
            {"input": {"nums": [3, 2, 4], "target": 6}, "expected": [1, 2]},
            {"input": {"nums": [3, 3], "target": 6}, "expected": [0, 1]},
            {"input": {"nums": [-1, -2, -3, -4, -5], "target": -8}, "expected": [2, 4]}
        ]
    },
    {
        "id": 2,
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "category": "Stack",
        "companies": ["Meta", "Amazon", "Bloomberg", "Google"],
        "description": "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.",
        "examples": [
            {"input": "s = '()' ", "output": "True"},
            {"input": "s = '()[]{}' ", "output": "True"},
            {"input": "s = '(]' ", "output": "False"}
        ],
        "constraints": ["1 <= s.length <= 10^4", "s consists of parentheses only '()[]{}'."],
        "starterCode": "def is_valid_parentheses(s: str) -> bool:\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                return False\n        else:\n            stack.append(char)\n    return not stack\n",
        "entryFunction": "is_valid_parentheses",
        "testCases": [
            {"input": {"s": "()"}, "expected": True},
            {"input": {"s": "()[]{}"}, "expected": True},
            {"input": {"s": "(]"}, "expected": False},
            {"input": {"s": "([)]"}, "expected": False},
            {"input": {"s": "{[]}"}, "expected": True}
        ]
    },
    {
        "id": 3,
        "title": "Best Time to Buy and Sell Stock",
        "difficulty": "Easy",
        "category": "Arrays & Dynamic Programming",
        "companies": ["Amazon", "Meta", "Google", "Microsoft"],
        "description": "You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.",
        "examples": [
            {"input": "prices = [7,1,5,3,6,4]", "output": "5", "explanation": "Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5."},
            {"input": "prices = [7,6,4,3,1]", "output": "0", "explanation": "In this case, no transactions are done and max profit = 0."}
        ],
        "constraints": ["1 <= prices.length <= 10^5", "0 <= prices[i] <= 10^4"],
        "starterCode": "def max_profit(prices: list[int]) -> int:\n    min_price = float('inf')\n    max_prof = 0\n    for p in prices:\n        if p < min_price:\n            min_price = p\n        elif p - min_price > max_prof:\n            max_prof = p - min_price\n    return max_prof\n",
        "entryFunction": "max_profit",
        "testCases": [
            {"input": {"prices": [7, 1, 5, 3, 6, 4]}, "expected": 5},
            {"input": {"prices": [7, 6, 4, 3, 1]}, "expected": 0},
            {"input": {"prices": [1, 2]}, "expected": 1},
            {"input": {"prices": [2, 4, 1]}, "expected": 2}
        ]
    },
    {
        "id": 4,
        "title": "Valid Palindrome",
        "difficulty": "Easy",
        "category": "Two Pointers",
        "companies": ["Meta", "Microsoft", "Apple"],
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.\n\nGiven a string `s`, return `True` if it is a palindrome, or `False` otherwise.",
        "examples": [
            {"input": "s = 'A man, a plan, a canal: Panama'", "output": "True"},
            {"input": "s = 'race a car'", "output": "False"}
        ],
        "constraints": ["1 <= s.length <= 2 * 10^5"],
        "starterCode": "def is_palindrome(s: str) -> bool:\n    cleaned = [c.lower() for c in s if c.isalnum()]\n    return cleaned == cleaned[::-1]\n",
        "entryFunction": "is_palindrome",
        "testCases": [
            {"input": {"s": "A man, a plan, a canal: Panama"}, "expected": True},
            {"input": {"s": "race a car"}, "expected": False},
            {"input": {"s": " "}, "expected": True},
            {"input": {"s": "0P"}, "expected": False}
        ]
    },
    {
        "id": 5,
        "title": "Valid Anagram",
        "difficulty": "Easy",
        "category": "Strings & Hashing",
        "companies": ["Uber", "Google", "Amazon"],
        "description": "Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise. An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "examples": [
            {"input": "s = 'anagram', t = 'nagaram'", "output": "True"},
            {"input": "s = 'rat', t = 'car'", "output": "False"}
        ],
        "constraints": ["1 <= s.length, t.length <= 5 * 10^4", "s and t consist of lowercase English letters."],
        "starterCode": "def is_anagram(s: str, t: str) -> bool:\n    if len(s) != len(t):\n        return False\n    counts = {}\n    for c in s:\n        counts[c] = counts.get(c, 0) + 1\n    for c in t:\n        if c not in counts or counts[c] == 0:\n            return False\n        counts[c] -= 1\n    return True\n",
        "entryFunction": "is_anagram",
        "testCases": [
            {"input": {"s": "anagram", "t": "nagaram"}, "expected": True},
            {"input": {"s": "rat", "t": "car"}, "expected": False},
            {"input": {"s": "a", "t": "ab"}, "expected": False}
        ]
    },
    {
        "id": 6,
        "title": "Binary Search",
        "difficulty": "Easy",
        "category": "Binary Search",
        "companies": ["Apple", "Google", "Amazon"],
        "description": "Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return -1.\n\nYou must write an algorithm with `O(log n)` runtime complexity.",
        "examples": [
            {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4"},
            {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1"}
        ],
        "constraints": ["1 <= nums.length <= 10^4", "-10^4 < nums[i], target < 10^4", "All integers in nums are unique and sorted."],
        "starterCode": "def search(nums: list[int], target: int) -> int:\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n",
        "entryFunction": "search",
        "testCases": [
            {"input": {"nums": [-1, 0, 3, 5, 9, 12], "target": 9}, "expected": 4},
            {"input": {"nums": [-1, 0, 3, 5, 9, 12], "target": 2}, "expected": -1},
            {"input": {"nums": [5], "target": 5}, "expected": 0}
        ]
    },
    {
        "id": 7,
        "title": "Maximum Subarray (Kadane's Algorithm)",
        "difficulty": "Easy",
        "category": "Arrays & Dynamic Programming",
        "companies": ["Amazon", "Microsoft", "LinkedIn", "Apple"],
        "description": "Given an integer array `nums`, find the subarray with the largest sum, and return its sum.",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "The subarray [4,-1,2,1] has the largest sum 6."},
            {"input": "nums = [1]", "output": "1"},
            {"input": "nums = [5,4,-1,7,8]", "output": "23"}
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "starterCode": "def max_sub_array(nums: list[int]) -> int:\n    max_sum = current_sum = nums[0]\n    for x in nums[1:]:\n        current_sum = max(x, current_sum + x)\n        max_sum = max(max_sum, current_sum)\n    return max_sum\n",
        "entryFunction": "max_sub_array",
        "testCases": [
            {"input": {"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]}, "expected": 6},
            {"input": {"nums": [1]}, "expected": 1},
            {"input": {"nums": [5, 4, -1, 7, 8]}, "expected": 23},
            {"input": {"nums": [-1]}, "expected": -1}
        ]
    },
    {
        "id": 8,
        "title": "Contains Duplicate",
        "difficulty": "Easy",
        "category": "Arrays & Hashing",
        "companies": ["Apple", "Amazon", "Microsoft"],
        "description": "Given an integer array `nums`, return `True` if any value appears at least twice in the array, and return `False` if every element is distinct.",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "True"},
            {"input": "nums = [1,2,3,4]", "output": "False"}
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
        "starterCode": "def contains_duplicate(nums: list[int]) -> bool:\n    return len(nums) != len(set(nums))\n",
        "entryFunction": "contains_duplicate",
        "testCases": [
            {"input": {"nums": [1, 2, 3, 1]}, "expected": True},
            {"input": {"nums": [1, 2, 3, 4]}, "expected": False},
            {"input": {"nums": [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]}, "expected": True}
        ]
    },
    {
        "id": 9,
        "title": "Climbing Stairs",
        "difficulty": "Easy",
        "category": "Dynamic Programming",
        "companies": ["Google", "Amazon", "Adobe"],
        "description": "You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "examples": [
            {"input": "n = 2", "output": "2", "explanation": "1 step + 1 step, or 2 steps."},
            {"input": "n = 3", "output": "3", "explanation": "1+1+1, 1+2, or 2+1."}
        ],
        "constraints": ["1 <= n <= 45"],
        "starterCode": "def climb_stairs(n: int) -> int:\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b\n",
        "entryFunction": "climb_stairs",
        "testCases": [
            {"input": {"n": 2}, "expected": 2},
            {"input": {"n": 3}, "expected": 3},
            {"input": {"n": 4}, "expected": 5},
            {"input": {"n": 5}, "expected": 8}
        ]
    },
    {
        "id": 10,
        "title": "Majority Element",
        "difficulty": "Easy",
        "category": "Arrays",
        "companies": ["Amazon", "Microsoft", "Google"],
        "description": "Given an array `nums` of size `n`, return the majority element. The majority element is the element that appears more than `⌊n / 2⌋` times. You may assume that the majority element always exists in the array.",
        "examples": [
            {"input": "nums = [3,2,3]", "output": "3"},
            {"input": "nums = [2,2,1,1,1,2,2]", "output": "2"}
        ],
        "constraints": ["n == nums.length", "1 <= n <= 5 * 10^4", "-10^9 <= nums[i] <= 10^9"],
        "starterCode": "def majority_element(nums: list[int]) -> int:\n    # Boyer-Moore Voting Algorithm O(N) time O(1) space\n    candidate = None\n    count = 0\n    for num in nums:\n        if count == 0:\n            candidate = num\n        count += (1 if num == candidate else -1)\n    return candidate\n",
        "entryFunction": "majority_element",
        "testCases": [
            {"input": {"nums": [3, 2, 3]}, "expected": 3},
            {"input": {"nums": [2, 2, 1, 1, 1, 2, 2]}, "expected": 2},
            {"input": {"nums": [1]}, "expected": 1}
        ]
    },
    {
        "id": 11,
        "title": "Single Number",
        "difficulty": "Easy",
        "category": "Bit Manipulation",
        "companies": ["Amazon", "Google", "Microsoft"],
        "description": "Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one. You must implement a solution with a linear runtime complexity and use only constant extra space.",
        "examples": [
            {"input": "nums = [2,2,1]", "output": "1"},
            {"input": "nums = [4,1,2,1,2]", "output": "4"}
        ],
        "constraints": ["1 <= nums.length <= 3 * 10^4", "-3 * 10^4 <= nums[i] <= 3 * 10^4"],
        "starterCode": "def single_number(nums: list[int]) -> int:\n    result = 0\n    for num in nums:\n        result ^= num\n    return result\n",
        "entryFunction": "single_number",
        "testCases": [
            {"input": {"nums": [2, 2, 1]}, "expected": 1},
            {"input": {"nums": [4, 1, 2, 1, 2]}, "expected": 4},
            {"input": {"nums": [1]}, "expected": 1}
        ]
    },
    {
        "id": 12,
        "title": "Missing Number",
        "difficulty": "Easy",
        "category": "Bit Manipulation & Math",
        "companies": ["Microsoft", "Amazon", "Meta"],
        "description": "Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.",
        "examples": [
            {"input": "nums = [3,0,1]", "output": "2"},
            {"input": "nums = [0,1]", "output": "2"},
            {"input": "nums = [9,6,4,2,3,5,7,0,1]", "output": "8"}
        ],
        "constraints": ["n == nums.length", "1 <= n <= 10^4", "0 <= nums[i] <= n"],
        "starterCode": "def missing_number(nums: list[int]) -> int:\n    n = len(nums)\n    expected_sum = n * (n + 1) // 2\n    return expected_sum - sum(nums)\n",
        "entryFunction": "missing_number",
        "testCases": [
            {"input": {"nums": [3, 0, 1]}, "expected": 2},
            {"input": {"nums": [0, 1]}, "expected": 2},
            {"input": {"nums": [9, 6, 4, 2, 3, 5, 7, 0, 1]}, "expected": 8}
        ]
    },
    {
        "id": 13,
        "title": "Move Zeroes",
        "difficulty": "Easy",
        "category": "Two Pointers",
        "companies": ["Meta", "Apple", "Amazon"],
        "description": "Given an integer array `nums`, move all 0's to the end of it while maintaining the relative order of the non-zero elements. Note that you must do this in-place without making a copy of the array.",
        "examples": [
            {"input": "nums = [0,1,0,3,12]", "output": "[1,3,12,0,0]"},
            {"input": "nums = [0]", "output": "[0]"}
        ],
        "constraints": ["1 <= nums.length <= 10^4", "-2^31 <= nums[i] <= 2^31 - 1"],
        "starterCode": "def move_zeroes(nums: list[int]) -> list[int]:\n    insert_pos = 0\n    for num in nums:\n        if num != 0:\n            nums[insert_pos] = num\n            insert_pos += 1\n    while insert_pos < len(nums):\n        nums[insert_pos] = 0\n        insert_pos += 1\n    return nums\n",
        "entryFunction": "move_zeroes",
        "testCases": [
            {"input": {"nums": [0, 1, 0, 3, 12]}, "expected": [1, 3, 12, 0, 0]},
            {"input": {"nums": [0]}, "expected": [0]},
            {"input": {"nums": [1, 0]}, "expected": [1, 0]}
        ]
    },
    {
        "id": 14,
        "title": "Reverse String",
        "difficulty": "Easy",
        "category": "Two Pointers",
        "companies": ["Microsoft", "Google"],
        "description": "Write a function that reverses an array of characters in-place with `O(1)` extra memory.",
        "examples": [
            {"input": "s = ['h','e','l','l','o']", "output": "['o','l','l','e','h']"}
        ],
        "constraints": ["1 <= s.length <= 10^5"],
        "starterCode": "def reverse_string(s: list[str]) -> list[str]:\n    left, right = 0, len(s) - 1\n    while left < right:\n        s[left], s[right] = s[right], s[left]\n        left += 1\n        right -= 1\n    return s\n",
        "entryFunction": "reverse_string",
        "testCases": [
            {"input": {"s": ["h", "e", "l", "l", "o"]}, "expected": ["o", "l", "l", "e", "h"]},
            {"input": {"s": ["H", "a", "n", "n", "a", "h"]}, "expected": ["h", "a", "n", "n", "a", "H"]}
        ]
    },
    {
        "id": 15,
        "title": "Roman to Integer",
        "difficulty": "Easy",
        "category": "Math & Strings",
        "companies": ["Amazon", "Google", "Apple"],
        "description": "Roman numerals are represented by seven different symbols: I (1), V (5), X (10), L (50), C (100), D (500) and M (1000). Given a roman numeral, convert it to an integer.",
        "examples": [
            {"input": "s = 'III'", "output": "3"},
            {"input": "s = 'LVIII'", "output": "58"},
            {"input": "s = 'MCMXCIV'", "output": "1994"}
        ],
        "constraints": ["1 <= s.length <= 15"],
        "starterCode": "def roman_to_int(s: str) -> int:\n    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}\n    total = 0\n    for i in range(len(s)):\n        if i + 1 < len(s) and vals[s[i]] < vals[s[i + 1]]:\n            total -= vals[s[i]]\n        else:\n            total += vals[s[i]]\n    return total\n",
        "entryFunction": "roman_to_int",
        "testCases": [
            {"input": {"s": "III"}, "expected": 3},
            {"input": {"s": "LVIII"}, "expected": 58},
            {"input": {"s": "MCMXCIV"}, "expected": 1994}
        ]
    },
    {
        "id": 16,
        "title": "Longest Common Prefix",
        "difficulty": "Easy",
        "category": "Strings",
        "companies": ["Amazon", "Google", "Meta"],
        "description": "Write a function to find the longest common prefix string amongst an array of strings. If there is no common prefix, return an empty string `\"\"`.",
        "examples": [
            {"input": "strs = ['flower','flow','flight']", "output": "'fl'"},
            {"input": "strs = ['dog','racecar','car']", "output": "''"}
        ],
        "constraints": ["1 <= strs.length <= 200", "0 <= strs[i].length <= 200"],
        "starterCode": "def longest_common_prefix(strs: list[str]) -> str:\n    if not strs:\n        return \"\"\n    prefix = strs[0]\n    for s in strs[1:]:\n        while not s.startswith(prefix):\n            prefix = prefix[:-1]\n            if not prefix:\n                return \"\"\n    return prefix\n",
        "entryFunction": "longest_common_prefix",
        "testCases": [
            {"input": {"strs": ["flower", "flow", "flight"]}, "expected": "fl"},
            {"input": {"strs": ["dog", "racecar", "car"]}, "expected": ""},
            {"input": {"strs": ["interview", "internet", "internal"]}, "expected": "inter"}
        ]
    },
    {
        "id": 17,
        "title": "Remove Duplicates from Sorted Array",
        "difficulty": "Easy",
        "category": "Two Pointers",
        "companies": ["Microsoft", "Meta"],
        "description": "Given an integer array `nums` sorted in non-decreasing order, remove duplicates in-place such that each unique element appears only once. Return the number of unique elements `k`.",
        "examples": [
            {"input": "nums = [1,1,2]", "output": "2, nums = [1,2,_]"}
        ],
        "constraints": ["1 <= nums.length <= 3 * 10^4"],
        "starterCode": "def remove_duplicates(nums: list[int]) -> int:\n    if not nums:\n        return 0\n    k = 1\n    for i in range(1, len(nums)):\n        if nums[i] != nums[i - 1]:\n            nums[k] = nums[i]\n            k += 1\n    return k\n",
        "entryFunction": "remove_duplicates",
        "testCases": [
            {"input": {"nums": [1, 1, 2]}, "expected": 2},
            {"input": {"nums": [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]}, "expected": 5}
        ]
    },
    {
        "id": 18,
        "title": "Search Insert Position",
        "difficulty": "Easy",
        "category": "Binary Search",
        "companies": ["Google", "Amazon"],
        "description": "Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.",
        "examples": [
            {"input": "nums = [1,3,5,6], target = 5", "output": "2"},
            {"input": "nums = [1,3,5,6], target = 2", "output": "1"}
        ],
        "constraints": ["1 <= nums.length <= 10^4", "-10^4 <= nums[i], target <= 10^4"],
        "starterCode": "def search_insert(nums: list[int], target: int) -> int:\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return left\n",
        "entryFunction": "search_insert",
        "testCases": [
            {"input": {"nums": [1, 3, 5, 6], "target": 5}, "expected": 2},
            {"input": {"nums": [1, 3, 5, 6], "target": 2}, "expected": 1},
            {"input": {"nums": [1, 3, 5, 6], "target": 7}, "expected": 4}
        ]
    },
    {
        "id": 19,
        "title": "Squares of a Sorted Array",
        "difficulty": "Easy",
        "category": "Two Pointers",
        "companies": ["Meta", "Amazon"],
        "description": "Given an integer array `nums` sorted in non-decreasing order, return an array of the squares of each number sorted in non-decreasing order.",
        "examples": [
            {"input": "nums = [-4,-1,0,3,10]", "output": "[0,1,9,16,100]"}
        ],
        "constraints": ["1 <= nums.length <= 10^4", "-10^4 <= nums[i] <= 10^4"],
        "starterCode": "def sorted_squares(nums: list[int]) -> list[int]:\n    n = len(nums)\n    res = [0] * n\n    left, right = 0, n - 1\n    idx = n - 1\n    while left <= right:\n        l_sq = nums[left] ** 2\n        r_sq = nums[right] ** 2\n        if l_sq > r_sq:\n            res[idx] = l_sq\n            left += 1\n        else:\n            res[idx] = r_sq\n            right -= 1\n        idx -= 1\n    return res\n",
        "entryFunction": "sorted_squares",
        "testCases": [
            {"input": {"nums": [-4, -1, 0, 3, 10]}, "expected": [0, 1, 9, 16, 100]},
            {"input": {"nums": [-7, -3, 2, 3, 11]}, "expected": [4, 9, 9, 49, 121]}
        ]
    },
    {
        "id": 20,
        "title": "Pascal's Triangle",
        "difficulty": "Easy",
        "category": "Dynamic Programming",
        "companies": ["Apple", "Amazon", "Google"],
        "description": "Given an integer `numRows`, return the first `numRows` of Pascal's triangle.",
        "examples": [
            {"input": "numRows = 5", "output": "[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]"}
        ],
        "constraints": ["1 <= numRows <= 30"],
        "starterCode": "def generate_pascal(numRows: int) -> list[list[int]]:\n    res = []\n    for i in range(numRows):\n        row = [1] * (i + 1)\n        for j in range(1, i):\n            row[j] = res[i - 1][j - 1] + res[i - 1][j]\n        res.append(row)\n    return res\n",
        "entryFunction": "generate_pascal",
        "testCases": [
            {"input": {"numRows": 5}, "expected": [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]},
            {"input": {"numRows": 1}, "expected": [[1]]}
        ]
    }
]

# We will expand questions programmatically up to 100 questions (50 Easy, 30 Medium, 20 Hard)
topics_easy = [
    ("Counting Bits", "Bit Manipulation", "count_bits", "n: int", "list[int]", "return [bin(i).count('1') for i in range(n + 1)]", [{"input": {"n": 2}, "expected": [0, 1, 1]}, {"input": {"n": 5}, "expected": [0, 1, 1, 2, 1, 2]}]),
    ("Number of 1 Bits", "Bit Manipulation", "hamming_weight", "n: int", "int", "return bin(n).count('1')", [{"input": {"n": 11}, "expected": 3}, {"input": {"n": 128}, "expected": 1}]),
    ("Power of Two", "Bit Manipulation", "is_power_of_two", "n: int", "bool", "return n > 0 and (n & (n - 1)) == 0", [{"input": {"n": 1}, "expected": True}, {"input": {"n": 16}, "expected": True}, {"input": {"n": 3}, "expected": False}]),
    ("Reverse Bits", "Bit Manipulation", "reverse_bits", "n: int", "int", "res = 0\n    for _ in range(32):\n        res = (res << 1) | (n & 1)\n        n >>= 1\n    return res", [{"input": {"n": 43261596}, "expected": 964176192}]),
    ("Merge Sorted Array", "Two Pointers", "merge_sorted", "nums1: list[int], m: int, nums2: list[int], n: int", "list[int]", "nums1[m:m+n] = nums2\n    nums1.sort()\n    return nums1", [{"input": {"nums1": [1, 2, 3, 0, 0, 0], "m": 3, "nums2": [2, 5, 6], "n": 3}, "expected": [1, 2, 2, 3, 5, 6]}]),
    ("Is Subsequence", "Two Pointers", "is_subsequence", "s: str, t: str", "bool", "i = 0\n    for c in t:\n        if i < len(s) and s[i] == c:\n            i += 1\n    return i == len(s)", [{"input": {"s": "abc", "t": "ahbgdc"}, "expected": True}, {"input": {"s": "axc", "t": "ahbgdc"}, "expected": False}]),
    ("Find Pivot Index", "Arrays", "pivot_index", "nums: list[int]", "int", "total = sum(nums)\n    left = 0\n    for i, x in enumerate(nums):\n        if left == total - left - x:\n            return i\n        left += x\n    return -1", [{"input": {"nums": [1, 7, 3, 6, 5, 6]}, "expected": 3}, {"input": {"nums": [1, 2, 3]}, "expected": -1}]),
    ("Min Cost Climbing Stairs", "Dynamic Programming", "min_cost_climbing_stairs", "cost: list[int]", "int", "a, b = cost[0], cost[1]\n    for i in range(2, len(cost)):\n        a, b = b, cost[i] + min(a, b)\n    return min(a, b)", [{"input": {"cost": [10, 15, 20]}, "expected": 15}, {"input": {"cost": [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]}, "expected": 6}]),
    ("Backspace String Compare", "Stack", "backspace_compare", "s: str, t: str", "bool", "def build(st):\n        b = []\n        for c in st:\n            if c != '#': b.append(c)\n            elif b: b.pop()\n        return ''.join(b)\n    return build(s) == build(t)", [{"input": {"s": "ab#c", "t": "ad#c"}, "expected": True}, {"input": {"s": "a#c", "t": "b"}, "expected": False}]),
    ("First Unique Character in a String", "Strings & Hash Map", "first_uniq_char", "s: str", "int", "from collections import Counter\n    count = Counter(s)\n    for idx, ch in enumerate(s):\n        if count[ch] == 1:\n            return idx\n    return -1", [{"input": {"s": "leetcode"}, "expected": 0}, {"input": {"s": "loveleetcode"}, "expected": 2}]),
    ("Intersection of Two Arrays", "Hash Set", "intersection", "nums1: list[int], nums2: list[int]", "list[int]", "return sorted(list(set(nums1) & set(nums2)))", [{"input": {"nums1": [1, 2, 2, 1], "nums2": [2, 2]}, "expected": [2]}]),
    ("Ransom Note", "Hash Map", "can_construct", "ransomNote: str, magazine: str", "bool", "from collections import Counter\n    r_cnt, m_cnt = Counter(ransomNote), Counter(magazine)\n    return all(m_cnt[ch] >= r_cnt[ch] for ch in r_cnt)", [{"input": {"ransomNote": "a", "magazine": "b"}, "expected": False}, {"input": {"ransomNote": "aa", "magazine": "aab"}, "expected": True}]),
    ("Happy Number", "Hash Set & Math", "is_happy", "n: int", "bool", "seen = set()\n    while n != 1 and n not in seen:\n        seen.add(n)\n        n = sum(int(d)**2 for d in str(n))\n    return n == 1", [{"input": {"n": 19}, "expected": True}, {"input": {"n": 2}, "expected": False}]),
    ("Excel Sheet Column Number", "Math", "title_to_number", "columnTitle: str", "int", "res = 0\n    for c in columnTitle:\n        res = res * 26 + (ord(c) - ord('A') + 1)\n    return res", [{"input": {"columnTitle": "A"}, "expected": 1}, {"input": {"columnTitle": "AB"}, "expected": 28}]),
    ("Max Consecutive Ones", "Arrays", "find_max_consecutive_ones", "nums: list[int]", "int", "max_c = cur_c = 0\n    for n in nums:\n        cur_c = cur_c + 1 if n == 1 else 0\n        max_c = max(max_c, cur_c)\n    return max_c", [{"input": {"nums": [1, 1, 0, 1, 1, 1]}, "expected": 3}]),
    ("Can Place Flowers", "Greedy", "can_place_flowers", "flowerbed: list[int], n: int", "bool", "count = 0\n    f = [0] + flowerbed + [0]\n    for i in range(1, len(f) - 1):\n        if f[i-1] == f[i] == f[i+1] == 0:\n            f[i] = 1\n            count += 1\n    return count >= n", [{"input": {"flowerbed": [1, 0, 0, 0, 1], "n": 1}, "expected": True}, {"input": {"flowerbed": [1, 0, 0, 0, 1], "n": 2}, "expected": False}]),
    ("Reverse Vowels of a String", "Two Pointers", "reverse_vowels", "s: str", "str", "vowels = set('aeiouAEIOU')\n    chars = list(s)\n    l, r = 0, len(chars) - 1\n    while l < r:\n        while l < r and chars[l] not in vowels: l += 1\n        while l < r and chars[r] not in vowels: r -= 1\n        chars[l], chars[r] = chars[r], chars[l]\n        l += 1; r -= 1\n    return ''.join(chars)", [{"input": {"s": "hello"}, "expected": "holle"}, {"input": {"s": "leetcode"}, "expected": "leotcede"}]),
    ("Monotonic Array", "Arrays", "is_monotonic", "nums: list[int]", "bool", "inc = dec = True\n    for i in range(len(nums) - 1):\n        if nums[i] > nums[i+1]: inc = False\n        if nums[i] < nums[i+1]: dec = False\n    return inc or dec", [{"input": {"nums": [1, 2, 2, 3]}, "expected": True}, {"input": {"nums": [1, 3, 2]}, "expected": False}]),
    ("Find the Difference", "Bit Manipulation & Strings", "find_the_difference", "s: str, t: str", "str", "from collections import Counter\n    diff = Counter(t) - Counter(s)\n    return list(diff.keys())[0]", [{"input": {"s": "abcd", "t": "abcde"}, "expected": "e"}]),
    ("Add Digits", "Math", "add_digits", "num: int", "int", "if num == 0: return 0\n    return 9 if num % 9 == 0 else num % 9", [{"input": {"num": 38}, "expected": 2}, {"input": {"num": 0}, "expected": 0}]),
    ("Word Pattern", "Hash Map", "word_pattern", "pattern: str, s: str", "bool", "words = s.split()\n    if len(pattern) != len(words): return False\n    return len(set(zip(pattern, words))) == len(set(pattern)) == len(set(words))", [{"input": {"pattern": "abba", "s": "dog cat cat dog"}, "expected": True}, {"input": {"pattern": "abba", "s": "dog cat cat fish"}, "expected": False}]),
    ("Isomorphic Strings", "Hash Map", "is_isomorphic", "s: str, t: str", "bool", "return len(set(zip(s, t))) == len(set(s)) == len(set(t))", [{"input": {"s": "egg", "t": "add"}, "expected": True}, {"input": {"s": "foo", "t": "bar"}, "expected": False}]),
    ("Length of Last Word", "Strings", "length_of_last_word", "s: str", "int", "words = s.strip().split()\n    return len(words[-1]) if words else 0", [{"input": {"s": "Hello World"}, "expected": 5}, {"input": {"s": "   fly me   to   the moon  "}, "expected": 4}]),
    ("Plus One", "Arrays & Math", "plus_one", "digits: list[int]", "list[int]", "num = int(''.join(map(str, digits))) + 1\n    return [int(d) for d in str(num)]", [{"input": {"digits": [1, 2, 3]}, "expected": [1, 2, 4]}, {"input": {"digits": [9, 9]}, "expected": [1, 0, 0]}]),
    ("Sqrt(x)", "Binary Search & Math", "my_sqrt", "x: int", "int", "import math\n    return int(math.isqrt(x))", [{"input": {"x": 4}, "expected": 2}, {"input": {"x": 8}, "expected": 2}]),
    ("Ugly Number", "Math", "is_ugly", "n: int", "bool", "if n <= 0: return False\n    for p in [2, 3, 5]:\n        while n % p == 0: n //= p\n    return n == 1", [{"input": {"n": 6}, "expected": True}, {"input": {"n": 14}, "expected": False}]),
    ("Check if Array Is Sorted and Rotated", "Arrays", "check_sorted_rotated", "nums: list[int]", "bool", "count = 0\n    n = len(nums)\n    for i in range(n):\n        if nums[i] > nums[(i + 1) % n]:\n            count += 1\n    return count <= 1", [{"input": {"nums": [3, 4, 5, 1, 2]}, "expected": True}, {"input": {"nums": [2, 1, 3, 4]}, "expected": False}]),
    ("Divisibility Problem (Codeforces 1328A)", "Math", "divisibility_problem", "a: int, b: int", "int", "return 0 if a % b == 0 else b - (a % b)", [{"input": {"a": 10, "b": 4}, "expected": 2}, {"input": {"a": 13, "b": 9}, "expected": 5}]),
    ("Watermelon (Codeforces 4A)", "Math", "watermelon", "w: int", "bool", "return w > 2 and w % 2 == 0", [{"input": {"w": 8}, "expected": True}, {"input": {"w": 2}, "expected": False}]),
    ("Way Too Long Words (Codeforces 71A)", "Strings", "abbreviate_word", "s: str", "str", "return s if len(s) <= 10 else f'{s[0]}{len(s)-2}{s[-1]}'", [{"input": {"s": "localization"}, "expected": "l10n"}, {"input": {"s": "word"}, "expected": "word"}])
]

cur_id = 21
for name, cat, fn_name, params, ret, body, tests in topics_easy:
    questions.append({
        "id": cur_id,
        "title": name,
        "difficulty": "Easy",
        "category": cat,
        "companies": ["Amazon", "Google", "Microsoft", "Codeforces"],
        "description": f"Solve problem: {name}.\nImplement `{fn_name}({params}) -> {ret}` with optimal time and space complexity.",
        "examples": [{"input": str(tests[0]["input"]), "output": str(tests[0]["expected"])}],
        "constraints": ["Optimal time complexity expected."],
        "starterCode": f"def {fn_name}({params}) -> {ret}:\n    # Write your solution here\n    {body}\n",
        "entryFunction": fn_name,
        "testCases": tests
    })
    cur_id += 1

print(f"Total Easy questions: {len(questions)}")

# ==================== 30 MEDIUM QUESTIONS ====================
medium_list = [
    ("Longest Substring Without Repeating Characters", "Sliding Window", "length_of_longest_substring", "s: str", "int",
     "seen = {}\n    max_len = start = 0\n    for i, c in enumerate(s):\n        if c in seen and seen[c] >= start:\n            start = seen[c] + 1\n        seen[c] = i\n        max_len = max(max_len, i - start + 1)\n    return max_len",
     [{"input": {"s": "abcabcbb"}, "expected": 3}, {"input": {"s": "bbbbb"}, "expected": 1}, {"input": {"s": "pwwkew"}, "expected": 3}]),

    ("3Sum", "Two Pointers", "three_sum", "nums: list[int]", "list[list[int]]",
     "nums.sort()\n    res = []\n    for i in range(len(nums) - 2):\n        if i > 0 and nums[i] == nums[i - 1]: continue\n        l, r = i + 1, len(nums) - 1\n        while l < r:\n            s = nums[i] + nums[l] + nums[r]\n            if s < 0: l += 1\n            elif s > 0: r -= 1\n            else:\n                res.append([nums[i], nums[l], nums[r]])\n                while l < r and nums[l] == nums[l + 1]: l += 1\n                while l < r and nums[r] == nums[r - 1]: r -= 1\n                l += 1; r -= 1\n    return res",
     [{"input": {"nums": [-1, 0, 1, 2, -1, -4]}, "expected": [[-1, -1, 2], [-1, 0, 1]]}]),

    ("Container With Most Water", "Two Pointers", "max_area", "height: list[int]", "int",
     "l, r = 0, len(height) - 1\n    max_water = 0\n    while l < r:\n        max_water = max(max_water, min(height[l], height[r]) * (r - l))\n        if height[l] < height[r]: l += 1\n        else: r -= 1\n    return max_water",
     [{"input": {"height": [1, 8, 6, 2, 5, 4, 8, 3, 7]}, "expected": 49}, {"input": {"height": [1, 1]}, "expected": 1}]),

    ("Group Anagrams", "Hash Map", "group_anagrams", "strs: list[str]", "list[list[str]]",
     "from collections import defaultdict\n    mp = defaultdict(list)\n    for s in strs:\n        mp[tuple(sorted(s))].append(s)\n    return sorted([sorted(v) for v in mp.values()])",
     [{"input": {"strs": ["eat", "tea", "tan", "ate", "nat", "bat"]}, "expected": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]}]),

    ("Product of Array Except Self", "Arrays", "product_except_self", "nums: list[int]", "list[int]",
     "n = len(nums)\n    res = [1] * n\n    prefix = 1\n    for i in range(n):\n        res[i] = prefix\n        prefix *= nums[i]\n    postfix = 1\n    for i in range(n - 1, -1, -1):\n        res[i] *= postfix\n        postfix *= nums[i]\n    return res",
     [{"input": {"nums": [1, 2, 3, 4]}, "expected": [24, 12, 8, 6]}, {"input": {"nums": [-1, 1, 0, -3, 3]}, "expected": [0, 0, 9, 0, 0]}]),

    ("Top K Frequent Elements", "Heap & Hashing", "top_k_frequent", "nums: list[int], k: int", "list[int]",
     "from collections import Counter\n    return [item for item, _ in Counter(nums).most_common(k)]",
     [{"input": {"nums": [1, 1, 1, 2, 2, 3], "k": 2}, "expected": [1, 2]}]),

    ("Longest Consecutive Sequence", "Hash Set", "longest_consecutive", "nums: list[int]", "int",
     "s = set(nums)\n    max_len = 0\n    for n in s:\n        if n - 1 not in s:\n            cur = n\n            cur_len = 1\n            while cur + 1 in s:\n                cur += 1\n                cur_len += 1\n            max_len = max(max_len, cur_len)\n    return max_len",
     [{"input": {"nums": [100, 4, 200, 1, 3, 2]}, "expected": 4}]),

    ("Search in Rotated Sorted Array", "Binary Search", "search_rotated", "nums: list[int], target: int", "int",
     "l, r = 0, len(nums) - 1\n    while l <= r:\n        m = (l + r) // 2\n        if nums[m] == target: return m\n        if nums[l] <= nums[m]:\n            if nums[l] <= target < nums[m]: r = m - 1\n            else: l = m + 1\n        else:\n            if nums[m] < target <= nums[r]: l = m + 1\n            else: r = m - 1\n    return -1",
     [{"input": {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 0}, "expected": 4}, {"input": {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 3}, "expected": -1}]),

    ("Daily Temperatures", "Monotonic Stack", "daily_temperatures", "temperatures: list[int]", "list[int]",
     "res = [0] * len(temperatures)\n    stack = []\n    for i, t in enumerate(temperatures):\n        while stack and temperatures[stack[-1]] < t:\n            prev = stack.pop()\n            res[prev] = i - prev\n        stack.append(i)\n    return res",
     [{"input": {"temperatures": [73, 74, 75, 71, 69, 72, 76, 73]}, "expected": [1, 1, 4, 2, 1, 1, 0, 0]}]),

    ("Subsets", "Backtracking", "subsets", "nums: list[int]", "list[list[int]]",
     "res = [[]]\n    for n in nums:\n        res += [curr + [n] for curr in res]\n    return sorted([sorted(x) for x in res])",
     [{"input": {"nums": [1, 2, 3]}, "expected": [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]}]),

    ("Permutations", "Backtracking", "permute", "nums: list[int]", "list[list[int]]",
     "from itertools import permutations\n    return sorted([list(p) for p in permutations(nums)])",
     [{"input": {"nums": [1, 2, 3]}, "expected": [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]}]),

    ("Combination Sum", "Backtracking", "combination_sum", "candidates: list[int], target: int", "list[list[int]]",
     "res = []\n    def dfs(i, cur, total):\n        if total == target:\n            res.append(cur[:])\n            return\n        if i >= len(candidates) or total > target:\n            return\n        cur.append(candidates[i])\n        dfs(i, cur, total + candidates[i])\n        cur.pop()\n        dfs(i + 1, cur, total)\n    dfs(0, [], 0)\n    return res",
     [{"input": {"candidates": [2, 3, 6, 7], "target": 7}, "expected": [[2, 2, 3], [7]]}]),

    ("Coin Change", "Dynamic Programming", "coin_change", "coins: list[int], amount: int", "int",
     "dp = [float('inf')] * (amount + 1)\n    dp[0] = 0\n    for c in coins:\n        for a in range(c, amount + 1):\n            dp[a] = min(dp[a], dp[a - c] + 1)\n    return dp[amount] if dp[amount] != float('inf') else -1",
     [{"input": {"coins": [1, 2, 5], "amount": 11}, "expected": 3}, {"input": {"coins": [2], "amount": 3}, "expected": -1}]),

    ("Longest Increasing Subsequence", "Dynamic Programming & Binary Search", "length_of_lis", "nums: list[int]", "int",
     "import bisect\n    tails = []\n    for x in nums:\n        idx = bisect.bisect_left(tails, x)\n        if idx == len(tails): tails.append(x)\n        else: tails[idx] = x\n    return len(tails)",
     [{"input": {"nums": [10, 9, 2, 5, 3, 7, 101, 18]}, "expected": 4}, {"input": {"nums": [0, 1, 0, 3, 2, 3]}, "expected": 4}]),

    ("House Robber", "Dynamic Programming", "rob", "nums: list[int]", "int",
     "r1 = r2 = 0\n    for n in nums:\n        r1, r2 = r2, max(n + r1, r2)\n    return r2",
     [{"input": {"nums": [1, 2, 3, 1]}, "expected": 4}, {"input": {"nums": [2, 7, 9, 3, 1]}, "expected": 12}]),

    ("Word Break", "Dynamic Programming", "word_break", "s: str, wordDict: list[str]", "bool",
     "words = set(wordDict)\n    dp = [True] + [False] * len(s)\n    for i in range(1, len(s) + 1):\n        for j in range(i):\n            if dp[j] and s[j:i] in words:\n                dp[i] = True\n                break\n    return dp[len(s)]",
     [{"input": {"s": "leetcode", "wordDict": ["leet", "code"]}, "expected": True}, {"input": {"s": "catsandog", "wordDict": ["cats", "dog", "sand", "and", "cat"]}, "expected": False}]),

    ("Unique Paths", "Dynamic Programming", "unique_paths", "m: int, n: int", "int",
     "import math\n    return math.comb(m + n - 2, m - 1)",
     [{"input": {"m": 3, "n": 7}, "expected": 28}, {"input": {"m": 3, "n": 2}, "expected": 3}]),

    ("Minimum Path Sum", "Dynamic Programming", "min_path_sum", "grid: list[list[int]]", "int",
     "m, n = len(grid), len(grid[0])\n    for i in range(m):\n        for j in range(n):\n            if i == 0 and j == 0: continue\n            if i == 0: grid[i][j] += grid[i][j - 1]\n            elif j == 0: grid[i][j] += grid[i - 1][j]\n            else: grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])\n    return grid[-1][-1]",
     [{"input": {"grid": [[1, 3, 1], [1, 5, 1], [4, 2, 1]]}, "expected": 7}]),

    ("Rotting Oranges", "Graphs & BFS", "oranges_rotting", "grid: list[list[int]]", "int",
     "from collections import deque\n    R, C = len(grid), len(grid[0])\n    q = deque()\n    fresh = 0\n    for r in range(R):\n        for c in range(C):\n            if grid[r][c] == 2: q.append((r, c, 0))\n            elif grid[r][c] == 1: fresh += 1\n    time = 0\n    while q:\n        r, c, time = q.popleft()\n        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:\n                grid[nr][nc] = 2\n                fresh -= 1\n                q.append((nr, nc, time + 1))\n    return time if fresh == 0 else -1",
     [{"input": {"grid": [[2, 1, 1], [1, 1, 0], [0, 1, 1]]}, "expected": 4}]),

    ("Course Schedule (Cycle Detection)", "Graphs & Topological Sort", "can_finish", "numCourses: int, prerequisites: list[list[int]]", "bool",
     "from collections import defaultdict\n    adj = defaultdict(list)\n    for a, b in prerequisites: adj[b].append(a)\n    visited = [0] * numCourses\n    def dfs(i):\n        if visited[i] == 1: return False\n        if visited[i] == 2: return True\n        visited[i] = 1\n        for nxt in adj[i]:\n            if not dfs(nxt): return False\n        visited[i] = 2\n        return True\n    return all(dfs(i) for i in range(numCourses))",
     [{"input": {"numCourses": 2, "prerequisites": [[1, 0]]}, "expected": True}, {"input": {"numCourses": 2, "prerequisites": [[1, 0], [0, 1]]}, "expected": False}]),

    ("Number of Islands", "Graphs & DFS", "num_islands", "grid: list[list[str]]", "int",
     "if not grid: return 0\n    R, C = len(grid), len(grid[0])\n    count = 0\n    def dfs(r, c):\n        if r < 0 or r >= R or c < 0 or c >= C or grid[r][c] != '1': return\n        grid[r][c] = '0'\n        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)\n    for r in range(R):\n        for c in range(C):\n            if grid[r][c] == '1':\n                count += 1\n                dfs(r, c)\n    return count",
     [{"input": {"grid": [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]}, "expected": 3}]),

    ("Kth Largest Element in an Array", "Heap & Quickselect", "find_kth_largest", "nums: list[int], k: int", "int",
     "import heapq\n    return heapq.nlargest(k, nums)[-1]",
     [{"input": {"nums": [3, 2, 1, 5, 6, 4], "k": 2}, "expected": 5}]),

    ("Find Minimum in Rotated Sorted Array", "Binary Search", "find_min", "nums: list[int]", "int",
     "l, r = 0, len(nums) - 1\n    while l < r:\n        m = (l + r) // 2\n        if nums[m] > nums[r]: l = m + 1\n        else: r = m\n    return nums[l]",
     [{"input": {"nums": [3, 4, 5, 1, 2]}, "expected": 1}, {"input": {"nums": [4, 5, 6, 7, 0, 1, 2]}, "expected": 0}]),

    ("Sort Colors (Dutch National Flag)", "Two Pointers", "sort_colors", "nums: list[int]", "list[int]",
     "l, cur, r = 0, 0, len(nums) - 1\n    while cur <= r:\n        if nums[cur] == 0:\n            nums[l], nums[cur] = nums[cur], nums[l]\n            l += 1; cur += 1\n        elif nums[cur] == 2:\n            nums[cur], nums[r] = nums[r], nums[cur]\n            r -= 1\n        else: cur += 1\n    return nums",
     [{"input": {"nums": [2, 0, 2, 1, 1, 0]}, "expected": [0, 0, 1, 1, 2, 2]}]),

    ("Subarray Sum Equals K", "Hash Map & Prefix Sum", "subarray_sum", "nums: list[int], k: int", "int",
     "from collections import defaultdict\n    mp = defaultdict(int)\n    mp[0] = 1\n    cur_sum = count = 0\n    for x in nums:\n        cur_sum += x\n        count += mp[cur_sum - k]\n        mp[cur_sum] += 1\n    return count",
     [{"input": {"nums": [1, 1, 1], "k": 2}, "expected": 2}, {"input": {"nums": [1, 2, 3], "k": 3}, "expected": 2}]),

    ("Maximum Product Subarray", "Dynamic Programming", "max_product", "nums: list[int]", "int",
     "res = max(nums)\n    cur_min = cur_max = 1\n    for n in nums:\n        if n == 0:\n            cur_min = cur_max = 1\n            continue\n        tmp = cur_max * n\n        cur_max = max(n * cur_max, n * cur_min, n)\n        cur_min = min(tmp, n * cur_min, n)\n        res = max(res, cur_max)\n    return res",
     [{"input": {"nums": [2, 3, -2, 4]}, "expected": 6}, {"input": {"nums": [-2, 0, -1]}, "expected": 0}]),

    ("Gas Station", "Greedy", "can_complete_circuit", "gas: list[int], cost: list[int]", "int",
     "if sum(gas) < sum(cost): return -1\n    total = start = 0\n    for i in range(len(gas)):\n        total += gas[i] - cost[i]\n        if total < 0:\n            total = 0\n            start = i + 1\n    return start",
     [{"input": {"gas": [1, 2, 3, 4, 5], "cost": [3, 4, 5, 1, 2]}, "expected": 3}]),

    ("Jump Game", "Greedy", "can_jump", "nums: list[int]", "bool",
     "reach = 0\n    for i, jump in enumerate(nums):\n        if i > reach: return False\n        reach = max(reach, i + jump)\n    return True",
     [{"input": {"nums": [2, 3, 1, 1, 4]}, "expected": True}, {"input": {"nums": [3, 2, 1, 0, 4]}, "expected": False}]),

    ("String to Integer (atoi)", "Strings", "my_atoi", "s: str", "int",
     "s = s.strip()\n    if not s: return 0\n    sign = -1 if s[0] == '-' else 1\n    if s[0] in ['-', '+']: s = s[1:]\n    res = 0\n    for c in s:\n        if not c.isdigit(): break\n        res = res * 10 + int(c)\n    res = sign * res\n    return max(-2**31, min(2**31 - 1, res))",
     [{"input": {"s": "42"}, "expected": 42}, {"input": {"s": "   -42"}, "expected": -42}, {"input": {"s": "4193 with words"}, "expected": 4193}]),

    ("Find All Anagrams in a String", "Sliding Window", "find_anagrams", "s: str, p: str", "list[int]",
     "from collections import Counter\n    res = []\n    p_cnt = Counter(p)\n    s_cnt = Counter(s[:len(p)])\n    if s_cnt == p_cnt: res.append(0)\n    for i in range(len(p), len(s)):\n        s_cnt[s[i]] += 1\n        s_cnt[s[i - len(p)]] -= 1\n        if s_cnt[s[i - len(p)]] == 0: del s_cnt[s[i - len(p)]]\n        if s_cnt == p_cnt: res.append(i - len(p) + 1)\n    return res",
     [{"input": {"s": "cbaebabacd", "p": "abc"}, "expected": [0, 6]}])
]

for name, cat, fn_name, params, ret, body, tests in medium_list:
    questions.append({
        "id": cur_id,
        "title": name,
        "difficulty": "Medium",
        "category": cat,
        "companies": ["Google", "Meta", "Amazon", "Microsoft", "Uber"],
        "description": f"Solve problem: {name}.\nImplement `{fn_name}({params}) -> {ret}` with optimal time and space complexity.",
        "examples": [{"input": str(tests[0]["input"]), "output": str(tests[0]["expected"])}],
        "constraints": ["Optimal O(N) or O(N log N) time complexity expected."],
        "starterCode": f"def {fn_name}({params}) -> {ret}:\n    # Write your solution here\n    {body}\n",
        "entryFunction": fn_name,
        "testCases": tests
    })
    cur_id += 1

print(f"Total Medium questions: {len(questions) - 50}")

# ==================== 20 HARD QUESTIONS ====================
hard_list = [
    ("Trapping Rain Water", "Two Pointers & Monotonic Stack", "trap", "height: list[int]", "int",
     "if not height: return 0\n    l, r = 0, len(height) - 1\n    l_max, r_max = height[l], height[r]\n    water = 0\n    while l < r:\n        if l_max < r_max:\n            l += 1\n            l_max = max(l_max, height[l])\n            water += l_max - height[l]\n        else:\n            r -= 1\n            r_max = max(r_max, height[r])\n            water += r_max - height[r]\n    return water",
     [{"input": {"height": [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]}, "expected": 6}, {"input": {"height": [4, 2, 0, 3, 2, 5]}, "expected": 9}]),

    ("Minimum Window Substring", "Sliding Window", "min_window", "s: str, t: str", "str",
     "from collections import Counter\n    if not t or not s: return ''\n    t_count = Counter(t)\n    window = {}\n    have, need = 0, len(t_count)\n    res, res_len = [-1, -1], float('inf')\n    l = 0\n    for r in range(len(s)):\n        c = s[r]\n        window[c] = window.get(c, 0) + 1\n        if c in t_count and window[c] == t_count[c]: have += 1\n        while have == need:\n            if (r - l + 1) < res_len:\n                res = [l, r]\n                res_len = r - l + 1\n            window[s[l]] -= 1\n            if s[l] in t_count and window[s[l]] < t_count[s[l]]: have -= 1\n            l += 1\n    l, r = res\n    return s[l:r + 1] if res_len != float('inf') else ''",
     [{"input": {"s": "ADOBECODEBANC", "t": "ABC"}, "expected": "BANC"}, {"input": {"s": "a", "t": "a"}, "expected": "a"}]),

    ("Median of Two Sorted Arrays", "Binary Search", "find_median_sorted_arrays", "nums1: list[int], nums2: list[int]", "float",
     "merged = sorted(nums1 + nums2)\n    n = len(merged)\n    if n % 2 == 1: return float(merged[n // 2])\n    return (merged[n // 2 - 1] + merged[n // 2]) / 2.0",
     [{"input": {"nums1": [1, 3], "nums2": [2]}, "expected": 2.0}, {"input": {"nums1": [1, 2], "nums2": [3, 4]}, "expected": 2.5}]),

    ("Largest Rectangle in Histogram", "Monotonic Stack", "largest_rectangle_area", "heights: list[int]", "int",
     "stack = []\n    max_area = 0\n    for i, h in enumerate(heights + [0]):\n        while stack and heights[stack[-1]] >= h:\n            height = heights[stack.pop()]\n            width = i if not stack else i - stack[-1] - 1\n            max_area = max(max_area, height * width)\n        stack.append(i)\n    return max_area",
     [{"input": {"heights": [2, 1, 5, 6, 2, 3]}, "expected": 10}, {"input": {"heights": [2, 4]}, "expected": 4}]),

    ("Sliding Window Maximum", "Monotonic Deque", "max_sliding_window", "nums: list[int], k: int", "list[int]",
     "from collections import deque\n    q = deque()\n    res = []\n    for i, n in enumerate(nums):\n        while q and q[0] < i - k + 1: q.popleft()\n        while q and nums[q[-1]] < n: q.pop()\n        q.append(i)\n        if i >= k - 1: res.append(nums[q[0]])\n    return res",
     [{"input": {"nums": [1, 3, -1, -3, 5, 3, 6, 7], "k": 3}, "expected": [3, 3, 5, 5, 6, 7]}]),

    ("Merge k Sorted Arrays", "Heap & Priority Queue", "merge_k_arrays", "arrays: list[list[int]]", "list[int]",
     "import heapq\n    return list(heapq.merge(*arrays))",
     [{"input": {"arrays": [[1, 4, 5], [1, 3, 4], [2, 6]]}, "expected": [1, 1, 2, 3, 4, 4, 5, 6]}]),

    ("Edit Distance (Levenshtein)", "Dynamic Programming", "min_distance", "word1: str, word2: str", "int",
     "m, n = len(word1), len(word2)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(m + 1): dp[i][0] = i\n    for j in range(n + 1): dp[0][j] = j\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if word1[i - 1] == word2[j - 1]: dp[i][j] = dp[i - 1][j - 1]\n            else: dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])\n    return dp[m][n]",
     [{"input": {"word1": "horse", "word2": "ros"}, "expected": 3}, {"input": {"word1": "intention", "word2": "execution"}, "expected": 5}]),

    ("Longest Valid Parentheses", "Dynamic Programming & Stack", "longest_valid_parentheses", "s: str", "int",
     "stack = [-1]\n    max_len = 0\n    for i, c in enumerate(s):\n        if c == '(': stack.append(i)\n        else:\n            stack.pop()\n            if not stack: stack.append(i)\n            else: max_len = max(max_len, i - stack[-1])\n    return max_len",
     [{"input": {"s": "(()"}, "expected": 2}, {"input": {"s": ")()())"}, "expected": 4}, {"input": {"s": ""}, "expected": 0}]),

    ("Burst Balloons", "Interval Dynamic Programming", "max_coins", "nums: list[int]", "int",
     "nums = [1] + [n for n in nums if n > 0] + [1]\n    n = len(nums)\n    dp = [[0] * n for _ in range(n)]\n    for length in range(2, n):\n        for left in range(0, n - length):\n            right = left + length\n            for k in range(left + 1, right):\n                dp[left][right] = max(dp[left][right], nums[left] * nums[k] * nums[right] + dp[left][k] + dp[k][right])\n    return dp[0][n - 1]",
     [{"input": {"nums": [3, 1, 5, 8]}, "expected": 167}]),

    ("N-Queens", "Backtracking", "solve_n_queens", "n: int", "int",
     "cols = set(); diag1 = set(); diag2 = set()\n    count = 0\n    def backtrack(r):\n        nonlocal count\n        if r == n:\n            count += 1\n            return\n        for c in range(n):\n            if c in cols or (r + c) in diag1 or (r - c) in diag2: continue\n            cols.add(c); diag1.add(r + c); diag2.add(r - c)\n            backtrack(r + 1)\n            cols.remove(c); diag1.remove(r + c); diag2.remove(r - c)\n    backtrack(0)\n    return count",
     [{"input": {"n": 4}, "expected": 2}, {"input": {"n": 1}, "expected": 1}, {"input": {"n": 5}, "expected": 10}]),

    ("Alien Dictionary (Topological Sort)", "Graphs & Topo Sort", "alien_order", "words: list[str]", "str",
     "from collections import defaultdict\n    adj = {c: set() for w in words for c in w}\n    for i in range(len(words) - 1):\n        w1, w2 = words[i], words[i + 1]\n        min_len = min(len(w1), len(w2))\n        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]: return ''\n        for j in range(min_len):\n            if w1[j] != w2[j]:\n                adj[w1[j]].add(w2[j])\n                break\n    visit = {}\n    res = []\n    def dfs(c):\n        if c in visit: return visit[c]\n        visit[c] = True\n        for nxt in adj[c]:\n            if dfs(nxt): return True\n        visit[c] = False\n        res.append(c)\n    for c in adj:\n        if dfs(c): return ''\n    return ''.join(res[::-1])",
     [{"input": {"words": ["wrt", "wrf", "er", "ett", "rftt"]}, "expected": "wertf"}]),

    ("Word Ladder (Shortest Transformation)", "Graphs & BFS", "ladder_length", "beginWord: str, endWord: str, wordList: list[str]", "int",
     "from collections import deque, defaultdict\n    if endWord not in wordList: return 0\n    L = len(beginWord)\n    all_combo = defaultdict(list)\n    for w in wordList:\n        for i in range(L): all_combo[w[:i] + '*' + w[i+1:]].append(w)\n    q = deque([(beginWord, 1)])\n    visited = {beginWord}\n    while q:\n        word, level = q.popleft()\n        for i in range(L):\n            inter = word[:i] + '*' + word[i+1:]\n            for neighbor in all_combo[inter]:\n                if neighbor == endWord: return level + 1\n                if neighbor not in visited:\n                    visited.add(neighbor)\n                    q.append((neighbor, level + 1))\n            all_combo[inter] = []\n    return 0",
     [{"input": {"beginWord": "hit", "endWord": "cog", "wordList": ["hot", "dot", "dog", "lot", "log", "cog"]}, "expected": 5}]),

    ("Shortest Path with Obstacles Elimination", "Graphs & BFS", "shortest_path", "grid: list[list[int]], k: int", "int",
     "from collections import deque\n    R, C = len(grid), len(grid[0])\n    if k >= R + C - 2: return R + C - 2\n    q = deque([(0, 0, k, 0)])\n    visited = {(0, 0, k)}\n    while q:\n        r, c, rem_k, steps = q.popleft()\n        if r == R - 1 and c == C - 1: return steps\n        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < R and 0 <= nc < C:\n                next_k = rem_k - grid[nr][nc]\n                if next_k >= 0 and (nr, nc, next_k) not in visited:\n                    visited.add((nr, nc, next_k))\n                    q.append((nr, nc, next_k, steps + 1))\n    return -1",
     [{"input": {"grid": [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]], "k": 1}, "expected": 6}]),

    ("Regular Expression Matching ('.' and '*')", "Dynamic Programming", "is_match", "s: str, p: str", "bool",
     "cache = {}\n    def dfs(i, j):\n        if (i, j) in cache: return cache[(i, j)]\n        if i >= len(s) and j >= len(p): return True\n        if j >= len(p): return False\n        match = i < len(s) and (s[i] == p[j] or p[j] == '.')\n        if (j + 1) < len(p) and p[j + 1] == '*':\n            cache[(i, j)] = dfs(i, j + 2) or (match and dfs(i + 1, j))\n            return cache[(i, j)]\n        if match:\n            cache[(i, j)] = dfs(i + 1, j + 1)\n            return cache[(i, j)]\n        cache[(i, j)] = False\n        return False\n    return dfs(0, 0)",
     [{"input": {"s": "aa", "p": "a*"}, "expected": True}, {"input": {"s": "ab", "p": ".*"}, "expected": True}, {"input": {"s": "mississippi", "p": "mis*is*p*."}, "expected": False}]),

    ("Find Median from Data Stream", "Two Heaps", "get_medians", "operations: list[int]", "list[float]",
     "import heapq\n    small, large = [], []\n    res = []\n    for num in operations:\n        heapq.heappush(small, -num)\n        if small and large and (-small[0] > large[0]):\n            val = -heapq.heappop(small)\n            heapq.heappush(large, val)\n        if len(small) > len(large) + 1:\n            val = -heapq.heappop(small)\n            heapq.heappush(large, val)\n        if len(large) > len(small):\n            val = heapq.heappop(large)\n            heapq.heappush(small, -val)\n        if len(small) > len(large):\n            res.append(float(-small[0]))\n        else:\n            res.append((-small[0] + large[0]) / 2.0)\n    return res",
     [{"input": {"operations": [1, 2, 3]}, "expected": [1.0, 1.5, 2.0]}]),

    ("Maximal Rectangle in Binary Matrix", "Monotonic Stack & DP", "maximal_rectangle", "matrix: list[list[str]]", "int",
     "if not matrix: return 0\n    R, C = len(matrix), len(matrix[0])\n    heights = [0] * C\n    max_area = 0\n    for row in matrix:\n        for c in range(C):\n            heights[c] = heights[c] + 1 if row[c] == '1' else 0\n        stack = []\n        for i, h in enumerate(heights + [0]):\n            while stack and heights[stack[-1]] >= h:\n                height = heights[stack.pop()]\n                width = i if not stack else i - stack[-1] - 1\n                max_area = max(max_area, height * width)\n            stack.append(i)\n    return max_area",
     [{"input": {"matrix": [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]}, "expected": 6}]),

    ("Segment Tree Range Sum Query", "Segment Tree & Data Structures", "range_sum_query", "nums: list[int], queries: list[list[int]]", "list[int]",
     "tree = [0] * (4 * len(nums))\n    def build(node, l, r):\n        if l == r:\n            tree[node] = nums[l]\n            return\n        mid = (l + r) // 2\n        build(2 * node, l, mid)\n        build(2 * node + 1, mid + 1, r)\n        tree[node] = tree[2 * node] + tree[2 * node + 1]\n    def query(node, l, r, ql, qr):\n        if ql <= l and r <= qr: return tree[node]\n        if r < ql or l > qr: return 0\n        mid = (l + r) // 2\n        return query(2 * node, l, mid, ql, qr) + query(2 * node + 1, mid + 1, r, ql, qr)\n    build(1, 0, len(nums) - 1)\n    return [query(1, 0, len(nums) - 1, q[0], q[1]) for q in queries]",
     [{"input": {"nums": [1, 3, 5, 7, 9, 11], "queries": [[0, 2], [1, 4]]}, "expected": [9, 24]}]),

    ("Disjoint Set Union (DSU) Kruskal Components", "Graphs & Disjoint Set", "count_connected_components", "n: int, edges: list[list[int]]", "int",
     "parent = list(range(n))\n    def find(i):\n        if parent[i] == i: return i\n        parent[i] = find(parent[i])\n        return parent[i]\n    components = n\n    for u, v in edges:\n        root_u = find(u)\n        root_v = find(v)\n        if root_u != root_v:\n            parent[root_u] = root_v\n            components -= 1\n    return components",
     [{"input": {"n": 5, "edges": [[0, 1], [1, 2], [3, 4]]}, "expected": 2}, {"input": {"n": 5, "edges": [[0, 1], [1, 2], [2, 3], [3, 4]]}, "expected": 1}]),

    ("Palindrome Partitioning II (Min Cuts)", "Dynamic Programming", "min_cut", "s: str", "int",
     "n = len(s)\n    is_pal = [[False] * n for _ in range(n)]\n    for i in range(n - 1, -1, -1):\n        for j in range(i, n):\n            if s[i] == s[j] and (j - i <= 2 or is_pal[i + 1][j - 1]):\n                is_pal[i][j] = True\n    dp = [0] * n\n    for i in range(n):\n        if is_pal[0][i]: dp[i] = 0\n        else:\n            dp[i] = min(dp[j] + 1 for j in range(i) if is_pal[j + 1][i])\n    return dp[-1]",
     [{"input": {"s": "aab"}, "expected": 1}, {"input": {"s": "a"}, "expected": 0}, {"input": {"s": "ab"}, "expected": 1}]),

    ("Tree Diameter & Longest Path", "Graph Theory & Trees", "tree_diameter", "n: int, edges: list[list[int]]", "int",
     "from collections import defaultdict, deque\n    if n <= 1: return 0\n    adj = defaultdict(list)\n    for u, v in edges:\n        adj[u].append(v); adj[v].append(u)\n    def bfs(start):\n        dist = {start: 0}\n        q = deque([start])\n        farthest = start\n        while q:\n            node = q.popleft()\n            for nxt in adj[node]:\n                if nxt not in dist:\n                    dist[nxt] = dist[node] + 1\n                    farthest = nxt\n                    q.append(nxt)\n        return farthest, dist[farthest]\n    node1, _ = bfs(0)\n    node2, max_dist = bfs(node1)\n    return max_dist",
     [{"input": {"n": 6, "edges": [[0, 1], [1, 2], [2, 3], [1, 4], [4, 5]]}, "expected": 4}])
]

for name, cat, fn_name, params, ret, body, tests in hard_list:
    questions.append({
        "id": cur_id,
        "title": name,
        "difficulty": "Hard",
        "category": cat,
        "companies": ["Google", "Meta", "Amazon", "Codeforces Div 1/2"],
        "description": f"Solve problem: {name}.\nImplement `{fn_name}({params}) -> {ret}` with optimal time and space complexity.",
        "examples": [{"input": str(tests[0]["input"]), "output": str(tests[0]["expected"])}],
        "constraints": ["Optimal time complexity expected.", "Corner cases and large bounds must be handled."],
        "starterCode": f"def {fn_name}({params}) -> {ret}:\n    # Write your solution here\n    {body}\n",
        "entryFunction": fn_name,
        "testCases": tests
    })
    cur_id += 1

print(f"Total questions generated: {len(questions)}")
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
med_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")
print(f"Breakdown -> Easy: {easy_count}, Medium: {med_count}, Hard: {hard_count}")

out_path = os.path.join(os.path.dirname(__file__), "data", "dsa_questions.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2)

print(f"Successfully saved {len(questions)} DSA questions to {out_path}")
