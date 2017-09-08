# Helper methods to parse Lisp-like expressions.

def parse_sexpr(sexpr_str):
    return recursive_descent(tokenize(sexpr_str))[0][0]

def tokenize(sexpr_str):
    return [x for x in sexpr_str.replace("(", " ( ")
                     .replace(")", " ) ")
                      .split(" ")
                       if x]

def recursive_descent(tokens, idx=0):
    sexpr = []

    while idx < len(tokens):
        token = tokens[idx]
        if token == ")":
            return tuple(sexpr), idx + 1
        if token == "(":
            child_sexpr, new_idx = recursive_descent(tokens, idx + 1)
            sexpr.append(child_sexpr)
            idx = new_idx
        else:
            try:
                sexpr.append(int(token))
            except ValueError:
                sexpr.append(token)
            idx += 1
    return tuple(sexpr), idx + 1
