from typing import Any, Optional, List
from mcp.server.fastmcp import FastMCP
import subprocess
import json
import re

# Initialize FastMCP server
mcp = FastMCP(
    name="qalc"
)

def _run_qalc(args: List[str], timeout: int = 30) -> str:
    """
    Execute qalc with given arguments and return the output.
    
    Args:
        args: List of command line arguments for qalc
        timeout: Maximum execution time in seconds
        
    Returns:
        The output from qalc command
        
    Raises:
        Various exceptions for different error conditions
    """
    try:
        result = subprocess.run(
            ['qalc'] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        raise Exception(f"Calculation timed out after {timeout} seconds")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "Unknown calculation error"
        raise Exception(f"Calculation error: {error_msg}")
    except FileNotFoundError:
        raise Exception("libqalculate (qalc) is not installed or not found in PATH. Please install it first.")

@mcp.tool()
def evaluate_expression(expression: str, timeout: int = 30) -> str:
    """
    Evaluate a mathematical expression using libqalculate with full formatting.
    
    This is the main evaluation tool that provides rich, formatted output including
    the original expression and detailed results. Supports all libqalculate features
    including units, symbolic math, functions, constants, and more.
    
    Args:
        expression: Mathematical expression to evaluate (e.g., "sqrt(32)", "5 ft to m", "solve x^2=4")
        timeout: Maximum execution time in seconds (default: 30)
        
    Returns:
        Formatted calculation result with full context
        
    Examples:
        - "2+2" → "2 + 2 = 4"
        - "sqrt(32)" → "sqrt(32) = 4 × √(2) ≈ 5.6568542"
        - "5 ft to m" → "5 feet = 1.524 m"
        - "solve x^2=4" → "x^2 = 4 = (x = 2 or x = -2)"
    """
    try:
        return _run_qalc([expression], timeout)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def evaluate_terse(expression: str, timeout: int = 30) -> str:
    """
    Evaluate a mathematical expression with minimal output (numbers only).
    
    Returns just the numerical result without formatting, units, or context.
    Useful when you need clean numerical values for further processing.
    
    Args:
        expression: Mathematical expression to evaluate
        timeout: Maximum execution time in seconds (default: 30)
        
    Returns:
        Minimal numerical result
        
    Examples:
        - "2+2" → "4"
        - "sqrt(32)" → "5.6568542"
        - "pi" → "3.1415927"
    """
    try:
        return _run_qalc(['-t', expression], timeout)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def evaluate_with_options(
    expression: str,
    precision: Optional[int] = None,
    approximation: Optional[str] = None,
    base: Optional[int] = None,
    angle_unit: Optional[str] = None,
    timeout: int = 30
) -> str:
    """
    Evaluate expression with specific calculation options and formatting control.
    
    Args:
        expression: Mathematical expression to evaluate
        precision: Number of decimal places for results (e.g., 10, 20)
        approximation: Approximation mode - "exact", "try_exact", or "approximate"
        base: Number base for input/output (2-36, e.g., 2 for binary, 16 for hex)
        angle_unit: Angle unit - "radians", "degrees", or "gradians"
        timeout: Maximum execution time in seconds (default: 30)
        
    Returns:
        Calculation result with specified formatting
        
    Examples:
        - evaluate_with_options("pi", precision=15) → High precision pi
        - evaluate_with_options("sqrt(2)", approximation="exact") → "√(2)"
        - evaluate_with_options("255", base=16) → "0xFF"
        - evaluate_with_options("sin(90)", angle_unit="degrees") → "1"
    """
    try:
        args = []
        
        # Build qalc arguments based on options
        if base is not None:
            if not (2 <= base <= 36):
                raise ValueError("Base must be between 2 and 36")
            args.extend(['-b', str(base)])
        
        # Set various options using -s (set) flag
        set_options = []
        
        if precision is not None:
            if precision < 1:
                raise ValueError("Precision must be at least 1")
            set_options.append(f"precision {precision}")
        
        if approximation is not None:
            if approximation not in ["exact", "try_exact", "approximate"]:
                raise ValueError("Approximation must be 'exact', 'try_exact', or 'approximate'")
            # Map to qalc approximation settings
            approx_map = {
                "exact": "approximation 0",
                "try_exact": "approximation 1", 
                "approximate": "approximation 2"
            }
            set_options.append(approx_map[approximation])
        
        if angle_unit is not None:
            if angle_unit not in ["radians", "degrees", "gradians"]:
                raise ValueError("Angle unit must be 'radians', 'degrees', or 'gradians'")
            # Map to qalc angle unit settings
            angle_map = {
                "radians": "angle radians",
                "degrees": "angle degrees", 
                "gradians": "angle gradians"
            }
            set_options.append(angle_map[angle_unit])
        
        # Add set options to arguments
        for option in set_options:
            args.extend(['-s', option])
        
        # Add the expression
        args.append(expression)
        
        return _run_qalc(args, timeout)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def convert_units(value: str, target_unit: str, timeout: int = 30) -> str:
    """
    Convert between different units of measurement.
    
    Supports all SI units, imperial units, currencies, and specialized units.
    Handles automatic unit recognition and conversion.
    
    Args:
        value: Value with source unit (e.g., "5 ft", "100 km/h", "25 °C")
        target_unit: Target unit to convert to (e.g., "m", "mph", "°F")
        timeout: Maximum execution time in seconds (default: 30)
        
    Returns:
        Conversion result with both original and converted values
        
    Examples:
        - convert_units("5 ft", "m") → "5 feet = 1.524 m"
        - convert_units("100 km/h", "mph") → "100 km/h = 62.137119 mph"
        - convert_units("25 °C", "°F") → "25 °C = 77 °F"
        - convert_units("1 atm", "Pa") → "1 atm = 101325 Pa"
    """
    try:
        expression = f"{value} to {target_unit}"
        return _run_qalc([expression], timeout)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def convert_base(number: str, target_base: int, source_base: Optional[int] = None, timeout: int = 30) -> str:
    """
    Convert numbers between different number bases.
    
    Supports bases 2-36, with automatic detection of common formats (0x for hex, 0b for binary).
    
    Args:
        number: Number to convert (e.g., "255", "0xFF", "0b1010")
        target_base: Target base (2-36)
        source_base: Source base if not auto-detectable (2-36)
        timeout: Maximum execution time in seconds (default: 30)
        
    Returns:
        Number conversion result
        
    Examples:
        - convert_base("255", 16) → "255 = 0xFF"
        - convert_base("0xFF", 10) → "0xFF = 255"
        - convert_base("1010", 10, 2) → "1010₂ = 10"
    """
    try:
        if not (2 <= target_base <= 36):
            raise ValueError("Target base must be between 2 and 36")
        
        if source_base is not None and not (2 <= source_base <= 36):
            raise ValueError("Source base must be between 2 and 36")
        
        args = ['-b', str(target_base)]
        
        # If source base is specified and different from 10, we need to indicate it
        if source_base is not None and source_base != 10:
            # For non-decimal source, we use the base() function
            expression = f"base({number}; {source_base})"
        else:
            expression = number
            
        args.append(expression)
        return _run_qalc(args, timeout)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def symbolic_calculation(expression: str, timeout: int = 30) -> str:
    """
    Perform symbolic mathematical operations like factoring, expanding, and solving.
    
    Handles algebraic manipulation, equation solving, and symbolic computation.
    
    Args:
        expression: Symbolic expression or command (e.g., "factor x^2-4", "expand (x+1)^2", "solve x^2=9")
        timeout: Maximum execution time in seconds (default: 30)
        
    Returns:
        Symbolic calculation result
        
    Examples:
        - "factor x^2-4" → "x^2 - 4 = (x - 2) × (x + 2)"
        - "expand (x+1)^2" → "(x + 1)^2 = x^2 + 2x + 1"
        - "solve x^2=9" → "x^2 = 9 = (x = 3 or x = -3)"
        - "simplify (x^2+2x+1)/(x+1)" → "(x^2 + 2x + 1)/(x + 1) = x + 1"
    """
    try:
        # Set to exact mode for symbolic calculations
        return _run_qalc(['-s', 'approximation 0', expression], timeout)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def calculus_operation(expression: str, operation: str, variable: str = "x", timeout: int = 30) -> str:
    """
    Perform calculus operations like differentiation and integration.
    
    Args:
        expression: Mathematical expression to operate on (e.g., "x^2", "sin(x)")
        operation: Calculus operation - "diff" for derivative, "integrate" for integral
        variable: Variable to differentiate/integrate with respect to (default: "x")
        timeout: Maximum execution time in seconds (default: 30)
        
    Returns:
        Calculus operation result
        
    Examples:
        - calculus_operation("x^2", "diff") → "diff(x^2) = 2x"
        - calculus_operation("x^3", "integrate") → "integrate(x^3) = x^4/4 + C"
        - calculus_operation("sin(t)", "diff", "t") → "diff(sin(t), t) = cos(t)"
    """
    try:
        if operation not in ["diff", "integrate"]:
            raise ValueError("Operation must be 'diff' or 'integrate'")
        
        if operation == "diff":
            calc_expression = f"diff({expression}; {variable})"
        else:  # integrate
            calc_expression = f"integrate({expression}; {variable})"
        
        # Use exact mode for symbolic calculus
        return _run_qalc(['-s', 'approximation 0', calc_expression], timeout)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def statistical_calculation(data: str, operation: str, timeout: int = 30) -> str:
    """
    Perform statistical calculations on data sets.
    
    Args:
        data: Data values separated by semicolons or as vector (e.g., "1; 2; 3; 4; 5" or "[1, 2, 3, 4, 5]")
        operation: Statistical operation - "mean", "median", "stdev", "variance", "min", "max", "quartile", "percentile"
        timeout: Maximum execution time in seconds (default: 30)
        
    Returns:
        Statistical calculation result
        
    Examples:
        - statistical_calculation("1; 2; 3; 4; 5", "mean") → "mean(1; 2; 3; 4; 5) = 3"
        - statistical_calculation("[1, 2, 3, 4, 5]", "stdev") → "stdev([1, 2, 3, 4, 5]) ≈ 1.58"
        - statistical_calculation("1; 2; 3; 4; 5", "median") → "median(1; 2; 3; 4; 5) = 3"
    """
    try:
        valid_operations = ["mean", "median", "stdev", "variance", "min", "max", "quartile", "percentile"]
        if operation not in valid_operations:
            raise ValueError(f"Operation must be one of: {', '.join(valid_operations)}")
        
        expression = f"{operation}({data})"
        return _run_qalc([expression], timeout)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def matrix_vector_operation(expression: str, timeout: int = 30) -> str:
    """
    Perform matrix and vector operations.
    
    Supports matrix arithmetic, determinants, inverses, dot products, cross products, and more.
    
    Args:
        expression: Matrix/vector expression (e.g., "[1, 2; 3, 4]", "det([1,2;3,4])", "[1,2,3] × [4,5,6]")
        timeout: Maximum execution time in seconds (default: 30)
        
    Returns:
        Matrix/vector operation result
        
    Examples:
        - "[1, 2; 3, 4]" → Matrix display
        - "det([1,2;3,4])" → "det(((1, 2), (3, 4))) = -2"
        - "[1,2,3] × [4,5,6]" → Cross product result
        - "inverse([1,2;3,4])" → Matrix inverse
        - "||[3,4,5]||" → Vector magnitude
    """
    try:
        return _run_qalc([expression], timeout)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_functions(search_term: Optional[str] = None, timeout: int = 30) -> str:
    """
    List available mathematical functions.
    
    Args:
        search_term: Optional search term to filter functions (e.g., "sin", "log")
        timeout: Maximum execution time in seconds (default: 30)
        
    Returns:
        List of available functions, optionally filtered by search term
        
    Examples:
        - list_functions() → All available functions
        - list_functions("sin") → Functions containing "sin"
        - list_functions("log") → Logarithmic functions
    """
    try:
        args = ['--list-functions']
        if search_term:
            args.append(search_term)
        return _run_qalc(args, timeout)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_units(search_term: Optional[str] = None, timeout: int = 30) -> str:
    """
    List available units of measurement.
    
    Args:
        search_term: Optional search term to filter units (e.g., "meter", "temp", "time")
        timeout: Maximum execution time in seconds (default: 30)
        
    Returns:
        List of available units, optionally filtered by search term
        
    Examples:
        - list_units() → All available units
        - list_units("meter") → Length units containing "meter"
        - list_units("temp") → Temperature units
    """
    try:
        args = ['--list-units']
        if search_term:
            args.append(search_term)
        return _run_qalc(args, timeout)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_variables(search_term: Optional[str] = None, timeout: int = 30) -> str:
    """
    List available variables and constants.
    
    Args:
        search_term: Optional search term to filter variables (e.g., "pi", "speed", "planck")
        timeout: Maximum execution time in seconds (default: 30)
        
    Returns:
        List of available variables and constants, optionally filtered by search term
        
    Examples:
        - list_variables() → All available variables and constants
        - list_variables("pi") → Variables containing "pi"
        - list_variables("speed") → Speed-related constants
        - list_variables("planck") → Planck-related constants
    """
    try:
        args = ['--list-variables']
        if search_term:
            args.append(search_term)
        return _run_qalc(args, timeout)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def list_prefixes(search_term: Optional[str] = None, timeout: int = 30) -> str:
    """
    List available unit prefixes (like kilo, mega, micro, etc.).
    
    Args:
        search_term: Optional search term to filter prefixes
        timeout: Maximum execution time in seconds (default: 30)
        
    Returns:
        List of available unit prefixes, optionally filtered by search term
        
    Examples:
        - list_prefixes() → All available prefixes
        - list_prefixes("k") → Prefixes containing "k"
    """
    try:
        args = ['--list-prefixes']
        if search_term:
            args.append(search_term)
        return _run_qalc(args, timeout)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def update_exchange_rates(timeout: int = 60) -> str:
    """
    Update currency exchange rates for conversions.
    
    Downloads the latest exchange rates from online sources for accurate currency conversions.
    
    Args:
        timeout: Maximum execution time in seconds (default: 60)
        
    Returns:
        Status message about exchange rate update
    """
    try:
        return _run_qalc(['-e'], timeout)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def programming_mode_calculation(expression: str, base: int = 16, timeout: int = 30) -> str:
    """
    Evaluate expressions in programming mode with bitwise operations and base conversions.
    
    Programming mode is useful for bitwise operations, boolean logic, and working with
    different number bases commonly used in programming.
    
    Args:
        expression: Expression to evaluate (e.g., "0xFF & 0x0F", "52 << 2", "~0b1010")
        base: Default base for input/output (default: 16 for hexadecimal)
        timeout: Maximum execution time in seconds (default: 30)
        
    Returns:
        Programming calculation result with base conversions
        
    Examples:
        - "0xFF & 0x0F" → Bitwise AND operation
        - "52 << 2" → Left bit shift
        - "~0b1010" → Bitwise NOT operation
    """
    try:
        # Programming mode with specified base
        args = ['-p', str(base), expression]
        return _run_qalc(args, timeout)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')