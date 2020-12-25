# CS635-parse-exp-value
1.
Add a new rule to Rule set 3:

3  <factor> → <number> | pi | -<factor> | (<exp>) | <func>

The last option adds the capability to parse parenthesized expressions.

2.
Implement the following grammar rules for the parser:

4 <func> → <func name>(<exp>)
5 <func name> → sin | cos | tan | exp | sqrt | abs

This will give the parser the capability to do function calls for one-parameter functions.

When implementing these rulesm we want to maintain the separation of the parser into a front end and back end, so when the parser front end parses a function call, it should call
a function like:

func_call (func_name, exp_value)

This function will be implemented in the parser back end to compute the value.

3.
Implement assign,ent and a symbol table. The project is described in this pdf:

ParseAssign.pdf

