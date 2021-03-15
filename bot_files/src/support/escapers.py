def aggressive_escaper(_s):
    return _s.translate(str.maketrans({"-": r"\-",
                                       "=": r"\=",
                                       "_": r"\_",
                                       "*": r"\*",
                                       "[": r"\[",
                                       "]": r"\]",
                                       "(": r"\(",
                                       ")": r"\)",
                                       "~": r"\~",
                                       "`": r"\`",
                                       "#": r"\#",
                                       "+": r"\+",
                                       "|": r"\|",
                                       "{": r"\{",
                                       "}": r"\}",
                                       "!": r"\!",
                                       ">": r"\>",
                                       "<": r"\<",
                                       ".": r"\."}))


def remove_regxx(_s):
    return _s.replace("regx*x", "").replace("regx_x", "")


def escaped(_s):
    _s = aggressive_escaper(_s)
    return _s.replace("regx\*x", "*").replace("regx\_x", "_")
