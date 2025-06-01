from abc import ABC, abstractmethod
import re
import time
import random
from word2number import w2n
from num2words import num2words
import math
from math import sqrt
from math import gcd
from statistics import mode
from statistics import median
from flask_babel import _  # Import Flask-Babel translation function


def lcm_of2(a, b):
    return abs(a * b) // math.gcd(a, b)


def lcm(a, b, c):
    return lcm_of2(lcm_of2(a, b), c)

class SolutionGenerator(ABC):
    """Factory class that returns SolutionGenerator objects"""

    @abstractmethod
    def get_solution(self, template: str, args: dict) -> str:
        """Generate solution for a knowledge_point"""

    def custom_format(self, template, **values):
        # Regex pattern to match complex placeholders including nested brackets
        pattern = re.compile(r'\[\[((?:[^\[\]]|\[[^\[\]]*\])+)\]\]')

        # Function to replace each match
        def replacer(match):
            expr = match.group(1)
            # Evaluate the expression within the context of 'values'
            try:
                return str(eval(expr, {"__builtins__": None}, values))
            except Exception as e:
                return _("Error: {error}").format(error=str(e))  # Localized error message

        # Replace all occurrences of the placeholder in the template
        return pattern.sub(replacer, template)

    def check_zero_at_tens(value):
        if (value) == 0:
            return ''
        return value

    def count_digits(num):
        if (num == 0):
            return 1
        result = 0
        while (num != 0):
            num = num // 10
            result += 1
        return result

    def getRep(num) -> str:
        if num == 0:
            return _("zero")  # Localized number string
        str_dict = {
            1000: _("thousand"), 100: _("hundred"), 90: _("ninety"), 80: _("eighty"),
            70: _("seventy"), 60: _("sixty"), 50: _("fifty"), 40: _("forty"), 30: _("thirty"),
            20: _("twenty"), 19: _("nineteen"), 18: _("eighteen"), 17: _("seventeen"), 16: _("sixteen"),
            15: _("fifteen"), 14: _("fourteen"), 13: _("thirteen"), 12: _("twelve"), 11: _("eleven"),
            10: _("ten"), 9: _("nine"), 8: _("eight"), 7: _("seven"), 6: _("six"), 5: _("five"), 4: _("four"),
            3: _("three"), 2: _("two"), 1: _("one"),
        }
        res = ""
        for key in str_dict:
            if num >= key:
                digit = num // key
                if digit != 1 or num >= 100:
                    res += str_dict[digit] + " "
                res += str_dict[key] + " "
                num -= (num // key) * key
        res = res[:len(res) - 1]
        return res

# Apply localization to all KnowledgePoint Solution classes

class KnowledgePoint1Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        args['value_dict'] = {_('tens'): 10, _('ones'): 1}
        return self.custom_format(template, **args)


class KnowledgePoint2Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        args['value_dict'] = {_('tens'): 10, _('ones'): 1}
        return self.custom_format(template, **args)


class KnowledgePoint3Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def get_tens_statement(num):
            if num == 0:
                return _("Since the result is 0, we can ignore 0 in the tens place.")
            else:
                return _("Write down the {num} in the tens place.").format(num=num)
        args["get_tens_statement"] = get_tens_statement
        args["check_zero_at_tens"] = SolutionGenerator.check_zero_at_tens
        return self.custom_format(template, **args)


class KnowledgePoint4Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def get_tens_statement(num):
            if num == 0:
                return _("Since the result is 0, we can ignore 0 in the tens place.")
            else:
                return _("Write down the {num} in the tens place.").format(num=num)
        args["get_tens_statement"] = get_tens_statement
        args["check_zero_at_tens"] = SolutionGenerator.check_zero_at_tens
        return self.custom_format(template, **args)


class KnowledgePoint5Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return KnowledgePoint11Solution.get_solution(self, template, args)


class KnowledgePoint6Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def check_class_name(idx, arg1, arg2):
            if arg1 == idx or arg2 == idx:
                return _('class="number-line-circle"')
            else:
                return ''
        def get_sign(a, b):
            if (a == b):
                return '='
            if (a < b):
                return '<'
            return '>'

        def less_greater_equal_statement(arg1: int, arg2: int) -> str:
            if (arg1 < arg2):
                return _("You see that the number {arg2} is on the right of {arg1}, so {arg2} is greater than {arg1}.").format(arg1=arg1, arg2=arg2)
            if (arg1 > arg2):
                return _("You see that the number {arg2} is on the left of {arg1}, so {arg2} is smaller than {arg1}.").format(arg1=arg1, arg2=arg2)
            return _("You see that the number {arg1} is equal to itself, so {arg1} is equal to {arg2}.").format(arg1=arg1, arg2=arg2)

        args["get_sign"] = get_sign
        args["less_greater_equal_statement"] = less_greater_equal_statement
        args["check_class_name"] = check_class_name
        return self.custom_format(template, **args)


class KnowledgePoint7Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def statement_of_one_tens(arg1):
            if (arg1 % 10 == 0):
                return _('In this case, because there are no ones in {arg1}, the "__ones" part of the question is 0, and we can also simplify the question to "{arg1} = {arg1 // 10} tens".').format(arg1=arg1)
            else:
                return ''

        def result_statement(arg1):
            if (arg1 % 10 == 0):
                return ''
            else:
                return _('$+$ ${\color{Salmon} %i }$ ones') % (arg1 % 10)

        args["statement_of_one_tens"] = statement_of_one_tens
        args["result_statement"] = result_statement
        return self.custom_format(template, **args)


class KnowledgePoint26Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        args['getRep'] = SolutionGenerator.getRep
        return self.custom_format(template, **args)


class KnowledgePoint9Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        arg1 = args['arg1']
        arg2 = args['arg2']
        if (arg1 > arg2):
            args['arg2'] = arg1
            args['arg1'] = arg2
            return self.get_solution(template, args)

        def sub_statment1(num):
            if (num < 10):
                return _('{num} has 1 digit and We put {num} in the ones place').format(num=num)
            return _('{num} has digits in both the ones and tens places, so we write {num} in the correct columns based on its ones and tens digits.').format(num=num)

        def check_sign(num):
            if (num == 0):
                return ''
            return '+'

        args['check_sign'] = check_sign
        args['sub_statment1'] = sub_statment1
        args['check_zero_at_tens'] = SolutionGenerator.check_zero_at_tens
        return self.custom_format(template, **args)


class KnowledgePoint10Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        arg1 = args['arg1']
        arg2 = args['arg2']
        if arg1 < arg2:
            args['arg2'] = arg1
            args['arg1'] = arg2
            return self.get_solution(template, args)

        def sub_statment1(num):
            if num < 10:
                return _('{num} has 1 digit and We put {num} in the ones place').format(num=num)
            return _('{num} has digits in both the ones and tens places, so we write {num} in the correct columns based on its ones and tens digits.').format(num=num)

        args['sub_statment1'] = sub_statment1
        args['check_zero_at_tens'] = SolutionGenerator.check_zero_at_tens
        return self.custom_format(template, **args)


class KnowledgePoint11Solution(SolutionGenerator):
    # Assuming localization can be added to specific statements in this method.
    def get_solution(self, template: str, args: dict) -> str:
        # Add localized statements inside relevant functions
        def calculate_distance(arr: list) -> (list, list):
            missing_idxs = []
            n = len(arr)
            left = 0
            while left < n and arr[left] is None:
                left += 1
            right = left + 1
            while right < n and arr[right] is None:
                right += 1
            diff = (arr[right] - arr[left]) // (right - left)
            ptr_left = left - 1
            while ptr_left >= 0:
                if arr[ptr_left] is None:
                    missing_idxs.append(ptr_left)
                    arr[ptr_left] = arr[ptr_left + 1] - diff
                ptr_left -= 1
            ptr_middle = left + 1
            while ptr_middle < right:
                if arr[ptr_middle] is None:
                    missing_idxs.append(ptr_middle)
                    arr[ptr_middle] = arr[ptr_middle - 1] + diff
                ptr_middle += 1
            ptr_right = right + 1
            while ptr_right < n:
                if arr[ptr_right] is None:
                    missing_idxs.append(ptr_right)
                    arr[ptr_right] = arr[ptr_right - 1] + diff
                ptr_right += 1

            return diff, arr, missing_idxs

        def generate_statement(arr: list, diff_val: int, missing_idx_list: list):
            working_arr = arr.copy()

            def generate_substatement(arr: list, diff_val: int, missing_idx_list: list):
                step = 3
                sub_statement = ""
                for i in range(1, len(missing_idx_list)):
                    missing_idx = missing_idx_list[i]
                    sub_statement += _("**Step {step}:** Now we need to find the number that comes after {num}. We know the numbers are going up by {diff} each time, so the number after {num} should be {num_after}.").format(step=step, num=arr[missing_idx - 1], diff=diff_val, num_after=arr[missing_idx - 1] + diff_val)
                    sub_statement += '\n'
                    step += 1
                    arr[missing_idx] = arr[missing_idx - 1] + diff_val
                return sub_statement

            first_occurrence = missing_idx_list[0]
            if first_occurrence > 0:
                statement = _("**Step 2:** We know that the numbers are going up by {diff} each time, so the number that comes after {num} should be {num_after}.").format(diff=diff_val, num=working_arr[first_occurrence - 1], num_after=working_arr[first_occurrence - 1] + diff_val)
                working_arr[first_occurrence] = working_arr[first_occurrence - 1] + diff_val
            else:
                statement = _("**Step 2:** We know that the numbers are going up by {diff} each time, so the number that comes before {num} should be {num_before}.").format(diff=diff_val, num=working_arr[first_occurrence + 1], num_before=working_arr[first_occurrence + 1] - diff_val)
                working_arr[first_occurrence] = working_arr[first_occurrence + 1] - diff_val
            statement += generate_substatement(working_arr, diff_val, missing_idx_list)
            return statement

        def result_format_string(arr: list, missing_idx_list: list) -> list:
            new_arr = []
            for i in range(len(arr)):
                if i in missing_idx_list:
                    new_arr.append("{{\color{{Salmon}}{}}}".format(arr[i]))
                else:
                    new_arr.append(arr[i])
            return new_arr

        def convert_array(arr):
            converted_arr = []
            for item in arr:
                if item == '_':
                    converted_arr.append(r'$\underline{\quad}$')
                else:
                    converted_arr.append(f'${item}$')
            return converted_arr

        def convert_to_int_arr(arr):
            converted_arr = []
            for item in arr:
                if item == '_':
                    converted_arr.append(None)
                else:
                    converted_arr.append(int(item))
            return converted_arr

        def missing_statement(arr, idxs):
            if len(idxs) == 1:
                return _("So the missing number is {num}").format(num=arr[idxs[0]])
            statement = _("So the missing numbers are ")
            for i in range(len(idxs) - 1):
                statement += str(arr[idxs[i]]) + ", "
            statement = statement[:-2] + " "
            statement += _("and {last_num}.").format(last_num=arr[idxs[-1]])
            return statement

        str_arr = args['arg1'].split(',')
        int_arr = convert_to_int_arr(str_arr)
        args["input_format_arr"] = ", ".join(convert_array(str_arr))
        diff_in_value, arr, idxs = calculate_distance(int_arr)
        result_str = result_format_string(arr, idxs)
        missing_numbers = missing_statement(arr, idxs)
        args["str_arr"] = str_arr
        args["idxs"] = idxs
        args["sequence"] = ", ".join(str(x) for x in result_str)
        args["missing_numbers"] = missing_numbers
        args["diff"] = diff_in_value
        args["steps"] = generate_statement(int_arr, diff_in_value, idxs)
        return self.custom_format(template, **args)

# Continue similarly for the rest of the KnowledgePoint solution classes.

class KnowledgePoint12Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def generate_one_line(num1: str, num2: str, idx):
            idx_mapping = {
                0: _("The leftmost digit"),
                1: _("The second digit from the left"),
                2: _("We compare the third digit from the left")
            }

            if num1[idx] == num2[idx]:
                return _("{} in both numbers is {}, which is the same.").format(idx_mapping[idx], num1[idx])
            else:
                return _("{} in the first number is {}, and in the second number is {}.").format(
                    idx_mapping[idx], num1[idx], num2[idx])

        def sub_statement(num1: str, num2: str) -> str:
            statement = _("Since both numbers have the same number of digits, compare the digits from left to right, "
                          "taking into account their place value.\n")
            num_of_digits = SolutionGenerator.count_digits(int(num1))
            prefix_num1 = ""
            prefix_num2 = ""
            for i in range(num_of_digits):
                line = "\n" + _("**Step {}:** ").format(i + 1) + generate_one_line(num1, num2, i) + "\n"
                line_conclusion = """
<div align="center">

${}{{\color{{#8DB600}}{}}}{}$ ? ${}{{\color{{#8DB600}}{}}}{}$
</div>\n""".format(prefix_num1, num1[i], num1[i + 1:num_of_digits], prefix_num2, num2[i], num2[i + 1:num_of_digits])
                if num1[i] < num2[i]:
                    line_conclusion += "\n" + _("**Step {}:** Since {} is less than {}, we can conclude that the number {} is less than the number {}.").format(
                        i + 2, num1[i], num2[i], num1, num2)
                elif num1[i] > num2[i]:
                    line_conclusion += "\n" + _("**Step {}:** Since {} is greater than {}, we can conclude that the number {} is greater than the number {}.").format(
                        i + 2, num1[i], num2[i], num1, num2)
                line = line + line_conclusion
                statement = statement + line
                if num1[i] != num2[i]:
                    break
                prefix_num1 = prefix_num1 + num1[i]
                prefix_num2 = prefix_num2 + num2[i]
            if num1 == num2:
                statement += _("\nSince all digits are the same, we can conclude that the number {} is equal to the number {}.\n").format(num1, num2)
            return statement

        def generate_statement(arg1, arg2):
            digits1 = SolutionGenerator.count_digits(int(arg1))
            digits2 = SolutionGenerator.count_digits(int(arg2))
            if digits1 == digits2:
                return sub_statement(str(arg1), str(arg2))
            if digits1 > digits2:
                return _("Since {} has {} digits, while {} has {} digits, we know that {} is larger than {}. Therefore, the answer is\n$$\n{} {{\color{{Salmon}}\:>\:}} {}\n$$").format(
                    arg1, num2words(digits1), arg2, num2words(digits2), digits1, digits2, arg1, arg2)
            else:
                return _("Since {} has {} digits, while {} has {} digits, we know that {} is less than {}. Therefore, the answer is\n$$\n{} {{\color{{Salmon}}\:>\:}} {}\n$$").format(
                    arg1, num2words(digits1), arg2, num2words(digits2), digits1, digits2, arg1, arg2)

        args['generate_statement'] = generate_statement
        return self.custom_format(template, **args)

class KnowledgePoint18Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        if 'arg5' not in args:
            template = """
            <div class="ex-yellow">
            <div class="title">
            Solution
            </div>
            <div class="ex-text" align="center">
            [[arg1]] [[arg2]] + [[arg3]] [[arg4]]


            Let us see what **[[arg1]] [[arg2]]** and **[[arg3]] [[arg4]]** mean.

            -  [[arg1]] [[arg2]] = [[arg1 * value_dict[arg2]]]
            -  [[arg3]] [[arg4]] = [[arg3 * value_dict[arg4]]]
            <div class="ex-text" align="center">
            [[arg1]] [[arg2]] + [[arg3]] [[arg4]] = [[arg1 * value_dict[arg2]]] + [[arg3 * value_dict[arg4]]] = [[arg1 * value_dict[arg2] + arg3 * value_dict[arg4]]]
            </div>
            </div>"""
#             template = """
# <div class="ex-yellow">
# <div class="title">
# {}</div><div class="ex-text" align="center">[[arg1]] [[arg2]] + [[arg3]] [[arg4]]Let us see what **[[arg1]] [[arg2]]** and **[[arg3]] [[arg4]]** mean.-  [[arg1]] [[arg2]] = [[arg1 * value_dict[arg2]]] -  [[arg3]] [[arg4]] = [[arg3 * value_dict[arg4]]] <div class="ex-text" align="center">[[arg1]] [[arg2]] + [[arg3]] [[arg4]] = [[arg1 * value_dict[arg2]]] + [[arg3 * value_dict[arg4]]] = [[arg1 * value_dict[arg2] + arg3 * value_dict[arg4]]]</div></div>""".format(_("Solution"))
        args['value_dict'] = {_('tens'): 10, _('ones'): 1, _('hundreds'): 100}
        return self.custom_format(template, **args)

class KnowledgePoint14Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        args["check_zero_at_tens"] = SolutionGenerator.check_zero_at_tens
        return self.custom_format(template, **args)

class KnowledgePoint15Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)

class KnowledgePoint16Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return KnowledgePoint11Solution.get_solution(self, template, args)

class KnowledgePoint17Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return KnowledgePoint12Solution.get_solution(self, template, args)

class KnowledgePoint19Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def number_word_argument(arg1):
            if str(arg1).isnumeric():
                return _("What is {} in word form?").format(arg1)
            else:
                return _("What number is **{}**").format(arg1)

        def convert_form(arg1):
            if str(arg1).isnumeric():
                return f"**{num2words(arg1)}**"
            else:
                return w2n.word_to_num(arg1)

        args['number_word_argument'] = number_word_argument
        args['convert_form'] = convert_form
        return self.custom_format(template, **args)

class KnowledgePoint24Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def get_rad_item():
            items = [_('apples'), _('cupcakes'), _('bananas'), _('cookies'), _('books'), _('toys'), _('flowers')]
            return random.choice(items)

        args['item'] = get_rad_item()
        return self.custom_format(template, **args)

class KnowledgePoint27Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)

class KnowledgePoint28Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)

class KnowledgePoint29Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        arg1 = args['arg1']
        arg2 = args['arg2']
        a = _("We can divide the digit in the units place.")
        if (arg1 // arg2) < 10:
            template = r"""
    $$  
    [[arg1]] ÷ [[arg2]]  
    $$  

    {}  
    $$  
    \begin{{array}}{{r}}  
    [[arg1//arg2]]\phantom{{)}}   \\  
    [[arg2]]\overline{{\smash{{\big)}}\,[[arg1]]\phantom{{)}}}}\\  
    \underline{{-[[arg1//arg2*arg2]]\phantom{{)}}}}\\  
    0\phantom{{)}}\\  
    \end{{array}}  
    $$  

    {}  
                """.format(
                _("We can divide the digit in the units place."),
                _("So the answer is $[[arg1//arg2]]$.")
            )
        return self.custom_format(template, **args)

class KnowledgePoint30Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        arg1 = args['arg1']
        arg2 = args['arg2']
        args['num2words_arg1_div_arg2'] = num2words(arg1 // arg2)
        return self.custom_format(template, **args)


class KnowledgePoint31Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)


class KnowledgePoint32Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)


class KnowledgePoint33Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)


class KnowledgePoint34Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        arg1 = args['arg1']
        arg2 = args['arg2']
        args['large_num'] = max(arg1, arg2)
        args['small_num'] = min(arg1, arg2)

        def compare_nums_statement(num1, num2):
            if num1 == num2:
                return _("First compare the numbers, {} equals {}. Place the first number as the **multiplicand** and the second number as the **multiplier**.").format(num1, num2)
            if num1 // 10 == num2 // 10:
                return _("First compare the numbers, {} is greater than {} **because in units place digits {} is greater than {}**. First place the bigger number as **multiplicand** and then second number as **multiplier**.").format(
                    max(num1, num2), min(num1, num2), max(num1, num2) % 10, min(num1, num2) % 10)
            else:
                return _("First compare the numbers, {} is greater than {} **because in tens place digits {} is greater than {}**. First place the bigger number as **multiplicand** and then second number as **multiplier**.").format(
                    max(num1, num2), min(num1, num2), max(num1, num2) // 10, min(num1, num2) // 10)

        args["compare_nums_statement"] = compare_nums_statement(arg1, arg2)
        return self.custom_format(template, **args)


class KnowledgePoint35Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)


class KnowledgePoint36Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def fractions_statement(a, b):
            if a < b:
                return _("{}/{} is a proper fraction because {} < {}.").format(a, b, a, b)
            else:
                return _("{}/{} is an improper fraction because {} > {}.").format(a, b, a, b)

        if 'arg3' not in args or args['arg3'] is None:
            template = r"""
<div class="ex-text">

$$
\frac{[[arg1]]}{[[arg2]]}
$$

</div>

[[fractions_statement(arg1, arg2)]]
"""
        args["fractions_statement"] = fractions_statement
        return self.custom_format(template, **args)

class KnowledgePoint38Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        # Extract arguments
        arg1 = args['arg1']
        arg2 = args['arg2']

        def count_digits(num):
            return len(str(num))

        result_digits = count_digits(arg1 // arg2)

        if result_digits == 3:
            step0_statement = ""

            step1_part1 = _("""
**Step 1:**
In this question, you divide the **hundreds** first. You divide {} hundreds into {} groups of 100.

**Step 1.1:** Write {} above the hundreds' place to show you have put 100 in each group.
""").format(arg1 // 100, arg1 // 100 // arg2, arg1 // 100 // arg2)

            step1_part2 = _("""
**Step 1.2:** Write {} underneath to show {} hundreds have been used.
""").format(arg1 // 100 // arg2 * arg2 * 100, arg1 // 100)

            step1_part3 = _("""
**Step 1.3:** You subtract {} from {} to see how many blocks are left that need to be grouped equally.
""").format(arg1 // 100 // arg2 * arg2 * 100, arg1)

            step1_statement = step1_part1 + step1_part2 + step1_part3

            step2_part1 = _("""
**Step 2:**
Let’s look at the {} tens. When you divide them into {} equal groups, you can put {} tens in each group.

**Step 2.1:** Write {} above the tens' place to show you have put {} tens in each group.
""").format(arg1 % 100 // 10, arg2, arg1 % 100 // 10 // arg2, arg1 % 100 // 10 // arg2, arg1 % 100 // 10 // arg2)

            step2_part2 = _("""
**Step 2.2:** Write {} underneath to show that {} groups of {} tens have been used.
""").format(arg1 % 100 // 10 // arg2 * arg2 * 10, arg2, arg1 % 100 // 10 // arg2)

            step2_statement = step2_part1 + step2_part2

            step3_part1 = _("""
**Step 3:**
Now you need to group the {} ones that are left into {} equal groups.

**Step 3.1:** Write {} above the ones' place to show you have put {} ones in each group.
""").format(arg1 // arg2 % 10 * arg2 + arg1 % arg2, arg2, arg1 // arg2 % 10 * arg2 + arg1 % arg2, arg2)

            step3_part2 = _("""
**Step 3.2:** Write {} underneath to show {} groups of {} have been used.
""").format(arg1 // arg2 % 10 * arg2, arg1 // arg2 % 10, arg2)

            step3_part3 = _("""
**Step 3.3:** Subtract {} from {} to see how many blocks are left.
""").format(arg1 // arg2 % 10 * arg2, arg1 // arg2 % 10 * arg2 + arg1 % arg2)

            step3_statement = step3_part1 + step3_part2 + step3_part3

            step4_statement = _("""
**Step 4: Write the remainder near the quotient and check**
As you can see, {} cannot be divided equally into {} equal groups. There is {} unit left over, and it can be represented as R (remainder).
""").format(arg1, arg2, arg1 % arg2)

        elif result_digits == 2 or result_digits == 1:
            step0_statement = _("""
When you come across a step in long division where the divisor is larger than the current working dividend, you need to put a zero in the quotient.
""")

            step1_part1 = _("""
**Step 1:**
How many {}s are there in {}? Since the answer is 0, we move on to the next place value.
""").format(arg2, arg1 // 100)

            step1_part2 = _("""
**Step 1.2:** We calculate {} × {} = {} and write it below {}.
""").format(arg1 // 10 // arg2, arg2, arg1 // 10 // arg2 * arg2, arg1 // 10)

            step1_part3 = _("""
**Step 1.3:** We subtract {} from {} and write {}.
""").format(arg1 // 10 // arg2 * arg2, arg1 // 10, arg1 // 10 - arg1 // 10 // arg2 * arg2)

            step1_statement = step1_part1 + step1_part2 + step1_part3

            step2_part1 = _("""
**Step 2:**
We bring down the number in the ones’ place.
""")

            step2_part2 = _("""
**Step 2.2:** How many {}s are there in {}? We estimate {} and write it above the ones' place.
""").format(arg2, arg1 - arg1 // 10 // arg2 * arg2 * 10, (arg1 - arg1 // 10 // arg2 * arg2 * 10) // arg2)

            step2_part3 = _("""
**Step 2.3:** We calculate {} × {} = {} and write it below {}.
""").format(arg2, (arg1 - arg1 // 10 // arg2 * arg2 * 10) // arg2, arg1 // arg2 % 10 * arg2, arg1 // arg2 % 10 * arg2)

            step2_statement = step2_part1 + step2_part2 + step2_part3

            step3_statement = _("""
**Step 3: Write the remainder near the quotient and check**
""")

            step4_statement = ""

        else:
            raise ValueError(_("Unsupported number of digits"))

        args["step0_statement"] = step0_statement
        args["step1_statement"] = step1_statement
        args["step2_statement"] = step2_statement
        args["step3_statement"] = step3_statement
        args["step4_statement"] = step4_statement

        # Format the template with arguments
        return self.custom_format(template, **args)


class KnowledgePoint39Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        arg1 = args['arg1']
        arg2 = args['arg2']

        def divisors(n):
            divs = []
            for i in range(1, n + 1):
                if n % i == 0:
                    divs.append(i)
            return divs

        # Find divisors of both numerator and denominator
        num_divisors = divisors(arg1)
        denom_divisors = divisors(arg2)

        # Find common divisors
        common_divs = [d for d in num_divisors if d in denom_divisors]

        # Prepare formatted divisors for template
        args["num_divisors"] = ", ".join(map(str, num_divisors))
        args["denom_divisors"] = ", ".join(map(str, denom_divisors))
        args["common_divs"] = ", ".join(map(str, common_divs))
        args["gcd"] = gcd(arg1, arg2)
        args["simplified_numerator"] = arg1 // gcd(arg1, arg2)
        args["simplified_denominator"] = arg2 // gcd(arg1, arg2)

        return self.custom_format(template, **args)


class KnowledgePoint41Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        # Extract arguments
        arg1 = args['arg1']
        arg2 = args['arg2']

        def count_digits(num):
            return len(str(num))

        result_digits = count_digits(arg1 // arg2)

        # Answer is 2-digit number
        if result_digits == 2:
            step2_part1 = _(r"""
**Step 2:**
**Step 2.1:** How many {}s are there in {}? We estimate {} and write it above the ten's place.
""").format(arg2, arg1 // 10, arg1 // 10 // arg2)

            step2_part2 = _(r"""
**Step 2.2:** We calculate ${} \times {} = {}$ and write {} below {}.
""").format(arg1 // 10 // arg2, arg2, arg1 // 10 // arg2 * arg2, arg1 // 10 // arg2 * arg2, arg1 // 10)

            step2_part3 = _(r"""
**Step 2.3:** We subtract {} from {} and write {}.
""").format(arg1 // 10 // arg2 * arg2, arg1 // 10, arg1 // 10 - arg1 // 10 // arg2 * arg2)

            step2_statement = step2_part1 + step2_part2 + step2_part3

            step3_part1 = _(r"""
**Step 3:**
**Step 3.1:** How many {}s are there in {}? We estimate {} and write it above the one's place.
""").format(arg2, arg1 - arg1 // 10 // arg2 * arg2 * 10, (arg1 - arg1 // 10 // arg2 * arg2 * 10) // arg2)

            step3_part2 = _(r"""
**Step 3.2:** We calculate ${} \times {} = {}$ and write {} below {}.
""").format((arg1 - arg1 // 10 // arg2 * arg2 * 10) // arg2, arg2, arg1 // arg2 % 10 * arg2, arg1 // arg2 % 10 * arg2, arg1 - arg1 // 10 // arg2 * arg2 * 10)

            step3_part3 = _("""
**Step 3.3:** We subtract {} from {} and write {}.
""").format(arg1 // arg2 % 10 * arg2, arg1 - arg1 // 10 // arg2 * arg2 * 10, arg1 % arg2)

            step3_statement = step3_part1 + step3_part2 + step3_part3

            step4_statement = _("""
**Step 4: Write the remainder near the quotient and check**
""")

        # Answer is 1-digit number
        elif result_digits == 1:
            step2_statement = _("""
**Step 2:**
**Step 2.1:** How many {}s are there in {}? We estimate {} and write it above the ten's place.
""").format(arg2, arg1 // 10, arg1 // 10 // arg2)

            step3_part1 = _("""
**Step 3:**
**Step 3.1:** How many {}s are there in {}? We estimate {} and write it above the ten's place.
""").format(arg2, arg1, arg1 // arg2)

            step3_part2 = _(r"""
**Step 3.2:** We calculate ${} \times {} = {}$ and write {} below {}.
""").format(arg1 // arg2, arg2, arg1 // arg2 * arg2, arg1 // arg2 * arg2, arg1)

            step3_part3 = _(r"""
**Step 3.3:** We subtract {} from {} and write {}.
""").format(arg1 // arg2 * arg2, arg1, arg1 % arg2)

            step3_statement = step3_part1 + step3_part2 + step3_part3

            step4_statement = _("""
**Step 4: Write the remainder near the quotient and check**
""")

        else:
            raise ValueError(_("Unsupported number of digits"))

        args["step2_statement"] = step2_statement
        args["step3_statement"] = step3_statement
        args["step4_statement"] = step4_statement

        # Format the template with arguments
        return self.custom_format(template, **args)



class KnowledgePoint42Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        arg1 = args['arg1']
        arg2 = args['arg2']

        def divisors(n):
            divs = []
            for i in range(1, n + 1):
                if n % i == 0:
                    divs.append(i)
            return divs

        # Find divisors of both numerator and denominator
        num_divisors = divisors(arg1)
        denom_divisors = divisors(arg2)

        # Find common divisors
        common_divs = [d for d in num_divisors if d in denom_divisors]

        # Prepare formatted divisors for template
        args["num_divisors"] = ", ".join(map(str, num_divisors))
        args["denom_divisors"] = ", ".join(map(str, denom_divisors))
        args["common_divs"] = ", ".join(map(str, common_divs))
        args["gcd"] = gcd(arg1, arg2)
        args["simplified_numerator"] = arg1 // gcd(arg1, arg2)
        args["simplified_denominator"] = arg2 // gcd(arg1, arg2)

        return self.custom_format(template, **args)

class KnowledgePoint43Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        # Extract arguments
        arg1 = args['arg1']
        arg2 = args['arg2']

        # Check for division by zero
        if arg2 == 0:
            return _("Division by zero is undefined.")

        # Compute the division result
        decimal = arg1 / arg2
        args['float_arg1'] = float(arg1)
        float_arg1 = float(arg1)

        # Function to count decimal digits
        def count_decimal_digits(num):
            str_num = str(num)
            if '.' in str_num:
                return len(str_num.split('.')[1])
            else:
                return 0

        # Determine the number of decimal digits
        decimal_digits = count_decimal_digits(decimal)

        # Select the appropriate template
        if decimal_digits == 1:
            step3_statement = _("""
**Step 3:** Since we have no leftovers, we have finished the calculation.
$$
\\begin{{aligned}}
&\\underline{{\\: 0.{{\\color {{Salmon}} {} }}\\:}} \\\[-5pt]
{} &\\big){} \:0 \\\[-4pt]
-&{{\\:{{\\color {{Salmon}} {} }}{{\\:\\!\\color {{Salmon}} {} }}\\:}} \\\[-4pt]
\\hline
&\\text{{ }}\\: \\:\\:{{\\!\\color {{Salmon}} {}}}\\[-4pt]
\\end{{aligned}}
\\: \\longrightarrow \\:
{}
$$
Therefore, the final solution is {}""").format(arg1 * 10 // arg2, arg2, arg1, arg1 * 10 // arg2 * arg2 // 10,
                                               arg1 * 10 // arg2 * arg2 % 10, arg1 * 10 % arg2, arg1 / arg2,
                                               arg1 / arg2)

            step4_statement = ""

        elif decimal_digits == 2:
            step3_statement = _("""
**Step 3:** Since we obtained a non-zero remainder in the previous step, the calculation isn't complete. Because the remainder {} can't be divided evenly by {}, we need to form a new number to continue the division process.
$$
\\begin{{aligned}}
&\\underline{{\\: 0.{{\\color {{Salmon}} {} }}\\:}} \\\[-5pt]
{} &\\big){} \:0 \\\[-4pt]
-&{{\\:{{\\color {{Salmon}} {} }}{{\\:\\!\\color {{Salmon}} {} }}\\:}} \\\[-4pt]
\\hline
&\\text{{ }}\\: \\:\\:{{\\!\\color {{Salmon}} {}}}\\[-4pt]
\\end{{aligned}}
$$""").format(arg1 * 10 % arg2, arg2, arg1 * 10 % arg2, arg1 * 10 // arg2, arg2, arg1, arg1 * 10 % arg2)

            step4_statement = _("""
**Step 4:** How many times does {} go into {}? ${}\times{} = {}$, we place the number {} in the quotient, next to the {}.
$$
\\begin{{aligned}}
&\\underline{{\\text{{ }} \\:{}\\text{{ }} }}\\[-5pt]
{} &\\big){} \:0 \\\[-4pt]
\\end{{aligned}}
$$""").format(arg2, arg1 * 10, arg2, arg1 * 10)

        else:
            raise ValueError(_("Unsupported number of decimal digits"))

        args["step3_statement"] = step3_statement
        args["step4_statement"] = step4_statement

        return self.custom_format(template, **args)

class KnowledgePoint44Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        arg1 = args['arg1']
        arg2 = args['arg2']

        def decimal_digits(num: float):
            str_num = str(num)
            if '.' in str_num:
                decimal = str_num.split('.')[1]
                # print(decimal)
                return decimal
            else:
                return '0'

        def count_decimal_digits(num: float):
            str_num = str(num)
            if '.' in str_num:
                decimal = str_num.split('.')[1]
                # print(decimal)
                return len(decimal)
            else:
                return 0

        def get_round_decimal(arg1, arg2):
            res_decimal_digits = count_decimal_digits(arg1 + arg2)
            if arg1 + arg2 == 1.0:
                return 1

            rounded_num = arg1 + arg2  # Default if no rounding is specified
            if res_decimal_digits > 2:
                rounded_num = round(arg1 + arg2, 2)
            return rounded_num

        result = get_round_decimal(arg1, arg2)

        decimal_arg1 = decimal_digits(args['arg1'])
        decimal_arg2 = decimal_digits(args['arg2'])
        arg1_fraction_digits = count_decimal_digits(args['arg1'])
        arg2_fraction_digits = count_decimal_digits(args['arg2'])

        if arg1_fraction_digits == 1 and arg2_fraction_digits == 1:
            int_arg1 = int(decimal_arg1)
            int_arg2 = int(decimal_arg2)

            # template3
            step2_statement = _(r"""
**Step 2:** We start with the rightmost column. In this case, it's the tenths column. We add the digits in that column: ${0} + {1} = {2}$ and write {3} in the tenths column.
$$
\begin{{array}}{{r c r}}
\\
&0.{0}\\
+&0.{1}\\
\hline
&\phantom{{0}}\,{3}
\end{{array}}
\:\:\:\longrightarrow\:\:
\begin{{array}}{{r c r}}
\\
& \tiny{4}\:\:\:\:\:\:\:\,\\[-3pt]
&0.{{\color {{Salmon}} {0}}}\\
+&0.{{\color {{Salmon}} {1}}}\\
\hline
&\phantom{{0}}\:{{\color {{Salmon}} {3}}}
\end{{array}}
$$
""").format(int_arg1, int_arg2, int_arg1 + int_arg2, (int_arg1 + int_arg2) % 10, (int_arg1 + int_arg2) // 10)

            step3_statement = _(r"""
**Step 3:** Then, we continue to move to the left column. In this case, it's the ones column. We add the digits in that column: ${0} + 0 + 0 = {0}$ and write it in the ones column. And don't forget to add the decimal point after the ones column.
$$
\begin{{array}}{{l l}}
\\
&0.{1}\\ 
+&0.{2} \\
\hline
&{{\color {{Salmon}} {0}}}.{3}
\end{{array}}
\:\:\:\longrightarrow\:\:
\begin{{array}}{{l l}}
\\
&0.{1}\\
+&0.{2} \\
\hline
&{4}\\
\end{{array}}
$$
""").format((int_arg1 + int_arg2) // 10, int_arg1, int_arg2, (int_arg1 + int_arg2) % 10, result)

            step4_statement = ""
            step5_statement = ""

        elif (arg1_fraction_digits == 1 and arg2_fraction_digits == 2) or (
                arg1_fraction_digits == 2 and arg2_fraction_digits == 1):

            if arg1_fraction_digits == 1:
                int_arg1 = int(decimal_arg1)
                int_arg2 = int(decimal_arg2)

            else:  # arg1_fraction_digits == 2 and arg2_fraction_digits == 1
                int_arg1 = int(decimal_arg2)
                int_arg2 = int(decimal_arg1)

            # Template1
            step2_statement = _(r"""
**Step 2:** Add zeros in the places where the length of the decimal numbers is not the same.
$$
\begin{{array}}{{r c r}}
&0.{0}\phantom{{0}}\\
+&0.{3}{4} \\
\hline
\end{{array}}
\:\:\:\longrightarrow\:\:
\begin{{array}}{{r c r}}
&0.{0}{{\color {{Salmon}} 0}}\\
+&0.{3}{4} \\
\hline
\end{{array}}
$$
*Note: When we line up the decimal points in decimal addition, we want to make sure that each digit is in the correct place. To add numbers accurately, equalize the digits after the decimal point by adding zeros.*
""").format(int_arg1, int_arg2, arg2, int_arg2 // 10, int_arg2 % 10)

            step3_statement = _(r"""
**Step 3:** We start with the rightmost column. In this case, it's the hundredths column. We add the digits in that column: $0 + {0} = {0}$ and write it in the hundredths column.
$$
\begin{{array}}{{r c r}}
&0.{1}0\\
+&0.{3}{0} \\
\hline
\end{{array}}
\:\:\:\longrightarrow\:\:
\begin{{array}}{{r c r}}
\\
&0.{1}{{\color {{Salmon}} 0}}\\
+&0.{{{3}}}{{\color{{Salmon}} {0}}} \\
\hline
&\phantom{{0}}\phantom{{0}}\:\,{{\color {{Salmon}} {0}}}
\end{{array}}
$$
""").format(int_arg2 % 10, int_arg1, int_arg2, int_arg2 // 10)

            step4_statement = _(r"""
**Step 4:** Next, we move to the left column. In this case, it's the tenths column. We add the digits in that column: ${0} + {1} = {2}$ and write {3} in the tenths column.
$$
\begin{{array}}{{r c r}}
&0.{0}0\\
+&0.{1}{4} \\
\hline
&\phantom{{0}}\phantom{{0}}\:\,{4}\\
\end{{array}}
\:\:\:\longrightarrow\:\:
\begin{{array}}{{r c r}}
& \tiny{6}\:\:\:\:\:\:\:\,\\[-3pt]
&0.{{\color {{Salmon}} {0}}}0\\
+&0.{{\color {{Salmon}} {1}}}{4} \\
\hline
&\phantom{{0}}\:{{\color {{Salmon}} {3}}}{4}
\end{{array}}
$$
""").format(int_arg1, int_arg2 // 10, int_arg1 + int_arg2 // 10, (int_arg1 + int_arg2 // 10) % 10, int_arg2 % 10,
           int_arg2, (int_arg1 + int_arg2 // 10) // 10, arg2)

            step5_statement = _(r"""
**Step 5:** Then, we continue to move to the left column. In this case, it's the ones column. We add the digits in that column: ${0} + 0 + 0 = {0}$ and write it in the ones column. And don't forget to add the decimal point after the ones column.
$$
\begin{{array}}{{l l}}
\\
&0.{1}0\\
+&0.{5}{4} \\
\hline
&{{\color {{Salmon}} {0}}}.{3}{4}
\end{{array}}
\:\:\:\longrightarrow\:\:
\begin{{array}}{{l l}}
\\
&0.{1}0\\
+&0.{5}{4} \\
\hline
&{6}\\
\end{{array}}
$$
""").format((int_arg1 + int_arg2 // 10) // 10, int_arg1, int_arg2, (int_arg1 + int_arg2 // 10) % 10, int_arg2 % 10,
           int_arg2 // 10, result)

        elif arg1_fraction_digits == 2 and arg2_fraction_digits == 2:
            int_arg1 = int(decimal_arg1)
            int_arg2 = int(decimal_arg2)

            # template2
            step2_statement = _(r"""
**Step 2:** We start with the rightmost column. In this case, it's the hundredths column. We add the digits in that column: ${0} + {1} = {2}$ and write {3} in the hundredths column.
$$
\begin{{array}}{{r c r}}
&{4} \\
+&{5} \\
\hline
\end{{array}}
\:\:\:\longrightarrow\:\:
\begin{{array}}{{r c r}}
\\
& \:\:\:\:\:\:\tiny{8}\:\:\:\:\:\:\:\,\\[-3pt]
&0.{6}{{\color{{Salmon}}{0}}}\\
+&0.{7}{{\color{{Salmon}}{1}}}\\
\hline
&\phantom{{0}}\phantom{{0}}\:\,{{\color{{Salmon}}{3}}}
\end{{array}}
$$
""").format(
                int_arg1 % 10, int_arg2 % 10, int_arg1 % 10 + int_arg2 % 10, (int_arg1 % 10 + int_arg2 % 10) % 10,
                arg1, arg2, int_arg1 // 10, int_arg2 // 10, (int_arg1 % 10 + int_arg2 % 10) // 10)

            step3_statement = _(r"""
**Step 3:** Next, we move to the left column. In this case, it's the tenths column. We add the digits in that column: ${2} + {1} + {0} = {3}$ and write {4} in the tenths column.
$$
\begin{{array}}{{r c r}}
\\
&{5} \\
+&{6}\\
\hline
&\phantom{{0}}\phantom{{0}}\:\,{7}
\end{{array}}
\:\:\:\longrightarrow\:\:
\begin{{array}}{{r c r}}
& \tiny{{\color{{Salmon}}{8}}}\:\:\:\:\:\:\:\,\\[-3pt]
&0.{{\color {{Salmon}} {0}}}{9}\\
+&0.{{\color {{Salmon}} {1}}}{10} \\
\hline
&\:\,\,.{{\color {{Salmon}} {4}}}{7}\\
\end{{array}}
$$
""").format(int_arg1 // 10, int_arg2 // 10, (int_arg1 % 10 + int_arg2 % 10) // 10,
           int_arg1 // 10 + int_arg2 // 10 + (int_arg1 % 10 + int_arg2 % 10) // 10,
           (int_arg1 // 10 + int_arg2 // 10 + (int_arg1 % 10 + int_arg2 % 10) // 10) % 10,
           arg1, arg2, (int_arg1 % 10 + int_arg2 % 10) % 10,
           (int_arg1 // 10 + int_arg2 // 10 + (int_arg1 % 10 + int_arg2 % 10) // 10) // 10, int_arg1 % 10,
           int_arg2 % 10)

            step4_statement = _(r"""
**Step 4:**  We carried over the {0} from the tenths column to the next column, which is the whole numbers or ones column.

In this column, we add the carried-over {0} with the digit 0 (since there are no digits in the ones column to add). When we add {0} and 0, we get {0} and write it in the ones column. And we add the decimal point after the ones column as the final step.
$$
\begin{{array}}{{l l}}
& \tiny{{{0}}}\:\:\:\:\:\:\:\,\\[-3pt]
&{1} \\
+&{2} \\
\hline
&\:\,\,.{3}{4}\\
\end{{array}}
\:\:\:\longrightarrow\:\:
\begin{{array}}{{l l}}
& \tiny{{\color{{Salmon}}{0}}}\:\:\:\:\:\:\:\,\\[-3pt]
&{1}\\
+&{2} \\
\hline
&{{\color {{Salmon}}{0}}}.{3}{4}\\
\end{{array}}
$$
""").format(
                (int_arg1 // 10 + int_arg2 // 10 + (int_arg1 % 10 + int_arg2 % 10) // 10) // 10,
                arg1, arg2, (int_arg1 // 10 + int_arg2 // 10 + (int_arg1 % 10 + int_arg2 % 10) // 10) % 10,
                (int_arg1 % 10 + int_arg2 % 10) % 10)

            step5_statement = ""

        else:
            # Handle cases where the digits are neither 1 nor 2 for both arguments or other undefined cases
            raise ValueError("Unexpected number of fraction digits in arguments")

        args['int_arg1'] = int_arg1
        args['int_arg2'] = int_arg2
        args['get_round_decimal'] = get_round_decimal
        args["step2_statement"] = step2_statement
        args["step3_statement"] = step3_statement
        args["step4_statement"] = step4_statement
        args["step5_statement"] = step5_statement

        return self.custom_format(template, **args)


class KnowledgePoint45Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        arg1 = args['arg1']
        arg2 = args['arg2']

        def decimal_digits(num: float):
            str_num = str(num)
            if '.' in str_num:
                decimal = str_num.split('.')[1]
                # print(decimal)
                return decimal
            else:
                return '0'

        def count_decimal_digits(num: float):
            str_num = str(num)
            if '.' in str_num:
                decimal = str_num.split('.')[1]
                # print(decimal)
                return len(decimal)
            else:
                return 0

        def get_round_decimal(arg1, arg2):
            res_decimal_digits = count_decimal_digits(arg1 - arg2)
            if arg1 - arg2 == 1.0:
                return 1

            rounded_num = arg1 - arg2  # Default if no rounding is specified
            if res_decimal_digits > 2:
                rounded_num = round(arg1 - arg2, 2)
            return rounded_num

        result = get_round_decimal(arg1, arg2)

        decimal_arg1 = decimal_digits(args['arg1'])
        decimal_arg2 = decimal_digits(args['arg2'])
        arg1_fraction_digits = count_decimal_digits(args['arg1'])
        arg2_fraction_digits = count_decimal_digits(args['arg2'])

        if arg1_fraction_digits == 1:
            if arg2_fraction_digits == 1:
                int_arg1 = int(decimal_arg1)
                int_arg2 = int(decimal_arg2)

                # template1
                step2_statement = r"""
**Step 2:** We start with the rightmost column. In the rightmost column, the first number in this column is {0}. We have ${0} - {1} ={2}$
in this column and write it in the tenths column.
$$
\begin{{array}}{{r c r}}
&0.{3}\\
-&0.{4}\\
\hline
\end{{array}}
\:\:\:\longrightarrow    \:\:
\begin{{array}}{{r c r}}
\\
&0.{{\color {{Salmon}} {0}}}\\
-&0.{{\color {{Salmon}} {1}}} \\
\hline
&\phantom{{0}}\,{{\color {{Salmon}} {2}}}
\end{{array}}
$$
""".format(int_arg1 % 10, int_arg2 % 10, int_arg1 % 10 - int_arg2 % 10,
           int_arg1, int_arg2)

                step3_statement = r"""
**Step 3:** Next, we move to the left column. The first number in this column is 0. We have $0 - 0 = 0$ in this column and write it in the ones column. And don't forget to add the decimal point after the ones column.

$$
\begin{{array}}{{l l}}\\
&0.{0}\\
-&0.{1}\\
\hline
&\:\,\,.{2}\\
\end{{array}}
\:\:\:\longrightarrow    \:\:
\begin{{array}}{{l l}}\\
&0.{0}\\
-&0.{1}\\
\hline
&{3}\\
\end{{array}}
$$
""".format(int_arg1, int_arg2, int_arg1 - int_arg2, result)

                step4_statement = ""
                step5_statement = ""

            else:
                int_arg1 = int(decimal_arg1)
                int_arg2 = int(decimal_arg2)

                # template2
                step2_statement = r"""
**Step 2:** Add zeros in the places where the length of the decimal numbers is not the same.
$$
\begin{{array}}{{r c r}}
&{0}{{ }}\phantom{{0}}\\
-&{1} \\
\hline
\end{{array}}
\:\:\:\longrightarrow    \:\:
\begin{{array}}{{r c r}}
&{0}{{\color {{Salmon}} 0}}\\
-&{1} \\
\hline
\end{{array}}
$$

*Note: When we line up the decimal points in decimal subtraction, we want to make sure that each digit is in the correct place. To subtract numbers accurately, equalize the digits after the decimal point by adding zeros.*
""".format(arg1, arg2)

                step3_statement = r"""
**Step 3:** We start with the rightmost column. In the rightmost column, the first number in this column is {1}. We can see that 0 is smaller than {1}. So, we need to borrow 1 from the left column which will make it 10. And the {0} in the left column becomes {2}. Now we have $10 - {1} = {3}$ in this column and write it in the hundredths column.
$$
\begin{{array}}{{r c r}}
&{0}0\\
-&{6} \\
\hline
\end{{array}}
\:\:\:\longrightarrow    \:\:
\begin{{array}}{{r c r}}
& \:\:\:\:\tiny{{\color{{Salmon}} {2}}}\:\tiny{{\color{{Salmon}} 10}}\\[-3pt]
&0.{{\color {{Salmon}} \cancel{4} }}{{\color {{Salmon}}\cancel0 }}\\
-&0.{5}{{\color {{Salmon}} {1}}} \\
\hline
&\phantom{{0}}\phantom{{0}}\:\,{{\color {{Salmon}} {3}}}
\end{{array}}
$$
""".format(arg1, int_arg2 % 10, int_arg1 - 1, 10 - int_arg2 % 10, int_arg1, int_arg2 // 10, arg2)

                step4_statement = r"""
**Step 4:** Next, we move to the left column. After giving 1 to the rightmost column in step 3, the {0} in this column becomes {1}. Now we have ${0} - {2} = {3}$ in this column and write it in the tenths column.

$$
\begin{{array}}{{r c r}}
& \:\:\:\:\tiny{1}\:\tiny10\\[-3pt]
&0.{{\cancel{0} }}{{\cancel0}}\\
-&{4}\\
\hline
&\phantom{{0}}\phantom{{0}}\:\,{5}
\end{{array}}
\:\:\:\longrightarrow    \:\:
\begin{{array}}{{r c r}}
& \:\:\:\:\tiny{{\color{{Salmon}} {1}}}\:\tiny10\\[-3pt]
&0.{{\cancel {0} }}{{\cancel0}}\\
-&0.{{\color{{Salmon}} {2}}}{6}\\
\hline
&\:\,\,.{{\color{{Salmon}} {3} }}{5}
\end{{array}}
$$
""".format(int_arg1, int_arg1 - 1, int_arg2 // 10, (int_arg1 - 1) - int_arg2 // 10,
           arg2, 10 - int_arg2 % 10, int_arg2 % 10)

                step5_statement = r"""
**Step 5:** Then, we continue to move to the left column, the first number in this column is 0. We have $0 - 0 = 0$ in this column and write it in the ones column. And don't forget to add the decimal point after the ones column.
$$
\begin{{array}}{{l l}}
& \:\:\:\:\tiny{0}\:\tiny{{10}}\\[-3pt]
&0.{{ \cancel{1} }}{{\cancel0}}\\
-&{2} \\
\hline
&\:\,\,.{3} \\
\end{{array}}
\:\:\:\longrightarrow    \:\:
\begin{{array}}{{l l}}
& \:\:\:\:\tiny{0}\:\tiny{{10}}\\[-3pt]
&0.{{ \cancel{1} }}{{\cancel0}}\\
-&{2} \\
\hline
&{4} \\
\end{{array}}
$$
""".format(int_arg1 - 1, int_arg1, arg2, int_arg1 * 10 - int_arg2, result)

        else:
            int_arg1 = int(args['arg1'] * 100)
            int_arg2 = int(args['arg2'] * 100)

            if int_arg1 % 10 < int_arg2 % 10:
                ##template3
                step2_statement = r"""
**Step 2:** We start with the rightmost column. In the rightmost column, the first number in this column is {}. We can see that {} is smaller than {}. So, we need borrow 1 from the left column which will make it {}. And the {} in the left column becomes {}. Now we have ${} - {} = {}$ in this column and write it in the hundredths column.
$$
\begin{{array}}{{r c r}}
&{}\\
-&{} \\
\hline
\end{{array}}
\:\:\:\longrightarrow    \:\:
\begin{{array}}{{r c r}}
& \:\:\:\:\tiny{{\color{{Salmon}} {}}}\:\tiny{{\color{{Salmon}} {}}}\\[-3pt]
&0.{{\color {{Salmon}} \cancel{} }}{{\color {{Salmon}}\cancel{} }}\\
-&0.{}{{\color {{Salmon}} {}}} \\
\hline
&\phantom{{0}}\phantom{{0}}\:\,{{\color {{Salmon}} {} }}
\end{{array}}
$$
""".format(int_arg1 % 10, int_arg1 % 10, int_arg2 % 10, (int_arg1 % 10) + 10, int_arg1 // 10, (int_arg1 // 10) - 1,
           (int_arg1 % 10) + 10, int_arg2 % 10, (int_arg1 - int_arg2) % 10,
           arg1, arg2, int_arg1 // 10 - 1, (int_arg1 % 10) + 10, int_arg1 // 10, int_arg1 % 10, int_arg2 // 10,
           int_arg2 % 10, (int_arg1 % 10 + 10) - int_arg2 % 10)

                step3_statement = r"""
**Step 3:** Next, we move to the left column. After giving 1 to the rightmost column in step 3, the {} in this column becomes {}. Now we have ${} - {} = {}$ in this column and write it in the tenths column.
$$
\begin{{array}}{{r c r}}
& \:\:\:\:\tiny{{{}}}\:\tiny{{{}}}\\[-3pt]
&0.{{\cancel{{{}}}}}{{\cancel{{{}}}}}\\
-&{}\\
\hline
&\phantom{{0}}\phantom{{0}}\:\, {{{}}}
\end{{array}}
\:\:\:\longrightarrow    \:\:
\begin{{array}}{{r c r}}
& \:\:\:\:\tiny{{\color{{Salmon}} {}}}\:\tiny{{{}}}\\[-3pt]
&0.{{\cancel{{{}}}}}{{\cancel{{{}}}}}\\
-&0.{{\color{{Salmon}} {}}}{{{}}}\\
\hline
&\:\,\,.{{\color{{Salmon}} {}}}{{{}}}
\end{{array}}
$$
""".format(int_arg1 // 10, int_arg1 // 10 - 1, int_arg1 // 10 - 1, int_arg2 // 10,
           (int_arg1 // 10 - 1) - int_arg2 // 10,
           int_arg1 // 10 - 1, int_arg1 % 10 + 10, int_arg1 // 10, int_arg1 % 10, arg2, (int_arg1 - int_arg2) % 10,
           int_arg1 // 10 - 1,
           int_arg1 % 10 + 10, int_arg1 // 10, int_arg1 % 10, int_arg2 // 10, int_arg2 % 10,
           (int_arg1 - int_arg2) // 10, (int_arg1 - int_arg2) % 10)

                step4_statement = r"""
**Step 4:** Then, we continue to move to the left column, the first number in this column is 0. We have $0 - 0 = 0$ in this column and write it in the ones column. And don't forget to add the decimal point after the ones column.

$$
\begin{{array}}{{l l}}\\
&{4}\\
-&{5}\\
\hline
&\:\,\,.{2}\\
\end{{array}}
\:\:\:\longrightarrow    \:\:
\begin{{array}}{{l l}}\\
&{4}\\
-&{5}\\
\hline
&{3}\\
\end{{array}}
$$
""".format(int_arg1, int_arg2, int_arg1 - int_arg2, result, arg1, arg2)

                step5_statement = ""

            ##template4
            else:
                step2_statement = r"""
**Step 2:** We start with the rightmost column. In the rightmost column, the first number in this column is {0}. We have ${0} - {1} = {2}$ in this column and write it in the hundredths column.
$$
\begin{{array}}{{r c r}}
&{7}\\
-&{8}\\
\hline
\end{{array}}
\:\:\:\longrightarrow    \:\:
\begin{{array}}{{r c r}}
\\
&.{5}{{\color {{Salmon}} {0}}}\\
-&.{6}{{\color {{Salmon}} {1}}} \\
\hline
&\phantom{{0}}\:\,{{\color {{Salmon}} {2}}}
\end{{array}}
$$
""".format(int_arg1 % 10, int_arg2 % 10, int_arg1 % 10 - int_arg2 % 10,
           int_arg1, int_arg2, int_arg1 // 10, int_arg2 // 10, arg1, arg2)

                step3_statement = r"""
**Step 3:** Next, we move to the left column, the first number in this column is {0}. We have ${0} - {1} = {2}$ in this column and write it in the tenths column.
$$
\begin{{array}}{{r c r}}
\\
&{8}\\
-&{9}\\
\hline
&\phantom{{0}}\phantom{{0}}\:\,{5}
\end{{array}}
\:\:\:\longrightarrow    \:\:
\begin{{array}}{{r c r}}\\
&0.{{\color {{Salmon}}  {0}}}{6}\\
-&0.{{\color {{Salmon}}  {1}}}{7} \\
\hline
&\:\,\,.{{\color {{Salmon}}{2}}}{5}\\
\end{{array}}
$$
""".format(int_arg1 // 10, int_arg2 // 10, int_arg1 // 10 - int_arg2 // 10,
           int_arg1, int_arg2, int_arg1 % 10 - int_arg2 % 10, int_arg1 % 10, int_arg2 % 10, arg1, arg2)

                step4_statement = r"""
**Step 4:** Then, we continue to move to the left column, the first number in this column is 0. We have $0 - 0 = 0$ in this column and write it in the ones column. And don't forget to add the decimal point after the ones column.

$$
\begin{{array}}{{l l}}\\
&{4}\\
-&{5}\\
\hline
&\:\,\,.{2}\\
\end{{array}}
\:\:\:\longrightarrow    \:\:
\begin{{array}}{{l l}}\\
&{4}\\
-&{5}\\
\hline
&{3}\\
\end{{array}}
$$
""".format(int_arg1, int_arg2, int_arg1 - int_arg2, result, arg1, arg2)

                step5_statement = ""

        args['int_arg1'] = int_arg1
        args['int_arg2'] = int_arg2
        args['get_round_decimal'] = get_round_decimal
        args["step2_statement"] = step2_statement
        args["step3_statement"] = step3_statement
        args["step4_statement"] = step4_statement
        args["step5_statement"] = step5_statement

        return self.custom_format(template, **args)


class KnowledgePoint46Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        arg1 = args['arg1']
        args['int_arg1'] = int(arg1 * 100)
        return self.custom_format(template, **args)


class KnowledgePoint47Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)


class KnowledgePoint48Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)


from flask_babel import _


class BabelStepGenerator:
    def gcd(self, a, b):
        return gcd(a, b)

    def is_lowest_term(self, a, b):
        return self.gcd(a, b) == 1

    def simplified_statement(self, numerator, denominator):
        gcd_val = self.gcd(numerator, denominator)
        if self.is_lowest_term(numerator, denominator):
            return _("**Step 3:** The fraction {}/{} is already in its lowest term.").format(numerator, denominator)
        else:
            simplified_numerator = numerator // gcd_val
            simplified_denominator = denominator // gcd_val
            return _("**Step 3:** Simplify the fraction {}/{} by dividing both the numerator and denominator by {}: "
                     "$\\frac{{{}}}{{{}}} = \\frac{{{}}}{{{}}}$").format(numerator, denominator, gcd_val, numerator,
                                                                         denominator, simplified_numerator,
                                                                         simplified_denominator)

    def improper_fraction_statement(self, numerator, denominator):
        if numerator > denominator:
            whole_part = numerator // denominator
            remainder = numerator % denominator
            return _("**Step 4:** Convert the improper fraction to a mixed number: "
                     "$\\frac{{{}}}{{{}}} = {} \\frac{{{}}}{{{}}}$").format(numerator, denominator, whole_part,
                                                                            remainder, denominator)
        else:
            return _("**Step 4:** The fraction is already a proper fraction: $\\frac{{{}}}{{{}}}$").format(numerator,
                                                                                                           denominator)


class BabelStepGenerator:
    def gcd(self, a, b):
        return gcd(a, b)

    def is_lowest_term(self, a, b):
        return self.gcd(a, b) == 1

    def simplified_statement(self, numerator, denominator):
        gcd_val = self.gcd(numerator, denominator)
        if self.is_lowest_term(numerator, denominator):
            return _("**Step 3:** The fraction {}/{} is already in its lowest term.").format(numerator, denominator)
        else:
            simplified_numerator = numerator // gcd_val
            simplified_denominator = denominator // gcd_val
            return _("**Step 3:** Simplify the fraction {}/{} by dividing both the numerator and denominator by {}: "
                     "$\\frac{{{}}}{{{}}} = \\frac{{{}}}{{{}}}$").format(numerator, denominator, gcd_val, numerator,
                                                                         denominator, simplified_numerator,
                                                                         simplified_denominator)

    def improper_fraction_statement(self, numerator, denominator):
        if numerator > denominator:
            whole_part = numerator // denominator
            remainder = numerator % denominator
            return _("**Step 4:** Convert the improper fraction to a mixed number: "
                     "$\\frac{{{}}}{{{}}} = {} \\frac{{{}}}{{{}}}$").format(numerator, denominator, whole_part,
                                                                            remainder, denominator)
        else:
            return _("**Step 4:** The fraction is already a proper fraction: $\\frac{{{}}}{{{}}}$").format(numerator,
                                                                                                           denominator)


class KnowledgePoint49Solution(SolutionGenerator, BabelStepGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        numerator = args['arg2'] + args['arg3']
        denominator = args['arg1']

        args["step3_statement"] = self.simplified_statement(numerator, denominator)
        args["step4_statement"] = self.improper_fraction_statement(numerator, denominator)

        return self.custom_format(template, **args)


class KnowledgePoint50Solution(SolutionGenerator, BabelStepGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        numerator = args['arg2'] - args['arg3']
        denominator = args['arg1']

        args["step3_statement"] = self.simplified_statement(numerator, denominator)
        args["step4_statement"] = self.improper_fraction_statement(numerator, denominator)

        return self.custom_format(template, **args)


class KnowledgePoint51Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        args['gcd'] = gcd
        return self.custom_format(template, **args)

class KnowledgePoint52Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        args['gcd'] = gcd
        return self.custom_format(template, **args)


class KnowledgePoint53Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def primeFactorsHelper(n):
            res = []
            while n % 2 == 0:
                res.append(2)
                n = n // 2
            for i in range(3, int(sqrt(n)) + 1, 2):
                while n % i == 0:
                    res.append(i)
                    n = n // i
            if n > 2:
                res.append(n)
            return res

        def smallestFactor(n):
            if n % 2 == 0:
                return 2
            i = 3
            while i * i <= n:
                if n % i == 0:
                    return i
                i += 2
            return n

        def getPrimeFactorization(num):
            og = num
            factors = primeFactorsHelper(num)
            if factors[0] == num:
                return _("    - {} is prime. So it is the only factor").format(num)
            res = (
                _("    - Start from small, the smallest number that can divide {} is {}, so we write down {}. Then ${} / {} = {}$.\n")
                .format(num, factors[0], factors[0], num, factors[0], num // factors[0])
            )
            num //= factors[0]
            for idx in range(1, len(factors) - 1):
                res += (
                    _("    - Now, the smallest number that can divide {} is {}, so we write down {}. Then ${} / {} = {}$.\n")
                    .format(num, factors[idx], factors[idx], num, factors[idx], num // factors[idx])
                )
                num //= factors[idx]
            res += (
                _("    - Notice {} is also a prime number, so we write down {}.\n")
                .format(factors[-1], factors[-1])
            )
            factorstr = str(factors)
            res += (
                _("    - So, the prime factors of {} are {} and {}. (${} = ")
                .format(og, factorstr[1:-3], factorstr[-2:-1], og)
            )
            res += "{}".format(factors[0])
            for factor in factors[1:]:
                res += " \\times {}".format(factor)
            res += "$)."
            return res

        def primeFactors(arg1, arg2, usage):
            arg1factors = primeFactorsHelper(arg1)
            arg2factors = primeFactorsHelper(arg2)
            iter1, iter2 = 0, 0
            sharedfactors, uniquefactors = [], []
            while iter1 < len(arg1factors) and iter2 < len(arg2factors):
                if arg1factors[iter1] == arg2factors[iter2]:
                    sharedfactors.append(arg1factors[iter1])
                    iter1 += 1
                    iter2 += 1
                elif arg1factors[iter1] < arg2factors[iter2]:
                    uniquefactors.append(arg1factors[iter1])
                    iter1 += 1
                else:
                    uniquefactors.append(arg2factors[iter2])
                    iter2 += 1

            if iter1 == len(arg1factors):
                uniquefactors.extend(arg2factors[iter2:])
            if iter2 == len(arg2factors):
                uniquefactors.extend(arg1factors[iter1:])

            if usage == 'Factor/Factors':
                res = ""
                if len(sharedfactors) == 0:
                    res += _("    - There are no common prime factors of {} and {}.\n").format(arg1, arg2)
                elif len(sharedfactors) == 1:
                    res += _("    - The common prime factor of {} and {} is {}.\n").format(arg1, arg2, sharedfactors[0])
                else:
                    res += _("    - The common prime factors of {} and {} are ").format(arg1, arg2)
                    res += "{}".format(sharedfactors[0])
                    for factor in sharedfactors[1:-1]:
                        res += ", {}".format(factor)
                    res += _(" and {}").format(sharedfactors[-1])

                if len(uniquefactors) == 0:
                    res += _("    - There are no unique prime factors of {} and {}.\n").format(arg1, arg2)
                elif len(uniquefactors) == 1:
                    res += _("    - The unique prime factor of {} and {} is {}.\n").format(arg1, arg2, uniquefactors[0])
                else:
                    res += _("    - The unique prime factors of {} and {} are ").format(arg1, arg2)
                    res += "{}".format(uniquefactors[0])
                    for factor in uniquefactors[1:-1]:
                        res += ", {}".format(factor)
                    res += _(" and {}").format(uniquefactors[-1])

                return res

            if usage == 'Chain':
                res = ""
                if len(sharedfactors) >= 1:
                    res += "{}".format(sharedfactors[0])
                    for factor in sharedfactors[1:]:
                        res += " \\times {}".format(factor)

                if len(uniquefactors) >= 1:
                    if len(sharedfactors) != 0:
                        res += " \\times "
                    res += "{}".format(uniquefactors[0])
                    for factor in uniquefactors[1:]:
                        res += " \\times {}".format(factor)

                res += " = {}".format(lcm_of2(arg1, arg2))
                return res

        args['gcd'] = gcd
        args['smallestFactor'] = smallestFactor
        args['getPrimeFactorization'] = getPrimeFactorization
        args['primeFactors'] = primeFactors
        return self.custom_format(template, **args)


class KnowledgePoint54Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def primeFactors(n):
            res = []
            while n % 2 == 0:
                res.append(2)
                n //= 2
            for i in range(3, int(sqrt(n)) + 1, 2):
                while n % i == 0:
                    res.append(i)
                    n //= i
            if n > 2:
                res.append(n)
            return res

        def smallestFactor(n):
            if n % 2 == 0:
                return 2
            i = 3
            while i * i <= n:
                if n % i == 0:
                    return i
                i += 2
            return n

        def getPrimeFactorization(num):
            og = num
            factors = primeFactors(num)
            if factors[0] == num:
                return _("    - {} is prime. So it is the only factor").format(num)
            res = (
                _("    - Start from small, the smallest number that can divide {} is {}, so we write down {}. Then ${} / {} = {}$.\n")
                .format(num, factors[0], factors[0], num, factors[0], num // factors[0])
            )
            num //= factors[0]
            for idx in range(1, len(factors) - 1):
                res += (
                    _("    - Now, the smallest number that can divide {} is {}, so we write down {}. Then ${} / {} = {}$.\n")
                    .format(num, factors[idx], factors[idx], num, factors[idx], num // factors[idx])
                )
                num //= factors[idx]
            res += (
                _("    - Notice {} is also a prime number, so we write down {}.\n")
                .format(factors[-1], factors[-1])
            )
            factorstr = str(factors)
            res += (
                _("    - So, the prime factors of {} are {} and {}. (${} = ")
                .format(og, factorstr[1:-3], factorstr[-2:-1], og)
            )
            res += "{}".format(factors[0])
            for factor in factors[1:]:
                res += " \\times {}".format(factor)
            res += "$)."
            return res

        def commonPrimeFactors(arg1, arg2, usage):
            arg1factors = primeFactors(arg1)
            arg2factors = primeFactors(arg2)
            iter1, iter2 = 0, 0
            sharedfactors = []
            while iter1 < len(arg1factors) and iter2 < len(arg2factors):
                if arg1factors[iter1] == arg2factors[iter2]:
                    sharedfactors.append(arg1factors[iter1])
                    iter1 += 1
                    iter2 += 1
                elif arg1factors[iter1] < arg2factors[iter2]:
                    iter1 += 1
                else:
                    iter2 += 1
            if len(sharedfactors) == 0:
                sharedfactors.append(1)

            if usage == 'Factor/Factors':
                if len(sharedfactors) > 1:
                    return _("factors")
                return _("factor")

            if usage == 'List':
                if len(sharedfactors) == 1:
                    return _("is {}").format(sharedfactors[0])
                res = _("are {}").format(sharedfactors[0])
                for factor in sharedfactors[1:]:
                    res += _(" and {}").format(factor)
                return res

            if usage == 'Chain':
                if len(sharedfactors) == 1:
                    return "{} = {}".format(sharedfactors[0], sharedfactors[0])
                res = "{}".format(sharedfactors[0])
                for factor in sharedfactors[1:]:
                    res += " \\times {}".format(factor)
                res += " = {}".format(gcd(arg1, arg2))
                return res

        args['gcd'] = gcd
        args['smallestFactor'] = smallestFactor
        args['getPrimeFactorization'] = getPrimeFactorization
        args['commonPrimeFactors'] = commonPrimeFactors
        return self.custom_format(template, **args)


class KnowledgePoint55Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def LCMFraction(denominator, lcm):
            if denominator == lcm:
                return ""
            return _(" \\times \\frac{{{}}}{{{}}}").format(lcm // denominator, lcm // denominator)

        def getNumerator(numerator, denominator, lcm):
            factor = lcm // denominator
            numerator *= factor
            return str(numerator)

        def addNumerators(arg1, arg2, arg3, arg4):
            lcm_val = lcm_of2(arg2, arg4)
            factor = lcm_val // arg2
            arg1 *= factor
            factor = lcm_val // arg4
            arg3 *= factor
            return str(arg1 + arg3)

        def simplify(numerator, denominator):
            numerator = int(numerator)
            gcd_val = gcd(numerator, denominator)
            if gcd_val == 1:
                if numerator < denominator:
                    return _("The result cannot be simplified.")
                else:
                    numerator //= gcd_val
                    denominator //= gcd_val
                    return _(
                        "Since the answer is an improper fraction, we can simplify it into the mixed number ${}\\frac{{{}}}{{{}}}$"
                    ).format(numerator // denominator, numerator - numerator // denominator * denominator,
                             denominator)
            res = _(
                "The result can be simplified. When we divide both {} and {} by their greatest common divisor {}, we get {} and {}, respectively."
            ).format(numerator, denominator, gcd_val, numerator // gcd_val, denominator // gcd_val)
            if numerator > denominator:
                numerator //= gcd_val
                denominator //= gcd_val
                res += _(
                    " Since the answer is an improper fraction, we can simplify it into the mixed number ${}\\frac{{{}}}{{{}}}$"
                ).format(numerator // denominator, numerator - numerator // denominator * denominator, denominator)
            return res

        def simplifyAlgebra(numerator, denominator):
            numerator = int(numerator)
            gcd_val = gcd(numerator, denominator)
            if gcd_val == 1:
                return ""
            res = _(
                "\\:\\:\\:\\longrightarrow    \\:\\: \\frac{{{}\\color {{Salmon}}\\div{}}}{{{}\\color {{Salmon}}\\div{}}} = \\frac{{\\color {{Salmon}}{}}}{{\\color {{Salmon}}{{{}}}}}"
            ).format(numerator, gcd_val, denominator, gcd_val, numerator // gcd_val, denominator // gcd_val)
            numerator //= gcd_val
            denominator //= gcd_val
            if numerator > denominator:
                res += _(
                    " = {{\\color {{Salmon}}{}}}\\frac{{\\color {{Salmon}}{}}}{{\\color {{Salmon}}{}}}"
                ).format(numerator // denominator, numerator - numerator // denominator * denominator, denominator)
            return res

        def finalAnswer(arg1, arg2, arg3, arg4):
            numerator = arg1 * arg4 + arg2 * arg3
            denominator = arg2 * arg4
            gcd_val = gcd(numerator, denominator)
            numerator //= gcd_val
            denominator //= gcd_val
            if numerator < denominator:
                return "\\frac{{{}}}{{{}}}".format(numerator, denominator)
            return "{}\\frac{{{}}}{{{}}}".format(numerator // denominator,
                                                 numerator - numerator // denominator * denominator, denominator)

        args['lcm'] = lcm_of2
        args['gcd'] = gcd
        args['LCMFraction'] = LCMFraction
        args['getNumerator'] = getNumerator
        args['addNumerators'] = addNumerators
        args['simplify'] = simplify
        args['simplifyAlgebra'] = simplifyAlgebra
        args['finalAnswer'] = finalAnswer

        return self.custom_format(template, **args)


class KnowledgePoint56Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def LCMFraction(denominator, lcm):
            if denominator == lcm:
                return ""
            return _(" \\times \\frac{{{}}}{{{}}}").format(lcm // denominator, lcm // denominator)

        def getNumerator(numerator, denominator, lcm):
            factor = lcm // denominator
            numerator *= factor
            return str(numerator)

        def subtractNumerators(arg1, arg2, arg3, arg4):
            lcm_val = lcm_of2(arg2, arg4)
            factor = lcm_val // arg2
            arg1 *= factor
            factor = lcm_val // arg4
            arg3 *= factor
            return str(arg1 - arg3)

        def simplify(numerator, denominator):
            numerator = int(numerator)
            gcd_val = gcd(numerator, denominator)
            if gcd_val == 1:
                if numerator < denominator:
                    return _("The result cannot be simplified further.")
                else:
                    numerator //= gcd_val
                    denominator //= gcd_val
                    return _(
                        "Since the answer is an improper fraction, we can simplify it into the mixed number ${}\\frac{{{}}}{{{}}}$"
                    ).format(numerator // denominator, numerator - numerator // denominator * denominator,
                             denominator)
            res = _(
                "The result can be simplified. When we divide both {} and {} by their greatest common divisor {}, we get {} and {}, respectively."
            ).format(numerator, denominator, gcd_val, numerator // gcd_val, denominator // gcd_val)
            if numerator > denominator:
                numerator //= gcd_val
                denominator //= gcd_val
                res += _(
                    " Since the answer is an improper fraction, we can simplify it into the mixed number ${}\\frac{{{}}}{{{}}}$"
                ).format(numerator // denominator, numerator - numerator // denominator * denominator, denominator)
            return res

        def simplifyAlgebra(numerator, denominator):
            numerator = int(numerator)
            gcd_val = gcd(numerator, denominator)
            if gcd_val == 1:
                return ""
            res = _(
                "\\:\\:\\:\\longrightarrow    \\:\\: \\frac{{{}\\color {{Salmon}}\\div{}}}{{{}\\color {{Salmon}}\\div{}}} = \\frac{{\\color {{Salmon}}{}}}{{\\color {{Salmon}}{{{}}}}}"
            ).format(numerator, gcd_val, denominator, gcd_val, numerator // gcd_val, denominator // gcd_val)
            numerator //= gcd_val
            denominator //= gcd_val
            if numerator > denominator:
                res += _(
                    " = {{\\color {{Salmon}}{}}}\\frac{{\\color {{Salmon}}{}}}{{\\color {{Salmon}}{}}}"
                ).format(numerator // denominator, numerator - numerator // denominator * denominator, denominator)
            return res

        def finalAnswer(arg1, arg2, arg3, arg4):
            numerator = arg1 * arg4 - arg2 * arg3
            denominator = arg2 * arg4
            gcd_val = gcd(numerator, denominator)
            numerator //= gcd_val
            denominator //= gcd_val
            if numerator < denominator:
                return "\\frac{{{}}}{{{}}}".format(numerator, denominator)
            return "{}\\frac{{{}}}{{{}}}".format(numerator // denominator,
                                                 numerator - numerator // denominator * denominator, denominator)

        args['lcm'] = lcm_of2
        args['gcd'] = gcd
        args['LCMFraction'] = LCMFraction
        args['getNumerator'] = getNumerator
        args['subtractNumerators'] = subtractNumerators
        args['simplify'] = simplify
        args['simplifyAlgebra'] = simplifyAlgebra
        args['finalAnswer'] = finalAnswer

        return self.custom_format(template, **args)


# have to return fraction strings sometimes bc answers can be whole numbers of fractions
from flask_babel import _

class KnowledgePoint57Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def getVals(arg1, arg2, arg3, arg4, arg5, arg6, justFrac):
            if arg1 < 0:
                arg2 = -arg2
            if arg4 < 0:
                arg5 = -arg5
            denominator = arg3 * arg6
            numerator = (arg2 * arg6 + arg3 * arg5)
            if not justFrac:
                arg1 *= denominator
                arg4 *= denominator
                numerator = arg1 + arg4 + arg2 * arg6 + arg3 * arg5
            gcd_val = gcd(numerator, denominator)
            numerator //= gcd_val
            denominator //= gcd_val
            if denominator < 0:
                numerator = -numerator
                denominator = -denominator
            whole_num = abs(numerator) // denominator
            if numerator < 0:
                whole_num = -whole_num
            if abs(numerator) > denominator:
                if numerator < 0:
                    numerator = -(abs(numerator) % denominator)
                else:
                    if denominator != 1:
                        numerator %= denominator
            if denominator == 1:
                numerator = 0
            return numerator, denominator, whole_num

        def createText(numerator, denominator, whole_num):
            if denominator == 1:
                return _("{}").format(numerator + whole_num)
            if whole_num == 0:
                if numerator < 0:
                    return _("-\\frac{{{}}}{{{}}}").format(abs(numerator), denominator)
                return _("\\frac{{{}}}{{{}}}").format(abs(numerator), denominator)
            return _("{}\\frac{{{}}}{{{}}}").format(whole_num, abs(numerator), denominator)

        def getSign(arg4, arg5):
            if arg4 < 0:
                return "-"
            if arg5 < 0:
                return "-"
            return "+"

        def AddOrSubtract(arg):
            if arg > 0:
                return _("Add")
            return _("Subtract")

        def getAnswerFrac(arg1, arg2, arg3, arg4, arg5, arg6):
            numerator, denominator, whole_num = getVals(arg1, arg2, arg3, arg4, arg5, arg6, True)
            return createText(numerator, denominator, whole_num)

        def getAnswerFracAndSign(arg1, arg2, arg3, arg4, arg5, arg6):
            ansFrac = getAnswerFrac(arg1, arg2, arg3, arg4, arg5, arg6)
            if ansFrac[0] == '-':
                return _("- {}").format(ansFrac[1:])
            return _("+ {}").format(ansFrac)

        def getFinal(arg1, arg2, arg3, arg4, arg5, arg6):
            numerator, denominator, whole_num = getVals(arg1, arg2, arg3, arg4, arg5, arg6, False)
            return createText(numerator, denominator, whole_num)

        args['abs'] = abs
        args['getAnswerFracAndSign'] = getAnswerFracAndSign
        args['getSign'] = getSign
        args['AddOrSubtract'] = AddOrSubtract
        args['getAnswerFrac'] = getAnswerFrac
        args['getFinal'] = getFinal
        return self.custom_format(template, **args)


class KnowledgePoint58Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def getWholeNum(arg):
            arg = str(arg)
            return int(arg.replace('.', ''))

        def getDecimalPlaces(arg1, arg2):
            if isinstance(arg1, float):
                arg1 = str(arg1)
                idx = arg1.index('.')
                return len(arg1) - idx - 1
            arg2 = str(arg2)
            idx = arg2.index('.')
            return len(arg2) - idx - 1

        def getPlaces(num):
            res = SolutionGenerator.getRep(num) + ' '
            if num > 1:
                return res + _('places')
            return res + _('place')

        def getColor(num):
            if isinstance(num, int):
                return "{{\\color{{Salmon}}{}}}".format(num)
            num = str(num)
            idx = num.index('.')
            return num[:idx + 1] + "{{\\color{{Salmon}}{}}}".format(num[idx + 1:])

        def simplifyAnswer(ans):
            ans = str(ans)
            idx = ans.index('.') + 1
            for idx in range(idx, len(ans)):
                if ans[idx] != '0':
                    return ""
            alt = '{:g}'.format(float(ans))
            return _(" or $ {} $").format(alt)

        args['getWholeNum'] = getWholeNum
        args['getDecimalPlaces'] = getDecimalPlaces
        args['getPlaces'] = getPlaces
        args['getColor'] = getColor
        args['simplifyAnswer'] = simplifyAnswer
        return self.custom_format(template, **args)


class KnowledgePoint59Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:

        def getAnswer(arg1, arg2):
            return '{:g}'.format(float(arg1 / arg2))

        def getWholeNum(arg):
            arg = str(arg)
            return int(arg.replace('.', ''))

        def getDecimalPlaces(arg1):
            arg1 = str(arg1)
            idx = arg1.index('.')
            res = "\\:"
            for iter in range(idx):
                res += "\\:"
            res += "."
            return res

        def getSteps(arg1, arg2):
            res = ""
            arg1str = str(getWholeNum(arg1))
            oldcarry, carry = 0, 0
            ans = getAnswer(arg1, arg2)
            for step in range(3, (len(str(arg1)) + 2)):
                res += _("**Step {}:**").format(step)
                if step == 3:
                    res += _(" Start with {} divided by {}, ").format(arg1str[step - 3], arg2)
                else:
                    res += _(" Bring down {} ").format(arg1str[step - 3])
                if int(arg1str[step - 3]) + carry * 10 < arg1:
                    res += _("but {} does not divide {} so we write zero, and move to the right.\n$$\n").format(
                        arg2, arg1str[step - 3])
                    carry *= 10
                    carry += int(arg1str[step - 3])
                else:
                    res += _("so we get {} divided by {}").format(carry * 10 + int(arg1str[step - 3]), arg2)
                    if carry > 0:
                        res += _(" because we had a remainder in the prior step")
                    res += _(". {} divided by {} equals {}, so we write that down.\n$$\n").format(
                        carry * 10 + int(arg1str[step - 3]), arg2, (carry * 10 + int(arg1str[step - 3])) // arg2)
                    oldcarry = carry
                    carry -= ((carry * 10 + int(arg1str[step - 3])) // arg2)
                if '.' in ans[0:step - 2]:
                    res += "\\:" * (len(ans[0:step - 2]) - 1)
                    res += "{}\\\\".format(ans[0:step - 2])
                else:
                    res += "\\:" * (len(ans[0:step - 2]))
                    res += "{}".format(ans[0:step - 2])
                    res += "\\:" * 2 * (ans.index('.') - step)
                    res += ".\\\\"
                res += "\n{{{}}}{{\\overline{{\\smash{{\\big)}}\\,{{{}}}\\phantom{{)}}}}}}\\\\\n".format(arg2, arg1str)
                if step == 3:
                    res += "$$\n"
                else:
                    for iter in range(4, step + 1):
                        res += "\\:" * (iter - 4) * 5
                        res += "\\underline{{-{}\\:\\:}}\\\\\n".format(
                            (int(arg1str[iter - 3]) + oldcarry * 10) // 9 * 9)
                        oldcarry -= ((oldcarry * 10 + int(arg1str[iter - 3])) // arg1)
                        oldcarry *= 10
                        if iter - 2 < len(arg1str):
                            oldcarry += int(arg1str[iter - 2])
                        res += "\\:\\:\\:\\:\\:\\:\\:"
                        res += "\\:" * (iter - 4)
                        res += "{}\\\\".format(oldcarry)
                    res += "\n$$\n"
            return res

        args['getWholeNum'] = getWholeNum
        args['getDecimalPlaces'] = getDecimalPlaces
        args['getSteps'] = getSteps
        args['getAnswer'] = getAnswer

        return self.custom_format(template, **args)

class KnowledgePoint60Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def getSide(arg1, side):
            res = str(arg1)
            if side == 1:
                return res[0:res.index('.')]
            return res[res.index('.') + 1:len(res)]

        def getPlaces(arg2):
            if arg2 == 1:
                return _("place")
            return _("places")

        def getAnswer(arg1, arg2):
            return str(arg1 * arg2)

        def calculate_digit_word(arg1):
            return SolutionGenerator.getRep(len(str(arg1)) - 1)

        args['getAnswer'] = getAnswer
        args['getRep'] = SolutionGenerator.getRep
        args['calculate_digit_word'] = calculate_digit_word
        args['getSide'] = getSide
        args['getPlaces'] = getPlaces
        return self.custom_format(template, **args)


class KnowledgePoint61Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def getSide(arg1, side):
            res = str(arg1)
            if side == 1:
                return res[0:res.index('.')]
            return res[res.index('.') + 1:len(res)]

        def calculate_digit_word(arg1):
            return SolutionGenerator.getRep(len(str(arg1)) - 1)

        def getPlaces(arg2):
            if arg2 == 1:
                return _("place")
            return _("places")

        def getAnswer(arg1, arg2):
            res = arg1 / arg2
            return res

        args['getAnswer'] = getAnswer
        args['getRep'] = SolutionGenerator.getRep
        args['getSide'] = getSide
        args['calculate_digit_word'] = calculate_digit_word
        args['getPlaces'] = getPlaces
        return self.custom_format(template, **args)


class KnowledgePoint62Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def getWholeNum(arg):
            arg = str(arg)
            return int(arg.replace('.', ''))

        def getDecimalPlaces(arg1, arg2):
            arg1 = str(arg1)
            idx1 = arg1.index('.')
            arg2 = str(arg2)
            idx2 = arg2.index('.')
            return (len(arg1) - idx1 - 1) + (len(arg2) - idx2 - 1)

        def getPlaces(num):
            res = SolutionGenerator.getRep(num) + ' '
            if num > 1:
                return res + _('places')
            return res + _('place')

        def getColor(num):
            if isinstance(num, int):
                return "{{\\color{{Salmon}}{}}}".format(num)
            num = str(num)
            idx = num.index('.')
            return num[:idx + 1] + "{{\\color{{Salmon}}{}}}".format(num[idx + 1:])

        def simplifyAnswer(ans):
            ans = str(ans)
            idx = ans.index('.') + 1
            for idx in range(idx, len(ans)):
                if ans[idx] != '0':
                    return ""
            alt = '{:g}'.format(float(ans))
            return _(" or $ {} $").format(alt)

        args['getWholeNum'] = getWholeNum
        args['getDecimalPlaces'] = getDecimalPlaces
        args['getPlaces'] = getPlaces
        args['getColor'] = getColor
        args['simplifyAnswer'] = simplifyAnswer
        args['round'] = round
        return self.custom_format(template, **args)


class KnowledgePoint64Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        args['arg1'] = ",".join(args['arg1'])

        def getSummationEquation(arg1):
            lst = arg1.split(",")
            nums = [int(num) for num in lst]
            res = lst[0]
            for num in nums[1:]:
                res += _(" + {}").format(num)
            res += _(" = {}").format(sum(nums))
            return res

        def getNumbers(arg1):
            nums = arg1.split(",")
            if len(nums) > 1:
                return _("are {} numbers").format(len(nums))
            return _("is 1 number")

        def mean(arg1, usage=1):
            lst = arg1.split(",")
            nums = [int(num) for num in lst]
            if usage == 1:
                return _("{} \\div {} = {}").format(sum(nums), len(nums), sum(nums) // len(nums))
            return sum(nums) // len(nums)

        args['mean'] = mean
        args['getSummationEquation'] = getSummationEquation
        args['getNumbers'] = getNumbers
        return self.custom_format(template, **args)


from flask_babel import _


class KnowledgePoint65Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        args['arg1'] = ",".join(args['arg1'])

        def getList(arg1):
            nums = arg1.split(",")
            nums.sort()
            lst = [int(num) for num in nums]
            res = ""
            for num in lst[:len(lst) - 1]:
                res += str(int(num)) + ","
            return res + str(int(lst[len(lst) - 1]))

        def getHighlightedMedian(arg1):
            nums = arg1.split(",")
            nums.sort()
            lst = [int(num) for num in nums]
            res = ""
            if len(lst) % 2 == 1:
                for i in range(len(lst) - 1):
                    if i == len(lst) // 2:
                        res += _("{\\color{salmon}%s},") % str(lst[i])
                    else:
                        res += str(int(lst[i])) + ", "
                return res + str(int(lst[len(lst) - 1]))
            for i in range(len(lst) - 1):
                if i == len(lst) // 2 or i == len(lst) // 2 - 1:
                    res += _("{\\color{salmon}%s},") % str(lst[i])
                else:
                    res += str(int(lst[i])) + ","
            return res + str(int(lst[len(lst) - 1]))

        def getPositionStatement(arg1):
            nums = arg1.split(",")
            lst = [int(num) for num in nums]
            if len(lst) % 2 == 1:
                return _("In this case, the middle number is at position %s.") % (len(lst) // 2 + 1)
            return _("In this case, the middle numbers are at positions %s and %s.") % (
            len(lst) // 2, len(lst) // 2 + 1)

        def getStatementForEven(arg1):
            nums = arg1.split(",")
            nums.sort()
            lst = [int(num) for num in nums]
            if len(lst) % 2 == 1:
                return ""
            return _(
                "Because the list is of even length, we must take the mean of the two middle numbers, %s and %s. The mean of %s and %s is %s.") % (
                lst[len(lst) // 2 - 1], lst[len(lst) // 2], lst[len(lst) // 2 - 1], lst[len(lst) // 2],
                '{:g}'.format(float((lst[len(lst) // 2 - 1] + lst[len(lst) // 2]) / 2)))

        def getAnswer(arg1):
            nums = arg1.split(",")
            lst = [int(num) for num in nums]
            med = median(lst)
            return '{:g}'.format(float(med))

        args['len'] = len
        args['getList'] = getList
        args['getHighlightedMedian'] = getHighlightedMedian
        args['getPositionStatement'] = getPositionStatement
        args['getStatementForEven'] = getStatementForEven
        args['getAnswer'] = getAnswer
        return self.custom_format(template, **args)


class KnowledgePoint66Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        args['arg1'] = ",".join(args['arg1'])

        def strmode(arg1):
            lst = arg1.split(",")
            nums = [int(num) for num in lst]
            return mode(nums)

        def getList(arg1):
            lst = arg1.split(",")
            nums = [int(num) for num in lst]
            nums.sort()
            res = "{}".format(nums[0])
            for num in nums[1:]:
                res += _(", %s") % num
            return res

        def getHighlightedOccurences(arg1):
            nums = arg1.split(",")
            lst = [int(num) for num in nums]
            res = ""
            val = mode(lst)
            for num in lst[:len(lst) - 1]:
                if num == val:
                    res += _("{\\color{salmon}%s}, ") % str(num)
                else:
                    res += str(num) + ", "
            if lst[-1] == val:
                res += _("{\\color{salmon}%s}") % str(val)
            else:
                res += str(lst[-1])
            return res

        args['mode'] = strmode
        args['getList'] = getList
        args['getHighlightedOccurences'] = getHighlightedOccurences
        return self.custom_format(template, **args)


class KnowledgePoint67Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def getAlternateName(arg1, arg2):
            if arg2 == 2:
                return _("or \"%s squared\"") % SolutionGenerator.getRep(arg1)
            elif arg2 == 3:
                return _("or \"%s cubed\"") % SolutionGenerator.getRep(arg1)
            return ""

        def getExpanded(arg1, arg2):
            if arg2 == 0:
                return "1"
            res = str(arg1)
            for iter in range(1, arg2):
                res += _("×%s") % str(arg1)
            return res

        args['getRep'] = SolutionGenerator.getRep
        args["getExpanded"] = getExpanded
        args["getAlternateName"] = getAlternateName
        return self.custom_format(template, **args)

class KnowledgePoint68Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def evalSelf(arg1):
            print(arg1)
            arg1 = arg1.replace('^', '**')
            arg1 = arg1.replace('/', '//')
            return str(eval(arg1))

        def getExpression(arg1):
            res = ""
            for char in arg1:
                if char == '*':
                    res += "\\times"
                elif char == '/':
                    res += "\\div"
                else:
                    res += char
            return res

        def getSteps(arg1):
            res = ""
            step = 1
            parenthesis = ''
            parenthesisOperations = 0
            if '(' in arg1:
                parenthesis = arg1[arg1.index('('):arg1.index(')') + 1]
                parenthesisOperations = parenthesis.count('+') + parenthesis.count('-') + parenthesis.count(
                    '*') + parenthesis.count('/') + parenthesis.count('^')

            # Localized string using Flask-Babel
            res += _(
                "**Step 1:** Based on the **Order of Operations**, we evaluate the equation inside the parenthesis first.")

            if parenthesisOperations == 0:
                res += _("In this case, there are no parenthesis.\n\n")
                step += 1
            else:
                step += 1
                res += "\n$$\n"
                res += getExpression(parenthesis) + "\n$$\n"
                res += _("**Step %s:** We now check for exponents within the parenthesis. ") % step
                count = parenthesis.count('^')
                if count == 0:
                    res += _("In this case there are no exponents within the parenthesis.\n\n")
                else:
                    if count == 1:
                        res += _("In this case there is 1 exponent within the parenthesis. ")
                    else:
                        res += _("In this case there are %s exponents within the parenthesis. ") % count
                    res += "\n$$\n" + getExpression(arg1)
                    res += " = "
                    oldparenthesis = parenthesis
                    for iter in range(count):
                        idx = parenthesis.index('^')
                        lower, higher = idx - 1, idx + 1
                        while lower >= 0 and parenthesis[lower].isdigit():
                            lower -= 1
                        while higher < len(parenthesis) and parenthesis[higher].isdigit():
                            higher += 1
                        subequation = parenthesis[lower + 1:higher]
                        idx = subequation.index('^')
                        parenthesis = parenthesis.replace(subequation, str(int(subequation[0:idx]) ** int(
                            subequation[idx + 1:len(subequation)])), 1)
                    arg1 = arg1.replace(oldparenthesis, parenthesis)
                    res += getExpression(arg1) + "\n$$\n"
                step += 1
                res += _(
                    "**Step %s:** We now check for multiplication and division operations within the parenthesis. ") % step
                countm, countd = parenthesis.count('*'), parenthesis.count('/')
                if countm + countd == 0:
                    res += _(
                        "In this case there are no multiplication or division operations within the parenthesis.\n\n")
                else:
                    res += _(
                        "In this case there are %s multiplication and %s division operations within the parenthesis and we go from left to right.") % (
                           countm, countd)
                    res += "\n$$\n" + getExpression(arg1)
                    res += " = "
                    oldparenthesis = parenthesis
                    for iter in range(countm + countd):
                        idxm = 100
                        idxd = 100
                        if '*' in parenthesis:
                            idxm = parenthesis.index('*')
                        if '/' in parenthesis:
                            idxd = parenthesis.index('/')
                        idx = min(idxm, idxd)
                        lower, higher = idx - 1, idx + 1
                        while lower >= 0 and parenthesis[lower].isdigit():
                            lower -= 1
                        while higher < len(parenthesis) and parenthesis[higher].isdigit():
                            higher += 1
                        subequation = parenthesis[lower + 1:higher]
                        if idx == idxm:
                            idx = subequation.index('*')
                            parenthesis = parenthesis.replace(subequation, str(int(subequation[0:idx]) * int(
                                subequation[idx + 1:len(subequation)])), 1)
                        else:
                            idx = subequation.index('/')
                            parenthesis = parenthesis.replace(subequation, str(int(subequation[0:idx]) // int(
                                subequation[idx + 1:len(subequation)])), 1)
                    arg1 = arg1.replace(oldparenthesis, parenthesis, 1)
                    res += getExpression(arg1) + "\n$$\n"
                step += 1
                res += _(
                    "**Step %s:** We now check for addition and subtraction operations within the parenthesis. ") % step
                counta, counts = parenthesis.count('+'), parenthesis.count('-')
                if counta + counts == 0:
                    res += _("In this case there are no addition or subtraction operations within the parenthesis.\n\n")
                else:
                    res += _(
                        "In this case there are %s addition and %s subtraction operations within the parenthesis and we go from left to right.") % (
                           counta, counts)
                    res += "\n$$\n" + getExpression(arg1)
                    res += " = "
                    oldparenthesis = parenthesis
                    for iter in range(counta + counts):
                        idxm = 100
                        idxd = 100
                        if '+' in parenthesis:
                            idxm = parenthesis.index('+')
                        if '-' in parenthesis:
                            idxd = parenthesis.index('-')
                        idx = min(idxm, idxd)
                        lower, higher = idx - 1, idx + 1
                        while lower >= 0 and parenthesis[lower].isdigit():
                            lower -= 1
                        while higher < len(parenthesis) and parenthesis[higher].isdigit():
                            higher += 1
                        subequation = parenthesis[lower + 1:higher]
                        parenthesis = parenthesis.replace(subequation, str(eval(subequation)), 1)
                    arg1 = arg1.replace(oldparenthesis, parenthesis, 1)
                    arg1 = arg1.replace('(', '')
                    arg1 = arg1.replace(')', '')
                    res += getExpression(arg1) + "\n$$\n"
                if '(' in arg1:
                    arg1 = arg1.replace('(', '')
                    arg1 = arg1.replace(')', '')
                step += 1
            res += _(
                "**Step %s**: Now that we've finished the operations within the parenthesis, we do operations outside of the parenthesis. Starting with exponents. ") % step
            count = arg1.count('^')
            if count == 0:
                res += _("In this case there are no exponents left.\n")
            else:
                if count == 1:
                    res += _("In this case there is 1 exponent operation left.")
                else:
                    res += _("In this case there are %s exponent operations left.") % count
                res += "\n$$\n" + getExpression(arg1)
                res += " = "
                for iter in range(count):
                    idx = arg1.index('^')
                    lower, higher = idx - 1, idx + 1
                    while lower >= 0 and arg1[lower].isdigit():
                        lower -= 1
                    while higher < len(arg1) and arg1[higher].isdigit():
                        higher += 1
                    subequation = arg1[lower + 1:higher]
                    idx = subequation.index('^')
                    arg1 = arg1.replace(subequation,
                                        str(int(subequation[0:idx]) ** int(subequation[idx + 1:len(subequation)])), 1)
                res += getExpression(arg1) + "\n$$\n"
            step += 1
            res += _("**Step %s:** We now check for multiplication and division operations. ") % step
            countm, countd = arg1.count('*'), arg1.count('/')
            if countm + countd == 0:
                res += _("In this case there are no multiplication or division operations left.\n\n")
            else:
                res += _(
                    "In this case there are %s multiplication and %s division operations and we go from left to right.") % (
                       countm, countd)
                res += "\n$$\n" + getExpression(arg1)
                res += " = "
                for iter in range(countm + countd):
                    idxm = 100
                    idxd = 100
                    if '*' in arg1:
                        idxm = arg1.index('*')
                    if '/' in arg1:
                        idxd = arg1.index('/')
                    idx = min(idxm, idxd)
                    lower, higher = idx - 1, idx + 1
                    while lower >= 0 and arg1[lower].isdigit():
                        lower -= 1
                    while higher < len(arg1) and arg1[higher].isdigit():
                        higher += 1
                    subequation = arg1[lower + 1:higher]
                    if idx == idxm:
                        idx = subequation.index('*')
                        arg1 = arg1.replace(subequation,
                                            str(int(subequation[0:idx]) * int(subequation[idx + 1:len(subequation)])),
                                            1)
                    else:
                        idx = subequation.index('/')
                        arg1 = arg1.replace(subequation,
                                            str(int(subequation[0:idx]) // int(subequation[idx + 1:len(subequation)])),
                                            1)
                res += getExpression(arg1) + "\n$$\n"
            step += 1
            res += _("**Step %s:** We now check for addition and subtraction operations. ") % step
            counta, counts = arg1.count('+'), arg1.count('-')
            if counta + counts == 0:
                res += _("In this case there are no addition or subtraction operations left.\n\n")
            else:
                res += _(
                    "In this case there are %s addition and %s subtraction operations and we go from left to right.") % (
                       counta, counts)
                res += "\n$$\n" + getExpression(arg1)
                res += " = "
                for iter in range(counta + counts):
                    idxm = 100
                    idxd = 100
                    if '+' in arg1:
                        idxm = arg1.index('+')
                    if '-' in arg1:
                        idxd = arg1.index('-')
                    idx = min(idxm, idxd)
                    lower, higher = idx - 1, idx + 1
                    while lower >= 0 and arg1[lower].isdigit():
                        lower -= 1
                    while higher < len(arg1) and arg1[higher].isdigit():
                        higher += 1
                    subequation = arg1[lower + 1:higher]
                    arg1 = arg1.replace(subequation, str(eval(subequation)), 1)

            return res + evalSelf(arg1) + "\n$$\n"

        args['eval'] = evalSelf
        args['getExpression'] = getExpression
        args['getSteps'] = getSteps
        return self.custom_format(template, **args)


class KnowledgePoint69Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        self.signs = {'x': '\\times', '/': '\\div'}
        self.step = 2

        def getEquation(arg1, arg2, arg3, arg4, arg5, arg6, sign1, sign2, convert=False):
            sign1 = self.signs[sign1]
            sign2 = self.signs[sign2]
            if convert:
                if sign1 == '\\div':
                    arg3, arg4 = arg4, arg3
                    sign1 = '\\times'
                if sign2 == '\\div':
                    sign2 = '\\times'
                    arg5, arg6 = arg6, arg5

            frac1 = "\\frac{{{}}}{{{}}}".format(arg1, arg2)
            frac2 = "\\frac{{{}}}{{{}}}".format(arg3, arg4)
            frac3 = "\\frac{{{}}}{{{}}}".format(arg5, arg6)
            if arg2 == 1:
                frac1 = arg1
            if arg4 == 1:
                frac2 = arg3
            if arg6 == 1:
                frac3 = arg5
            return _("{} {} {} {} {}").format(frac1, sign1, frac2, sign2, frac3)

        def getStep(numerator, denominator, gcd_val, arg1, arg2, arg3, arg4, arg5, arg6, sign1, sign2):
            res = _(
                "The numerator in the {} fraction and the denominator in the {} fraction have a greatest common divisor of {}. We divide these two numbers by {}.\n$$\n"
            ).format(numerator, denominator, gcd_val, gcd_val)

            revert = (arg1, arg2, arg3, arg4, arg5, arg6)
            if numerator == 'first':
                arg1 = "{}\\div{{\\color{{Salmon}}{{{}}}}}".format(arg1, gcd_val)
            elif numerator == 'second':
                arg3 = "{}\\div{{\\color{{Salmon}}{{{}}}}}".format(arg3, gcd_val)
            elif numerator == 'third':
                arg5 = "{}\\div{{\\color{{Salmon}}{{{}}}}}".format(arg5, gcd_val)
            if denominator == 'first':
                arg2 = "{}\\div{{\\color{{Salmon}}{{{}}}}}".format(arg2, gcd_val)
            elif denominator == 'second':
                arg4 = "{}\\div{{\\color{{Salmon}}{{{}}}}}".format(arg4, gcd_val)
            elif denominator == 'third':
                arg6 = "{}\\div{{\\color{{Salmon}}{{{}}}}}".format(arg6, gcd_val)

            res += getEquation(arg1, arg2, arg3, arg4, arg5, arg6, sign1, sign2, True) + " = "
            arg1, arg2, arg3, arg4, arg5, arg6 = revert

            if numerator == 'first':
                arg1 = "{{\\color{{Salmon}}{{{}}}}}".format(arg1 // gcd_val)
            elif numerator == 'second':
                arg3 = "{{\\color{{Salmon}}{{{}}}}}".format(arg3 // gcd_val)
            elif numerator == 'third':
                arg5 = "{{\\color{{Salmon}}{{{}}}}}".format(arg5 // gcd_val)
            if denominator == 'first':
                arg2 = "{{\\color{{Salmon}}{{{}}}}}".format(arg2 // gcd_val)
            elif denominator == 'second':
                arg4 = "{{\\color{{Salmon}}{{{}}}}}".format(arg4 // gcd_val)
            elif denominator == 'third':
                arg6 = "{{\\color{{Salmon}}{{{}}}}}".format(arg6 // gcd_val)

            res += getEquation(arg1, arg2, arg3, arg4, arg5, arg6, sign1, sign2, True)
            return res + "\n$$\n"

        def getFinalAnswer(arg1, arg2, arg3, arg4, arg5, arg6, sign1, sign2):
            if sign1 == '/':
                arg3, arg4 = arg4, arg3
            if sign2 == '/':
                arg5, arg6 = arg6, arg5
            numerator = arg1 * arg3 * arg5
            denominator = arg2 * arg4 * arg6
            gcd_val = gcd(numerator, denominator)
            numerator //= gcd_val
            denominator //= gcd_val
            if numerator > denominator:
                return "{}\\frac{{{}}}{{{}}}".format(numerator // denominator,
                                                     numerator - numerator // denominator * denominator, denominator)
            return "\\frac{{{}}}{{{}}}".format(numerator, denominator)

        def getSteps(arg1, arg2, arg3, arg4, arg5, arg6, sign1, sign2):
            if sign1 == '/':
                arg3, arg4 = arg4, arg3
                sign1 = 'x'
            if sign2 == '/':
                arg5, arg6 = arg6, arg5
                sign2 = 'x'

            gcds = [gcd(arg2, arg3), gcd(arg2, arg5), gcd(arg4, arg1), gcd(arg4, arg5),
                    gcd(arg6, arg1), gcd(arg6, arg3), gcd(arg1, arg2), gcd(arg3, arg4), gcd(arg5, arg6)]

            fracnum = {0: ('second', 'first'), 1: ('third', 'first'), 2: ('first', 'second'),
                       3: ('third', 'second'), 4: ('first', 'third'), 5: ('second', 'third'),
                       6: ('first', 'first'), 7: ('second', 'second'), 8: ('third', 'third'), }

            res = ""
            for i in range(6):
                if gcds[i] != 1:
                    if self.step != 2:
                        res += _("**Step {}:**  ").format(self.step)
                    n, d = fracnum[i]
                    res += getStep(n, d, gcds[i], arg1, arg2, arg3, arg4, arg5, arg6, sign1, sign2)
                    if n == 'first':
                        arg1 = arg1 // gcds[i]
                    elif n == 'second':
                        arg3 = arg3 // gcds[i]
                    elif n == 'third':
                        arg5 = arg5 // gcds[i]
                    if d == 'first':
                        arg2 = arg2 // gcds[i]
                    elif d == 'second':
                        arg4 = arg4 // gcds[i]
                    elif d == 'third':
                        arg6 = arg6 // gcds[i]
                    self.step += 1

            res += _(
                "**Step {}:** Now all fractions have been simplified to their lowest terms, multiply them.\n$$\n").format(
                self.step)
            res += getEquation(arg1, arg2, arg3, arg4, arg5, arg6, sign1, sign2, True) + " = "
            res += getFinalAnswer(arg1, arg2, arg3, arg4, arg5, arg6, sign1, sign2) + "\n$$"
            return res

        args['gcd'] = gcd
        args['getRep'] = SolutionGenerator.getRep
        args['getEquation'] = getEquation
        args['getStep'] = getStep
        args['getFinalAnswer'] = getFinalAnswer
        args['getSteps'] = getSteps
        return self.custom_format(template, **args)


class KnowledgePoint70Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def getAnswer(arg1, arg2, arg3, arg4, arg5, arg6, usage):
            d = lcm(arg2, arg4, arg6)
            arg1 *= d // arg2
            arg3 *= d // arg4
            arg5 *= d // arg6
            n = arg1 + arg3 + arg5
            gcd_val = gcd(n, d)
            if gcd_val == 1 and usage == 1:
                return ""
            res = ""
            if usage == 1:
                res += " = "
            n //= gcd_val
            d //= gcd_val
            if n < d:
                return res + "\\frac{{{}}}{{{}}}".format(n, d)
            return res + "{}\\frac{{{}}}{{{}}}".format(n // d, n - n // d * d, d)
        args['gcd'] = gcd
        args['lcm'] = lcm
        args['lcm_of_three'] = lcm(args.get('arg2'), args.get('arg4'), args.get('arg6'))
        args['getAnswer'] = getAnswer
        return self.custom_format(template, **args)


class KnowledgePoint71Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def getAnswer(arg1, arg2, arg3, arg4, arg5, arg6, sign1, sign2, usage):
            if sign1 == '-':
                arg3 = -arg3
            if sign2 == '-':
                arg5 = -arg5
            d = lcm(arg2, arg4, arg6)
            arg1 *= d // arg2
            arg3 *= d // arg4
            arg5 *= d // arg6
            n = arg1 + arg3 + arg5
            gcd_val = gcd(n, d)
            res = ""
            sign = ""
            if n < 0:
                sign = "-"
                n = -n
            if usage == 1:
                res += " = {}\\frac{{{}}}{{{}}}".format(sign, n, d)
                if gcd_val == 1 and n < d:
                    return res
                if n % d == 0:
                    res += " = {}{}".format(sign, n // d)
                    return res
                n //= gcd_val
                d //= gcd_val
                whole_num = ""
                if n > d:
                    whole_num = "{}".format(n // d)
                res += " = {}{}\\frac{{{}}}{{{}}}".format(sign, whole_num, n - n // d * d, d)
                return res
            n //= gcd_val
            d //= gcd_val
            if n < d:
                return "{}\\frac{{{}}}{{{}}}".format(sign, n, d)
            return "{}{}\\frac{{{}}}{{{}}}".format(sign, n // d, n - n // d * d, d)

        args['gcd'] = gcd
        args['lcm'] = lcm
        args['getAnswer'] = getAnswer
        return self.custom_format(template, **args)

class KnowledgePoint72Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        self.answer = 0

        def getAnswer():
            return self.answer

        def getVals(arg):
            idx = arg.index('|')
            return arg[1:idx], arg[idx + 1:len(arg) - 1]

        def getExpression(arg1):
            res = ""
            nums = re.findall(r'\[.*?\]', arg1)
            nums = [getVals(num) for num in nums]
            ops = []
            withinbraces = False
            for char in arg1:
                if char == '[':
                    withinbraces = True
                elif char == ']':
                    withinbraces = False
                if not withinbraces and char in ['-', '*', '+', '/', '^', '(', ')']:
                    ops.append(char)
            ops_idx = 0
            for i in range(len(ops)):
                if ops[i] == '*':
                    ops[i] = '\\times'
                if ops[i] == '/':
                    ops[i] = '\\div'
            for numerator, denominator in nums:
                if ops_idx < len(ops):
                    if ops[ops_idx] == '(':
                        res += '('
                        ops_idx += 1
                res += '\\frac{{{}}}{{{}}}'.format(numerator, denominator)
                if ops_idx < len(ops):
                    res += ops[ops_idx]
                    if ops[ops_idx] == ')':
                        ops_idx += 1
                        if ops_idx < len(ops):
                            res += ops[ops_idx]
                    ops_idx += 1
            return res

        def getSteps(arg1):
            res = ""
            step = 1
            parenthesis = ''
            parenthesisOperations = 0
            if '(' in arg1:
                parenthesis = arg1[arg1.index('('):arg1.index(')') + 1]
                parenthesisOperations = parenthesis.count('+') + parenthesis.count('-') + parenthesis.count(
                    '*') + parenthesis.count('/') + parenthesis.count('^')
            res += _(
                "**Step 1:** Based on the **Order of Operations**, we evaluate the equation inside the parenthesis first.")
            if parenthesisOperations == 0:
                res += _("In this case, there are no parenthesis.\n\n")
                step += 1
            else:
                step += 1
                res += "\n$$\n"
                res += getExpression(parenthesis) + "\n$$\n"
                res += _("**Step {}:** We now check for exponents within the parenthesis.").format(step)
                res += _("In this case, there are no exponents within the parenthesis.\n\n")
                step += 1
                res += _(
                    "**Step {}:** We now check for multiplication and division operations within the parenthesis.").format(
                    step)
                countm, countd = parenthesis.count('*'), parenthesis.count('/')
                if countm + countd == 0:
                    res += _(
                        "In this case, there are no multiplication or division operations within the parenthesis.\n\n")
                else:
                    res += _(
                        "In this case, there are {} multiplication and {} division operations within the parenthesis, and we simplify them left to right.").format(
                        countm, countd)
                    res += "\n$$\n" + getExpression(arg1) + " = "
                    oldparenthesis = parenthesis
                    unsimplified, simplifystatement = parenthesis, parenthesis
                    needtosimplify = False
                    for iter in range(countm + countd):
                        idxm = 100
                        idxd = 100
                        if '*' in parenthesis:
                            idxm = parenthesis.index('*')
                        if '/' in parenthesis:
                            idxd = parenthesis.index('/')
                        idx = min(idxm, idxd)
                        lower, higher = idx - 1, idx + 1
                        while lower >= 0 and parenthesis[lower] != '[':
                            lower -= 1
                        while higher < len(parenthesis) and parenthesis[higher] != ']':
                            higher += 1
                        subequation = parenthesis[lower:higher + 1]
                        if idx == idxm:
                            idx = subequation.index('*')
                            numerator1, denominator1 = getVals(subequation[0:idx])
                            numerator2, denominator2 = getVals(subequation[idx + 1:])
                            numerator1 = int(numerator1)
                            numerator2 = int(numerator2)
                            denominator1 = int(denominator1)
                            denominator2 = int(denominator2)
                            numerator1 *= numerator2
                            denominator1 *= denominator2
                            gcd_val = gcd(numerator1, denominator1)
                            replace1 = "[{}|{}]".format(numerator1, denominator1)
                            replace2 = _(
                                "[{}\\div{{\\color{{Salmon}}{{{}}}}}|{}\\div{{\\color{{Salmon}}{{{}}}}}]").format(
                                numerator1, gcd_val, denominator1, gcd_val)
                            if gcd_val != 1:
                                needtosimplify = True
                                unsimplified = unsimplified.replace(subequation, replace1, 1)
                                simplifystatement = simplifystatement.replace(subequation, replace2, 1)
                            numerator1 //= gcd_val
                            denominator1 //= gcd_val
                            replace = "[{}|{}]".format(numerator1, denominator1)
                            parenthesis = parenthesis.replace(subequation, replace, 1)
                        else:
                            idx = subequation.index('/')
                            numerator1, denominator1 = getVals(subequation[0:idx])
                            numerator2, denominator2 = getVals(subequation[idx + 1:])
                            numerator1 = int(numerator1)
                            numerator2 = int(numerator2)
                            denominator1 = int(denominator1)
                            denominator2 = int(denominator2)
                            numerator1 *= denominator2
                            denominator1 *= numerator2
                            gcd_val = gcd(numerator1, denominator1)
                            replace1 = "[{}|{}]".format(numerator1, denominator1)
                            replace2 = _(
                                "[{}\\div{{\\color{{Salmon}}{{{}}}}}|{}\\div{{\\color{{Salmon}}{{{}}}}}]").format(
                                numerator1, gcd_val, denominator1, gcd_val)
                            if gcd_val != 1:
                                needtosimplify = True
                                unsimplified = unsimplified.replace(subequation, replace1, 1)
                                simplifystatement = simplifystatement.replace(subequation, replace2, 1)
                            numerator1 //= gcd_val
                            denominator1 //= gcd_val
                            replace = "[{}|{}]".format(numerator1, denominator1)
                            parenthesis = parenthesis.replace(subequation, replace, 1)
                    if needtosimplify:
                        arg1 = arg1.replace(oldparenthesis, unsimplified, 1)
                        res += getExpression(arg1) + " = "
                        arg1 = arg1.replace(unsimplified, simplifystatement, 1)
                        res += getExpression(arg1) + " = "
                        arg1 = arg1.replace(simplifystatement, parenthesis, 1)
                    else:
                        arg1 = arg1.replace(oldparenthesis, parenthesis, 1)
                    res += getExpression(arg1) + "\n$$\n"
                step += 1
                res += _(
                    "**Step {}:** We now check for addition and subtraction operations within the parenthesis.").format(
                    step)
                counta, counts = parenthesis.count('+'), parenthesis.count('-')
                if counta + counts == 0:
                    res += _(
                        "In this case, there are no addition or subtraction operations within the parenthesis.\n\n")
                else:
                    res += _(
                        "In this case, there are {} addition and {} subtraction operations, and we simplify them from left to right.").format(
                        counta, counts)
                    res += "\n$$\n" + getExpression(arg1) + " = "
                    # Continue adding logic for addition/subtraction steps and simplification checks...

            # Further refactoring can be done for subsequent steps similarly

        args['getAnswer'] = getAnswer
        args['getExpression'] = getExpression
        args['getSteps'] = getSteps
        return self.custom_format(template, **args)

class KnowledgePoint73Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        self.answer = 0

        def getAnswer():
            return self.answer

        def getVals(arg):
            idx = arg.index('|')
            if '<' in arg:
                return arg[2:arg.index('>')], arg[arg.index('>') + 1:idx], arg[idx + 1:len(arg) - 1]
            return 0, arg[1:idx], arg[idx + 1:len(arg) - 1]

        def getExpression(arg1):
            res = ""
            nums = re.findall(r'\[.*?\]', arg1)
            nums = [getVals(num) for num in nums]
            ops = []
            withinbraces = False
            for char in arg1:
                if char == '[':
                    withinbraces = True
                elif char == ']':
                    withinbraces = False
                if not withinbraces and char in ['-', '*', '+', '/', '^', '(', ')']:
                    ops.append(char)
            ops_idx = 0
            for i in range(len(ops)):
                if ops[i] == '*':
                    ops[i] = '\\times'
                if ops[i] == '/':
                    ops[i] = '\\div'
            for wholenum, numerator, denominator in nums:
                if ops_idx < len(ops):
                    if ops[ops_idx] == '(':
                        res += '('
                        ops_idx += 1
                if wholenum != 0:
                    res += '{}\\frac{{{}}}{{{}}}'.format(wholenum, numerator, denominator)
                else:
                    res += '\\frac{{{}}}{{{}}}'.format(numerator, denominator)
                if ops_idx < len(ops):
                    res += ops[ops_idx]
                    if ops[ops_idx] == ')':
                        ops_idx += 1
                        if ops_idx < len(ops):
                            res += ops[ops_idx]
                    ops_idx += 1
            return res

        def getSteps(arg1):
            res = _("**Step 1:** First convert all mixed numbers into improper fractions.")
            if '<' not in arg1:
                res += _("In this case, there are no mixed numbers.\n\n")
            else:
                res += "\n$$\n" + getExpression(arg1) + _(" = ")
                nums = re.findall(r'\[.*?\]', arg1)
                nums = [num for num in nums if '<' in num]
                replace = [num for num in nums if '<' in num]
                for i in range(len(replace)):
                    num = replace[i]
                    idx = num.index('|')
                    denom = int(num[idx + 1:len(num) - 1])
                    numer = int(num[num.index('>') + 1:idx])
                    wholenum = int(num[2:num.index('>')])
                    numer += wholenum * denom
                    replace[i] = '[{}|{}]'.format(numer, denom)
                    arg1 = arg1.replace(nums[i], replace[i], 1)
                res += getExpression(arg1) + "\n$$\n\n"

            step = 2
            parenthesis = ''
            parenthesisOperations = 0
            if '(' in arg1:
                parenthesis = arg1[arg1.index('('):arg1.index(')') + 1]
                parenthesisOperations = parenthesis.count('+') + parenthesis.count('-') + parenthesis.count(
                    '*') + parenthesis.count('/') + parenthesis.count('^')
            res += _(
                "**Step 2:** Based on the **Order of Operations**, we evaluate the equation inside the parenthesis first. ")
            if parenthesisOperations == 0:
                res += _("In this case, there are no parenthesis.\n\n")
                step += 1
            else:
                step += 1
                res += "\n$$\n" + getExpression(parenthesis) + "\n$$\n"
                res += _("**Step {}:** We now check for exponents within the parenthesis. ").format(step)
                res += _("In this case there are no exponents within the parenthesis.\n\n")

                step += 1
                res += _(
                    "**Step {}:** We now check for multiplication and division operations within the parenthesis. ").format(
                    step)
                countm, countd = parenthesis.count('*'), parenthesis.count('/')
                if countm + countd == 0:
                    res += _(
                        "In this case there are no multiplication or division operations within the parenthesis.\n\n")
                else:
                    res += _(
                        "In this case there are {} multiplication and {} division operations within the parenthesis, and we go from left to right. Simplify at the end if possible. ").format(
                        countm, countd)
                    res += "\n$$\n" + getExpression(arg1) + " = "
                    unsimplified, simplifystatement, oldparenthesis = parenthesis, parenthesis, parenthesis
                    needtosimplify = False
                    for iter in range(countm + countd):
                        idxm = 100
                        idxd = 100
                        if '*' in parenthesis:
                            idxm = parenthesis.index('*')
                        if '/' in parenthesis:
                            idxd = parenthesis.index('/')
                        idx = min(idxm, idxd)
                        lower, higher = idx - 1, idx + 1
                        while lower >= 0 and parenthesis[lower] != '[':
                            lower -= 1
                        while higher < len(parenthesis) and parenthesis[higher] != ']':
                            higher += 1
                        subequation = parenthesis[lower:higher + 1]
                        if idx == idxm:
                            idx = subequation.index('*')
                            trash, numerator1, denominator1 = getVals(subequation[0:idx])
                            trash, numerator2, denominator2 = getVals(subequation[idx + 1:])
                            numerator1 = int(numerator1)
                            numerator2 = int(numerator2)
                            denominator1 = int(denominator1)
                            denominator2 = int(denominator2)
                            numerator1 *= numerator2
                            denominator1 *= denominator2
                            gcd_val = gcd(numerator1, denominator1)
                            replace1 = "[{}|{}]".format(numerator1, denominator1)
                            replace2 = ("[{}\\div{{\\color{{Salmon}}{{{}}}}}|{}\\div{{\\color{{Salmon}}{{{}}}}}]"
                                        .format(numerator1, gcd_val, denominator1, gcd_val))
                            if gcd_val != 1:
                                needtosimplify = True
                                unsimplified = unsimplified.replace(subequation, replace1, 1)
                                simplifystatement = simplifystatement.replace(subequation, replace2, 1)
                            numerator1 //= gcd_val
                            denominator1 //= gcd_val
                            replace = "[{}|{}]".format(numerator1, denominator1)
                            parenthesis = parenthesis.replace(subequation, replace, 1)
                        else:
                            idx = subequation.index('/')
                            trash, numerator1, denominator1 = getVals(subequation[0:idx])
                            trash, numerator2, denominator2 = getVals(subequation[idx + 1:])
                            numerator1 = int(numerator1)
                            numerator2 = int(numerator2)
                            denominator1 = int(denominator1)
                            denominator2 = int(denominator2)
                            numerator1 *= denominator2
                            denominator1 *= numerator2
                            gcd_val = gcd(numerator1, denominator1)
                            replace1 = "[{}|{}]".format(numerator1, denominator1)
                            replace2 = ("[{}\\div{{\\color{{Salmon}}{{{}}}}}|{}\\div{{\\color{{Salmon}}{{{}}}}}]"
                                        .format(numerator1, gcd_val, denominator1, gcd_val))
                            if gcd_val != 1:
                                needtosimplify = True
                                unsimplified = unsimplified.replace(subequation, replace1, 1)
                                simplifystatement = simplifystatement.replace(subequation, replace2, 1)
                            numerator1 //= gcd_val
                            denominator1 //= gcd_val
                            replace = "[{}|{}]".format(numerator1, denominator1)
                            parenthesis = parenthesis.replace(subequation, replace, 1)
                    if needtosimplify:
                        arg1 = arg1.replace(oldparenthesis, unsimplified, 1)
                        res += getExpression(arg1) + _(" = ")
                        arg1 = arg1.replace(unsimplified, simplifystatement, 1)
                        res += getExpression(arg1) + _(" = ")
                        arg1 = arg1.replace(simplifystatement, parenthesis, 1)
                    else:
                        arg1 = arg1.replace(oldparenthesis, parenthesis, 1)
                    res += getExpression(arg1) + "\n$$\n"

                step += 1
                res += _(
                    "**Step {}:** We now check for addition and subtraction operations within the parenthesis. ").format(
                    step)
                counta, counts = parenthesis.count('+'), parenthesis.count('-')
                if counta + counts == 0:
                    res += _(
                        "In this case, there are no addition or subtraction operations within the parenthesis.\n\n")
                else:
                    res += _(
                        "In this case there are {} addition and {} subtraction operations within the parenthesis, and we go from left to right. Simplify at the end if possible. ").format(
                        counta, counts)
                    res += "\n$$\n" + getExpression(arg1) + _(" = ")
                    oldparenthesis = parenthesis
                    middle, middle2 = arg1, arg1
                    unsimplified, simplifystatement = parenthesis, parenthesis
                    needtosimplify = False
                    for iter in range(counta + counts):
                        idxa = 100
                        idxs = 100
                        if '+' in parenthesis:
                            idxa = parenthesis.index('+')
                        if '-' in parenthesis:
                            idxs = parenthesis.index('-')
                        idx = min(idxa, idxs)
                        lower, higher = idx - 1, idx + 1
                        while lower >= 0 and parenthesis[lower] != '[':
                            lower -= 1
                        while higher < len(parenthesis) and parenthesis[higher] != ']':
                            higher += 1
                        subequation = parenthesis[lower:higher + 1]
                        if idx == idxa:
                            idx = subequation.index('+')
                            trash, numerator1, denominator1 = getVals(subequation[0:idx])
                            trash, numerator2, denominator2 = getVals(subequation[idx + 1:])
                            numerator1 = int(numerator1)
                            numerator2 = int(numerator2)
                            denominator1 = int(denominator1)
                            denominator2 = int(denominator2)
                            lcm_val = lcm_of2(denominator1, denominator2)
                            factor1 = lcm_val // denominator1
                            factor2 = lcm_val // denominator2
                            replace1 = (
                                "[{}\\times{{\\color{{Salmon}}{{{}}}}}|{}\\times{{\\color{{Salmon}}{{{}}}}}]+[{}\\times{{\\color{{Salmon}}{{{}}}}}|{}\\times{{\\color{{Salmon}}{{{}}}}}]"
                                .format(numerator1, factor1, denominator1, factor1, numerator2, factor2, denominator2,
                                        factor2))
                            middle = middle.replace(subequation, replace1, 1)
                            replace2 = ("[{}+{}|{}]"
                                        .format(numerator1 * factor1, numerator2 * factor2, lcm_val))
                            middle2 = middle2.replace(subequation, replace2, 1)
                            n = numerator1 * factor1 + numerator2 * factor2
                            gcd_val = gcd(n, lcm_val)
                            if gcd_val != 1:
                                needtosimplify = True
                                replace3 = "[{}|{}]".format(n, lcm_val)
                                unsimplified = unsimplified.replace(subequation, replace3, 1)
                                replacesimpstatement = (
                                    "[{}\\div{{\\color{{Salmon}}{{{}}}}}|{}\\div{{\\color{{Salmon}}{{{}}}}}]"
                                    .format(n, gcd_val, lcm_val, gcd_val))
                                simplifystatement = simplifystatement.replace(subequation, replacesimpstatement, 1)
                            numerator1 //= gcd_val
                            denominator1 //= gcd_val
                            replace = "[{}|{}]".format(n // gcd_val, lcm_val // gcd_val)
                            parenthesis = parenthesis.replace(subequation, replace, 1)
                        else:
                            idx = subequation.index('-')
                            trash, numerator1, denominator1 = getVals(subequation[0:idx])
                            trash, numerator2, denominator2 = getVals(subequation[idx + 1:])
                            numerator1 = int(numerator1)
                            numerator2 = int(numerator2)
                            denominator1 = int(denominator1)
                            denominator2 = int(denominator2)
                            lcm_val = lcm_of2(denominator1, denominator2)
                            factor1 = lcm_val // denominator1
                            factor2 = lcm_val // denominator2
                            replace1 = (
                                "[{}\\times{{\\color{{Salmon}}{{{}}}}}|{}\\times{{\\color{{Salmon}}{{{}}}}}]-[{}\\times{{\\color{{Salmon}}{{{}}}}}|{}\\times{{\\color{{Salmon}}{{{}}}}}]"
                                .format(numerator1, factor1, denominator1, factor1, numerator2, factor2, denominator2,
                                        factor2))
                            middle = middle.replace(subequation, replace1, 1)
                            replace2 = ("[{}-{}|{}]"
                                        .format(numerator1 * factor1, numerator2 * factor2, lcm_val))
                            middle2 = middle2.replace(subequation, replace2, 1)
                            n = numerator1 * factor1 - numerator2 * factor2
                            gcd_val = gcd(n, lcm_val)
                            if gcd_val != 1:
                                needtosimplify = True
                                replace3 = "[{}|{}]".format(n, lcm_val)
                                unsimplified = unsimplified.replace(subequation, replace3, 1)
                                replacesimpstatement = (
                                    "[{}\\div{{\\color{{Salmon}}{{{}}}}}|{}\\div{{\\color{{Salmon}}{{{}}}}}]"
                                    .format(n, gcd_val, lcm_val, gcd_val))
                                simplifystatement = simplifystatement.replace(subequation, replacesimpstatement, 1)
                            numerator1 //= gcd_val
                            denominator1 //= gcd_val
                            replace = "[{}|{}]".format(n // gcd_val, lcm_val // gcd_val)
                            parenthesis = parenthesis.replace(subequation, replace, 1)
                    arg1 = arg1.replace(oldparenthesis, parenthesis, 1)
                    arg1 = arg1.replace('(', '')
                    arg1 = arg1.replace(')', '')
                    res += getExpression(middle) + _(" = ")
                    res += getExpression(middle2) + _(" = ")
                    if needtosimplify:
                        arg1 = arg1.replace(middle2, unsimplified, 1)
                        res += getExpression(arg1) + _(" = ")
                        arg1 = arg1.replace(unsimplified, simplifystatement, 1)
                        res += getExpression(arg1) + _(" = ")
                        arg1 = arg1.replace(simplifystatement, parenthesis, 1)
                    else:
                        arg1 = arg1.replace(middle2, parenthesis, 1)
                    res += getExpression(arg1) + "\n$$\n"

            step += 1
            res += _(
                "**Step {}:** Now that we've finished the operations within the parenthesis, we do operations outside of the parenthesis. Starting with exponents. ").format(
                step)
            count = arg1.count('^')
            res += _("In this case there are no exponents left.\n\n")

            step += 1
            res += _("**Step {}:** We now check for multiplication and division operations. ").format(step)
            countm, countd = arg1.count('*'), arg1.count('/')
            if countm + countd == 0:
                res += _("In this case there are no multiplication or division operations left.\n\n")
            else:
                res += _(
                    "In this case there are {} multiplication and {} division operations, and we go from left to right. Simplify at the end if possible. ").format(
                    countm, countd)
                res += "\n$$\n" + getExpression(arg1) + _(" = ")
                unsimplified, simplifystatement = arg1, arg1
                needtosimplify = False
                for iter in range(countm + countd):
                    idxm = 100
                    idxd = 100
                    if '*' in arg1:
                        idxm = arg1.index('*')
                    if '/' in arg1:
                        idxd = arg1.index('/')
                    idx = min(idxm, idxd)
                    lower, higher = idx - 1, idx + 1
                    while lower >= 0 and arg1[lower] != '[':
                        lower -= 1
                    while higher < len(arg1) and arg1[higher] != ']':
                        higher += 1
                    subequation = arg1[lower:higher + 1]
                    if idx == idxm:
                        idx = subequation.index('*')
                        trash, numerator1, denominator1 = getVals(subequation[0:idx])
                        trash, numerator2, denominator2 = getVals(subequation[idx + 1:])
                        numerator1 = int(numerator1)
                        numerator2 = int(numerator2)
                        denominator1 = int(denominator1)
                        denominator2 = int(denominator2)
                        numerator1 *= numerator2
                        denominator1 *= denominator2
                        gcd_val = gcd(numerator1, denominator1)
                        replace1 = "[{}|{}]".format(numerator1, denominator1)
                        replace2 = ("[{}\\div{{\\color{{Salmon}}{{{}}}}}|{}\\div{{\\color{{Salmon}}{{{}}}}}]"
                                    .format(numerator1, gcd_val, denominator1, gcd_val))
                        if gcd_val != 1:
                            needtosimplify = True
                            unsimplified = unsimplified.replace(subequation, replace1, 1)
                            simplifystatement = simplifystatement.replace(subequation, replace2, 1)
                        numerator1 //= gcd_val
                        denominator1 //= gcd_val
                        replace = "[{}|{}]".format(numerator1, denominator1)
                        arg1 = arg1.replace(subequation, replace, 1)
                    else:
                        idx = subequation.index('/')
                        trash, numerator1, denominator1 = getVals(subequation[0:idx])
                        trash, numerator2, denominator2 = getVals(subequation[idx + 1:])
                        numerator1 = int(numerator1)
                        numerator2 = int(numerator2)
                        denominator1 = int(denominator1)
                        denominator2 = int(denominator2)
                        numerator1 *= denominator2
                        denominator1 *= numerator2
                        gcd_val = gcd(numerator1, denominator1)
                        replace1 = "[{}|{}]".format(numerator1, denominator1)
                        replace2 = ("[{}\\div{{\\color{{Salmon}}{{{}}}}}|{}\\div{{\\color{{Salmon}}{{{}}}}}]"
                                    .format(numerator1, gcd_val, denominator1, gcd_val))
                        if gcd_val != 1:
                            needtosimplify = True
                            unsimplified = unsimplified.replace(subequation, replace1, 1)
                            simplifystatement = simplifystatement.replace(subequation, replace2, 1)
                        numerator1 //= gcd_val
                        denominator1 //= gcd_val
                        replace = "[{}|{}]".format(numerator1, denominator1)
                        arg1 = arg1.replace(subequation, replace, 1)
                if needtosimplify:
                    res += getExpression(unsimplified) + _(" = ")
                    res += getExpression(simplifystatement) + _(" = ")
                res += getExpression(arg1) + "\n$$\n"

            step += 1
            res += _("**Step {}:** We now check for addition and subtraction operations. ").format(step)
            counta, counts = arg1.count('+'), arg1.count('-')
            if counta + counts == 0:
                res += _("In this case there are no addition or subtraction operations left.\n\n")
            else:
                res += _(
                    "In this case there are {} addition and {} subtraction operations, and we go from left to right. ").format(
                    counta, counts)
                res += "\n$$\n" + getExpression(arg1) + _(" = ")
                middle, middle2, unsimplified, simplifystatement = arg1, arg1, arg1, arg1
                needtosimplify = False
                for iter in range(counta + counts):
                    idxa = 100
                    idxs = 100
                    if '+' in arg1:
                        idxa = arg1.index('+')
                    if '-' in arg1:
                        idxs = arg1.index('-')
                    idx = min(idxa, idxs)
                    lower, higher = idx - 1, idx + 1
                    while lower >= 0 and arg1[lower] != '[':
                        lower -= 1
                    while higher < len(arg1) and arg1[higher] != ']':
                        higher += 1
                    subequation = arg1[lower:higher + 1]
                    if idx == idxa:
                        idx = subequation.index('+')
                        trash, numerator1, denominator1 = getVals(subequation[0:idx])
                        trash, numerator2, denominator2 = getVals(subequation[idx + 1:])
                        numerator1 = int(numerator1)
                        numerator2 = int(numerator2)
                        denominator1 = int(denominator1)
                        denominator2 = int(denominator2)
                        lcm_val = lcm_of2(denominator1, denominator2)
                        factor1 = lcm_val // denominator1
                        factor2 = lcm_val // denominator2
                        replace1 = (
                            "[{}\\times{{\\color{{Salmon}}{{{}}}}}|{}\\times{{\\color{{Salmon}}{{{}}}}}]+[{}\\times{{\\color{{Salmon}}{{{}}}}}|{}\\times{{\\color{{Salmon}}{{{}}}}}]"
                            .format(numerator1, factor1, denominator1, factor1, numerator2, factor2, denominator2,
                                    factor2))
                        middle = middle.replace(subequation, replace1, 1)
                        replace2 = ("[{}+{}|{}]"
                                    .format(numerator1 * factor1, numerator2 * factor2, lcm_val))
                        middle2 = middle2.replace(subequation, replace2, 1)
                        n = numerator1 * factor1 + numerator2 * factor2
                        gcd_val = gcd(n, lcm_val)
                        if gcd_val != 1:
                            needtosimplify = True
                            replace3 = "[{}|{}]".format(n, lcm_val)
                            unsimplified = unsimplified.replace(subequation, replace3, 1)
                            replacesimpstatement = (
                                "[{}\\div{{\\color{{Salmon}}{{{}}}}}|{}\\div{{\\color{{Salmon}}{{{}}}}}]"
                                .format(n, gcd_val, lcm_val, gcd_val))
                            simplifystatement = simplifystatement.replace(subequation, replacesimpstatement, 1)
                        numerator1 //= gcd_val
                        denominator1 //= gcd_val
                        replace = "[{}|{}]".format(n // gcd_val, lcm_val // gcd_val)
                        arg1 = arg1.replace(subequation, replace, 1)
                    else:
                        idx = subequation.index('-')
                        trash, numerator1, denominator1 = getVals(subequation[0:idx])
                        trash, numerator2, denominator2 = getVals(subequation[idx + 1:])
                        numerator1 = int(numerator1)
                        numerator2 = int(numerator2)
                        denominator1 = int(denominator1)
                        denominator2 = int(denominator2)
                        lcm_val = lcm_of2(denominator1, denominator2)
                        factor1 = lcm_val // denominator1
                        factor2 = lcm_val // denominator2
                        replace1 = (
                            "[{}\\times{{\\color{{Salmon}}{{{}}}}}|{}\\times{{\\color{{Salmon}}{{{}}}}}]-[{}\\times{{\\color{{Salmon}}{{{}}}}}|{}\\times{{\\color{{Salmon}}{{{}}}}}]"
                            .format(numerator1, factor1, denominator1, factor1, numerator2, factor2, denominator2,
                                    factor2))
                        middle = middle.replace(subequation, replace1, 1)
                        replace2 = ("[{}-{}|{}]"
                                    .format(numerator1 * factor1, numerator2 * factor2, lcm_val))
                        middle2 = middle2.replace(subequation, replace2, 1)
                        n = numerator1 * factor1 - numerator2 * factor2
                        gcd_val = gcd(n, lcm_val)
                        if gcd_val != 1:
                            needtosimplify = True
                            replace3 = "[{}|{}]".format(n, lcm_val)
                            unsimplified = unsimplified.replace(subequation, replace3, 1)
                            replacesimpstatement = (
                                "[{}\\div{{\\color{{Salmon}}{{{}}}}}|{}\\div{{\\color{{Salmon}}{{{}}}}}]"
                                .format(n, gcd_val, lcm_val, gcd_val))
                            simplifystatement = simplifystatement.replace(subequation, replacesimpstatement, 1)
                        numerator1 //= gcd_val
                        denominator1 //= gcd_val
                        replace = "[{}|{}]".format(n // gcd_val, lcm_val // gcd_val)
                        arg1 = arg1.replace(subequation, replace, 1)
                arg1 = arg1.replace('(', '')
                arg1 = arg1.replace(')', '')
                res += getExpression(middle) + _(" = ")
                res += getExpression(middle2) + _(" = ")
                if needtosimplify:
                    res += getExpression(unsimplified) + _(" = ")
                    res += getExpression(simplifystatement) + _(" = ")
                res += getExpression(arg1) + "\n$$\n"

            step += 1
            res += _("**Step {}:** Simplify if possible. ").format(step)
            trash, numerator, denominator = getVals(arg1)
            numerator = int(numerator)
            denominator = int(denominator)
            gcd_val = gcd(numerator, denominator)
            if gcd_val == 1:
                res += _("In this case, the fraction cannot be further simplified.\n\n")
                self.answer = "\\frac{{{}}}{{{}}}".format(numerator, denominator)
            else:
                res += "\n$$\n" + getExpression(arg1) + _(" = ")
                simplifyStep = arg1
                numReplace = "{}\\div{{\\color{{Salmon}}{}}}".format(numerator, gcd_val)
                denReplace = "{}\\div{{\\color{{Salmon}}{}}}".format(denominator, gcd_val)
                simplifyStep = simplifyStep.replace(str(numerator), numReplace, 1)
                simplifyStep = simplifyStep.replace(str(denominator), denReplace, 1)
                res += "\\frac{{{}}}{{{}}} = ".format(numReplace, denReplace)
                numerator //= gcd_val
                denominator //= gcd_val
                res += "\\frac{{{}}}{{{}}}".format(numerator, denominator)
                self.answer = "\\frac{{{}}}{{{}}}".format(numerator, denominator)
                if denominator == 1:
                    res += " = " + str(numerator)
                    self.answer = str(numerator)
                    return res + "\n$$\n"
                if numerator > denominator:
                    neg = ''
                    if numerator < 0:
                        neg += '-'
                    res += neg + "{}\\frac{{{}}}{{{}}}".format(abs(numerator) // denominator, abs(numerator) - abs(
                        numerator) // denominator * denominator, denominator)
                    return res + "\n$$\n"
            return res

        args['getAnswer'] = getAnswer
        args['getExpression'] = getExpression
        args['getSteps'] = getSteps
        return self.custom_format(template, **args)
