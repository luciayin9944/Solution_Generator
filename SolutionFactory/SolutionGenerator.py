from abc import ABC, abstractmethod
import re
import time


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


def main():
    start_time = time.time()
    template = r"""<div class="ex-yellow">  
<div class="title">  
Solution  
</div>  
<div class="ex-text" align="center">  
  
$[[arg1]]$ $=$ __tens $+$ __ones  
</div>  
  
<div class="cube-display">  
<div class="cube-wrap">  
<div class="cube-container">  
<div class="cube-box">  
<span></span>  
<span></span>  
<span></span>  
<span></span>  
<span></span>  
<span></span>  
<span></span>  
<span></span>  
<span></span>  
<span></span>  
</div>  
</div>  
  
$+$  
<div class="cube-container">  
</div>  
  
</div>  
<div class="cube-number">  
<span>  
  
$[[arg1 //10]]$  
</span>  
<span>  
  
$[[arg1 % 10]]$  
</span>  
</div>  
</div>  
  
**Step 1:** The "tens" part tells us how many groups of ten there are in [[arg1]]. In this case, there is only [[arg1//10]] group of ten.  
<div align="center">  
  
$[[arg1//10]] $ tens = $[[arg1//10 * 10]] $  
</div>  
  
**Step 2:** The "ones" part tells us how many ones there are in [[arg1]]. In this case, there are [[arg1 % 10]] ones.  
<div align="center">  
  
$ [[arg1 % 10]] $ ones = $ [[arg1 % 10]] $  
</div>  
  
**Step 3:** When we add the number of tens and the number of ones together, we get the original number, which is [[arg1]].  
  
So, **[[arg1]] = __tens + __ones** just helps us understand how the number [[arg1]] is made up of two smaller parts, and how those parts add up to give us [[arg1]]. [[statement_of_one_tens(arg1)]]  
<div align="center">  
  
$[[arg1]]$ $=$ ${\color{Salmon}[[arg1//10]]}$ tens [[result_statement(arg1)]]  
</div>  
</div>  
  
<div class="ex-yellow">  
<div class="title">
<div class="ex-yellow">  
<div class="title">  
Solution  
</div>  
<div class="ex-text" align="center">  
  
$[[arg1]]$ $=$ __tens $+$ __ones  
</div>  
  
<div class="cube-display">  
<div class="cube-wrap">  
<div class="cube-container">  
<div class="cube-box">  
<span></span>  
<span></span>  
<span></span>  
<span></span>  
<span></span>  
<span></span>  
<span></span>  
<span></span>  
<span></span>  
<span></span>  
</div>  
</div>  
  
$+$  
<div class="cube-container">  
</div>  
  
</div>  
<div class="cube-number">  
<span>  
  
$[[arg1 //10]]$  
</span>  
<span>  
  
$[[arg1 % 10]]$  
</span>  
</div>  
</div>  
  
**Step 1:** The "tens" part tells us how many groups of ten there are in [[arg1]]. In this case, there is only [[arg1//10]] group of ten.  
<div align="center">  
  
$[[arg1//10]] $ tens = $[[arg1//10 * 10]] $  
</div>  
  
**Step 2:** The "ones" part tells us how many ones there are in [[arg1]]. In this case, there are [[arg1 % 10]] ones.  
<div align="center">  
  
$ [[arg1 % 10]] $ ones = $ [[arg1 % 10]] $  
</div>  
  
**Step 3:** When we add the number of tens and the number of ones together, we get the original number, which is [[arg1]].  
  
So, **[[arg1]] = __tens + __ones** just helps us understand how the number [[arg1]] is made up of two smaller parts, and how those parts add up to give us [[arg1]]. [[statement_of_one_tens(arg1)]]  
<div align="center">  
  
$[[arg1]]$ $=$ ${\color{Salmon}[[arg1//10]]}$ tens [[result_statement(arg1)]]
</div>  
</div>  
  
<div class="ex-yellow">  
<div class="title">"""
    args = {'arg1': 15, 'arg2': "ones", 'arg3': 2, 'arg4': "tens"}
    solution = KnowledgePoint7Solution().get_solution(template, args)
    print(solution)


main()
