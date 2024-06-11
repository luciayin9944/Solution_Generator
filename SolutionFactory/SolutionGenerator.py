from abc import ABC, abstractmethod
import re
import time
from num2words import num2words
from math import gcd


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
                return f"Error: {e}"

        # Replace all occurrences of the placeholder in the template
        return pattern.sub(replacer, template)

    # THIS FUNCTION DOES NOT WORK ABOVE 20,000
    # I only made it work for less than 20000 because it'll make it more simple
    # I haven't even seen us use numbers greater than 50 so there's no point for now.
    def getRep(num) -> str:
        if num == 0:
            return "zero"
        str_dict = {
            1000: "thousand", 100: "hundred", 90: "ninety", 80: "eighty",
            70: "seventy", 60: "sixty", 50: "fifty", 40: "forty", 30: "thirty",
            20: "twenty", 19: "nineteen", 18: "eighteen", 17: "seventeen", 16: "sixteen",
            15: "fifteen", 14: "fourteen", 13: "thirteen", 12: "twelve", 11: "eleven",
            10: "ten", 9: "nine", 8: "eight", 7: "seven", 6: "six", 5: "five", 4: "four",
            3: "three", 2: "two", 1: "one",
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


class KnowledgePoint1Solution(SolutionGenerator):
    """four arguments,
     example: 30(arg1) ones(arg2) + 2(arg3) tens(arg4)"""

    def get_solution(self, template: str, args: dict) -> str:
        args['value_dict'] = {'tens': 10, 'ones': 1}
        return self.custom_format(template, **args)


class KnowledgePoint2Solution(SolutionGenerator):
    """four arguments,
     example: 40(arg1) ones(arg2) - 2(arg3) tens(arg4)"""

    def get_solution(self, template: str, args: dict) -> str:
        args['value_dict'] = {'tens': 10, 'ones': 1}
        return self.custom_format(template, **args)


class KnowledgePoint3Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def check_zero_at_tens(value):
            if (value) == '0':
                return ''
            return str(value)

        args["check_zero_at_tens"] = check_zero_at_tens
        return self.custom_format(template, **args)


class KnowledgePoint4Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def check_zero_at_tens(value):
            if (value) == 0:
                return ''
            return value

        args["check_zero_at_tens"] = check_zero_at_tens
        return self.custom_format(template, **args)


class KnowledgePoint5Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return "unimplemented"


class KnowledgePoint6Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def get_sign(a, b):
            if (a == b):
                return '='
            if (a < b):
                return '<'
            return '>'

        def less_greater_equal_statement(arg1, arg2):
            if (arg1 < arg2):
                return "You see that the number {} is on the right of {}, so {} is greater than {}.".format(arg2, arg1,
                                                                                                            arg2, arg1)
            if (arg1 > arg2):
                return "You see that the number {} is on the left of {}, so {} is smaller than {}.".format(arg2, arg1,
                                                                                                           arg2, arg1)
            return "You see that the number {} is equal to itself, so {} equal to {}.".format(arg1, arg2, arg1)

        args["get_sign"] = get_sign
        args["less_greater_equal_statement"] = less_greater_equal_statement
        return self.custom_format(template, **args)


class KnowledgePoint7Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def statement_of_one_tens(arg1):
            if (arg1 % 10 == 0):
                return 'In this case, because there are no ones in {}, the "__ones" part of the question is 0, and we can also simplify the question to "{} = _tens".'.format(
                    arg1, arg1)
            else:
                return ''

        def result_statement(arg1):
            if (arg1 % 10 == 0):
                return ''
            else:
                return '$+$ ${\color{Salmon} %i }$ ones' % (arg1 % 10)

        args["statement_of_one_tens"] = statement_of_one_tens
        args["result_statement"] = result_statement
        return self.custom_format(template, **args)


########################################################################################

class KnowledgePoint26Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        args['getRep'] = SolutionGenerator.getRep
        return self.custom_format(template, **args)


#########################################################################################
class KnowledgePoint27Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        # arg1 = args['arg1']
        # arg2 = args['arg2']
        # arg3 = arg1 // arg2
        # args['arg3'] = arg3
        return self.custom_format(template, **args)


class KnowledgePoint28Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        # arg1 = args['arg1']
        # arg3 = arg1 % 10
        # args['arg3'] = arg3
        return self.custom_format(template, **args)


#
# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title">
# <div class="ex-text">
#
# $$
# [[arg1]] × [[arg2]]
# $$
#
#
# **Step 1:** In the below example first multiply the digit in units place
# $$
# \begin{array}{l r}
# &[[arg1//10]]{\color{Salmon}{[[arg1 % 10]]}}\\
# \times  &{\color{Salmon}[[arg2]]}\\
# \hline
# &{\color{Salmon}{[[arg1 % 10 * arg2]]}}\\
# \end{array}
# $$
#
#
# **Step 2:** Next multiply digit in tens place
# $$
# \begin{array}{l r}
# &{\color{Salmon}{[[arg1 // 10]]}}[[arg1 % 10]]\\
# \times &{\color{Salmon}[[arg2]]}\\
# \hline
# &{\color{Salmon}{[[arg1 // 10* arg2]]}}{[[arg1 % 10 *arg2]]}\\
# \end{array}
# $$
#
# So the answer is $[[arg1 // 10 * arg2]][[arg1 % 10 *arg2]]$.
# </div>
# </div>
#     """
#     args = {'arg1': 21, 'arg2': 5}
#     solution = KnowledgePoint28Solution().get_solution(template, args)
#     print(solution)
#
# main()


class KnowledgePoint29Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)


class KnowledgePoint30Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        arg1 = args['arg1']
        arg2 = args['arg2']
        args['num2words_arg1_div_arg2'] = num2words(arg1 // arg2)

        # arg3 = num2words(arg1//arg2)
        # args['arg3'] = arg3
        return self.custom_format(template, **args)


class KnowledgePoint31Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)


# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title"
#
# <div class="ex-text">
#
# $$
# [[arg1]] × [[arg2]]
# $$
#
#
# **Step 1:** First compare the numbers,[[arg1]]  has more digits than [[arg2]], first place the bigger number and then second number.
#
# $$
# \begin{array}{l r}
# & {\color{#21ABCD}tens}\:\:\:{\color{#8DB600}ones}\\
# &{\color{#21ABCD}[[arg1//10]]}\:\:\:\:\:\:\:\:\:\:{\color{#8DB600}[[arg1%10]]}\:\:\:\\
# ×&{\color{#21ABCD}}\:\:\:\:\:\:\:\:\:\:{\color{#8DB600}[[arg2]]}\:\:\:\\
# \hline
# \end{array}
# $$
#
#
# **Step 2:** Next multiply [[arg2]] by [[arg1 % 10]] (the ones place of the first number), and the product is [[arg1 % 10*arg2]] which is greater than 9, so carry [[arg1 % 10*arg2//10]] tens to the tens place column.
#
# $$
# \begin{array}{l r}
# & \tiny[[arg1%10*arg2//10]]\:\:\:\:\\[-3pt]
# &[[arg1//10]]{\color{Salmon}[[arg1%10]]}\\
# ×&{\color{Salmon}[[arg2]]}\\
# \hline
# & {\color{Salmon}[[arg1%10*arg2%10]]}\\
# \end{array}
# $$
#
# **Step 3:** Now, multiply [[arg2]] by [[arg1//10]] (the tens place of the first number).
#
# $$
# \begin{array}{l r}
# & \tiny[[arg1%10*arg2//10]]\:\:\:\:\\[-3pt]
# &{\color{Salmon}[[arg1//10]]}[[arg1%10]]\\
# ×&{\color{Salmon}[[arg2]]}\\
# \hline
# &[[arg1%10*arg2%10]]\\
# &{\color{Salmon}[[arg1//10*arg2]]}\phantom{0}\\
# \hline
# \end{array}
# $$
#
# **Step 4:** Finally, add the carryover.
#
# $$
# \begin{array}{l r}
# & {\color{Salmon}\tiny[[arg1%10*arg2//10]]}\:\:\:\\[-3pt]
# &[[arg1]]\\
# ×&[[arg2]]\\
# \hline
# &[[arg1%10*arg2%10]]\\
# &{\color{Salmon}[[arg1//10*arg2]]}\phantom{0}\\
# \hline
# &{\color{Salmon}[[arg1//10*arg2 + arg1% 10*arg2//10]]}[[arg1%10*arg2%10]]
# \end{array}
# $$
#
# So the answer is $[[arg1*arg2]]$.
# </div>
# </div>
#         """
#     args = {'arg1': 13, 'arg2':8}
#     solution = KnowledgePoint31Solution().get_solution(template, args)
#     print(solution)
#
# main()
################################################################################

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
        return self.custom_format(template, **args)


#
# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title">
#
# <div class="ex-text">
#
# $$
# [[arg1]] × [[arg2]]
# $$
#
#
# **Step 1:** First compare the numbers, [[large_num]]  is greater than [[small_num]] **because in tens place digits [[large_num//10]] is greater than [[small_num//10]]**. First place the bigger number as **multiplicand** and then second number as **multiplier**.
#
# $$
# \begin{array}{l r}
# & {\color{#21ABCD}tens}\:\:\:{\color{#8DB600}ones}\\
# &{\color{#21ABCD}[[large_num//10]]}\:\:\:\:\:\:\:\:\:\:{\color{#8DB600}[[large_num%10]]}\:\:\:\\
# ×&{\color{#21ABCD}[[small_num//10]]}\:\:\:\:\:\:\:\:\:\:{\color{#8DB600}[[small_num%10]]}\:\:\:\\
# \hline
# \end{array}
# $$
#
#
# **Step 2:** Multiply the multiplicand with the ones digit of the multiplier. Place those digits under the line.
#
# $$
# \begin{array}{l r}
# &{\color{Salmon}[[large_num]]}\\
# ×&[[small_num//10]]{\color{Salmon}[[small_num%10]]}\\
# \hline
# & {\color{Salmon}[[small_num%10*large_num]]}\\
# \end{array}
# $$
#
# **Step 3:** Next multiply the multiplicand with the tens digit of multiplier. Place those under the ones digit value .
#
# $$
# \begin{array}{l r}
# &{\color{Salmon}[[large_num]]}\\
# ×&{\color{Salmon}[[small_num//10]]}[[small_num%10]]\\
# \hline
# &[[small_num%10*large_num]]\\
# &{\color{Salmon}[[small_num//10*large_num]]}\phantom{0}\\
# \hline
# \end{array}
# $$
#
# **Step 4:** Finally, adding those digits will get the product.
#
# $$
# \begin{array}{l r}
# &[[large_num]]\\
# ×&[[small_num]]\\
# \hline
# &{\color{Salmon}[[small_num%10*large_num]]}\\
# +&{\color{Salmon}[[small_num//10*large_num]]}\phantom{0}\\
# \hline
# &{\color{Salmon}[[large_num*small_num]]}
# \end{array}
# $$
#
# So the answer is $[[arg1*arg2]]$.
# </div>
# </div>
#
#         """
#     args = {'arg1': 12, 'arg2': 49}
#     solution = KnowledgePoint34Solution().get_solution(template, args)
#     print(solution)
#
# main()


class KnowledgePoint35Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)


class KnowledgePoint36Solution(SolutionGenerator):
    # def get_solution(self, template: str, args: dict) -> str:
    def get_solution(self, template1: str, template2: str, args: dict) -> str:
        def fractions_statement(a, b):
            if a < b:
                return "{}/{} is a proper fraction because {} < {}.".format(a, b, a, b)
            elif a > b:
                return "{}/{} is an improper fraction because {} > {}.".format(a, b, a, b)
            return "{}/{} is neither proper nor improper.".format(a, b)

        if len(args) == 3:
            return self.custom_format(template1, **args)
            # return self.custom_format(template, **args)

        elif len(args) == 2:
            args["fractions_statement"] = fractions_statement
            return self.custom_format(template2, **args)
            # return self.custom_format(template, **args)


# def main():
#     start_time = time.time()
#     template1 = r"""
# <div class="ex-text">
# <div class="ex-text">
#
# $$
# [[arg3]]\frac{[[arg1]]}{[[arg2]]}
# $$
#
# $[[arg3]]\frac{[[arg1]]}{[[arg2]]}$  is a mixed fraction because it consists of a whole number and a proper fraction.
#
# </div>
# </div>
#         """
#
#     template2 = r"""<div class="ex-text">
# <div class="ex-text">
#
# $$
# \frac{[[arg1]]}{[[arg2]]}
# $$
#
# [[fractions_statement(arg1, arg2) ]]
#
# </div>
# </div>
#         """
#     # args = {'arg1': 3, 'arg2': 5, 'arg3': 1}
#     args = {'arg1': 8, 'arg2': 5}
#
#     solution = KnowledgePoint36Solution().get_solution(template1, template2, args)
#     print(solution)

###old version###
# args1 = {'arg1': 3, 'arg2': 5, 'arg3': 1}
# args2 = {'arg1': 8, 'arg2': 5}
#
# solution1 = KnowledgePoint36Solution().get_solution(template1, args1)
# solution2 = KnowledgePoint36Solution().get_solution(template2, args2)
#
# print(solution1)
# print(solution2)

# main()
#
#


class KnowledgePoint36Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def fractions_statement(a, b):
            if (a < b):
                return "{}/{} is a proper fraction because {} < {}.".format(a, b, a, b)
            elif (a > b):
                return "{}/{} is a improper fraction because {} > {}.".format(a, b, a, b)

        args["fractions_statement"] = fractions_statement
        return self.custom_format(template, **args)


################################################################################################
####not work#########################################
# def fractions_statement(args: dict):
#     if len(args) == 3:
#         return "is a mixed fraction because It consists of a whole number and a proper fraction."
#     elif len(args) == 2:
#         if args['arg1'] < args['arg2']:
#             return "is a proper fraction because {} < {}.".format(args['arg1'], args['arg2'])
#         elif args['arg1'] > args['arg2']:
#             return "is an improper fraction because {} > {}.".format(args['arg1'], args['arg2'])

# def fractions_statement(arg1, arg2, arg3):
#     if arg3 is not None:
#         return "is a mixed fraction because It consists of a whole number and a proper fraction.".format(arg3, arg1, arg2)
#     else:
#         if (arg1 < arg2):
#             return "{}/{} is a proper fraction because {} < {}.".format(arg1, arg2, arg1, arg2)
#         elif (arg1 > arg2):
#             return "{}/{} is a improper fraction because {} > {}.".format(arg1, arg2, arg1, arg2)
#
# args["fractions_statement"] = fractions_statement
# return self.custom_format(template, **args)
######################################################################################################


# def main():
#     start_time = time.time()
#     template1 = r"""<div class="ex-text">
# <div class="ex-text">
#
# $$
# [[arg3]]\frac{[[arg1]]}{[[arg2]]}
# $$
#
# $[[arg3]]\frac{[[arg1]]}{[[arg2]]}$  is a mixed fraction because It consists of a whole number and a proper fraction.
#
# </div>
# </div>
#         """
#
#     template2 = r"""<div class="ex-text">
# <div class="ex-text">
#
# $$
# \frac{[[arg1]]}{[[arg2]]}
# $$
#
# [[fractions_statement(arg1, arg2)]]
#
# </div>
# </div>
# """
#     args = {'arg1': 3, 'arg2': 5, 'arg3':1}
# args = {'arg1': 8, 'arg2': 5}

#     if len(args) == 3:
#         template = template1
#     elif len(args) == 2:
#         template = template2
#
#     solution = KnowledgePoint36Solution().get_solution(template, args)
#     print(solution)
#
# main()

####################################################################################


class KnowledgePoint37Solution(SolutionGenerator):
    def get_solution(self, template1: str, template2: str, args: dict) -> str:
        arg1 = args['arg1']
        arg2 = args['arg2']
        args['large_num'] = max(arg1, arg2)
        args['small_num'] = min(arg1, arg2)

        if arg2 < 100:
            return self.custom_format(template1, **args)
        else:
            return self.custom_format(template2, **args)


# def main():
#     start_time = time.time()
#     template1 = r"""<div class="ex-yellow">
# <div class="title">
# <div class="ex-text" align="center">
#
# $[[arg1]] \times [[arg2]] =?$
#
#
# **Step 1: Organize**
#
# Place the large number (the 3-digit number) above the smaller number (the 2-digit number) with each digit in its corresponding place.
#
# $$
# \begin{array}{l r}
# & {\color{#C4A680}hundreds}\:\:\:{\color{#21ABCD}tens}\:\:\:{\color{#8DB600}ones}\\
# &{\color{#C4A680}[[arg1//100]]}\:\:\:\:\:\:\:\:\:\:\:\:\:\:{\color{#21ABCD}[[arg1%100 //10]]}\:\:\:\:\:\:\:\:\:\:{\color{#8DB600}[[arg1%10]]}\:\:\:\\
# \times&{\color{#C4A680}}\:\:\:\:\:\:\:\:\:\:\:\:\:\:{\color{#21ABCD}[[arg2//10]]}\:\:\:\:\:\:\:\:\:\:{\color{#8DB600}[[arg2% 10]]}\:\:\:\\
# \hline
# \end{array}
# $$
#
# *Note: Make sure you line them up so the ones places are in a column, and the tens places are in a column.*
#
# **Step 2: Multiply the Ones**
#
# **Step 2.1:** We start by multiplying the one's place column of the lower number by each of the places of the bigger number. Calculate the numbers in the ones place: $[[arg1% 10]] \times [[arg2% 10]] = [[(arg1%10)*(arg2% 10)]]$. We write down the [[(arg1%10)*(arg2% 10)%10]] ones, carry the [[(arg1%10)*(arg2% 10) //10]] tens, and trend it over to the 3 tens' place.
#
# $$
# \begin{array}{l r}
# & {\color{Salmon}\tiny[[(arg1%10)*(arg2% 10) //10]] }\:\:\:\\[-3pt]
# &[[arg1//10]]{\color{Salmon}[[arg1%10]]}\\
# \times&[[arg2//10]]{\color{Salmon}[[arg2%10]]}\\
# \hline
# &{\color{Salmon}[[(arg1%10)*(arg2%10)%10]]}\\
# \end{array}
# $$
#
# **Step 2.2:** Then calculate the bigger number in the tens digit: $[[arg2% 10]] \times [[arg1%100 //10]] = [[(arg2% 10)*(arg1%100//10)]]$. Add the 1 ten you traded to the 3 tens' place: $[[(arg2% 10)*(arg1%100//10)]] + [[(arg1%10)*(arg2% 10) //10]] = [[(arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10]]$. We write down the $[[((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)%10]]$ ones, carry the [[((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10]] ten, and trend it over to the 2 hundred places.
#
# $$
# \begin{array}{l r}
# &{\color{Salmon}\tiny1}\:\:\:\:\:\\[-3pt]
# &[[arg1//100]]{\color{Salmon}[[arg1%100 //10]]}[[arg1% 10]]\\
# \times&[[arg2//10]]{\color{Salmon}[[arg2% 10]]}\\
# \hline
# &{\color{Salmon}[[((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)%10]]}[[(arg1%10)*(arg2% 10)%10]] \\
# \end{array}
# $$
#
#
# **Step 2.3:** Next calculate the bigger number in the hundreds place: $[[arg2% 10]] \times [[arg1//100]] = [[(arg2% 10)*(arg1//100)]]$. Add the [[((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10]] ten you traded to the 2 hundred place: $[[(arg2% 10)*(arg1//100)]] + [[((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10]] = [[(arg2% 10)*(arg1//100)+(((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10)]]$. We write down the [[(arg2% 10)*(arg1//100)+(((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2%10) //10)//10)]].
#
# $$
# \begin{array}{l r}
# &{\color{Salmon}[[arg1//100]]}[[arg1%100]]\\
# \times&[[arg2//10]]{\color{Salmon}[[arg2% 10]]}\\
# \hline
# &{\color{Salmon}[[arg1*(arg2%10)//100]]}[[arg1*(arg2%10)%100]]\\
# \end{array}
# $$
#
# **Step 3: Multiply the Tens**
#
# **Step 3.1:** First, let’s add a zero down the ones column before we move on to the tens column. This will help us not get confused over where the numbers for the tens multiplications start on this new line.
#
# $$
# \begin{array}{l r}
# &[[arg1]]\\
# \times&[[arg2]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}0}\\
# \end{array}
# $$
# **Step 3.2:** Then we multiply the bottom tens place number with the ones place number in the top number. In our example, that’s $[[arg2//10]] \times [[arg1% 10]] = [[(arg2//10) * (arg1%10)]]$. We write down the [[(arg2//10) * (arg1%10)]].
#
# $$
# \begin{array}{l r}
# &[[arg1//10]]{\color{Salmon}[[arg1% 10]]}\\
# \times&{\color{Salmon}[[arg2//10]]}[[arg2%10]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}[[(arg2//10) * (arg1%10)]]}0\\
# \end{array}
# $$
# **Step 3.3:** Next is the tens place turn. We multiply $[[arg2//10]] \times [[arg1%100 //10]] = [[(arg2//10) * (arg1%100 //10)]]$. We write down the [[(arg2//10) * (arg1%100 //10)]].
#
# $$
# \begin{array}{l r}
# &[[arg1//100]]{\color{Salmon}[[arg1%100 //10]]}[[arg1%10]]\\
# \times&{\color{Salmon}[[arg2//10]]}[[arg2%10]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}[[(arg2//10) * (arg1%100 //10)]]}[[(arg2//10) * (arg1%10)]]0\\
# \end{array}
# $$
#
# **Step 3.4:** Finally, we need to multiply the tens value number on the bottom number with the hundreds place number in the top number. That is $[[arg2//10]] \times [[arg1//100]] = [[(arg2//10) * (arg1//100)]]$. We write down the [[(arg2//10) * (arg1//100)]].
#
# $$
# \begin{array}{l r}
# &{\color{Salmon}[[arg1//100]]}[[arg1%100]]\\
# \times&{\color{Salmon}[[arg2//10]]}[[arg2%10]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}[[(arg2//10) * (arg1//100)]]}[[arg2//10*arg1%100]]0\\
# \end{array}
# $$
# **Step 4: Add two Numbers**
#
# From here on, we add the two partial products together: $[[arg1*(arg2%10)]]$ is the partial product in the ones column and $[[arg1*(arg2//10)*10]]$ is the partial product in the tens column. We combine both partial products: $[[arg1*(arg2%10)]] + [[arg1*(arg2//10)*10]] = [[arg1*(arg2%10) + arg1*(arg2//10)*10]]$. This is our final product.
#
# $$
# \begin{array}{l r}
# &[[arg1]]\\
# \times&[[arg2]]\\
# \hline\\[-16pt]
# &\:\:\!\:\:\:\:\:\:\\[-3pt]
# &[[arg1*(arg2%10)]]\\
# +&[[arg1*(arg2//10)]]0\\
# \hline
# &{\color{Salmon}[[arg1*arg2]]}\\
# \end{array}
# $$
#
# So the answer is $[[arg1*arg2]]$.
# </div>
# </div>
#
#         """
#
#     template2 = r"""<div class="ex-yellow">
# <div class="title">
# <div class="ex-text" align="center">
#
# $[[arg1]] \times [[arg2]] =?$
#
# **Step 1: Organize**
#
# Place the numbers aligned with each digit in its corresponding place.
#
# $$
# \begin{array}{l r}
# & {\color{#C4A680}hundreds}\:\:\:{\color{#21ABCD}tens}\:\:\:{\color{#8DB600}ones}\\
# &{\color{#C4A680}[[arg1//100]]}\:\:\:\:\:\:\:\:\:\:\:\:\:\:{\color{#21ABCD}[[arg1%100//10]]}\:\:\:\:\:\:\:\:\:\:{\color{#8DB600}[[arg1%10]]}\:\:\:\\
# \times&{\color{#C4A680}[[arg2//100]]}\:\:\:\:\:\:\:\:\:\:\:\:\:\:{\color{#21ABCD}[[arg2%100//10]]}\:\:\:\:\:\:\:\:\:\:{\color{#8DB600}[[arg2%10]]}\:\:\:\\
# \hline
# \end{array}
# $$
#
# *Note: Make sure you line them up so the hundreds places are in a column, the ones places are in a column, and the tens places are in a column.*
#
# **Step 2: Multiply the Ones**
#
# **Step 2.1:** We start by multiplying the one's place column of the lower number by each of the places of the number on top. Calculate the numbers in the ones place: $[[arg1%10]] \times [[arg2%10]] = [[(arg1%10)*(arg2% 10)%10]]$.
#
# $$
# \begin{array}{l r}
# &[[arg1//10]]{\color{Salmon}[[arg1%10]]}\\
# \times&[[arg2//10]]{\color{Salmon}[[arg2%10]]}\\
# \hline
# &{\color{Salmon}[[(arg1%10)*(arg2% 10)%10]]}\\
# \end{array}
# $$
#
# **Step 2.2:** Then calculate the number in the tens digit: $[[arg1%100//10]] \times [[arg2%10]] = [[(arg1%100//10)*(arg2%10)]]$.   We multiply $[[arg1%100//10]] \times [[arg2%10]] = [[(arg1%100//10)*(arg2%10)]]$. We write down the $[[(arg1%100//10)*(arg2%10)]]$.
#
# $$
# \begin{array}{l r}
# &[[arg1//100]]{\color{Salmon}[[arg1%100//10]]}[[arg1%10]]\\
# \times&[[arg2//10]]{\color{Salmon}[[arg2%10]]}\\
# \hline
# &{\color{Salmon}[[(arg1%100//10)*(arg2%10)]]}[[(arg1%10)*(arg2%10)%10]]\\
# \end{array}
# $$
#
# **Step 2.3:** Next calculate the number in the hundreds place: $[[arg1//100]] \times [[arg2%10]] = [[(arg1//100)*(arg2%10)]]$. We write down the $[[(arg1//100)*(arg2%10)]]$.
#
# $$
# \begin{array}{l r}
# &[[arg1//100]]{\color{Salmon}[[arg1%100//10]]}[[arg1%10]]\\
# \times&[[arg2//10]]{\color{Salmon}[[arg2%10]]}\\
# \hline
# &{\color{Salmon}[[(arg1%100//10)*(arg2%10)]]}[[(arg1%10)*(arg2%10)]]\\
# \end{array}
# $$
#
# **Step 3: Multiply the Tens**
#
# **Step 3.1:** First, let’s add a zero down the ones column before we move on to the tens column. This will help us not get confused over where the numbers for the tens multiplications start on this new line.
#
# $$
# \begin{array}{l r}
# &[[arg1]]\\
# \times&[[arg2]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}0}\\
# \end{array}
# $$
# **Step 3.2:** Then we multiply the bottom tens place number with the ones place number in the top number. In our example, that’s $[[arg1%10]] \times [[arg2%100//10]] = [[(arg1%10)*(arg2%100//10)]]$. We write down the $[[(arg1%10)*(arg2%100//10)]]$.
#
# $$
# \begin{array}{l r}
# &[[arg1//10]]{\color{Salmon}[[arg1%10]]}\\
# \times&[[arg2//100]]{\color{Salmon}[[arg2%100//10]]}[[arg2%10]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}[[(arg1%10)*(arg2%100//10)]]}0\\
# \end{array}
# $$
#
# **Step 3.3:** Next is the tens place turn. We multiply $[[arg1%100//10]] \times [[arg2%100//10]] = [[(arg1%100//10)*(arg2%100//10)]]$.
#
# $$
# \begin{array}{l r}
# &[[arg1//100]]{\color{Salmon}[[arg1%100//10]]}[[arg1%10]]\\
# \times&[[arg2//100]]{\color{Salmon}[[arg2%100//10]]}[[arg2%10]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}[[(arg1%100//10)*(arg2%100//10)]]}[[(arg1%10)*(arg2%100//10)]]0\\
# \end{array}
# $$
#
# **Step 3.4:** Finally, we need to multiply the tens value number on the bottom number with the hundreds place number in the top number. That is $[[arg1//100]] \times [[arg2%100//10]] = [[(arg1//100)*(arg2%100//10)]]$. We write down the $[[(arg1//100)*(arg2%100//10)]]$.
#
# $$
# \begin{array}{l r}
# &{\color{Salmon}[[arg1//100]]}[[arg1%100]]\\
# \times&[[arg2//100]]{\color{Salmon}[[arg2%100//10]]}[[arg2%10]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}[[(arg1//100)*(arg2%100//10)]]}[[(arg1%100//10)*(arg2%100//10)]][[(arg1%10)*(arg2%100//10)]]0\\
# \end{array}
# $$
#
# **Step 4: Multiply the Hundreds**
#
# **Step 4.1:** Let’s add two zeros down the ones and tens columns before we move on to the ten columns.
#
# $$
# \begin{array}{l r}
# &[[arg1]]\\
# \times&[[arg2]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &[[(arg1//100)*(arg2%100//10)]][[(arg1%100//10)*(arg2%100//10)]][[(arg1%10)*(arg2%100//10)]]0\\
# &{\color{Salmon}00}\\
# \end{array}
# $$
# **Step 4.2:** Multiply the tens place of the lower number by each of the places of the number on top. In our example, that’s $[[arg1%10]] \times [[arg2//100]] =[[(arg1%10)*(arg2//100)]]$. We write down the $[[(arg1%10)*(arg2//100)]]$.
#
# $$
# \begin{array}{l r}
# &[[arg1//10]]{\color{Salmon}[[arg1%10]]}\\
# \times&{\color{Salmon}[[arg2//100]]}[[arg2%100//10]][[arg2%10]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &[[(arg1//100)*(arg2%100//10)]][[(arg1%100//10)*(arg2%100//10)]][[(arg1%10)*(arg2%100//10)]]0\\
# &{\color{Salmon}[[(arg1%10)*(arg2//100)]]}00\\
# \end{array}
# $$
# **Step 4.3:** Next is the tens place turn. We multiply $[[arg1%100//10]] \times [[arg2//100]] = [[(arg1%100//10)*(arg2//100)]]$. We write down the $[[(arg1%100//10)*(arg2//100)]]$.
#
# $$
# \begin{array}{l r}
# &[[arg1//100]]{\color{Salmon}[[arg1%100//10]]}[[arg1%10]]\\
# \times&{\color{Salmon}[[arg2//100]]}[[arg2%100//10]][[arg2%10]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &[[(arg1//100)*(arg2%100//10)]][[(arg1%100//10)*(arg2%100//10)]][[(arg1%10)*(arg2%100//10)]]0\\
# &{\color{Salmon}[[(arg1%100//10)*(arg2//100)]]}[[(arg1%10)*(arg2//100)]]00\\
# \end{array}
# $$
#
# **Step 4.4:** Finally, we need to multiply the hundreds value number on the bottom number with the hundreds place number in the top number. That is $[[arg1//100]] \times [[arg2//100]] = [[(arg1//100)*(arg2//100)]]$. We write down the $[[(arg1//100)*(arg2//100)]]$.
#
# $$
# \begin{array}{l r}
# &{\color{Salmon}[[arg1//100]]}[[arg1%100]]\\
# \times&{\color{Salmon}[[arg2//100]]}[[arg2%100//10]][[arg2%10]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &[[(arg1//100)*(arg2%100//10)]][[(arg1%100//10)*(arg2%100//10)]][[(arg1%10)*(arg2%100//10)]]0\\
# &{\color{Salmon}[[(arg1//100)*(arg2//100)]]}[[(arg1%100)*(arg2//100)]]00\\
# \end{array}
# $$
# **Step 5: Add two Numbers**
# From here on, we add these three partial products together: $[[arg1*(arg2%10)]]$ is the partial product in the ones column, $[[arg1*(arg2%100//10)*10]]$ is the partial product in the tens column and $[[arg1*(arg2//100)*100]]$ is the partial product in the hundreds column. We combine three partial products: $[[arg1*(arg2%10)]] + [[arg1*(arg2%100//10)*10]] + [[arg1*(arg2//100)*100]] = [[arg1*arg2]]$. This is our final product.
#
# $$
# \begin{array}{l r}
# &[[arg1]]\\
# \times&[[arg2]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &[[(arg1//100)*(arg2%100//10)]][[(arg1%100//10)*(arg2%100//10)]][[(arg1%10)*(arg2%100//10)]]0\\
# +&[[arg1*(arg2//100)*100]]\\
# \hline
# &{\color{Salmon}[[arg1*arg2]]}
# \end{array}
# $$
# So the answer is $[[arg1*arg2]]$.
#
# </div>
# </div>
#     """
#
#     #args = {'arg1': 232, 'arg2': 26}
#     args = {'arg1': 232, 'arg2': 201}
#     solution = KnowledgePoint37Solution().get_solution(template1, template2, args)

#     print(solution)
#
# main()


class KnowledgePoint38Solution(SolutionGenerator):
    def get_solution(self, template1: str, template2: str, template3: str, args: dict) -> str:
        # Extract arguments
        arg1 = args['arg1']
        arg2 = args['arg2']

        def count_digits(num):
            return len(str(num))

        result_digits = count_digits(arg1 // arg2)

        # Select the appropriate template
        if result_digits == 3:
            template = template1
        elif result_digits == 2:
            template = template2
        elif result_digits == 1:
            template = template3
        else:
            raise ValueError("Unsupported number of digits")

        # Format the template with arguments
        return self.custom_format(template, **args)


#
# def main():
#     start_time = time.time()
#     template1 = r"""
# <div class="ex-yellow">
# <div class="title">
# <div class="ex-text" align="center">
#
# $[[arg1]] \div [[arg2]] =?$
#
# </div>
#
# When you solve division questions, you work in reverse. You begin with the **largest** place value.
#
# **Step 1:**
#
# In this question, you divide the **hundreds** first. You divide [[arg1//100]] hundreds into [[arg1//100//arg2]] groups of 100.
#
# **Step 1.1:** Write [[arg1//100//arg2]] above the hundreds' place to show you have put 100 in each group.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\text{ }\text{ }\text{ }\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:{\color {Salmon}[[arg1//100//arg2]]}\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# $$
# **Step 1.2:** Write [[arg1//100//arg2*arg2*100]] underneath to show [[arg1//100]] hundreds have been used.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:[[arg1//100//arg2]]\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:[[arg1//100//arg2]]\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:{\color {Salmon} [[arg1//100//arg2*arg2*100]]}\:\:}\\[-4pt]
# \hline
# \end{aligned}
# $$
# **Step 1.3:** You subtract [[arg1//100//arg2*arg2*100]] from [[arg1]] to see how many blocks are left that need to be grouped equally.
# $$
# \begin{aligned}
# &\underline{\text{ }\:[[arg1//100//arg2]]\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:[[arg1//100//arg2*arg2*100]]\:\:}\\[-4pt]
# \hline
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:[[arg1//100//arg2]]\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# -&{\:\:{\color {Salmon} [[arg1//100//arg2*arg2*100]]}\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:{\color {Salmon} [[arg1-arg1//100//arg2*arg2*100]]}\\[-4pt]
# \end{aligned}
# $$
# **Step 2:**
#
#  Let’s look at the [[arg1%100//10]] tens. When you divide them into [[arg2]] equal groups you can put [[arg1%100//10//arg2]] tens in each group.
#
# **Step 2.1:** Write [[arg1%100//10//arg2]] above the tens' place to show you have put [[arg1%100//10//arg2]] tens in each group.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:[[arg1//100//arg2]]\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:[[arg1//100//arg2*arg2*100]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//100//arg2*arg2*100]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\:\:[[arg1//100//arg2]]{\color {Salmon} [[arg1%100//10//arg2]]}\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:[[arg1//100//arg2*arg2*100]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:{\color {Salmon} [[arg1-arg1//100//arg2*arg2*100]]}\\[-4pt]
# \end{aligned}
# $$
#
# **Step 2.2:** Write [[arg1%100//10//arg2*arg2*10]]  underneath to show that [[arg2]] groups of [[arg1%100//10//arg2]]  tens have been used.
#
# $$
# \begin{aligned}
# &\underline{\:\:[[arg1//10//arg2]]\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:[[arg1//100//arg2*arg2*100]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//100//arg2*arg2*100]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\:\:[[arg1//10//arg2]]\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:[[arg1//100//arg2*arg2*100]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//100//arg2*arg2*100]]\\[-4pt]
# -&\text{ }\:\:\:{\color {Salmon} [[arg1%100//10//arg2*arg2*10]]}\\[-4pt]
# \hline
# &\text{ }\:\:\:{\:\:\color {Salmon}[[arg1//arg2%10*arg2+arg1%arg2]]}\\[-4pt]
# \end{aligned}
# $$
#
# **Step 3:**
#
# Now you need to group the [[arg1//arg2%10*arg2+arg1%arg2]] ones that are left into [[arg2]] equal groups.
#
# **Step 3.1:** Write [[arg1//arg2%10*arg2+arg1%arg2]] above the ones' place to show you have put [[arg2]] ones in each group.
#
# $$
# \begin{aligned}
# &\underline{\:\:[[arg1//10//arg2]]\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:[[arg1//100//arg2*arg2*100]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//100//arg2*arg2*100]]\\[-4pt]
# -&\text{ }\:\:\:[[arg1%100//10//arg2*arg2*10]]\\[-4pt]
# \hline
# &\text{ }\:\:\:\:\:[[arg1//arg2%10*arg2+arg1%arg2]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\:\:[[arg1//10//arg2]]{\color{salmon}[[arg1//arg2%10]] }\small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:[[arg1//100//arg2*arg2*100]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//100//arg2*arg2*100]]\\[-4pt]
# -&\text{ }\:\:\:[[arg1%100//10//arg2*arg2*10]]\\[-4pt]
# \hline
# &\text{ }\:\:\:\:\:[[arg1//arg2%10*arg2+arg1%arg2]]\\[-4pt]
# \end{aligned}
# $$
#
# **Step 3.2:** Write [[arg1//arg2%10*arg2]]  underneath to show [[arg1//arg2%10]]  groups of [[arg2]] have been used.
# $$
# \begin{aligned}
# &\underline{\:\:[[arg1//arg2]] \small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:[[arg1//100//arg2*arg2*100]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//100//arg2*arg2*100]]\\[-4pt]
# -&\text{ }\:\:\:[[arg1%100//10//arg2*arg2*10]]\\[-4pt]
# \hline
# &\text{ }\:\:\:\:\:[[arg1//arg2%10*arg2+arg1%arg2]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\:\:[[arg1//arg2]] \small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:[[arg1//100//arg2*arg2*100]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//100//arg2*arg2*100]]\\[-4pt]
# -&\text{ }\:\:\:[[arg1%100//10//arg2*arg2*10]]\\[-4pt]
# \hline
# &\text{ }\:\:\:\:\:[[arg1//arg2%10*arg2+arg1%arg2]]\\[-4pt]
# -&\text{ }\:\:\:\:\:{\color{salmon}[[arg1//arg2%10*arg2]]}\\[-4pt]
# \hline
# \end{aligned}
# $$
# **Step 3.3:** Subtract [[arg1//arg2%10*arg2]] from [[arg1//arg2%10*arg2+arg1%arg2]] to see how many blocks are left.
#
# $$
# \begin{aligned}
# &\underline{\:\:[[arg1//arg2]] \small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:[[arg1//100//arg2*arg2*100]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//100//arg2*arg2*100]]\\[-4pt]
# -&\text{ }\:\:\:[[arg1%100//10//arg2*arg2*10]]\\[-4pt]
# \hline
# &\text{ }\:\:\:\:\:[[arg1//arg2%10*arg2+arg1%arg2]]\\[-4pt]
# -&\text{ }\:\:\:\:\:[[arg1//arg2%10*arg2]]\\[-4pt]
# \hline
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\:\:[[arg1//arg2]] \small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:[[arg1//100//arg2*arg2*100]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//100//arg2*arg2*100]]\\[-4pt]
# -&\text{ }\:\:\:[[arg1%100//10//arg2*arg2*10]]\\[-4pt]
# \hline
# &\text{ }\:\:\:\:\:[[arg1//arg2%10*arg2+arg1%arg2]]\\[-4pt]
# -&\text{ }\:\:\:\:\:[[arg1//arg2%10*arg2]]\\[-4pt]
# \hline
# &\text{ }\:\:\:\:\:{\color{salmon}[[arg1%arg2]]}\\[-4pt]
# \end{aligned}
# $$
# **Step 4: Write the remainder near the quotient and check**
#
# As you can see [[arg1]] cannot be divided equally into [[arg2]] equal groups. There is [[arg1%arg2]] unit left over and it can be represented as R (remainder).
#
# $$
# \begin{aligned}
# &\underline{\:\:[[arg1//arg2]] \small\:{\color{salmon}R\small\,[[arg1%arg2]]}}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:[[arg1//100//arg2*arg2*100]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//100//arg2*arg2*100]]\\[-4pt]
# -&\text{ }\:\:\:[[arg1%100//10//arg2*arg2*10]]\\[-4pt]
# \hline
# &\text{ }\:\:\:\:\:[[arg1//arg2%10*arg2+arg1%arg2]] \\[-4pt]
# -&\text{ }\:\:\:\:\:[[arg1//arg2%10*arg2]]\\[-4pt]
# \hline
# &\text{ }\:\:\:\:\:{\color{salmon}[[arg1%arg2]]}\\[-4pt]
# \end{aligned}
# $$
# You can always check your answer by multiplying the quotient by the divisor and adding the remainder.
#
# <div class="ex-text" align="center">
#
# ${\color{#8DB600}Divisor}$ × ${\color {Salmon}Quotient}$ + ${\color{#21ABCD}Remainder}$ = ${\color{#C4A680}Dividend}$
# </div>
#
# $$
# [[arg2]] \times [[arg1//arg2]] + [[arg1%arg2]] =[[arg1]]
# $$
# </div>
# </div>
#     """
#
#
#     template2 = r"""<div class="ex-yellow">
# <div class="title">
#
# <div class="ex-text" align="center">
#
# $[[arg1]] \div [[arg2]] =?$
#
# </div>
#
# When you solve division questions, you work in reverse. You begin with the **largest** place value first, in this case, the **hundreds** place.
#
# When you come across a step in a long division where the divisor is larger than the current working dividend, you need to put a zero in the quotient.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\text{ }\text{ }\text{ }\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:\!\:{\color {Salmon}0}\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# $$
#
# **Step 1:**
#
# The short way to think is this: How many [[arg2]]s are there in [[arg1//100]]? Since the answer is 0, we move on to the next place value.
#
# **Step 1.1:** How many [[arg2]]s are there in [[arg1//10]]? We estimate [[arg1//10//arg2]] and write it above the tens' place.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:0\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:0{\color {Salmon}[[arg1//10//arg2]]}\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# $$
# **Step 1.2:**  We calculate $[[arg2]] \times  [[arg1//10//arg2]] = [[arg1//10//arg2 * arg2]]$ and write [[arg1//10//arg2 * arg2]] below [[arg1//10]].
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:0[[arg1//10//arg2]]\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:0[[arg1//10//arg2]]\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\!{\color {Salmon} [[arg1//10//arg2 * arg2]]}\:\:}\\[-4pt]
# \hline
# \end{aligned}
# $$
# **Step 1.3:** And we subtract [[arg1//10//arg2 * arg2]] from [[arg1//10]] and then write [[arg1//10 - arg1//10//arg2*arg2]].
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:0[[arg1//10//arg2]]\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\![[arg1//10//arg2 * arg2]]\:\:}\\[-4pt]
# \hline
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:0[[arg1//10//arg2]]\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\![[arg1//10//arg2 * arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:{\color {Salmon}[[arg1//10 - arg1//10//arg2*arg2]]}\\[-4pt]
# \end{aligned}
# $$
# **Step 2:**
#
# **Step 2.1:** We bring down  the number in the ones’ place.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:0[[arg1//10//arg2]]\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\![[arg1//10//arg2 * arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1//10 - arg1//10//arg2*arg2]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:0[[arg1//10//arg2]]\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1//10]]{\color {Salmon}[[arg1%10]]}\\[-4pt]
# &{\:\:\:\![[arg1//10//arg2 * arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1//10 - arg1//10//arg2*arg2]]{\color {Salmon}[[arg1%10]]}\\[-4pt]
# \end{aligned}
# $$
#
# **Step 2.2:** How many [[arg2]]s are there is [[arg1- arg1//10//arg2 * arg2*10]]? We estimate $[[(arg1- arg1//10//arg2 * arg2*10)//arg2]]$ and write it above the one's place.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:0[[arg1//10//arg2]]\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\![[arg1//10//arg2 * arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1- arg1//10//arg2 * arg2*10]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:0[[arg1//10//arg2]]{\color {Salmon}[[(arg1- arg1//10//arg2 * arg2*10)//arg2]]}\text{ }\small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\![[arg1//10//arg2 * arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1- arg1//10//arg2 * arg2*10]]\\[-4pt]
# \end{aligned}
# $$
# **Step 2.3:**  We calculate $[[arg2]] \times [[(arg1- arg1//10//arg2 * arg2*10)//arg2]] = [[arg1//arg2%10*arg2]]$ and write [[arg1//arg2%10*arg2]] below [[arg1- arg1//10//arg2 * arg2*10]].
# $$
# \begin{aligned}
# &\underline{\text{ }\:0[[arg1//arg2]]\text{ }\small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\![[arg1//10//arg2 * arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1- arg1//10//arg2 * arg2*10]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:0[[arg1//arg2]]\text{ }\small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\![[arg1//10//arg2 * arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1- arg1//10//arg2 * arg2*10]]\\[-4pt]
# &\text{ }\:\:\:{\color {Salmon} [[arg1//arg2%10*arg2]]}\\[-4pt]
# \hline
# \end{aligned}
# $$
# **Step 2.4:** And we subtract [[arg1//arg2%10*arg2]] from [[arg1- arg1//10//arg2 * arg2*10]] and then write [[arg1%arg2]].
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:0[[arg1//arg2]]\text{ }\small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\![[arg1//10//arg2 * arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1- arg1//10//arg2 * arg2*10]]\\[-4pt]
# &\text{ }\:\:\:[[arg1//arg2%10*arg2]]\\[-4pt]
# \hline
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:0[[arg1//arg2]]\text{ }\small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\![[arg1//10//arg2 * arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1- arg1//10//arg2 * arg2*10]]\\[-4pt]
# -&\text{ }\:\:\:[[arg1//arg2%10*arg2]]\\[-4pt]
# \hline
# &\text{ }\:\:\:{\color {Salmon}[[arg1%arg2]]}\\[-4pt]
# \end{aligned}
# $$
# **Step 3: Write the remainder near the quotient and check**
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:\:\:[[arg1//arg2]]\small\:{\color{salmon}R\small\,[[arg1%arg2]]}}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\![[arg1//10//arg2 * arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1- arg1//10//arg2 * arg2*10]]\\[-4pt]
# -&\text{ }\:\:\:[[arg1//arg2%10*arg2]]\\[-4pt]
# \hline
# &\text{ }\:\:\:{\color {Salmon}[[arg1%arg2]]}\\[-4pt]
# \end{aligned}
# $$
#
# <div class="ex-text" align="center">
#
# ${\color{#8DB600}Divisor}$ × ${\color {Salmon}Quotient}$ + ${\color{#21ABCD}Remainder}$ = ${\color{#C4A680}Dividend}$
# </div>
#
# $$
# [[arg2]] \times [[arg1//arg2]] + [[arg1%arg2]] = [[arg1//arg2*arg2]] + [[arg1%arg2]] =[[arg1]]
# $$
#
# </div>
# </div>
#     """
#
#     template3 = r"""<div class="ex-yellow">
# <div class="title">
# <div class="ex-text" align="center">
#
# $[[arg1]] \div [[arg2]] =?$
#
# </div>
#
# When you solve division questions, you work in reverse. You begin with the **largest** place value first, in this case, the **hundreds** place.
#
# When you come across a step in a long division where the divisor is larger than the current working dividend, you need to put a zero in the quotient.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\text{ }\text{ }\text{ }\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:\!\:{\color {Salmon}0}\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# $$
#
# **Step 1:**
#
# The short way to think is this: How many  [[arg2]]s are there in [[arg1//100]]? Since the answer is , we move on [[arg1//100//arg2]] to the next place value.
#
# **Step 1.1:** How many [[arg2]]s are there in [[arg1//10]]? We estimate [[arg1//10//arg2]] and write it above the tens' place.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:0\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:0{\color {Salmon}[[arg1//10//arg2]] }\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# $$
# **Step 1.2:**  We calculate $[[arg2]] \times  [[arg1//10//arg2]] = [[arg1//10//arg2*arg2]]$ and write [[arg1//10//arg2*arg2]] below [[arg1//10]].
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:00\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:00\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\!{\color {Salmon} [[arg1//10//arg2*arg2]]}\:\:}\\[-4pt]
# \hline
# \end{aligned}
# $$
# **Step 1.3:** And we subtract [[arg1//10//arg2*arg2]] from [[arg1//10]] and then write [[arg1//10-arg1//10//arg2*arg2]].
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:00\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\! [[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:00\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\! [[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:{\color {Salmon}[[arg1//10-arg1//10//arg2*arg2]]}\\[-4pt]
# \end{aligned}
# $$
# **Step 2:**
#
# **Step 2.1:** We bring down  the number in the ones’ place.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:00\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\! [[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1//10-arg1//10//arg2*arg2]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:00\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\! [[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1//10-arg1//10//arg2*arg2]]{\color {Salmon}[[arg1%10]]}\\[-4pt]
# \end{aligned}
# $$
#
# **Step 2.2:** How many [[arg2]]s are there is [[arg1]]? We estimate $[[arg1//arg2]]$ and write it above the one's place.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:00\text{ }\text{ }\small\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\! [[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//10//arg2*arg2]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:00{\color {Salmon}[[arg1//arg2]]}\text{ }\small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\! [[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//10//arg2*arg2]]\\[-4pt]
# \end{aligned}
# $$
#
# **Step 2.3:**  We calculate $[[arg2]] \times [[arg1//arg2]] = [[arg1//arg2*arg2]]$ and write [[arg1//arg2*arg2]] below [[arg1]].
# $$
# \begin{aligned}
# &\underline{\text{ }\:00[[arg1//arg2]]\text{ }\small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\! [[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//10//arg2*arg2]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:00[[arg1//arg2]]\text{ }\small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\! [[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//10//arg2*arg2]]\\[-4pt]
# &\text{ }\:\:\:{\color {Salmon} [[arg1//arg2*arg2]]}\\[-4pt]
# \hline
# \end{aligned}
# $$
#
# **Step 2.4:** And we subtract [[arg1//arg2*arg2]] from [[arg1-arg1//10//arg2*arg2]] and then write [[arg1%arg2]].
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:00[[arg1//arg2]]\text{ }\small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\! [[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//10//arg2*arg2]]\\[-4pt]
# &\text{ }\:\:\:[[arg1//arg2*arg2]]\\[-4pt]
# \hline
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:00[[arg1//arg2]]\text{ }\small\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# &{\:\:\:\! [[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//10//arg2*arg2]]\\[-4pt]
# -&\text{ }\:\:\:[[arg1//arg2*arg2]]\\[-4pt]
# \hline
# &\text{ }\:\:\:{\color {Salmon}[[arg1%arg2]]}\\[-4pt]
# \end{aligned}
# $$
# **Step 3: Write the remainder near the quotient and check**
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:\:\:2\small\:{\color{salmon}R\small\,[[arg1%arg2]]}}\\[-5pt]
# 42&\big)109\\[-4pt]
# &{\:\:\:\!0\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:[[arg1-arg1//10//arg2*arg2]]\\[-4pt]
# -&\text{ }\:\:\:[[arg1//arg2*arg2]]\\[-4pt]
# \hline
# &\text{ }\:\:\:{\color {Salmon}[[arg1%arg2]]}\\[-4pt]
# \end{aligned}
# $$
#
# <div class="ex-text" align="center">
#
# ${\color{#8DB600}Divisor}$ × ${\color {Salmon}Quotient}$ + ${\color{#21ABCD}Remainder}$ = ${\color{#C4A680}Dividend}$
# </div>
#
# $$
# [[arg2]] \times [[arg1//arg2]]  + [[arg1%arg2]] = [[arg1//arg2*arg2]] + [[arg1%arg2]] = [[arg1]]
# $$
# </div>
# </div>
#
#     """

# args = {'arg1': 232, 'arg2': 4}
# args = {'arg1': 109, 'arg2': 42}
#
# args = {'arg1': 275, 'arg2': 2}
# args = {'arg1': 265, 'arg2': 2}

# args = {'arg1': 265, 'arg2': 189}

#     #solution = KnowledgePoint38Solution()
#     solution = KnowledgePoint38Solution().get_solution(template1, template2, template3, args)
#     print(solution)
#
# main()


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

        # args["num_divisors"] = num_divisors
        # args["denom_divisors"] = denom_divisors
        # args["common_divs"] = common_divs

        # Prepare formatted divisors for template
        args["num_divisors"] = ", ".join(map(str, num_divisors))
        args["denom_divisors"] = ", ".join(map(str, denom_divisors))
        args["common_divs"] = ", ".join(map(str, common_divs))
        args["gcd"] = gcd(arg1, arg2)
        args["simplified_numerator"] = arg1 // gcd(arg1, arg2)
        args["simplified_denominator"] = arg2 // gcd(arg1, arg2)

        return self.custom_format(template, **args)


# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title">
#
# Write the simplified form of the fraction $\large\frac{[[arg1]]}{[[arg2]]}$
#
#
# **Step 1:** List all the numbers that divide the numerator and denominator completely, meaning without leaving any remainder.
#
# $$
# \begin{aligned}
# &[[arg1]]: [[num_divisors]] \\
# &[[arg2]]: [[denom_divisors]] \\
# \end{aligned}
# $$
# **Step 2:** Identify the common factors of both the numerator and denominator.
#
# $$
# \begin{aligned}
# &[[arg1]]: \bold{[[common_divs]]} \\
# &[[arg2]]: \bold{[[common_divs]]} \\
# \end{aligned}
# $$
# **Step 3:** The greatest common divisor (GCD) of two integers is the largest integer that divides each of the integers evenly. We have to divide the numerator and denominator by the largest common factor in this step.
#
# $$
#  \frac{[[arg1]]\color{Salmon}\div[[gcd]]}{[[arg2]]\color{Salmon}\div[[gcd]]} = \frac{{\color{salmon}[[simplified_numerator]]}}{{\color{salmon}[[simplified_denominator]]}}
# $$
# Therefore, the lowest term of $\large\frac{{[[arg1]]}}{{[[arg2]]}}$ is $\large\frac{{[[simplified_numerator]]}}{{[[simplified_denominator]]}}$.
# </div>
# </div>
#         """
#     args = {'arg1': 9, 'arg2': 12}
#     solution = KnowledgePoint39Solution().get_solution(template, args)
#     print(solution)
#
# main()


#############################################################################################


class KnowledgePoint40Solution(SolutionGenerator):
    def get_solution(self, template1: str, template2: str, args: dict) -> str:
        arg1 = args['arg1']
        arg2 = args['arg2']
        args['large_num'] = max(arg1, arg2)
        args['small_num'] = min(arg1, arg2)

        if arg2 < 100:
            return self.custom_format(template1, **args)
        else:
            return self.custom_format(template2, **args)


# def main():
#     start_time = time.time()
#     template1 = r"""
#     <div class="ex-yellow">
# <div class="title">
# <div class="ex-text" align="center">
#
# $[[arg1]] \times [[arg2]] =?$
#
# **Step 1: Organize**
#
# Place the large number (the 4-digit number) above the smaller number (the 2-digit number) with each digit in its corresponding place.
#
# $$
# \begin{array}{l r}
# &{\color{#F1A7DA}thousands}\:\:\:{\color{#C4A680}hundreds}\:\:\:{\color{#21ABCD}tens}\:\:\:{\color{#8DB600}ones}\\
# &{\color{#F1A7DA}[[arg1//1000]]}\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:{\color{#C4A680}[[arg1%1000//100]]}\:\:\:\:\:\:\:\:\:\:\:\:\:\:{\color{#21ABCD}[[arg1%100//10]]}\:\:\:\:\:\:\:\:\:\:{\color{#8DB600}[[arg1%10]]}\:\:\:\\
# \times&{\color{#21ABCD}[[arg2//10]]}\:\:\:\:\:\:\:\:\:\:{\color{#8DB600}[[arg2%10]]}\:\:\:\\
# \hline
# \end{array}
# $$
#
# *Note: Make sure you line them up so the ones places are in a column, and the tens places are in a column.*
#
# **Step 2: Multiply the Ones**
#
# **Step 2.1:** We start by multiplying the one's place column of the lower number by each of the places of the bigger number. Calculate the numbers in the ones place: $[[arg2%10]] \times [[arg1%10]] = [[(arg1%10)*(arg2% 10)]]$. We write down the [[(arg1%10)*(arg2% 10)%10]] ones, carry the $[[(arg1%10)*(arg2%10) //10]]$ tens, and trend it over to the $[[arg1%100//10]]$ tens’ place.
#
# $$
# \begin{array}{l r}
# & {\color{Salmon}\tiny[[(arg1%10)*(arg2%10) //10]] }\:\:\:\\[-3pt]
# &[[arg1//10]]{\color{Salmon}[[arg1%10]]}\\
# \times&[[arg2//10]]{\color{Salmon}[[arg2%10]]}\\
# \hline
# &{\color{Salmon}[[(arg1%10)*(arg2% 10)%10]]}\\
# \end{array}
# $$
# **Step 2.2:** Then calculate the bigger number in the tens digit: $[[arg2%10]] \times [[arg1%100 //10]] = [[(arg2% 10)*(arg1%100//10)]]$. Add the $[[(arg1%10)*(arg2%10) //10]]$  ten you traded to the $[[arg1%100//10]]$ tens' place: $[[(arg2% 10)*(arg1%100//10)]] + [[(arg1%10)*(arg2%10) //10]]  = [[(arg2%10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10]]$. We write down the $[[((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)%10]]$ ones, carry the $[[((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10]]$ ten, and trend it over to the $[[arg1%1000//100]]$ hundred places.
#
# $$
# \begin{array}{l r}
# &{\color{Salmon}\tiny[[((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10]]}\:\:\:\:\:\\[-3pt]
# &[[arg1//100]]{\color{Salmon}[[arg1%100 //10]]}[[arg1% 10]]\\
# \times&[[arg2//10]]{\color{Salmon}[[arg2%10]]}\\
# \hline
# &{\color{Salmon}[[((arg2%10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)%10]]}[[(arg1%10)*(arg2% 10)%10]]\\
# \end{array}
# $$
# **Step 2.3:** Next calculate the bigger number in the hundreds place: $[[arg2%10]] \times [[arg1%1000//100]] = [[(arg1%1000//100)*(arg2%10)]]$. Add the [[((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10]]  ten you traded to the [[arg1\%100 //10]] hundred place: $[[(arg1%1000//100)*(arg2%10)]] + [[((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10]] = [[(((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10)+(arg1%1000//100)*(arg2%10)]]$. We write down the $[[(((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10+(arg1%1000//100)*(arg2%10))%10]]$ ones, carry the $[[(((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10+(arg1%1000//100)*(arg2%10))//10]]$ tens, and trend it over to the $[[arg1//1000]]$ thousand’s place.
#
# $$
# \begin{array}{l r}
# &{\color{Salmon}\tiny[[(((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10+(arg1%1000//100)*(arg2%10))//10]]}\:\:\:\:\:\:\,\,\\[-3pt]
# &[[arg1//1000]]{\color{Salmon}[[arg1%1000//100]]}[[arg1%100]]\\
# \times&[[arg2//10]]{\color{Salmon}[[arg2%10]]}\\
# \hline
# &{\color{Salmon}[[(((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10+(arg1%1000//100)*(arg2%10))%10]]}[[arg2%10*arg1%100]]\\
# \end{array}
# $$
#
#
# **Step 2.4:** Finally calculate the bigger number in the thousand's place: $[[arg2%10]] \times [[arg1//1000]] = [[(arg2%10)*(arg1//1000)]]$. Add the $[[(((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10+(arg1%1000//100)*(arg2%10))//10]]$ ten you traded to the [[arg1//1000]] thousand’s place: $[[(arg2%10)*(arg1//1000)]] + [[(((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10+(arg1%1000//100)*(arg2%10))//10]] = [[(((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10+(arg1%1000//100)*(arg2%10))//10 + (arg2%10)*(arg1//1000)]]$. We write down the $[[(((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10+(arg1%1000//100)*(arg2%10))//10 + (arg2%10)*(arg1//1000)]]$.
#
# $$
# \begin{array}{l r}
# &{\color{Salmon}[[arg1//1000]]}[[arg1%1000]]\\
# \times&[[arg2//10]]{\color{Salmon}[[arg2%10]]}\\
# \hline
# &{\color{Salmon}[[(((arg2% 10)*(arg1%100//10) + (arg1%10)*(arg2% 10) //10)//10+(arg1%1000//100)*(arg2%10))//10 + (arg2%10)*(arg1//1000)]]}[[arg2%10*arg1%1000]]\\
# \end{array}
# $$
#
# **Step 3: Multiply the Tens**
#
# **Step 3.1:** First, let’s add a zero down the one's column before we move on to the tens column. This will help us not get confused over where the numbers for the tens multiplications start on this new line.
#
# $$
# \begin{array}{l r}
# &[[arg1]]\\
# \times&[[arg2]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}0}\\
# \end{array}
# $$
#
# **Step 3.2:** Then we multiply the bottom tens place number with the ones place number in the top number. In our example, that’s $[[arg2//10]] \times [[arg1%10]] = [[(arg2//10) * (arg1%10)]]$.  We write down the $[[(arg2//10)*(arg1%10)%10]]$ ones, carry the $[[(arg2//10)*(arg1%10)//10]]$ ones tens, and trend it over to the [[arg1%100//10]] tens’ place.
#
# $$
# \begin{array}{l r}
# & {\color{Salmon}\tiny[[(arg2//10)*(arg1%10)//10]]}\:\:\:\\[-3pt]
# &[[arg1//10]]{\color{Salmon}[[arg1%10]]}\\
# \times&{\color{Salmon}[[arg2//10]]}[[arg2%10]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}[[(arg2//10)*(arg1%10)%10]]}0\\
# \end{array}
# $$
#
# **Step 3.3:** Next is the tens place turn. We multiply $[[arg2//10]] \times  [[arg1%100 //10]] = [[(arg2//10) * (arg1%100 //10)]]$. Add the 1 ten you traded to the $[[arg1%100//10]]$ tens' place: $[[(arg2//10) * (arg1%100 //10)]] + [[(arg2//10)*(arg1%10)//10]] = [[(arg2//10)*(arg1%10)//10 + ((arg2//10) * (arg1%100 //10))]]$. We write down the $[[(arg2//10)*(arg1%10)//10 + ((arg2//10) * (arg1%100 //10))]]$.
#
# $$
# \begin{array}{l r}
# &[[arg1//100]]{\color{Salmon}[[arg1%100 //10]]}[[arg1%10]]\\
# \times&{\color{Salmon}[[arg2//10]]}[[arg2%10]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}[[(arg2//10)*(arg1%10)//10 + ((arg2//10) * (arg1%100 //10))]]}[[(arg2//10) * (arg1%10)%10]]0\\
# \end{array}
# $$
# **Step 3.4:** We need to multiply the tens value number on the bottom number with the hundreds place number in the top number. That is $[[arg2//10]] \times [[arg1%1000//100]] = [[(arg1%1000//100)*(arg2//10)]]$. Write down the $[[(arg1%1000//100)*(arg2//10)%10]]$ ones, carry the $[[(arg1%1000//100)*(arg2//10)//10]]$  ten, and trend it over to the [[arg1//1000]] thousand’s place.
#
# $$
# \begin{array}{l r}
# &{\color{Salmon}\tiny[[(arg1%1000//100)*(arg2//10)//10]]}\:\:\:\:\:\:\,\,\\[-3pt]
# &[[arg1//1000]]{\color{Salmon}[[arg1%1000//100]]}[[arg1%100]]\\
# \times&{\color{Salmon}[[arg2//10]]}[[arg2%10]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}[[(arg2//10) * (arg1%1000//100)%10]]}[[arg2//10*arg1%100]]0\\
# \end{array}
# $$
# **Step 3.5:** Finally, we need to multiply the tens value number on the bottom number with the thousands place number in the top number. That is $[[arg2//10]] \times [[arg1//1000]] = [[(arg2//10)*(arg1//1000)]]$. Add the [[(arg1%1000//100)*(arg2//10)//10]] ten you traded to the [[arg1//1000]] thousand’s place: $[[(arg2//10)*(arg1//1000)]] + [[(arg1%1000//100)*(arg2//10)//10]] = [[(arg1%1000//100)*(arg2//10)//10 + ((arg2//10)*(arg1//1000))]]$. We write down the $[[(arg1%1000//100)*(arg2//10)//10 + ((arg2//10)*(arg1//1000))]]$.
#
# $$
# \begin{array}{l r}
# &{\color{Salmon}[[arg1//1000]]}[[arg1%1000]]\\
# \times&{\color{Salmon}[[arg2//10]]}[[arg2%10]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}[[(arg1%1000//100)*(arg2//10)//10 + ((arg2//10)*(arg1//1000))]]}[[(arg2//10) * (arg1%1000//100)%10]][[arg2//10*arg1%100]]0\\
# \end{array}
# $$
# **Step 4: Add two Numbers**
#
# From here on, we add the two partial products together: $[[arg1*(arg2%10)]]$ is the partial product in the ones column and $[[arg1*(arg2//10)*10]]$ is the partial product in the tens column. We combine both partial products: $[[arg1*(arg2%10)]] + [[arg1*(arg2//10)*10]] = [[arg1*(arg2%10) + arg1*(arg2//10)*10]]$. This is our final product.
#
# $$
# \begin{array}{l r}
# &[[arg1]]\\
# \times&[[arg2]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# +&[[arg1*(arg2//10)]]0\\
# \hline
# &{\color{Salmon}[[arg1*arg2]]}\\
# \end{array}
# $$
# So the answer is $[[arg1*arg2]]$.
# </div>
# </div>
# #     """
#
#     template2 = r"""<div class="ex-red">
# <div class="title">
# <div class="ex-text" align="center">=
#
# $[[arg1]] \times [[arg2]] =?$
#
# **Step 1: Organize**
#
# Place the large number (the 4-digit number) above the smaller number (the 2-digit number) with each digit in its corresponding place.
#
# $$
# \begin{array}{l r}
# &{\color{#F1A7DA}thousands}\:\:\:{\color{#C4A680}hundreds}\:\:\:{\color{#21ABCD}tens}\:\:\:{\color{#8DB600}ones}\\
# &{\color{#F1A7DA}[[arg1//1000]]}\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:{\color{#C4A680}[[arg1%1000//100]]}\:\:\:\:\:\:\:\:\:\:\:\:\:\:{\color{#21ABCD}[[arg1%100//10]]}\:\:\:\:\:\:\:\:\:\:{\color{#8DB600}[[arg1%10]]}\:\:\:\\
# \times&{\color{#C4A680}[[arg2//100]]}\:\:\:\:\:\:\:\:\:\:\:\:\:\:{\color{#21ABCD}[[arg2%100//10]]}\:\:\:\:\:\:\:\:\:\:{\color{#8DB600}[[arg2%10]]}\:\:\:\\
# \hline
# \end{array}
# $$
#
# *Note: Make sure you line them up so the ones places are in a column, and the tens places are in a column.*
#
# **Step 2: Multiply the Ones**
#
# **Step 2.1:** We start by multiplying the one's place column of the lower number by each of the places of the bigger number. Calculate the numbers in the ones place: $[[arg2%10]] \times [[arg1%10]] = [[(arg1%10)*(arg2% 10)]]$. We Write down the [[(arg1%10)*(arg2% 10)]] ones.
#
# $$
# \begin{array}{l r}
# &[[arg1//10]]{\color{Salmon}[[arg1%10]]}\\
# \times&[[arg2//10]]{\color{Salmon}[[arg2%10]]}\\
# \hline
# &{\color{Salmon}[[(arg1%10)*(arg2%10)]]}\\
# \end{array}
# $$
# **Step 2.2:** Then calculate the bigger number in the tens digit: $[[arg2%10]] \times [[arg1%100 //10]] = [[(arg2% 10)*(arg1%100//10)]]$. We Write down the [[(arg2% 10)*(arg1%100//10)]] ones.
#
# $$
# \begin{array}{l r}
# &[[arg1//100]]{\color{Salmon}[[arg1%100 //10]]}[[arg1% 10]]\\
# \times&[[arg2//10]]{\color{Salmon}[[arg2%10]]}\\
# \hline
# &{\color{Salmon}[[(arg2%10)*(arg1%100//10)]]}[[(arg1%10)*(arg2%10)]]\\
# \end{array}
# $$
# **Step 2.3:** Next calculate the bigger number in the hundreds place: $[[arg2%10]] \times [[arg1%1000//100]] = [[(arg1%1000//100)*(arg2%10)]]$. We Write down the $[[(arg1%1000//100)*(arg2%10)]]$ ones.
#
# $$
# \begin{array}{l r}
# &[[arg1//1000]]{\color{Salmon}[[arg1%1000//100]]}[[arg1%100]]\\
# \times&[[arg2//10]]{\color{Salmon}[[arg2%10]]}\\
# \hline
# &{\color{Salmon}[[(arg1%1000//100)*(arg2%10)]]}[[arg1*(arg2%10)%100]]\\
# \end{array}
# $$
# **Step 2.4:** Finally calculate the bigger number in the thousand's place:  $[[arg2%10]] \times [[arg1//1000]] = [[(arg2%10)*(arg1//1000)]]$. We Write down the $[[(arg2%10)*(arg1//1000)]]$ ones.
#
# $$
# \begin{array}{l r}
# &{\color{Salmon}[[arg1//1000]]}[[arg1%1000]]\\
# \times&[[arg2//10]]{\color{Salmon}[[arg2%10]]}\\
# \hline
# &{\color{Salmon}[[(arg2%10)*(arg1//1000)]]}[[arg2%10*arg1%1000]]\\
# \end{array}
# $$
# **Step 3: Multiply the Tens**
#
# **Step 3.1:** First, let’s add a zero down the one's column before we move on to the tens column. This will help us not get confused over where the numbers for the tens multiplications start on this new line.
#
# $$
# \begin{array}{l r}
# &[[arg1]]\\
# \times&[[arg2]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}0}\\
# \end{array}
# $$
#
# **Step 3.2:** Likewise, what happened to multiplying ones will occur to tens,  corresponding to the multiplication of: $[[arg2%100//10]] \times [[arg1%10]] = [[arg2%100//10*(arg1%10)]]$, $[[arg2%100//10]] \times [[arg1%100//10]] = [[arg2%100//10*(arg1%100//10)]]$, $[[arg2%100//10]] \times [[arg1%1000//100]] = [[arg2%100//10*(arg1%1000//100)]]$, $[[arg2%100//10]] \times [[arg1%10]] = [[arg2%100//10*(arg1%10)]]$.
# $$
# \begin{array}{l r}
# &{\color{Salmon}[[arg1]]}\\
# \times&[[arg2//100]]{\color{Salmon}[[arg2%100//10]]}[[arg2%10]]\\
# \hline
# &[[arg1*(arg2%10)]]\\
# &{\color{Salmon}[[(arg2%100//10)*arg1]]}0\\
# \end{array}
# $$
#
# **Step 4: Multiply the Hundreds**
#
# **Step 4.1:** First, let’s add two zeros down the one’s and ten’s columns before we move on to the ten columns. This will help us not get confused over where the numbers for the hundred multiplications start on this new line.
# $$
# \begin{array}{l r}
# &[[arg1]]\\
# \times&[[arg2]]\\
# \hline
# &[[arg2%10*arg1]]\\
# &[[arg2%100//10*arg1]]0\\
# &{\color{Salmon}00}\\
# \end{array}
# $$
#
# We will proceed with multiplying the hundreds' place column of the lower number by each of the places of the bigger number.
#
# **Step 4.2:** Then we multiply the bottom hundreds place number with the ones place number in the top number. In our example, that’s $[[arg2//100]] \times [[arg1%10]] = [[arg1%10*(arg2//100)]]$. We write down the [[arg1%10*(arg2//100)]] ones.
# $$
# \begin{array}{l r}
# &[[arg1//10]]{\color{Salmon}[[arg1%10]]}\\
# \times&{\color{Salmon}[[arg2//100]]}[[arg2%100]]\\
# \hline
# &[[arg2%10*arg1]]\\
# &[[arg2%100//10*arg1]]0\\
# &{\color{Salmon}[[arg1%10*(arg2//100)]]}00\\
# \end{array}
# $$
# **Step 4.3:** Next is the tens place turn. We multiply $[[arg2//100]] \times [[arg1%100//10]] = [[arg1%100//10*(arg2//100)]]$. We write down the [[arg1%100//10*(arg2//100)]].
#
# $$
# \begin{array}{l r}
# &[[arg1//100]]{\color{Salmon}[[arg1%100//10]]}[[arg1%10]]\\
# \times&{\color{Salmon}[[arg2//100]]}[[arg2%100]]\\
# \hline
# &[[arg2%10*arg1]]\\
# &[[arg2%100//10*arg1]]0\\
# &{\color{Salmon}[[arg1%100//10*(arg2//100)]]}[[arg1%10*(arg2//100)]]00\\
# \end{array}
# $$
#
# **Step 4.4:** We need to multiply the hundreds value number on the bottom number with the hundreds place number in the top number. That is $[[arg2//100]] \times [[arg1%1000//100]] = [[arg1%1000//100*(arg2//100)]]$. Write down the [[arg1%1000//100*(arg2//100)]].
#
# $$
# \begin{array}{l r}
# &[[arg1//100]]{\color{Salmon}[[arg1%1000//100]]}[[arg1%100]]\\
# \times&{\color{Salmon}[[arg2//100]]}[[arg2%100]]\\
# \hline
# &[[arg2%10*arg1]]\\
# &[[arg2%100//10*arg1]]0\\
# &{\color{Salmon}[[arg1%1000//100*(arg2//100)]]}[[arg1%100//10*(arg2//100)]][[arg1%10*(arg2//100)]]00\\
# \end{array}
# $$
#
# **Step 4.5:** Finally calculate the bigger number in the thousand's place: $[[arg2//100]] \times [[arg1//1000]] = [[arg1//1000*(arg2//100)]]$. We write down the [[arg1//1000*(arg2//100)]].
# $$
# \begin{array}{l r}
# &{\color{Salmon}[[arg1//1000]]}[[arg1%1000]]\\
# \times&{\color{Salmon}[[arg2//100]]}[[arg2%100]]\\
# \hline
# &[[arg2%10*arg1]]\\
# &[[arg2%100//10*arg1]]0\\
# &{\color{Salmon}[[arg1//1000*(arg2//100)]]}[[arg1*(arg2//100)%1000]]00\\
# \end{array}
# $$
# **Step 5: Add three Numbers**
#
# From here on, we add the three partial products together: We combine these three partial products: $[[arg2%10*arg1]] + [[arg2%100//10*arg1*10]] + [[arg2//100*arg1*100]] = [[arg2%10*arg1 + arg2%100//10*arg1*10 + arg2//100*arg1*100]]$. This is our final product.
# $$
# \begin{array}{l r}
# &[[arg1]]\\
# \times&[[arg2]]\\
# \hline
# &[[arg2%10*arg1]]\\
# &[[arg2%100//10*arg1*10]]\\
# +&[[arg2//100*arg1*100]]\\
# \hline
# &{\color{Salmon}[[arg1*arg2]]}\\
# \end{array}
# $$
# So the answer is $[[arg1*arg2]]$.
# </div>
# </div>
#     """
#
#     args = {'arg1': 1432, 'arg2': 211}
#     #args = {'arg1': 1536, 'arg2': 25}
#     solution = KnowledgePoint40Solution().get_solution(template1, template2, args)
#     print(solution)
#
# main()
#
#
#


###############################################################################
class KnowledgePoint41Solution(SolutionGenerator):
    def get_solution(self, template1: str, template2: str, args: dict) -> str:
        # Extract arguments
        arg1 = args['arg1']
        arg2 = args['arg2']

        def count_digits(num):
            return len(str(num))

        result_digits = count_digits(arg1 // arg2)

        # Select the appropriate template
        if result_digits == 2:
            template = template1
        elif result_digits == 1:
            template = template2
        else:
            raise ValueError("Unsupported number of digits")

        # Format the template with arguments
        return self.custom_format(template, **args)


# def main():
#     start_time = time.time()
#     template1 = r"""<div class="ex-yellow">
# <div class="title">
# <div class="ex-text" align="center">
#
# $[[arg1]] \div [[arg2]] =?$
#
# When you solve division questions, you work in reverse. You begin with the **largest** place value.
#
# When you come across a step in a long division where the divisor is larger than the current working dividend, you need to put a zero in the quotient.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\text{ }\text{ }\text{ }\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:\!\:{\color {Salmon}0}\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# $$
# **Step 1:**
#
# The short way to think is this: How many [[arg2]]s are there in [[arg1//1000]]? Since the answer is 0, we move on to the next place value.
#
# **Step 1.1:** How many [[arg2]]s are there in [[arg1//100]]? We estimate [[arg1//100//arg2]] and write it above the tens' place.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:0\text{ }\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:0{\color {Salmon}[[arg1//100//arg2]]}\text{ }\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# $$
#
# **Step 2:**
#
# **Step 2.1:** How many [[arg2]]s are there in [[arg1//10]]? We estimate [[arg1//10//arg2]] and write it above the ten's place.
# $$
# \begin{aligned}
# &\underline{\text{ }\:00\text{ }\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:00{\color {Salmon}[[arg1//10//arg2]]}\text{ }\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# $$
#
# **Step 2.2:**  We calculate $[[arg1//10//arg2]] \times [[arg2]] = [[arg1//10//arg2*arg2]]$ and write [[arg1//10//arg2*arg2]] below [[arg1//10]].
# $$
# \begin{aligned}
# &\underline{\text{ }\:00[[arg1//10//arg2]]\text{ }\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:00[[arg1//10//arg2]]\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# -&{\:\:\:{\color {Salmon}[[arg1//10//arg2*arg2]]}\:\:}\\[-4pt]
# \hline
# \end{aligned}
# $$
# **Step 2.3:** And we subtract [[arg1//10//arg2*arg2]] from [[arg1//10]] and then write [[arg1//10-arg1//10//arg2*arg2]].
# $$
# \begin{aligned}
# &\underline{\text{ }\:00[[arg1//10//arg2]]\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# -&{\:\:\:[[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:00[[arg1//10//arg2]]\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# -&{\:\:\:[[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &{\:\:\:\:{\color {Salmon}[[arg1//10-arg1//10//arg2*arg2]]}\:\:}\\[-4pt]
# \end{aligned}
# $$
# **Step 3:**
#
# **Step 3.1:** How many [[arg2]]s are there in [[arg1-arg1//10//arg2*arg2*10]]? We estimate [[(arg1-arg1//10//arg2*arg2*10)//arg2]] and write it above the one's place.
# $$
# \begin{aligned}
# &\underline{\text{ }\:00[[arg1//10//arg2]]\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# -&{\:\:\:[[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &{\:\:\:\:[[arg1//10-arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:00[[arg1//10//arg2]]{\color {Salmon} [[(arg1-arg1//10//arg2*arg2*10)//arg2]]}\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# -&{\:\:\:[[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &{\:\:\:\:[[arg1-arg1//10//arg2*arg2*10]]\:\:}\\[-4pt]
# \end{aligned}
# $$
#
# **Step 3.2:**  We calculate $[[(arg1-arg1//10//arg2*arg2*10)//arg2]] \times [[arg2]] = [[arg1//arg2%10*arg2]]$ and write [[arg1//arg2%10*arg2]] below [[arg1-arg1//10//arg2*arg2*10]].
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:00[[arg1//arg2]]\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# -&{\:\:\:[[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &{\:\:\:\:[[arg1-arg1//10//arg2*arg2*10]]\:\:}\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:00[[arg1//arg2]]\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# -&{\:\:\:[[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &{\:\:\:\:[[arg1-arg1//10//arg2*arg2*10]]\:\:}\\[-4pt]
# -&{\:\:\:\:{\color {Salmon}[[arg1//arg2%10*arg2]]}\:\:}\\[-4pt]
# \hline
# \end{aligned}
# $$
# **Step 3.3:** And we subtract $[[arg1//arg2%10*arg2]]$ from [[arg1-arg1//10//arg2*arg2*10]] and then write $[[arg1%arg2]]$.
# $$
# \begin{aligned}
# &\underline{\text{ }\:00[[arg1//arg2]]\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# -&{\:\:\:[[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &{\:\:\:\:[[arg1-arg1//10//arg2*arg2*10]]\:\:}\\[-4pt]
# -&{\:\:\:\:[[arg1//arg2%10*arg2]]\:\:}\\[-4pt]
# \hline
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:00[[arg1//arg2]]\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# -&{\:\:\:[[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &{\:\:\:\:[[arg1-arg1//10//arg2*arg2*10]]\:\:}\\[-4pt]
# -&{\:\:\:\:[[arg1//arg2%10*arg2]]\:\:}\\[-4pt]
# \hline
# &{\:\:\:\:\:\:\:\:\!{\color {Salmon}[[arg1%arg2]]}\:\:}\\[-4pt]
# \end{aligned}
# $$
# **Step 4: Write the remainder near the quotient and check**
# $$
# \begin{aligned}
# &\underline{\text{ }\:\:\:\:\:[[arg1//arg2]]\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# -&{\:\:\:[[arg1//10//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &{\:\:\:\:[[arg1-arg1//10//arg2*arg2*10]]\:\:}\\[-4pt]
# -&{\:\:\:\:[[arg1//arg2%10*arg2]]\:\:}\\[-4pt]
# \hline
# &{\:\:\:\:\:\:\:\:\![[arg1%arg2]]\:\:}\\[-4pt]
# \end{aligned}
# $$
# <div class="ex-text" align="center">
#
# ${\color{#8DB600}Divisor}$ × ${\color {Salmon}Quotient}$ + ${\color{#21ABCD}Remainder}$ = ${\color{#C4A680}Dividend}$
# </div>
#
# $$
# [[arg1//arg2]] \times [[arg2]] + [[arg1%arg2]] = [[arg1]]
# $$
# </div>
# </div>
#         """
#
#     template2 = r"""<div class="ex-yellow">
# <div class="title">
# <div class="ex-text" align="center">
#
# $[[arg1]] \div [[arg2]] =?$
#
# When you solve division questions, you work in reverse. You begin with the **largest** place value.
#
# When you come across a step in a long division where the divisor is larger than the current working dividend, you need to put a zero in the quotient.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\text{ }\text{ }\text{ }\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:\!\:{\color {Salmon}0}\text{ }\text{ }\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# $$
# **Step 1:**
#
# The short way to think is this: How many [[arg2]]s are there in [[arg1//100]]? Since the answer is 0, we move on to the next place value.
#
# **Step 1.1:** How many [[arg2]]s are there in [[arg1//100]]? We estimate [[arg1//100//arg2]] and write it above the tens' place.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:0\text{ }\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:0{\color {Salmon}[[arg1//100//arg2]]}\text{ }\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# $$
#
# **Step 2:**
#
# **Step 2.1:** How many [[arg2]]s are there in [[arg1//10]]? We estimate [[arg1//10//arg2]] and write it above the ten's place.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:00\text{ }\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:00{\color {Salmon}[[arg1//100//arg2]]}\text{ }\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# $$
#
# **Step 3:**
#
# **Step 3.1:** How many [[arg2]]s are there in [[arg1]]? We estimate [[arg1//arg2]] and write it above the ten's place.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:000\text{ }\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:000{\color {Salmon}[[arg1//arg2]]}\text{ }\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# $$
#
# **Step 3.2:**  We calculate $[[arg1//arg2]] \times [[arg2]] = [[arg1//arg2*arg2]]$ and write [[arg1//arg2*arg2]] below [[arg1]].
#
# $$
# \begin{aligned}
# &\underline{\text{ }\:000[[arg1//arg2]]\text{ }\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:000[[arg1//arg2]]\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# -&{\:\:{\color {Salmon}[[arg1//arg2*arg2]]}\:\:}\\[-4pt]
# \hline
# \end{aligned}
# $$
#
# **Step 3.3:** And we subtract [[arg1//arg2*arg2]] from [[arg1]] and then write [[arg1%arg2]].
# $$
# \begin{aligned}
# &\underline{\text{ }\:000[[arg1//arg2]]\text{ }\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\:000[[arg1//arg2]]\text{ }\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# -&{\:\:{\color {Salmon}[[arg1//arg2*arg2]]}\:\:}\\[-4pt]
# \hline
# &{\:\:\:\:\:\:\:\:{\color {Salmon}[[arg1%arg2]]}\:\:}\\[-4pt]
# \end{aligned}
# $$
#
#
# **Step 4: Write the remainder near the quotient and check**
# $$
# \begin{aligned}
# &\underline{\text{ }\:\:\:\:\:\:\:[[arg1//arg2]]\:\:\small\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# -&{\:\:[[arg1//arg2*arg2]]\:\:}\\[-4pt]
# \hline
# &{\:\:\:\:\:\:\:\:\:\![[arg1%arg2]]\:\:}\\[-4pt]
# \end{aligned}
# $$
# <div class="ex-text" align="center">
#
# ${\color{#8DB600}Divisor}$ × ${\color {Salmon}Quotient}$ + ${\color{#21ABCD}Remainder}$ = ${\color{#C4A680}Dividend}$
# </div>
#
# $$
# [[arg1//arg2]] \times [[arg2]] + [[arg1%arg2]] = [[arg1]]
# $$
# </div>
# </div>
#     """
#
#     ##template2: answer is a 2-digit number
#     #args = {'arg1': 1750, 'arg2': 125}
#     args = {'arg1': 1080, 'arg2': 31}
#
#     ##template2: answer is a 1-digit number
#     # args = {'arg1': 1073, 'arg2': 134}
#
#     solution = KnowledgePoint41Solution().get_solution(template1, template2, args)
#     print(solution)
#
# main()


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


#
# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title">
#
# Write the simplified form of the fraction $\large\frac{[[arg1]]}{[[arg2]]}$
#
#
# **Step 1:** List all the numbers that divide the numerator and denominator completely, meaning without leaving any remainder.
#
# $$
# \begin{aligned}
# &[[arg1]]: [[num_divisors]] \\
# &[[arg2]]: [[denom_divisors]] \\
# \end{aligned}
# $$
# **Step 2:** Identify the common factors of both the numerator and denominator.
#
# $$
# \begin{aligned}
# &[[arg1]]: \bold{[[common_divs]]} \\
# &[[arg2]]: \bold{[[common_divs]]} \\
# \end{aligned}
# $$
# **Step 3:** The greatest common divisor (GCD) of two integers is the largest integer that divides each of the integers evenly. We have to divide the numerator and denominator by the largest common factor in this step.
#
# $$
#  \frac{[[arg1]]\color{Salmon}\div[[gcd]]}{[[arg2]]\color{Salmon}\div[[gcd]]} = \frac{{\color{salmon}[[simplified_numerator]]}}{{\color{salmon}[[simplified_denominator]]}}$$
# Therefore, the lowest term of $\large\frac{{[[arg1]]}}{{[[arg2]]}}$ is $\large\frac{{[[simplified_numerator]]}}{{[[simplified_denominator]]}}$.
# </div>
# </div>
#         """
#     args = {'arg1': 24, 'arg2': 36}
#
#     solution = KnowledgePoint42Solution().get_solution(template, args)
#     print(solution)
#
# main()


######################################################################################
# class KnowledgePoint43Solution(SolutionGenerator):
#     def get_solution(self, template: str, args: dict) -> str:
#         arg1 = args['arg1']
#         args['float_arg1'] = float(arg1)
#         return self.custom_format(template, **args)
# #
# def main():
#     template1 = r"""<div class="ex-yellow">...</div>"""
#     template2 = r"""<div class="ex-yellow">...</div>"""
#
#     args = {'arg1': 3, 'arg2': 4}
#
#     decimal = args['arg1'] / args['arg2']
#
#     def count_decimal_digits(num):
#         str_num = str(num)
#         if '.' in str_num:
#             return len(str_num.split('.')[1])
#         else:
#             return 0
#
#     decimal_digits = count_decimal_digits(decimal)
#     # print(decimal_digits)
#
#     if decimal_digits == 1:
#         template = template1
#     if decimal_digits == 2:
#         template = template2
#
#     solution = KnowledgePoint43Solution().get_solution(template, args)
#     print(solution)
#
# main()


#######################################################################################


class KnowledgePoint43Solution(SolutionGenerator):
    def get_solution(self, template1: str, template2: str, args: dict) -> str:
        # Extract arguments
        arg1 = args['arg1']
        arg2 = args['arg2']

        # Compute the division result
        decimal = arg1 / arg2
        args['float_arg1'] = float(arg1)

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
            template = template1
        elif decimal_digits == 2:
            template = template2
        else:
            raise ValueError("Unsupported number of decimal digits")

        # Format the template with arguments
        return self.custom_format(template, **args)


#
# def main():
#     start_time = time.time()
#     template1 = r"""<div class="ex-yellow">
# <div class="title">
#
# <div class="ex-text" align="center">
#
# $\frac{[[arg1]]}{[[arg2]]} =?$
#
#
# We start by placing the divisor, [[arg2]]. Outside the division bracket, and the dividend, [[arg1]].
#
# $$
# \begin{aligned}
# &\underline{\text{ }\text{ }\text{ }\text{ }\text{ }\small}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# $$
# **Step 1:** We notice that [[arg1]] can't be divided evenly by [[arg2]], which means our answer will be a number smaller than 1. Since we can't find a whole number answer for this problem, we need to add a decimal point and a zero after [[arg1]] to make it [[float_arg1]]. Similarly, we add a decimal point to the quotient.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\text{ }\text{ }\text{ }\text{ }\small}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\:\:{\color {Salmon} 0}{\color {Salmon}.}\:\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]{\color {Salmon}.}{\color {Salmon}0}\\[-4pt]
# \end{aligned}
# $$
#
#
# **Step 2:** To make it easier to understand and calculate, we treat '[[float_arg1]]' as '[[arg1*10]]' when dividing. How many times does [[arg2]] go into [[arg1*10]]? $[[arg2]]\times[[arg1*10//arg2]] = [[arg1*10//arg2*arg2]]$, we place the number [[arg1*10//arg2]] in the quotient, next to the decimal point. We then write [[arg1*10//arg2*arg2]] below the dividend and subtract to get the remainder, which is [[arg1*10%arg2]]. Since we have no leftovers, we have finished the calculation.
#
# $$
# \begin{aligned}
# &\underline{\:\:0.\:\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[float_arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\:\,0.{\color {Salmon} [[arg1*10//arg2]] }\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\:0\\[-4pt]
# -&{\:\:{\color {Salmon} [[arg1*10//arg2*arg2//10]]}{\:\:\!\color {Salmon} [[arg1*10//arg2*arg2%10]]}\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:{\:\:\!\color {Salmon} [[arg1*10%arg2]]}\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# [[arg1/arg2]]
# $$
#
# Therefore, the final solution is [[arg1/arg2]].
#
# **Tips:** Another way to convert the fraction to a decimal is to use the concept of place value. The number [[arg1]] has one digit and no tenths, so we write it as [[float_arg1]].
#
# When we move the decimal point one place to the left, the 6 stays in the same place and the decimal point moves one place to the left, so we get [[arg1/arg2]].
#
# $$
# \begin{aligned}
# \frac{[[arg1]]}{[[arg2]]}
# \:\:\:\longrightarrow    \:\:
# [[arg1]]\div[[arg2]]
# \:\:\:\longrightarrow    \:\:
# [[arg1/arg2]]
# \end{aligned}
# $$
#
# </div>
# </div>
#         """
#     template2 = r"""
#     <div class="ex-yellow">
# <div class="title">
#
# <div class="ex-text" align="center">
#
# $\frac{[[arg1]]}{[[arg2]]} =?$
#
# We start by placing the divisor, [[arg2]]. Outside the division bracket, and the dividend, [[arg1]].
#
# $$
# \begin{aligned}
# &\underline{\text{ }\text{ }\text{ }\text{ }\text{ }\small}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# $$
# **Step 1:** We notice that [[arg1]] can't be divided evenly by [[arg2]], which means our answer will be a number smaller than 1. Since we can't find a whole number answer for this problem, we need to add a decimal point and a zero after [[arg1]] to make it [[float_arg1]]. Similarly, we add a decimal point to the quotient.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\text{ }\text{ }\text{ }\text{ }\small}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\:\:{\color {Salmon} 0}{\color {Salmon}.}\:\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]{\color {Salmon}.}{\color {Salmon}0}\\[-4pt]
# \end{aligned}
# $$
#
# **Step 2:** To make it easier to understand and calculate, we treat '[[float_arg1]]' as '[[arg1*10]]' when dividing. How many times does [[arg2]] go into [[arg1*10]]? $[[arg2]]\times[[arg1*10//arg2]] = [[arg1*10//arg2*arg2]]$, we place the number [[arg1*10//arg2]] in the quotient, next to the decimal point. We then write [[arg1*10//arg2*arg2]] below the dividend and subtract to get the remainder, which is [[arg1*10%arg2]].
#
# $$
# \begin{aligned}
# &\underline{\:\:0.\:\:\:\:}\\[-5pt]
# [[arg2]]&\big)[[float_arg1]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\:\,0.{\color {Salmon} [[arg1*10//arg2]] }\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\:0\\[-4pt]
# -&{\:\:{\color {Salmon} [[arg1*10//arg2*arg2//10]]}{\:\:\!\color {Salmon} [[arg1*10//arg2*arg2%10]]}\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:{\:\:\!\color {Salmon} [[arg1*10%arg2]]}\\[-4pt]
# \end{aligned}
# $$
#
# **Step 3:** Since we obtained a non-zero remainder in the previous step, the calculation isn't complete. Because the remainder [[arg1*10%arg2]] can't be divided evenly by [[arg2]], we need to form a new number to continue the division process. To do this, we take the last digit of the dividend, which is 0, and write it next to the [[arg1*10%arg2]], starting to work with this [[arg1*10%arg2*10]].
#
# $$
# \begin{aligned}
# &\underline{\:\,0.{ [[arg1*10//arg2]] }\:}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\:0\\[-4pt]
# -&{\:\:{[[arg1*10//arg2*arg2//10]]}{\:\:\! [[arg1*10//arg2*arg2%10]]}\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:{\:\:\! [[arg1*10%arg2]]}\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\,0.[[arg1*10//arg2]] \text{ }\text{ }}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\:0{\color {Salmon} 0}\\[-4pt]
# &{\:\:[[arg1*10//arg2*arg2//10]]\:[[arg1*10//arg2*arg2%10]]\!\:\small{\downarrow}\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:\:[[arg1*10%arg2]]{\color {Salmon} 0}\:\\[-4pt]
# \end{aligned}
# $$
# *Note: In step 1, we attempted to divide $[[float_arg1]]$ by [[arg2]]. During this process, we encountered a remainder of [[arg1*10%arg2]]. To continue our division, we appended a zero to the $[[float_arg1]]$ (noting that adding a zero after a decimal doesn't change the value of the number itself). We then brought this zero down and placed it after the [[arg1*10%arg2]], turning it into [[arg1*10%arg2*10]]. This allowed us to continue the division until there was no remainder.*
#
# **Step 4:** How many times does [[arg2]] go into [[arg1*10%arg2*10]]? $[[arg2]]\times[[arg1*10%arg2*10//arg2]] = [[arg1*10%arg2*10]]$, we place the number [[arg1*10%arg2*10//arg2]] in the quotient, next to the [[arg1*10//arg2]]. We then write [[arg1*10%arg2*10]] below the dividend and subtract to get the remainder, which is 0. Since we have no leftovers, we have finished the calculation.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\,[[arg1*10//arg2/10]] \text{ }\text{ }}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\:00\\[-4pt]
# &{\:\:[[arg1*10//arg2*arg2//10]]\:[[arg1*10//arg2*arg2%10]]\!\:\small\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:\:[[arg1*10%arg2*10]]\:\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\text{ }\,[[arg1*10//arg2/10]]{\color {Salmon} [[arg1*10%arg2*10//arg2]]}\text{ }}\\[-5pt]
# [[arg2]]&\big)[[arg1]]\:00\\[-4pt]
# &{\:\:[[arg1*10//arg2*arg2//10]]\:[[arg1*10//arg2*arg2%10]]\:\:\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:\:[[arg1*10%arg2*10]]\:\\[-4pt]
# &{-\,\!\:\,{\color {Salmon} [[arg1*10%arg2*10]]}\:\:}\\[-4pt]
# \hline
# &\text{ }\:\:\:\:\:\:\!\:\,\!{\color {Salmon} 0}\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# [[arg1/arg2]]
# $$
#
# Therefore, the final solution is [[arg1/arg2]].
# </div>
# </div>
#     """

#     args = {'arg1': 6, 'arg2': 20}
#     #args = {'arg1': 3, 'arg2': 4}
#     solution = KnowledgePoint43Solution().get_solution(template1, template2, args)
#     print(solution)
#
# main()


###########################################################################################


class KnowledgePoint44Solution(SolutionGenerator):
    def count_decimal_digits(self, num: float):
        str_num = str(num)
        if '.' in str_num:
            decimal = str_num.split('.')[1]
            return len(decimal)
        else:
            return 0

    def get_solution(self, template1: str, template2: str, template3: str, args: dict) -> str:
        arg1_fraction_digits = self.count_decimal_digits(args['arg1'])
        arg2_fraction_digits = self.count_decimal_digits(args['arg2'])

        # if arg1_fraction_digits == 1:
        #     args['int_arg1'] = int(args['arg1'] * 10)
        #     if arg2_fraction_digits == 1:
        #         #args['int_arg1'] = int(args['arg1'] * 10)
        #         args['int_arg2'] = int(args['arg2'] * 10)
        #         template = template3
        #     else:
        #         #args['int_arg1'] = int(args['arg1'] * 10)
        #         args['int_arg2'] = int(args['arg2'] * 100)
        #         template = template1
        if arg1_fraction_digits == 1 and arg2_fraction_digits == 1:
            args['int_arg1'] = int(args['arg1'] * 10)
            args['int_arg2'] = int(args['arg2'] * 10)
            template = template3
        elif arg1_fraction_digits == 1:
            args['int_arg1'] = int(args['arg1'] * 10)
            args['int_arg2'] = int(args['arg2'] * 100)
            template = template1
        elif arg2_fraction_digits == 1:
            args['int_arg1'] = int(args['arg2'] * 10)
            args['int_arg2'] = int(args['arg1'] * 100)
            template = template1
        else:
            args['int_arg1'] = int(args['arg1'] * 100)
            args['int_arg2'] = int(args['arg2'] * 100)
            template = template2

        return self.custom_format(template, **args)

    # def get_solution(self, template: str, args: dict) -> str:
    #     ##template1##
    #     args['int_arg1'] = int(args['arg1']*10)
    #     args['int_arg2'] = int(args['arg2']*100)
    #
    #     #template2##
    #     args['int_arg1'] = int(args['arg1']*100)
    #     args['int_arg2'] = int(args['arg2']*100)
    #
    #     return self.custom_format(template, **args)


def main():
    start_time = time.time()
    template1 = r"""Template1
<div class="ex-yellow">
<div class="title">
<div class="ex-text" align="center">

$$ [[arg1]] + [[arg2]] $$

</div>

**Step 1:** Align each decimal number, making sure to line up the **decimal points**. Let's start by writing the number [[arg1]] and below it write the number [[arg2]].
$$
\begin{array}{r c r}
&0{\color {Salmon} .}[[int_arg1]]\phantom{0}\\
+&0{\color {Salmon} .}[[int_arg2]] \\
\hline
\end{array}
$$

**Step 2:** Add zeros in the places where the length of the decimal numbers is not the same.

$$
\begin{array}{r c r}
&0.[[int_arg1]]{ }\phantom{0}\\
+&0.[[int_arg2]]\\
\hline
\end{array}
\:\:\:\longrightarrow    \:\:
\begin{array}{r c r}
&0.[[int_arg1]]{\color {Salmon} 0}\\
+&0.[[int_arg2]]\\
\hline
\end{array}
$$
*Note: When we line up the decimal points in decimal addition, we want to make sure that each digit is in the correct place. To add numbers accurately, equalize the digits after the decimal point by adding zeros.*

**Step 3:** We start with the rightmost column. In this case, it's the hundredths column. We add the digits in that column: $0 + [[int_arg2%10]] =[[int_arg2%10]]$ and write it in the hundredths column.

$$
\begin{array}{r c r}
&0.[[int_arg1]]{0}\\
+&0.[[int_arg2]]\\
\hline
\end{array}
\:\:\:\longrightarrow    \:\:
\begin{array}{r c r}
\\
&0.[[int_arg1]]{\color {Salmon} 0}\\
+&0.[[int_arg2//10]]{\color{Salmon}[[int_arg2%10]]} \\
\hline
&\phantom{0}\phantom{0}\:\,{\color {Salmon} [[int_arg2%10]]}\\
\end{array}
$$

**Step 4:** Next, we move to the left column. In this case, it's the tenths column. We add the digits in that column: $[[int_arg1]] + [[int_arg2//10]] =[[int_arg1+int_arg2//10]]$ and write [[(int_arg1+int_arg2//10)%10]] in the tenths column.

$$
\begin{array}{r c r}
\\
&0.[[int_arg1]]{0}\\
+&0.[[int_arg2]] \\
\hline
&\phantom{0}\phantom{0}\:\,[[int_arg2%10]]\\
\end{array}
\:\:\:\longrightarrow    \:\:
\begin{array}{r c r}
\\
& \tiny[[(int_arg1+int_arg2//10)//10]]\:\:\:\:\:\:\:\,\\[-3pt]
&0.{\color {Salmon} [[int_arg1]]}0\\
+&0.{\color {Salmon} [[int_arg2//10]]}[[int_arg2%10]] \\
\hline
&\phantom{0}\:{\color {Salmon} [[(int_arg1+int_arg2//10)%10]]}[[int_arg2%10]]
\end{array}
$$

**Step 5:** Then, we continue to move to the left column. In this case, it's the ones column. We add the digits in that column: $0 + 0 + [[(int_arg1+int_arg2//10)//10]]= [[(int_arg1+int_arg2//10)//10]]$ and write it in the ones column. And don't forget to add the decimal point after the ones column.

$$
\begin{array}{r c r}
\\
&0.[[int_arg1]]{0}\\
+&0.[[int_arg2]] \\
\hline
&{\color {Salmon} [[(int_arg1+int_arg2//10)//10]]}.[[(int_arg1+int_arg2//10)%10]][[int_arg2%10]]
\end{array}
\:\:\:\longrightarrow    \:\:
\begin{array}{r c r}
\\
&0.[[int_arg1]]{0}\\
+&0.[[int_arg2]] \\
\hline
&[[arg1+arg2]]\\
\end{array}
$$
Therefore, the final solution is [[arg1+arg2]].
</div>
</div>
        """

    template2 = r"""template2
<div class="ex-yellow">
<div class="title">
<div class="ex-text" align="center">

$$ [[arg1]] + [[arg2]] $$

</div>

**Step 1:** Align each decimal number, making sure to line up the **decimal points**. Let's start by writing the number [[arg1]] and below it write the number [[arg2]].
$$
\begin{array}{r c r}
&0{\color {Salmon} .}[[int_arg1]]\\
+&0{\color {Salmon} .}[[int_arg2]] \\
\hline
\end{array}
$$


**Step 2:** We start with the rightmost column. In this case, it's the hundredths column. We add the digits in that column: $[[int_arg1%10]] + [[int_arg2%10]] =[[int_arg1%10+int_arg2%10]]$ and write [[(int_arg1%10+int_arg2%10)%10]] in the hundredths column.
$$
\begin{array}{r c r}
&[[arg1]] \\
+&[[arg2]] \\
\hline
\end{array}
\:\:\:\longrightarrow    \:\:
\begin{array}{r c r}
\\
&0.[[int_arg1//10]]{\color{Salmon}[[int_arg1%10]]}\\
+&0.[[int_arg2//10]]{\color{Salmon}[[int_arg2%10]]}\\
\hline
&\phantom{0}\phantom{0}\:\,{\color{Salmon}[[(int_arg1%10+int_arg2%10)%10]]}
\end{array}
$$

**Step 3:** Next, we move to the left column. In this case, it's the tenths column. We add the digits in that column: $[[int_arg1//10]] + [[int_arg2//10]] + [[(int_arg1%10+int_arg2%10)//10]]=[[int_arg1//10+int_arg2//10+(int_arg1%10+int_arg2%10)//10]]$ and write [[(int_arg1//10+int_arg2//10+(int_arg1%10+int_arg2%10)//10)%10]] in the tenths column.

$$
\begin{array}{r c r}
\\
&[[arg1]] \\
+&[[arg2]]\\
\hline
&\phantom{0}\phantom{0}\:\,[[(int_arg1%10+int_arg2%10)%10]]
\end{array}
\:\:\:\longrightarrow    \:\:
\begin{array}{r c r}
& \tiny{\color{Salmon}[[(int_arg1//10+int_arg2//10+(int_arg1%10+int_arg2%10)//10)//10]]}\:\:\:\:\:\:\:\,\\[-3pt]
&0.{\color {Salmon} [[int_arg1//10]]}[[int_arg1%10]]\\
+&0.{\color {Salmon} [[int_arg2//10]]}[[int_arg2%10]] \\
\hline
&\:\,\,.{\color {Salmon} [[(int_arg1//10+int_arg2//10+(int_arg1%10+int_arg2%10)//10)%10]]}[[(int_arg1%10+int_arg2%10)%10]]\\
\end{array}
$$

**Step 4:**  We carried over the [[(int_arg1//10+int_arg2//10+(int_arg1%10+int_arg2%10)//10)//10]] from the tenths column to the next column, which is the whole numbers or ones column.

In this column, we add the carried-over [[(int_arg1//10+int_arg2//10+(int_arg1%10+int_arg2%10)//10)//10]] with the digit 0 (since there are no digits in the ones column to add). When we add [[(int_arg1//10+int_arg2//10+(int_arg1%10+int_arg2%10)//10)//10]] and 0, we get [[(int_arg1//10+int_arg2//10+(int_arg1%10+int_arg2%10)//10)//10]] and write it in the ones column. And we add the decimal point after the ones column as the final step.

$$
\begin{array}{r c r}
& \tiny[[(int_arg1//10+int_arg2//10+(int_arg1%10+int_arg2%10)//10)//10]]\:\:\:\:\:\:\:\,\\[-3pt]
&[[arg1]] \\
+&[[arg2]] \\
\hline
&\:\,\,.[[(int_arg1//10+int_arg2//10+(int_arg1%10+int_arg2%10)//10)%10]][[(int_arg1%10+int_arg2%10)%10]]\\
\end{array}
\:\:\:\longrightarrow    \:\:
\begin{array}{r c r}
& \tiny{\color{Salmon}[[(int_arg1//10+int_arg2//10+(int_arg1%10+int_arg2%10)//10)//10]]}\:\:\:\:\:\:\:\,\\[-3pt]
&[[arg1]]\\
+&[[arg2]] \\
\hline
&{\color {Salmon}[[(int_arg1//10+int_arg2//10+(int_arg1%10+int_arg2%10)//10)//10]]}.[[(int_arg1//10+int_arg2//10+(int_arg1%10+int_arg2%10)//10)%10]][[(int_arg1%10+int_arg2%10)%10]]\\
\end{array}
$$
Therefore, the final solution is [[arg1+arg2]].
</div>
</div>
    """

    template3 = r"""template3
<div class="ex-yellow">  
<div class="title">  
<div class="ex-text" align="center">  
  
$$ [[arg1]] + [[arg2]] $$  
  
**Step 1:** Align each decimal number, making sure to line up the **decimal points**. Let's start by writing the number [[arg1]] and below it write the number [[arg2]].  
$$  
\begin{array}{r c r}  
&0{\color {Salmon} .}[[int_arg1]] \\  
+&0{\color {Salmon} .}[[int_arg2]] \\  
\hline  
\end{array}  
$$  
   
**Step 2:** We start with the rightmost column. In this case, it's the tenths column. We add the digits in that column: $[[int_arg1]] + [[int_arg2]] =[[int_arg1+int_arg2]]$ and write [[(int_arg1+int_arg2)%10]] in the tenths column.  
  
$$  
\begin{array}{r c r}  
\\  
&0.[[int_arg1]]\\  
+&0.[[int_arg2]] \\  
\hline  
&\phantom{0}\,[[(int_arg1+int_arg2)%10]]\\  
\end{array}  
\:\:\:\longrightarrow    \:\:  
\begin{array}{r c r}  
\\  
& \tiny[[(int_arg1+int_arg2)//10]]\:\:\:\:\:\:\:\,\\[-3pt]  
&0.{\color {Salmon} [[int_arg1]]}\\  
+&0.{\color {Salmon} [[int_arg2]]}\\  
\hline  
&\phantom{0}\:{\color {Salmon} [[(int_arg1+int_arg2)%10]]}
\end{array}  
$$  
  
**Step 3:** Then, we continue to move to the left column. In this case, it's the ones column. We add the digits in that column: $0 + 0 + [[(int_arg1+int_arg2)//10]]= [[(int_arg1+int_arg2)//10]]$ and write it in the ones column. And don't forget to add the decimal point after the ones column.  
  
$$  
\begin{array}{r c r}  
\\  
&0.[[int_arg1]]\\  &0.[[int_arg2]] \\  
\hline  
&{\color {Salmon} [[(int_arg1+int_arg2)//10]]}.[[(int_arg1+int_arg2)%10]] 
\end{array}  
\:\:\:\longrightarrow    \:\:  
\begin{array}{r c r}  
\\  
&0.[[int_arg1]]\\  
+&0.[[int_arg2]] \\  
\hline  
&[[arg1+arg2]]\\  
\end{array}  
$$  
Therefore, the final solution is [[arg1+arg2]].  
</div>  
</div>  
    """

    args = {'arg1': 0.3, 'arg2': 0.65}
    #args = {'arg1': 0.5, 'arg2': 0.35}
    #args = {'arg1': 0.72, 'arg2': 0.5}

    #args = {'arg1': 0.55, 'arg2': 0.35}
    #args = {'arg1': 0.89, 'arg2': 0.16}

    #args = {'arg1': 0.9, 'arg2': 0.3}
    #args = {'arg1': 0.2, 'arg2': 0.3}

    solution = KnowledgePoint44Solution().get_solution(template1, template2, template3, args)
    print(solution)

main()


########################################################################################


class KnowledgePoint45Solution(SolutionGenerator):
    def count_decimal_digits(self, num: float):
        str_num = str(num)
        if '.' in str_num:
            decimal = str_num.split('.')[1]
            return len(decimal)
        else:
            return 0

    def get_solution(self, template1: str, template2: str, template3: str, template4: str, args: dict) -> str:
        arg1_fraction_digits = self.count_decimal_digits(args['arg1'])
        arg2_fraction_digits = self.count_decimal_digits(args['arg2'])

        if arg1_fraction_digits == 1:
            if arg2_fraction_digits == 1:
                args['int_arg1'] = int(args['arg1'] * 10)
                args['int_arg2'] = int(args['arg2'] * 10)
                template = template1
            else:
                args['int_arg1'] = int(args['arg1'] * 10)
                args['int_arg2'] = int(args['arg2'] * 100)
                template = template2
        else:
            args['int_arg1'] = int(args['arg1'] * 100)
            args['int_arg2'] = int(args['arg2'] * 100)
            if args['int_arg1'] % 10 < args['int_arg2'] % 10:
                template = template3
            else:
                template = template4

        return self.custom_format(template, **args)


# def main():
#     start_time = time.time()
#     template2 = r"""template2
# <div class="ex-yellow">
# <div class="title">
# <div class="ex-text" align="center">
#
# $$ [[arg1]] - [[arg2]] $$
#
# **Step 1:** Align each decimal number, making sure to line up the **decimal points**. Let's start by writing the number [[arg1]] and below it write the number [[arg2]].
#
# $$
# \begin{array}{r c r}
# &0{\color {Salmon} .}[[int_arg1]]\phantom{0}\\
# -&0{\color {Salmon} .}[[int_arg2]] \\
# \hline
# \end{array}
# $$
#
# **Step 2:** Add zeros in the places where the length of the decimal numbers is not the same.
#
# $$
# \begin{array}{r c r}
# &[[arg1]]{ }\phantom{0}\\
# -&[[arg2]] \\
# \hline
# \end{array}
# \:\:\:\longrightarrow    \:\:
# \begin{array}{r c r}
# &[[arg1]]{\color {Salmon} 0}\\
# -&[[arg2]] \\
# \hline
# \end{array}
# $$
#
# *Note: When we line up the decimal points in decimal subtraction, we want to make sure that each digit is in the correct place. To subtract numbers accurately, equalize the digits after the decimal point by adding zeros.*
#
# **Step 3:** We start with the rightmost column. In the rightmost column, the first number in this column is [[int_arg2%10]]. We can see that 0 is smaller than [[int_arg2%10]]. So, we need borrow 1 from the left column which will make it 10. And the [[int_arg1]] in the left column becomes [[int_arg1-1]]. Now we have $10 - [[int_arg2%10]] =[[10-int_arg2%10]]$ in this column and write it in the hundredths column.
#
# $$
# \begin{array}{r c r}
# &[[arg1]]{0}\\
# -&[[arg2]] \\
# \hline
# \end{array}
# \:\:\:\longrightarrow    \:\:
# \begin{array}{r c r}
# & \:\:\:\:\tiny{\color{Salmon}[[int_arg1-1]]}\:\tiny{\color{Salmon}10}\\[-3pt]
# &0.{\color {Salmon} \cancel[[int_arg1]]}{\color {Salmon}\cancel0}\\
# -&0.[[int_arg2//10]]{\color {Salmon} [[int_arg2%10]]} \\
# \hline
# &\phantom{0}\phantom{0}\:\,{\color {Salmon} [[10-int_arg2%10]]}
# \end{array}
# $$
#
# **Step 4:** Next, we move to the left column. After giving 1 to the rightmost column in step 3, the [[int_arg1]] in this column becomes [[int_arg1-1]]. Now we have $[[int_arg1-1]] - [[int_arg2//10]] = [[(int_arg1-1)-int_arg2//10]]$ in this column and write it in the tenths column.
#
# $$
# \begin{array}{r c r}
# & \:\:\:\:\tiny[[int_arg1-1]]\:\tiny10\\[-3pt]
# &0.{\cancel[[int_arg1]]}{\cancel0}\\
# -&[[arg2]]\\
# \hline
# &\phantom{0}\phantom{0}\:\,[[10-int_arg2%10]]
# \end{array}
# \:\:\:\longrightarrow    \:\:
# \begin{array}{r c r}
# & \:\:\:\:\tiny{\color {Salmon} [[int_arg1-1]]}\:\tiny10\\[-3pt]
# &0.{\cancel[[int_arg1]]}{\cancel0}\\
# -&0.{\color {Salmon} [[int_arg2//10]]}[[int_arg2%10]]\\
# \hline
# &\:\,\,.{\color {Salmon} [[(int_arg1-1)-int_arg2//10]]}[[10-int_arg2%10]]\\
# \end{array}
# $$
#
# **Step 5:** Then, we continue to move to the left column, the first number in this column is 0. We have $0 - 0 =0$ in this column and write it in the ones column. And don't forget to add the decimal point after the ones column.
#
# $$
# \begin{array}{r c r}
# & \:\:\:\:\tiny[[int_arg1-1]]\:\tiny10\\[-3pt]
# &0.{ \cancel[[int_arg1]]}{\cancel0}\\
# -&[[arg2]] \\
# \hline
# &\:\,\,.[[int_arg1*10-int_arg2]]\\
# \end{array}
# \:\:\:\longrightarrow    \:\:
# \begin{array}{r c r}
# & \:\:\:\:\tiny[[int_arg1-1]]\:\tiny10\\[-3pt]
# &0.{ \cancel[[int_arg1]]}{\cancel0}\\
# -&[[arg2]] \\
# \hline
# &[[arg1-arg2]] \\
# \end{array}
# $$
# Therefore, the final solution is [[arg1-arg2]].
#
# </div>
# </div>
#     """
#
#     template4 = r"""template4
# <div class="ex-yellow">
# <div class="title">
# <div class="ex-text" align="center">
#
# $$ [[arg1]] - [[arg2]] $$
#
# **Step 1:** Align each decimal number, making sure to line up the **decimal points**. Let's start by writing the number  [[arg1]]  and below it write the number  [[arg2]].
#
# $$
# \begin{array}{r c r}
# &0{\color {Salmon} .}[[int_arg1]]\\
# -&0{\color {Salmon} .}[[int_arg2]] \\
# \hline
# \end{array}
# $$
# **Step 2:** We start with the rightmost column. In the rightmost column, the first number in this column is [[int_arg1%10]]. We have $[[int_arg1%10]] - [[int_arg2%10]] =[[int_arg1%10-int_arg2%10]]$
#  in this column and write it in the hundredths column.
#
# $$
# \begin{array}{r c r}
# &0.[[int_arg1]]\\
# -&0.[[int_arg2]]\\
# \hline
# \end{array}
# \:\:\:\longrightarrow    \:\:
# \begin{array}{r c r}
# \\
# &.[[int_arg1//10]]{\color {Salmon} [[int_arg1%10]]}\\
# -&.[[int_arg2//10]]{\color {Salmon} [[int_arg2%10]]} \\
# \hline
# &\phantom{0}\:\,{\color {Salmon} [[int_arg1%10-int_arg2%10]]}
# \end{array}
# $$
#
# **Step 3:** Next, we move to the left column, the first number in this column is [[int_arg1//10]]. We have $[[int_arg1//10]] - [[int_arg2//10]] = [[int_arg1//10-int_arg2//10]]$ in this column and write it in the tenths column.
#
# $$
# \begin{array}{r c r}
# \\
# &0.[[int_arg1]]\\
# -&0.[[int_arg2]]\\
# \hline
# &\phantom{0}\phantom{0}\:\,[[int_arg1%10-int_arg2%10]]
# \end{array}
# \:\:\:\longrightarrow    \:\:
# \begin{array}{r c r}\\
# &0.{\color {Salmon}  [[int_arg1//10]]}[[int_arg1%10]]\\
# -&0.{\color {Salmon}  [[int_arg2//10]]}[[int_arg2%10]] \\
# \hline
# &\:\,\,.{\color {Salmon}[[int_arg1//10-int_arg2//10]]}[[int_arg1%10-int_arg2%10]]\\
# \end{array}
# $$
#
# **Step 4:** Then, we continue to move to the left column, the first number in this column is 0. We have $0 - 0 =0$ in this column and write it in the ones column. And don't forget to add the decimal point after the ones column.
#
# $$
# \begin{array}{r c r}\\
# &0.[[int_arg1]]\\
# -&0.[[int_arg2]]\\
# \hline
# &\:\,\,.[[int_arg1-int_arg2]]\\
# \end{array}
# \:\:\:\longrightarrow    \:\:
# \begin{array}{r c r}\\
# &0.[[int_arg1]]\\
# -&0.[[int_arg2]]\\
# \hline
# &[[arg1-arg2]]\\
# \end{array}
# $$
# Therefore, the final solution is [[arg1-arg2]].
#
# </div>
# </div>
#         """
#
#     template1 = r"""template1
# <div class="ex-yellow">
# <div class="title">
# <div class="ex-text" align="center">
#
# $$ [[arg1]] - [[arg2]] $$
#
# **Step 1:** Align each decimal number, making sure to line up the **decimal points**. Let's start by writing the number  [[arg1]]  and below it write the number  [[arg2]].
#
# $$
# \begin{array}{r c r}
# &0{\color {Salmon} .}[[int_arg1]]\\
# -&0{\color {Salmon} .}[[int_arg2]] \\
# \hline
# \end{array}
# $$
# **Step 2:** We start with the rightmost column. In the rightmost column, the first number in this column is [[int_arg1%10]]. We have $[[int_arg1%10]] - [[int_arg2%10]] =[[int_arg1%10-int_arg2%10]]$
#  in this column and write it in the tenths column.
#
# $$
# \begin{array}{r c r}
# &0.[[int_arg1]]\\
# -&0.[[int_arg2]]\\
# \hline
# \end{array}
# \:\:\:\longrightarrow    \:\:
# \begin{array}{r c r}
# \\
# &0.{\color {Salmon} [[int_arg1%10]]}\\
# -&0.{\color {Salmon} [[int_arg2%10]]} \\
# \hline
# &\phantom{0}\,{\color {Salmon} [[int_arg1%10-int_arg2%10]]}
# \end{array}
# $$
#
# **Step 3:** Next, we move to the left column the first number in this column is 0. We have $0 - 0 =0$ in this column and write it in the ones column. And don't forget to add the decimal point after the ones column.
#
# $$
# \begin{array}{r c r}\\
# &0.[[int_arg1]]\\
# -&0.[[int_arg2]]\\
# \hline
# &\:\,\,.[[int_arg1-int_arg2]]\\
# \end{array}
# \:\:\:\longrightarrow    \:\:
# \begin{array}{r c r}\\
# &0.[[int_arg1]]\\
# -&0.[[int_arg2]]\\
# \hline
# &[[arg1-arg2]]\\
# \end{array}
# $$
# Therefore, the final solution is [[arg1-arg2]].
#
# </div>
# </div>
#     """
#
#     template3 = r"""template3
# <div class="ex-yellow">
# <div class="title">
# <div class="ex-text" align="center">
#
# $$ [[arg1]] - [[arg2]] $$
#
# **Step 1:** Align each decimal number, making sure to line up the **decimal points**. Let's start by writing the number  [[arg1]]  and below it write the number  [[arg2]].
#
# $$
# \begin{array}{r c r}
# &0{\color {Salmon} .}[[int_arg1]]\\
# -&0{\color {Salmon} .}[[int_arg2]] \\
# \hline
# \end{array}
# $$
#
# **Step 2:** We start with the rightmost column. In the rightmost column, the first number in this column is [[int_arg1%10]]. We can see that [[int_arg1%10]] is smaller than [[int_arg2%10]]. So, we need borrow 1 from the left column which will make it [[int_arg1%10+10]]. And the [[int_arg1//10]] in the left column becomes [[int_arg1//10-1]]. Now we have $[[int_arg1%10+10]] - [[int_arg2%10]] =[[(int_arg1-int_arg2)%10]]$ in this column and write it in the hundredths column.
#
# $$
# \begin{array}{r c r}
# &[[arg1]]\\
# -&[[arg2]] \\
# \hline
# \end{array}
# \:\:\:\longrightarrow    \:\:
# \begin{array}{r c r}
# & \:\:\:\:\tiny{\color{Salmon}[[int_arg1//10-1]]}\:\tiny{\color{Salmon}[[int_arg1%10+10]]}\\[-3pt]
# &0.{\color {Salmon} \cancel[[int_arg1//10]]}{\color {Salmon}\cancel[[int_arg1%10]]}\\
# -&0.[[int_arg2//10]]{\color {Salmon} [[int_arg2%10]]} \\
# \hline
# &\phantom{0}\phantom{0}\:\,{\color {Salmon} [[(int_arg1%10+10)-int_arg2%10]]}
# \end{array}
# $$
#
# **Step 3:** Next, we move to the left column. After giving 1 to the rightmost column in step 3, the [[int_arg1//10]] in this column becomes [[int_arg1//10-1]]. Now we have $[[int_arg1//10-1]] - [[int_arg2//10]] = [[(int_arg1//10-1)-int_arg2//10]]$ in this column and write it in the tenths column.
#
# $$
# \begin{array}{r c r}
# & \:\:\:\:\tiny[[int_arg1//10-1]]\:\tiny[[int_arg1%10+10]]\\[-3pt]
# &0.{\cancel[[int_arg1//10]]}{\cancel[[int_arg1%10]]}\\
# -&[[arg2]]\\
# \hline
# &\phantom{0}\phantom{0}\:\, [[(int_arg1-int_arg2)%10]]
# \end{array}
# \:\:\:\longrightarrow    \:\:
# \begin{array}{r c r}
# & \:\:\:\:\tiny{\color {Salmon} [[int_arg1//10-1]]}\:\tiny[[int_arg1%10+10]]\\[-3pt]
# &0.{\cancel[[int_arg1//10]]}{\cancel[[int_arg1%10]]}\\
# -&0.{\color {Salmon} [[int_arg2//10]]}[[int_arg2%10]]\\
# \hline
# &\:\,\,.{\color {Salmon} [[(int_arg1-int_arg2)//10]]}[[(int_arg1-int_arg2)%10]]\\
# \end{array}
# $$
#
# **Step 4:** Then, we continue to move to the left column, the first number in this column is 0. We have $0 - 0 =0$ in this column and write it in the ones column. And don't forget to add the decimal point after the ones column.
#
# $$
# \begin{array}{r c r}
# & \:\:\:\:\tiny[[int_arg1//10-1]]\:\tiny[[int_arg1%10+10]]\\[-3pt]
# &0.{\cancel[[int_arg1//10]]}{\cancel[[int_arg1%10]]}\\
# -&[[arg2]] \\
# \hline
# &\:\,\,.[[int_arg1-int_arg2]]\\
# \end{array}
# \:\:\:\longrightarrow    \:\:
# \begin{array}{r c r}
# & \:\:\:\:\tiny[[int_arg1//10-1]]\:\tiny[[int_arg1%10+10]]\\[-3pt]
# &0.{\cancel[[int_arg1//10]]}{\cancel[[int_arg1%10]]}\\
# -&[[arg2]] \\
# \hline
# &[[arg1-arg2]] \\
# \end{array}
# $$
# Therefore, the final solution is [[arg1-arg2]].
#
# </div>
# </div>
#     """
#
#     #args = {'arg1': 0.8, 'arg2': 0.3} # template1
#     #args = {'arg1': 0.4, 'arg2': 0.12} # template2
#
#     #args = {'arg1': 0.95, 'arg2': 0.19}  # template3
#     args = {'arg1': 0.98, 'arg2': 0.1}  # template4
#
#
#     solution = KnowledgePoint45Solution().get_solution(template1, template2, template3, template4, args)
#     print(solution)
#
#
# main()
#

##################################################################################
class KnowledgePoint46Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)


class KnowledgePoint47Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)


class KnowledgePoint48Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        return self.custom_format(template, **args)


#


class KnowledgePoint49Solution(SolutionGenerator):
    def get_solution(self, template1: str, template2: str, template3: str, args: dict) -> str:
        # Extract arguments
        arg1 = args['arg1']
        arg2 = args['arg2']
        arg3 = args['arg3']
        args["gcd"] = gcd(arg2 + arg3, arg1)

        def is_lowest_term(a, b):
            if gcd(a, b) == 1:
                return True

        if is_lowest_term(arg2 + arg3, arg1):
            # if gcd(arg2+arg3, arg1) == 1:
            if arg2 + arg3 < arg1:
                template = template1
            else:
                template = template3
        else:
            template = template2

        return self.custom_format(template, **args)


# def main():
#     start_time = time.time()
#     template1 = r"""<div class="ex-yellow">
# <div class="title">
#
# <div class="ex-text" align="center">
#
# $\frac{[[arg2]]}{[[arg1]]} + \frac{[[arg3]]}{[[arg1]]}\text{}=?$
#
# </div>
#
# **Step 1:** To add fractions with the **same denominator**, simply add the numerators of all fractions and keep the common denominator. In this case, we add the numerators, which are [[arg2]] and [[arg3]], we get [[arg2 + arg3]].
#
# $$
# \frac{{\color {Salmon} [[arg2]]}}{[[arg1]]} + \frac{{\color {Salmon} [[arg3]]}}{[[arg1]]}\text{}=\frac{{\color {Salmon} [[arg2 + arg3]]}}{ }
# $$
#
#
# **Step 2:** The denominator stays the same.
#
# $$
# \frac{[[arg2]]}{{\color {Salmon} [[arg1]]}} + \frac{[[arg3]]}{{\color {Salmon} [[arg1]]}}\text{}=\frac{[[arg2 + arg3]]}{{\color {Salmon} [[arg1]]}}
# $$
#
# **Step 3:** Always reduce your final answer to its **lowest term**. Since $\large\frac{[[arg2 + arg3]]}{[[arg1]]}$ is already the lowest term, $\large\frac{[[arg2 + arg3]]}{[[arg1]]}$ is our final answer.
#
# $$
# \frac{[[arg2]]}{[[arg1]]} + \frac{[[arg3]]}{[[arg1]]}\text{}=\frac{[[arg2 + arg3]]}{[[arg1]]}
# $$
# Therefore, the final solution is $\large\frac{[[arg2 + arg3]]}{[[arg1]]}$.
#
# </div>
# </div>
#         """
#
#     template2 = r"""<div class="ex-yellow">
# <div class="title">
#
# <div class="ex-text" align="center">
#
# $\frac{[[arg2]]}{[[arg1]]} + \frac{[[arg3]]}{[[arg1]]}\text{}=?$
#
# </div>
#
# **Step 1:** To add fractions with the **same denominator**, simply add the numerators of all fractions and keep the common denominator. In this case, we add the numerators, which are [[arg2]] and [[arg3]], we get [[arg2 + arg3]].
#
# $$
# \frac{{\color {Salmon} [[arg2]]}}{[[arg1]]} + \frac{{\color {Salmon} [[arg3]]}}{[[arg1]]}\text{}=\frac{{\color {Salmon} [[arg2 + arg3]]}}{ }
# $$
#
#
# **Step 2:** The denominator stays the same.
#
# $$
# \frac{[[arg2]]}{{\color {Salmon} [[arg1]]}} + \frac{[[arg3]]}{{\color {Salmon} [[arg1]]}}\text{}=\frac{[[arg2 + arg3]]}{{\color {Salmon} [[arg1]]}}
# $$
#
# **Step 3:** Always reduce your final answer to its **lowest term**. In this case, the fraction $\large\frac{[[arg2+arg3]]}{[[arg1]]}$ can be simplified. Both [[arg2+arg3]] and [[arg1]] are divisible by [[gcd]]. When we divide both [[arg2+arg3]] and [[arg1]] by their greatest common divisor [[gcd]], we get [[(arg2+arg3)//gcd]] and [[arg1//gcd]] respectively.
#
# $$
# \frac{[[arg2]]}{[[arg1]]} + \frac{[[arg3]]}{[[arg1]]} = \frac{[[arg2+arg3]]}{[[arg1]]}=
#  \frac{[[arg2+arg3]]\color {Salmon}\div[[gcd]]}{[[arg1]]\color {Salmon}\div[[gcd]]}= \frac{\color {Salmon}[[(arg2+arg3)//gcd]]}{\color {Salmon}[[arg1//gcd]]}
# $$
#
# Therefore, the final solution is $\large\frac{[[(arg2+arg3)//gcd]]}{[[arg1//gcd]]}$.
#
# </div>
# </div>
#
#     """
#     template3 = r"""<div class="ex-yellow">
# <div class="title">
#
# <div class="ex-text" align="center">
#
# $\frac{[[arg2]]}{[[arg1]]} + \frac{[[arg3]]}{[[arg1]]}\text{}=?$
#
# </div>
#
# **Step 1:** To add fractions with the **same denominator**, simply add the numerators of all fractions and keep the common denominator. In this case, we add the numerators, which are [[arg2]] and [[arg3]], we get [[arg2 + arg3]].
#
# $$
# \frac{{\color {Salmon} [[arg2]]}}{[[arg1]]} + \frac{{\color {Salmon} [[arg3]]}}{[[arg1]]}\text{}=\frac{{\color {Salmon} [[arg2 + arg3]]}}{ }
# $$
#
#
# **Step 2:** The denominator stays the same.
#
# $$
# \frac{[[arg2]]}{{\color {Salmon} [[arg1]]}} + \frac{[[arg3]]}{{\color {Salmon} [[arg1]]}}\text{}=\frac{[[arg2 + arg3]]}{{\color {Salmon} [[arg1]]}}
# $$
#
# **Step 3:** Always reduce your final answer to its **lowest term**. And $\large\frac{[[arg2 + arg3]]}{[[arg1]]}$ is already the lowest term.
#
# **Step 4:** Since our answer in the previous step is in the form of an improper fraction, we can further simplify it and convert it into a mixed number.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\text{ }\text{ }\text{ }\text{ }\small}\\[-5pt]
# [[arg1]]&\big)[[arg2 + arg3]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\:\:{\color {Salmon}[[(arg2+arg3) // arg1]]}\:\:}\\[-5pt]
# [[arg1]]&\big)[[arg2 + arg3]]\:\\[-4pt]
# -&{\:\:[[(arg2+arg3)//arg1*arg1]]\:\:}\\[-4pt]
# \hline
# &\:\:{\color {Salmon}[[(arg2+arg3) %arg1]]}\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# {\color {Salmon}[[(arg2+arg3)//arg1]]}\frac{\color {Salmon}[[(arg2+arg3)%arg1]]}{[[arg1]]}
# $$
# Therefore, the final solution is $[[(arg2+arg3)//arg1]]\large\frac{[[(arg2+arg3)%arg1]]}{[[arg1]]}$.
#
# </div>
# </div>
#
#
#     """
#
#     #args = {'arg1': 19, 'arg2': 10, 'arg3': 5}
#     #args = {'arg1': 12, 'arg2': 5, 'arg3': 4}
#     args = {'arg1': 7, 'arg2': 5, 'arg3': 4}
#     solution = KnowledgePoint49Solution().get_solution(template1, template2, template3, args)
#     print(solution)
#
# main()
#


class KnowledgePoint50Solution(SolutionGenerator):
    def get_solution(self, template1: str, template2: str, template3: str, args: dict) -> str:
        # Extract arguments
        arg1 = args['arg1']
        arg2 = args['arg2']
        arg3 = args['arg3']

        # Compute gcd and add it to args
        args["gcd"] = gcd(arg2 - arg3, arg1)

        # def is_lowest_term(a, b):
        #     if gcd(a, b) == 1:
        #         return True
        def is_lowest_term(a, b):
            return gcd(a, b) == 1

        if is_lowest_term(arg2 - arg3, arg1):
            if arg2 - arg3 < arg1:
                template = template1
            else:
                template = template3
        else:
            template = template2

        return self.custom_format(template, **args)


# def main():
#     start_time = time.time()
#     template1 = r"""<div class="ex-yellow">
# <div class="title">
#
# <div class="ex-text" align="center">
#
# $\frac{[[arg2]]}{[[arg1]]} - \frac{[[arg3]]}{[[arg1]]}\text{}=?$
#
# </div>
#
# **Step 1:** To subtract fractions with the **same denominator**, simply subtract the numerators of all fractions and keep the common denominator. In this case, we subtract the numerators, which are [[arg2]] minus [[arg3]], we get [[arg2 - arg3]].
#
# $$
# \frac{{\color {Salmon} [[arg2]]}}{[[arg1]]} - \frac{{\color {Salmon} [[arg3]]}}{[[arg1]]}\text{}=\frac{{\color {Salmon} [[arg2 - arg3]]}}{ }
# $$
#
# **Step 2:** The size of the equal pieces does not change when you subtract the fractions with the same denominator.
#
# $$
# \frac{[[arg2]]}{{\color {Salmon} [[arg1]]}} - \frac{[[arg3]]}{{\color {Salmon} [[arg1]]}}\text{}=\frac{[[arg2 - arg3]]}{{\color {Salmon} [[arg1]]}}
# $$
# **Step 3:** Always reduce your final answer to its **lowest term**. Since $\large\frac{[[arg2 - arg3]]}{[[arg1]]}$ is already the lowest term, $\large\frac{[[arg2 - arg3]]}{[[arg1]]}$ is our final answer.
#
# $$
# \frac{[[arg2]]}{[[arg1]]} - \frac{[[arg3]]}{[[arg1]]}\text{}=\frac{[[arg2 - arg3]]}{[[arg1]]}
# $$
# Therefore, the final solution is $\large\frac{[[arg2 - arg3]]}{[[arg1]]}$.
#
# </div>
# </div>
#     """
#
#     template2 = r"""<div class="ex-yellow">
# <div class="title">
#
# <div class="ex-text" align="center">
#
# $\frac{[[arg2]]}{[[arg1]]} - \frac{[[arg3]]}{[[arg1]]}\text{}=?$
#
# </div>
#
# **Step 1:** To subtract fractions with the **same denominator**, simply subtract the numerators of all fractions and keep the common denominator. In this case, we subtract the numerators, which are [[arg2]] minus [[arg3]], we get [[arg2 - arg3]].
#
# $$
# \frac{{\color {Salmon} [[arg2]]}}{[[arg1]]} - \frac{{\color {Salmon} [[arg3]]}}{[[arg1]]}\text{}=\frac{{\color {Salmon} [[arg2 - arg3]]}}{ }
# $$
#
# **Step 2:** The size of the equal pieces does not change when you subtract the fractions with the same denominator.
#
# $$
# \frac{[[arg2]]}{{\color {Salmon} [[arg1]]}} - \frac{[[arg3]]}{{\color {Salmon} [[arg1]]}}\text{}=\frac{[[arg2 - arg3]]}{{\color {Salmon} [[arg1]]}}
# $$
#
# **Step 3:** Always reduce your final answer to its **lowest term**. In this case, the fraction $\large\frac{[[arg2 - arg3]]}{[[arg1]]}$ can be simplified. When we divide both [[arg2 - arg3]] and [[arg1]] by their greatest common divisor [[gcd]], we get [[(arg2 - arg3)//gcd]] and [[arg1//gcd]] respectively.
#
# $$
# \frac{[[arg2]]}{[[arg1]]} - \frac{[[arg3]]}{[[arg1]]} = \frac{[[arg2 - arg3]]}{[[arg1]]}
# \:\:\:\longrightarrow    \:\:
#  \frac{[[arg2 - arg3]]\color {Salmon}\div[[gcd]]}{[[arg1]]\color {Salmon}\div[[gcd]]} = \frac{\color {Salmon}[[(arg2 - arg3)//gcd]]}{\color {Salmon}[[arg1//gcd]]}
# $$
# Therefore, the final solution is $\large\frac{[[(arg2 - arg3)//gcd]]}{[[arg1//gcd]]}$.
#
# </div>
# </div>
#     """
#
#     template3 = r"""<div class="ex-yellow">
# <div class="title">
#
# <div class="ex-text" align="center">
#
# $\frac{[[arg2]]}{[[arg1]]} - \frac{[[arg3]]}{[[arg1]]}\text{}=?$
#
# </div>
#
# **Step 1:** To subtract fractions with the **same denominator**, simply subtract the numerators of all fractions and keep the common denominator. In this case, we subtract the numerators, which are [[arg2]] minus [[arg3]], we get [[arg2 - arg3]].
#
# $$
# \frac{{\color {Salmon} [[arg2]]}}{[[arg1]]} - \frac{{\color {Salmon} [[arg3]]}}{[[arg1]]}\text{}=\frac{{\color {Salmon} [[arg2 - arg3]]}}{ }
# $$
#
# **Step 2:** The size of the equal pieces does not change when you subtract the fractions with the same denominator.
#
# $$
# \frac{[[arg2]]}{{\color {Salmon} [[arg1]]}} - \frac{[[arg3]]}{{\color {Salmon} [[arg1]]}}\text{}=\frac{[[arg2 - arg3]]}{{\color {Salmon} [[arg1]]}}
# $$
# **Step 3:** Always reduce your final answer to its **lowest term**. And $\large\frac{[[arg2 - arg3]]}{[[arg1]]}$ is already the lowest term.
#
# **Step 4:** Since our answer in the previous step is in the form of an improper fraction, we can further simplify it and convert it into a mixed number.
#
# $$
# \begin{aligned}
# &\underline{\text{ }\text{ }\text{ }\text{ }\text{ }\small}\\[-5pt]
# [[arg1]]&\big)[[arg2 - arg3]]\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# \begin{aligned}
# &\underline{\:\:{\color {Salmon}[[(arg2-arg3) // arg1]]}\:\:}\\[-5pt]
# [[arg1]]&\big)[[arg2 - arg3]]\:\\[-4pt]
# -&{\:\:[[(arg2-arg3)//arg1*arg1]]\:\:}\\[-4pt]
# \hline
# &\:\:{\color {Salmon}[[(arg2-arg3) % arg1]]}\\[-4pt]
# \end{aligned}
# \:\:\:\longrightarrow    \:\:
# {\color {Salmon}[[(arg2-arg3) // arg1]]}\frac{\color {Salmon}[[(arg2-arg3) %arg1]]}{[[arg1]]}
# $$
# Therefore, the final solution is $[[(arg2-arg3) // arg1]]\large\frac{[[(arg2-arg3) %arg1]]}{[[arg1]]}$.
#
# </div>
# </div>
#             """
#
#     #args = {'arg1': 10, 'arg2': 4, 'arg3': 1}  ##template1
#     #args = {'arg1': 9, 'arg2': 4, 'arg3': 1} ##template2
#     args = {'arg1': 3, 'arg2': 10, 'arg3':5} ##template3
#     solution = KnowledgePoint50Solution().get_solution(template1, template2, template3, args)
#     print(solution)
#
# main()


#############################################################


class KnowledgePoint51Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        args['gcd'] = gcd
        return self.custom_format(template, **args)


class KnowledgePoint67Solution:
    pass


class KnowledgePoint67Solution(SolutionGenerator):
    def get_solution(self, template: str, args: dict) -> str:
        def getAlternateName(arg1, arg2):
            if arg2 == 2:
                return "or \"" + SolutionGenerator.getRep(arg1) + " squared\""
            elif arg2 == 3:
                return "or \"" + SolutionGenerator.getRep(arg1) + " cubed\""
            return ""

        def getExpanded(arg1, arg2):
            if arg2 == 0:
                return "1"
            res = str(arg1)
            for iter in range(1, arg2):
                res += "x" + str(arg1)
            return res

        args['getRep'] = SolutionGenerator.getRep
        args["getExpanded"] = getExpanded
        args["getAlternateName"] = getAlternateName
        return self.custom_format(template, **args)

# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title"
#
# <div class="ex-text">
#
# $$
# [[arg1]]^[[arg2]] = ?
# $$
#
#
# The number [[getRep(arg1)]] with an exponent of [[getRep(arg2)]]. This means you take the number [[arg1]] and multiply it by itself [[getRep(arg2)]] times. $[[arg1]]^[[arg2]]$ read as "[[getRep(arg1)]] to the power of [[getRep(arg2)]]" [[getAlternateName(arg1, arg2)]].
# $$
# [[getExpanded(arg1, arg2)]] = [[arg1**arg2]]
# $$
# </div>
# </div>
#             """
#     args = {'arg1': 3, 'arg2': 3}
#     solution = KnowledgePoint67Solution().get_solution(template, args)
#     print(solution)
#
# main()


################################################################################
# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title"
#
# <div class="ex-text" align="center">
#
# $\frac{[[arg1]]}{[[arg2]]} \times \frac{[[arg3]]}{[[arg4]]}\text{}=?$
#
#
#
# **Step 1:** Multiply the top numbers (numerators) of the fractions together. In this case, [[arg1]] multiplied by [[arg3]] equals [[arg1*arg3]]. Then we multiply the bottom numbers (denominators) of the fractions together. In this case, [[arg2]] multiplied by [[arg4]] equals [[arg2*arg4]].
#
# $$
# \frac{[[arg1]]}{[[arg2]]} \times \frac{[[arg3]]}{[[arg4]]}\text{}=  \frac{[[arg1]]\times[[arg3]]}{[[arg2]]\times[[arg4]]} = \frac{[[arg1*arg3]]}{[[arg2*arg4]]}
# $$
# **Step 2:** Always reduce your final answer to its **lowest term**. Since the greatest common denominator of [[arg1*arg3]] and [[arg2*arg4]] is [[gcd(arg1*arg3, arg2*arg4)]], $\large\frac{[[arg1*arg3]]÷[[gcd(arg1*arg3, arg2*arg4)]]}{[[arg2*arg4]]÷[[gcd(arg1*arg3, arg2*arg4)]]}$ equals $\large\frac{[[arg1*arg3//gcd(arg1*arg3, arg2*arg4)]]}{[[arg2*arg4//gcd(arg1*arg3, arg2*arg4)]]}$. So $\large\frac{[[arg1*arg3//gcd(arg1*arg3, arg2*arg4)]]}{[[arg2*arg4//gcd(arg1*arg3, arg2*arg4)]]}$ is our final answer.
#
# Therefore, the final solution is $\large\frac{[[arg1*arg3//gcd(arg1*arg3, arg2*arg4)]]}{[[arg2*arg4//gcd(arg1*arg3, arg2*arg4)]]}$.
# </div>
# </div>
#         """
#     args = {'arg1': 1, 'arg2': 2, 'arg3': 1, 'arg4': 3}
#     solution = KnowledgePoint51Solution().get_solution(template, args)
#     print(solution)
#
# main()

########################################################


##########################################################################################

#
#


####################################################
# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title"
#
# <div class="ex-text" align="center">
#
# $[[arg1]]\frac{[[arg2]]}{[[arg3]]} =?$
#
#
# **Step 1:** Multiply the denominator (the bottom number in the fraction) and the whole number.
#
# $$
# {\color {salmon}[[arg1]]}\frac{[[arg2]]}{{\color {salmon}[[arg3]]}} \text{}\:\:\:\:\:\:\:\:\:\:\:\text{}
# {\color {salmon}[[arg1]]}  \: \times \: {\color {salmon}[[arg3]]}\  = \: {\color {salmon}[[arg1*arg3]]}
# $$
# **Step 2:** Add the answer from step 1 to the numerator (the top number in the fraction).
#
# $$
# [[arg1]]\frac{{\color {salmon}[[arg2]]}}{[[arg3]]} \text{}\:\:\:\:\:\:\:\:\:\:\:\text{}
# {\color {salmon}[[arg1*arg3]]}  \: + \: {{\color {salmon}[[arg2]]}}\  = \: {\color {salmon}[[arg1*arg3+arg2]]}
# $$
# **Step 3:** Write answer from step 2 over the denominator.
#
# $$
# \frac{{\color {salmon}[[arg1*arg3+arg2]]}}{[[arg3]]}
# $$
# </div>
# </div>
#         """
#     args = {'arg1': 1, 'arg2':2, 'arg3':3}
#
#     solution = KnowledgePoint48Solution().get_solution(template, args)
#     print(solution)
#
# main()


#######################################################
# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title"
#
# <div class="ex-text" align="center">
#
# $[[arg1]] = \underline{\quad}\%$
#
#
#
# **Step 1:** To convert a decimal to a percent, we simply multiply the number by 100. In this case, we have [[arg1]]. When we multiply it by 100, it becomes [[arg1*100]].
#
# $$
# [[arg1]] \times 100 =[[int_arg1]]
# $$
# **Step 2:** Then we add the percentage symbol **%** to the result. And we read as "[[int_arg1]] percent".
#
# $$
# [[int_arg1]]
# \:\:\:\longrightarrow    \:\:
# [[int_arg1]]\%
# $$
# </div>
# </div>
#         """
#     args = {'arg1': 0.13}
#
#     solution = KnowledgePoint46Solution().get_solution(template, args)
#     print(solution)
#
# main()

###############################################################################


###############################################################################

# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title"
#
# <div class="ex-text">
#
# $$
# [[arg1]] ÷ [[arg2]]
# $$
#
# Divide each number or find the quotient
#
#
# **Step 1:** First we ask ourselves: how many times can [[arg2]] fit into [[arg1]]? The answer is [[arg1//arg2]]. So, we can write [[arg1//arg2]] above the digit [[arg1]] , then we multiply [[arg1//arg2]] by [[arg2]]
#  to get [[arg1//arg2*arg2]] , and write the result underneath the [[arg1]] :
#
# $$
# \begin{array}{r}
# {\color{Salmon}[[arg1//arg2]]}\phantom{)}   \\
# {\color{Salmon}[[arg2]]}{\overline{\smash{\big)}\,[[arg1]] \phantom{)}}}\\
# \underline{{\color{Salmon}-[[arg1//arg2*arg2]]}\phantom{)}}\\
# [[arg1 - arg1//arg2*arg2]]\phantom{)}\\
# \end{array}
# $$
#
#
# So the quotient is $[[arg1//arg2]] $ and the remainder is $[[arg1 - arg1//arg2*arg2]]$.
# </div>
# </div>
#         """
#     args = {'arg1': 49, 'arg2':5}
#     solution = KnowledgePoint35Solution().get_solution(template, args)
#     print(solution)
#
# main()

#############################################################
#
# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title"
#
# <div class="ex-text">
#
# $$
# \frac{[[arg1]]}{[[arg2]]}
# $$
#
#
# $[[arg1]]$ is the numerator and $[[arg2]]$ is denominator.
# </div>
# </div>
#         """
#     args = {'arg1': 9, 'arg2':5}
#     solution = KnowledgePoint33Solution().get_solution(template, args)
#     print(solution)
#
# main()


####################################################################
# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title"
#
# <div class="ex-text">
#
# $$
# [[arg1]] ÷ [[arg2]]
# $$
#
# Divide each number or find the quotient
#
#
# **Step 1:** First we ask ourselves: how many times can [[arg2]] fit into [[arg1]]? The answer is [[arg1//arg2]]. So, we can write [[arg1//arg2]] above the digit [[arg1 %10]], like this:
#
# $$
# \begin{array}{r}
# [[arg1//arg2]]\phantom{)}   \\
# [[arg2]]{\overline{\smash{\big)}\,[[arg1]]\phantom{)}}}\\
# \end{array}
# $$
#
# **Step 2:** Now, we need to multiply $[[arg1//arg2]]$ by [[arg2]] to get [[arg1//arg2 * arg2]], and write the result underneath the [[arg1]]:
# $$
# \begin{array}{r}
# {\color{Salmon}[[arg1//arg2]]}\phantom{)}   \\
# {\color{Salmon}[[arg2]]}{\overline{\smash{\big)}\,[[arg1]]\phantom{)}}}\\
# \underline{{\color{Salmon}-[[arg1//arg2  * arg2]]}\phantom{)}}\\
# [[arg1 - arg1//arg2  * arg2]]\phantom{)}\\
# \end{array}
# $$
#
# So the quotient is [[arg1//arg2]] and the remainder is $[[arg1 %arg2]]$.
# </div>
# </div>
#         """
#     args = {'arg1': 12, 'arg2':5}
#     solution = KnowledgePoint32Solution().get_solution(template, args)
#     print(solution)
#
# main()


# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title">
#
# <div class="ex-text">
#
# $$
# [[arg1]] ÷ [[arg2]]
# $$
#
#
# We can first divide the digit in tens place, and then divide the digit in units place.
# $$
# \begin{array}{r}
# [[arg1//arg2]]\phantom{)}   \\
# [[arg2]]{\overline{\smash{\big)}\,[[arg1]]\phantom{)}}}\\
# \underline{-[[arg1//10]]\phantom{)[[arg1 %10]]}}\\
# [[arg1 %10]]\phantom{)}\\
# -[[arg1 %10]]\phantom{)}\\
# \overline{\phantom{)[[arg1 % 10]]}0\phantom{)}}\\
# \end{array}
# $$
#
# So the answer is $[[arg1//arg2]]$.
# </div>
# </div>
#         """
#     args = {'arg1': 30, 'arg2': 2}
#     solution = KnowledgePoint29Solution().get_solution(template, args)
#     print(solution)
#
# main()


###############################################################
#
# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title">
#
# <div class="ex-text">
# A toy costs $[[arg1]]. Mr.Joe has $[[arg2]]. How many toys can he buy?
#
#
# To find out how many toys Mr.Joe can buy, we can use division.
#
# To divide [[arg1]] by [[arg2]], we can ask ourselves, "How many groups of [[arg2]] are in [[arg1]]?" Each group represents one toy that Mr. Joe can buy. We can count them like this:
# [[arg2]] goes into [[arg1]] [[num2words_arg1_div_arg2]] times.
# Therefore, Mr.Joe can buy $[[arg1]] ÷ [[arg2]] = [[arg1//arg2]]$ toys.
# </div>
# </div>
#
#
#
#
# <div class="ex-yellow">
#     <div class="title">
#         <h2>How Many Toys Can Mr. Joe Buy?</h2>
#     </div>
#     <div class="ex-text">
#         A toy costs $[[arg1]]. Mr. Joe has $[[arg2]]. How many toys can he buy?
#         <p>To find out how many toys Mr. Joe can buy, we can use division.</p>
#         <p>To divide [[arg1]] by [[arg2]], we can ask ourselves, "How many groups of [[arg2]] are in [[arg1]]?" Each group represents one toy that Mr. Joe can buy. We can count them like this:</p>
#         <p>[[arg2]] goes into [[arg1]] [[num2words_arg1_div_arg2]] times.</p>
#         <p>Therefore, Mr. Joe can buy $[[arg1]] ÷ [[arg2]] = [[arg1//arg2]]$ toys.</p>
#     </div>
# </div>
#
#         """
#     args = {'arg1': 120, 'arg2': 5}
#     solution = KnowledgePoint30Solution().get_solution(template, args)
#     print(solution)
#
# main()


# ######################################################################


#######################################################
# def main():
#     start_time = time.time()
#     template = r"""<div class="ex-yellow">
# <div class="title"
# <div class="ex-text" align="center">
#
# There are **[[arg1]]** pencils and the teacher has to distribute these equally among **[[arg2]]** students.
# How many pencils will each student get?
#
# To distribute **[[arg1]]** pencils equally among **[[arg2]]** students, we can use division.
#
# We can divide the total number of pencils **[[arg1]]** by the number of students **[[arg2]]** :
#
# **[[arg1]]** pencils ÷ **[[arg2]]** students = **[[arg1//arg2]]** pencils per student
#
# Therefore, each student will get [[arg1]] ÷ [[arg2]] = [[arg1//arg2]] pencils.
# </div>
# </div>
#
#     """
#     args = {'arg1': 20, 'arg2': 4}
#     solution = KnowledgePoint27Solution().get_solution(template, args)
#     print(solution)
#
# main()

#############################################################################

# def main():
#     start_time = time.time()
#     template = r"""
#     """
#     args = {'arg1': 20, 'arg2': "ones", 'arg3': 2, 'arg4': "tens"}
#     solution = KnowledgePoint7Solution().get_solution(template, args)
#     print(solution)
#
# main()

##################################################################################
#     template = r"""<div class="ex-yellow">
# <div class="title">
# Solution
# </div>
# <div class="ex-text" align="center">
#
# $[[arg1]]$ $=$ __tens $+$ __ones
# </div>
#
# <div class="cube-display">
# <div class="cube-wrap">
# <div class="cube-container">
# <div class="cube-box">
# <span></span>
# <span></span>
# <span></span>
# <span></span>
# <span></span>
# <span></span>
# <span></span>
# <span></span>
# <span></span>
# <span></span>
# </div>
# </div>
#
# $+$
# <div class="cube-container">
# </div>
#
# </div>
# <div class="cube-number">
# <span>
#
# $[[arg1 //10]]$
# </span>
# <span>
#
# $[[arg1 % 10]]$
# </span>
# </div>
# </div>
#
# **Step 1:** The "tens" part tells us how many groups of ten there are in [[arg1]]. In this case, there is only [[arg1//10]] group of ten.
# <div align="center">
#
# $[[arg1//10]] $ tens = $[[arg1//10 * 10]] $
# </div>
#
# **Step 2:** The "ones" part tells us how many ones there are in [[arg1]]. In this case, there are [[arg1 % 10]] ones.
# <div align="center">
#
# $ [[arg1 % 10]] $ ones = $ [[arg1 % 10]] $
# </div>
#
# **Step 3:** When we add the number of tens and the number of ones together, we get the original number, which is [[arg1]].
#
# So, **[[arg1]] = __tens + __ones** just helps us understand how the number [[arg1]] is made up of two smaller parts, and how those parts add up to give us [[arg1]]. [[statement_of_one_tens(arg1)]]
# <div align="center">
#
# $[[arg1]]$ $=$ ${\color{Salmon}[[arg1//10]]}$ tens [[result_statement(arg1)]]
# </div>
# </div>
#
# <div class="ex-yellow">
# <div class="title">
# <div class="ex-yellow">
# <div class="title">
# Solution
# </div>
# <div class="ex-text" align="center">
#
# $[[arg1]]$ $=$ __tens $+$ __ones
# </div>
#
# <div class="cube-display">
# <div class="cube-wrap">
# <div class="cube-container">
# <div class="cube-box">
# <span></span>
# <span></span>
# <span></span>
# <span></span>
# <span></span>
# <span></span>
# <span></span>
# <span></span>
# <span></span>
# <span></span>
# </div>
# </div>
#
# $+$
# <div class="cube-container">
# </div>
#
# </div>
# <div class="cube-number">
# <span>
#
# $[[arg1 //10]]$
# </span>
# <span>
#
# $[[arg1 % 10]]$
# </span>
# </div>
# </div>
#
# **Step 1:** The "tens" part tells us how many groups of ten there are in [[arg1]]. In this case, there is only [[arg1//10]] group of ten.
# <div align="center">
#
# $[[arg1//10]] $ tens = $[[arg1//10 * 10]] $
# </div>
#
# **Step 2:** The "ones" part tells us how many ones there are in [[arg1]]. In this case, there are [[arg1 % 10]] ones.
# <div align="center">
#
# $ [[arg1 % 10]] $ ones = $ [[arg1 % 10]] $
# </div>
#
# **Step 3:** When we add the number of tens and the number of ones together, we get the original number, which is [[arg1]].
#
# So, **[[arg1]] = __tens + __ones** just helps us understand how the number [[arg1]] is made up of two smaller parts, and how those parts add up to give us [[arg1]]. [[statement_of_one_tens(arg1)]]
# <div align="center">
#
# $[[arg1]]$ $=$ ${\color{Salmon}[[arg1//10]]}$ tens [[result_statement(arg1)]]
# </div>
# </div>
#
# <div class="ex-yellow">
# <div class="title">"""
#     args = {'arg1': 21, 'arg2': "ones", 'arg3': 2, 'arg4': "tens"}
#     solution = KnowledgePoint7Solution().get_solution(template, args)
#     print(solution)


## main()
