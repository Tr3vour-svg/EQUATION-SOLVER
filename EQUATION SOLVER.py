from abc import ABC, abstractmethod
import re
import math


class Equation(ABC):
    degree: int
    type: str

    def __init__(self, *args):
        if (self.degree + 1) != len(args):
            raise TypeError(
                f"'Equation' object takes {self.degree + 1} positional arguments but {len(args)} were given"
            )
        if any(not isinstance(arg, (int, float)) for arg in args):
            raise TypeError("Coefficients must be of type 'int' or 'float'")
        if args[0] == 0:
            raise ValueError(
                "Highest degree coefficient must be different from zero")
        self.coefficients = {
            (len(args) - n - 1): arg for n, arg in enumerate(args)}

    def __init_subclass__(cls):
        if not hasattr(cls, "degree"):
            raise AttributeError(
                f"Cannot create '{cls.__name__}' class: missing required attribute 'degree'"
            )
        if not hasattr(cls, "type"):
            raise AttributeError(
                f"Cannot create '{cls.__name__}' class: missing required attribute 'type'"
            )

    def __str__(self):
        terms = []
        for n, coefficient in self.coefficients.items():
            if not coefficient:
                continue
            if n == 0:
                terms.append(f'{coefficient:+}')
            elif n == 1:
                terms.append(f'{coefficient:+}x')
            else:
                terms.append(f"{coefficient:+}x**{n}")
        equation_string = ' '.join(terms) + ' = 0'
        return re.sub(r"(?<!\d)1(?=x)", "", equation_string.strip("+"))

    @abstractmethod
    def solve(self):
        pass

    @abstractmethod
    def analyze(self):
        pass


class LinearEquation(Equation):
    degree = 1
    type = 'Linear Equation'

    def solve(self):
        a, b = self.coefficients.values()
        x = -b / a
        return [x]

    def analyze(self):
        slope, intercept = self.coefficients.values()
        return {'slope': slope, 'intercept': intercept}


class QuadraticEquation(Equation):
    degree = 2
    type = 'Quadratic Equation'

    def __init__(self, *args):
        super().__init__(*args)
        a, b, c = self.coefficients.values()
        self.delta = b**2 - 4 * a * c

    def solve(self):
        if self.delta < 0:
            return []
        a, b, _ = self.coefficients.values()
        x1 = (-b + self.delta ** 0.5) / (2 * a)
        x2 = (-b - self.delta ** 0.5) / (2 * a)
        return [x1] if self.delta == 0 else [x1, x2]

    def analyze(self):
        a, b, c = self.coefficients.values()
        x = -b / (2 * a)
        y = a * x**2 + b * x + c
        concavity = 'upwards' if a > 0 else 'downwards'
        min_max = 'min' if a > 0 else 'max'
        return {'x': x, 'y': y, 'min_max': min_max, 'concavity': concavity}


class CubicEquation(Equation):
    degree = 3
    type = 'Cubic Equation'

    def __init__(self, *args):
        super().__init__(*args)
        a, b, c, d = self.coefficients.values()
        self.a, self.b, self.c, self.d = a, b, c, d

    def solve(self):
        a, b, c, d = self.a, self.b, self.c, self.d
        f = ((3 * c / a) - ((b ** 2) / (a ** 2))) / 3
        g = ((2 * (b ** 3) / (a ** 3)) -
             (9 * b * c / (a ** 2)) + (27 * d / a)) / 27
        h = (g ** 2) / 4 + (f ** 3) / 27

        roots = []
        if h > 0:
            R = -(g / 2) + h ** 0.5
            S = R ** (1 / 3)
            T = -(g / 2) - h ** 0.5
            U = T ** (1 / 3)
            x1 = (S + U) - (b / (3 * a))
            roots.append(x1)
        elif f == g == h == 0:
            x = - (d / a) ** (1 / 3)
            roots.append(x)
        else:
            i = math.sqrt((g ** 2) / 4 - h)
            j = i ** (1 / 3)
            k = math.acos(-(g / (2 * i)))
            L = -j
            M = math.cos(k / 3)
            N = math.sqrt(3) * math.sin(k / 3)
            P = - (b / (3 * a))
            x1 = 2 * j * math.cos(k / 3) - (b / (3 * a))
            x2 = L * (M + N) + P
            x3 = L * (M - N) + P
            roots.extend([x1, x2, x3])
        return roots

    def analyze(self):
        x_inflect = -self.b / (3 * self.a)
        y_inflect = self.a * x_inflect**3 + self.b * \
            x_inflect**2 + self.c * x_inflect + self.d
        return {'inflection_x': x_inflect, 'inflection_y': y_inflect}


def solver(equation):
    if not isinstance(equation, Equation):
        raise TypeError("Argument must be an Equation object")

    output_string = f'\n{equation.type:-^24}'
    output_string += f'\n\n{equation!s:^24}\n\n'
    output_string += f'{"Solutions":-^24}\n\n'
    results = equation.solve()
    match results:
        case []:
            result_list = ['No real roots']
        case [x]:
            result_list = [f'x = {x:+.3f}']
        case [x1, x2]:
            result_list = [f'x1 = {x1:+.3f}', f'x2 = {x2:+.3f}']
        case [x1, x2, x3]:
            result_list = [f'x1 = {x1:+.3f}',
                           f'x2 = {x2:+.3f}', f'x3 = {x3:+.3f}']
    for result in result_list:
        output_string += f'{result:^24}\n'

    output_string += f'\n{"Details":-^24}\n\n'
    details = equation.analyze()
    match details:
        case {'slope': slope, 'intercept': intercept}:
            details_list = [
                f'slope = {slope:>16.3f}',
                f'y-intercept = {intercept:>10.3f}'
            ]
        case {'x': x, 'y': y, 'min_max': min_max, 'concavity': concavity}:
            coord = f'({x:.3f}, {y:.3f})'
            details_list = [
                f'concavity = {concavity:>13}',
                f'{min_max} = {coord:>20}'
            ]
        case {'inflection_x': x, 'inflection_y': y}:
            coord = f'({x:.3f}, {y:.3f})'
            details_list = [
                f'inflection point = {coord:>14}'
            ]
    for detail in details_list:
        output_string += f'{detail}\n'
    return output_string


# Example usage
if __name__ == "__main__":
    lin_eq = LinearEquation(2, 3)
    quadr_eq = QuadraticEquation(1, 2, 1)
    cubic_eq = CubicEquation(1, -6, 11, -6)

    print(solver(lin_eq))
    print(solver(quadr_eq))
    print(solver(cubic_eq))
