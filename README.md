# EQUATION-SOLVER
A robust, user-friendly tool that solves various mathematical equations (linear, quadratic, cubic equations.). Provides step-by-step solutions for enhanced learning and quick results. Accurate and efficient computation engine using OOP.
## Features
This toolkit implements an abstract base class (Equation) from which concrete classes for specific polynomial degrees inherit. The core features include:

Robust Initialization: Validates coefficient inputs, ensuring the highest degree coefficient is non-zero.

Clear Representation: A user-friendly __str__ method to display the equation in standard form (e.g., ax^n + ... = 0).

Root Calculation: Solves for real roots using appropriate mathematical methods (direct solution, quadratic formula, Cardano's method).

Equation Analysis: Provides key mathematical details for each equation type.
Formatted Output: The solver utility function presents results and analysis in a clean, centered format.
### Getting Started
Prerequisites
You need Python 3.10 or later to run this project, as it utilizes the modern match/case statement in the solver function.

Installation
No external libraries are required beyond the standard Python abc, re, and math modules.

Save the Code: Save the provided Python code as a file named equation_solver.py.

Run the Examples: Execute the file directly to see the example usage:

Bash
python equation_solver.py
#### Design Structure
Equation(ABC)The base class defines the structure:Attributes: degree, type, coefficientsAbstract Methods: solve(), analyze()Validation: Ensures the number of coefficients matches the degree and that the leading coefficient is non-zero.Derived ClassesEach class provides concrete implementations:LinearEquation: Simple division for solving, returns slope/intercept for analysis.QuadraticEquation: Calculates the discriminant (self.delta) on initialization to handle real/complex root cases in solve(), calculates the vertex for analysis.CubicEquation: Implements the complex steps of Cardano's method to find up to three real roots, calculates the inflection point ($\frac{-b}{3a}$) for analysis.solver(equation)The utility function responsible for:Type-checking the input.Calling the object's __str__, solve(), and analyze() methods.Formatting the output using match/case to properly display the roots ($x, x1, x2...$) and analysis details.
