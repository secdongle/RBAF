from sympy import *


def calc_count(average_rate_of_return, average_loss_rate, average_accuracy, target_rate_of_return, position_ratio):
    x = Symbol('x')
    try:
        solved_value = solve([(1 + average_rate_of_return) ** (average_accuracy * x) * (1 - average_loss_rate) ** (
                (1 - average_accuracy) * x) - (1 + target_rate_of_return)], x)
        if len(solved_value) == 0:
            return 0
        else:
            all_count = solved_value[0][0]
            counts = all_count * (1 / position_ratio)
            return counts
    except Exception as e:
        print(e)


def calc_return_loss(succ_count, fail_count, target_return, benefit_risk_ratio):
    x = Symbol('x')
    y = Symbol('y')
    solved_value = solve([succ_count * x - y * fail_count - target_return, x - benefit_risk_ratio * y], [x, y])
    xy_result = list()
    for _, v in solved_value.items():
        xy_result.append(float(v))
    return xy_result
