# Qalc MCP Server

A comprehensive Model Context Protocol (MCP) server that exposes the powerful libqalculate calculation engine to LLM agents. This server provides advanced mathematical computation capabilities including basic arithmetic, symbolic math, unit conversions, calculus operations, statistical calculations, and much more.

## Features

### Core Mathematical Operations
- **Basic Arithmetic**: Standard operations (+, -, *, /, ^, mod, etc.)
- **Advanced Functions**: Trigonometric, logarithmic, exponential, hyperbolic functions
- **Complex Numbers**: Full support for complex number arithmetic
- **Exact vs Approximate**: Choose between exact symbolic results or decimal approximations

### Unit System Support
- **Comprehensive Units**: All SI units, imperial units, and many specialized units
- **Automatic Conversion**: Smart unit conversion and dimensional analysis
- **Currency Conversion**: Real-time exchange rates (when available)
- **Custom Units**: Support for user-defined units

### Number Systems
- **Multiple Bases**: Binary, octal, decimal, hexadecimal, and custom bases (2-36)
- **Roman Numerals**: Convert to/from Roman numeral notation
- **Sexagesimal**: Support for time format and angular measurements
- **Scientific Notation**: Handle very large and very small numbers

### Symbolic Mathematics
- **Algebraic Manipulation**: Expand, factor, and simplify expressions
- **Equation Solving**: Solve equations and inequalities symbolically
- **Calculus**: Derivatives, integrals, limits
- **Matrix Operations**: Matrix arithmetic, determinants, inverses

### Statistical Functions
- **Descriptive Statistics**: Mean, median, mode, standard deviation, variance
- **Probability Distributions**: Normal, binomial, and other distributions
- **Data Analysis**: Support for vectors and data sets

### Advanced Features
- **Uncertainty Propagation**: Handle measurements with uncertainty (±)
- **Interval Arithmetic**: Calculate with ranges of values
- **Date/Time Calculations**: Date arithmetic and time zone conversions
- **Physical Constants**: Access to extensive library of physical constants

## Installation

### Prerequisites

This MCP server requires [uv](https://docs.astral.sh/uv/) and libqalculate to be installed on your system.

Install uv if you don't have it:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install libqalculate for your platform:

#### macOS (using Homebrew)
```bash
brew install libqalculate
```

#### Ubuntu/Debian
```bash
sudo apt-get install qalc
```

#### Windows
Download from [libqalculate releases](https://github.com/Qalculate/libqalculate/releases) or use package managers like Chocolatey.

#### Other Systems
See the [libqalculate installation guide](https://qalculate.github.io/downloads.html) for your platform.

### Clone and Set Up the MCP Server

```bash
git clone https://github.com/Genteure/qalc-mcp.git
cd qalc-mcp
uv sync
```

### Verify Installation

```bash
uv run mcp run qalc.py
```

## Usage

This server provides 15 comprehensive tools for different calculation needs:

## Core Evaluation Tools

### `evaluate_expression(expression, timeout=30)`
General mathematical expression evaluation with rich formatting.
```python
evaluate_expression("sqrt(32)")
# Output: "sqrt(32) = 4 × √(2) ≈ 5.656854249"

evaluate_expression("5 ft to m") 
# Output: "5 feet = 1.524 m"

evaluate_expression("solve x^2 = 9")
# Output: "x² = 9 = (x = 3 or x = -3)"
```

### `evaluate_terse(expression, timeout=30)`
Minimal output for clean numerical results.
```python
evaluate_terse("sqrt(32)")
# Output: "5.656854249"

evaluate_terse("pi")
# Output: "3.141592654"
```

### `evaluate_with_options(expression, precision=None, approximation=None, base=None, angle_unit=None, timeout=30)`
Advanced evaluation with precision, approximation mode, and formatting control.
```python
evaluate_with_options("pi", precision=15)
# Output: "π ≈ 3.14159265358979"

evaluate_with_options("sqrt(2)", approximation="exact")
# Output: "sqrt(2) = √(2)"

evaluate_with_options("255", base=16)
# Output: "255 = 0xFF"
```

## Specialized Calculation Tools

### `convert_units(value, target_unit, timeout=30)`
Convert between any supported units with automatic unit recognition.
```python
convert_units("100 km/h", "mph")
# Output: "100 km/h ≈ 62.137119 mph"

convert_units("25 °C", "°F")
# Output: "25 °C = 77 °F"

convert_units("1 atm", "Pa")
# Output: "1 atm = 101325 Pa"
```

### `convert_base(number, target_base, source_base=None, timeout=30)`
Number base conversions (bases 2-36) with automatic format detection.
```python
convert_base("255", 16)
# Output: "255 = 0xFF"

convert_base("0xFF", 10)
# Output: "0xFF = 255"

convert_base("1010", 10, 2)
# Output: "1010₂ = 10"
```

### `symbolic_calculation(expression, timeout=30)`
Algebraic manipulation, factoring, expanding, and equation solving.
```python
symbolic_calculation("factor x^2-4")
# Output: "x² - 4 = (x - 2)(x + 2)"

symbolic_calculation("expand (x+1)^2")
# Output: "(x + 1)² = x² + 2x + 1"

symbolic_calculation("x^2 + 5x + 6 = 0")
# Output: "x = -2 or x = -3"
```

### `calculus_operation(expression, operation, variable="x", timeout=30)`
Calculus operations: differentiation and integration.
```python
calculus_operation("x^3", "diff")
# Output: "diff(x³) = 3x²"

calculus_operation("cos(x)", "integrate")
# Output: "integrate(cos(x)) = sin(x) + C"
```

### `statistical_calculation(data, operation, timeout=30)`
Statistical analysis of data sets.
```python
statistical_calculation("1; 2; 3; 4; 5", "mean")
# Output: "mean([1 2 3 4 5]) = 3"

statistical_calculation("[1, 2, 3, 4, 5]", "stdev")
# Output: "stdev([1 2 3 4 5]) ≈ 1.581"
```

### `matrix_vector_operation(expression, timeout=30)`
Matrix and vector arithmetic, including determinants, inverses, and products.
```python
matrix_vector_operation("det([1, 2; 3, 4])")
# Output: "det([1 2; 3 4]) = -2"

matrix_vector_operation("cross([1, 2, 3], [4, 5, 6])")
# Output: "cross([1 2 3], [4 5 6]) = [-3 6 -3]"

matrix_vector_operation("||[3, 4, 5]||")
# Output: "magnitude([3 4 5]) ≈ 7.071"
```

### `programming_mode_calculation(expression, base=16, timeout=30)`
Programming calculations with bitwise operations and base conversions.
```python
programming_mode_calculation("0xFF & 0x0F", 16)
# Output: "0xFF & 0xF = 0xF"

programming_mode_calculation("52 << 2", 16)
# Output: "shift(0x52, 0x2) = 0x148"
```

## Discovery and Utility Tools

### `list_functions(search_term=None, timeout=30)`
Browse available mathematical functions with optional filtering.
```python
list_functions("sin")
# Lists all trigonometric functions containing "sin"
```

### `list_units(search_term=None, timeout=30)`
Browse available units of measurement with optional filtering.
```python
list_units("meter")
# Lists all units containing "meter"
```

### `list_variables(search_term=None, timeout=30)`
Browse available variables and constants with optional filtering.
```python
list_variables("speed")
# Lists speed-related constants like speed of light
```

### `list_prefixes(search_term=None, timeout=30)`
Browse available unit prefixes (kilo, mega, micro, etc.).

### `update_exchange_rates(timeout=60)`
Update currency exchange rates for accurate conversions.

## Expression Syntax

### Basic Operations
```
2 + 3 * 4          # Basic arithmetic
2^3                # Exponentiation  
sqrt(16)           # Square root
sin(pi/2)          # Trigonometric functions
log(100)           # Logarithms
```

### Units
```
5 ft + 2 m         # Mixed unit arithmetic
100 km/h to mph    # Unit conversion
5 kg * 9.8 m/s^2   # Dimensional analysis
```

### Symbolic Math
```
(x + y)^2          # Symbolic expressions
solve(x^2 = 9)     # Equation solving
factor(x^2 - 4)    # Factorization
diff(x^3)          # Differentiation
```

### Matrices and Vectors
```
[1, 2; 3, 4]       # 2x2 matrix
[1, 2, 3]          # Vector
det([1,2;3,4])     # Determinant
[1,2] × [3,4]      # Vector operations
```

### Number Bases
```
0xFF               # Hexadecimal
0b1010             # Binary
52 to hex          # Base conversion
```

### Statistical Data
```
mean(1; 2; 3; 4; 5)        # Semicolon-separated
stdev([1, 2, 3, 4, 5])     # Vector format
```

## Error Handling

The server includes comprehensive error handling:
- **Timeout Protection**: Calculations timeout after 30 seconds
- **Dependency Checking**: Verifies libqalculate installation
- **Input Validation**: Validates parameters and expressions
- **Graceful Degradation**: Provides helpful error messages

## Advanced Usage

### Precision Control
Use `evaluate_with_options` to control calculation precision and formatting:
```python
# High precision calculations
evaluate_with_options("pi", precision=20)

# Exact symbolic results
evaluate_with_options("sqrt(2)", approximation="exact")

# Base conversions
evaluate_with_options("255", base=16)

# Angle unit control
evaluate_with_options("sin(90)", angle_unit="degrees")
```

### Approximation Modes
- `exact`: Force exact symbolic results (e.g., √2, π/4)
- `try_exact`: Prefer exact when possible, fall back to decimal
- `approximate`: Force decimal approximation

### Number Base Support
Support for any base from 2 to 36 with automatic format detection:
```python
convert_base("255", 16)        # Decimal to hex: "0xFF"
convert_base("0xFF", 10)       # Hex to decimal: "255"
convert_base("1010", 10, 2)    # Binary to decimal: "10"
```

### Programming Mode Features
- Bitwise operations: `&`, `|`, `^`, `~`, `<<`, `>>`
- Multiple base display formats
- Boolean logic operations
- Hexadecimal, binary, and octal literals

### Error Handling and Timeouts
All tools include comprehensive error handling:
- **Timeout Protection**: 30-second default timeout for calculations
- **Dependency Verification**: Automatic libqalculate availability check
- **Input Validation**: Parameter validation with helpful error messages
- **Graceful Degradation**: Meaningful error messages for invalid expressions

## Physical Constants and Variables

Access extensive libraries of:
- **Physical Constants**: `c` (speed of light), `h` (Planck constant), `k_e` (Coulomb constant)
- **Mathematical Constants**: `pi`, `e`, `golden_ratio`
- **Chemical Elements**: `atom(H; weight)` for atomic weights

## Examples

### Scientific Calculations
```
# Kinetic energy calculation
0.5 * 2 kg * (10 m/s)^2 to J

# Gravitational force
G * (mass_earth * mass_moon) / (384400 km)^2

# Wave frequency
c / (550 nm) to Hz
```

### Engineering Applications
```
# Electrical power
12 V * 2 A to W

# Mechanical advantage
100 lbf * 5 ft to Nm

# Fluid dynamics
0.5 * 1.225 kg/m^3 * (25 m/s)^2 * 2 m^2 to N
```

### Financial Calculations
```
# Compound interest (if exchange rates available)
1000 USD * (1.05)^10

# Currency conversion
500 EUR to USD
```

## Configuration

The server automatically loads libqalculate's default configuration, including:
- Standard mathematical functions
- SI and imperial units
- Physical constants
- Currency exchange rates (when available)

## Testing and Verification

Verify that libqalculate is installed and accessible:
```bash
qalc "2+2"
```

You should see output like `2 + 2 = 4`.

## Troubleshooting

### Common Issues

1. **"qalc command not found"**
   - Install libqalculate: `brew install libqalculate` (macOS) or `apt-get install qalc` (Ubuntu)
   - Ensure qalc is in your system PATH
   - Test with: `qalc "2+2"`

2. **Timeout errors**
   - Complex calculations timeout after 30 seconds (configurable)
   - Break complex expressions into simpler parts
   - Use symbolic mode for algebraic expressions

3. **Unit conversion errors**
   - Verify unit names: `list_units("search_term")`
   - Check unit spelling and abbreviations
   - Use proper unit syntax: `5 ft` not `5ft`

4. **Expression parsing errors**
   - Use parentheses for operator precedence
   - Check function names: `list_functions("function_name")`
   - Use proper mathematical syntax

5. **Base conversion issues**
   - Ensure base is between 2-36
   - Use proper prefixes: `0x` for hex, `0b` for binary
   - Check source base specification for non-decimal inputs

### Performance Notes
- Simple calculations: < 100ms
- Unit conversions: < 200ms
- Symbolic operations: 1-5 seconds
- Complex integrations: 5-30 seconds
- Matrix operations: Depends on size and complexity

## MCP Integration

This server is designed for seamless integration with MCP-compatible applications. Replace `/path/to/qalc-mcp` with the absolute path to your cloned repository.

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "qalc": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/qalc-mcp", "mcp", "run", "qalc.py"]
    }
  }
}
```

### Cursor

Add to your Cursor MCP settings (`~/.cursor/mcp.json` or via **Cursor Settings → MCP**):

```json
{
  "mcpServers": {
    "qalc": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/qalc-mcp", "mcp", "run", "qalc.py"]
    }
  }
}
```

### VS Code (Cline / Continue)

Add the following to your Cline or Continue MCP server configuration:

```json
{
  "mcpServers": {
    "qalc": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/qalc-mcp", "mcp", "run", "qalc.py"]
    }
  }
}
```

### Windsurf

Edit `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "qalc": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/qalc-mcp", "mcp", "run", "qalc.py"]
    }
  }
}
```

## Architecture

The server provides a clean abstraction layer over libqalculate:
- **Input Validation**: All parameters are validated before processing
- **Error Handling**: Comprehensive error catching and user-friendly messages
- **Timeout Management**: Prevents infinite calculations
- **Output Formatting**: Consistent, readable results across all tools

## Contributing

Contributions are welcome! Areas for improvement:
- Additional statistical functions
- Enhanced matrix operations
- Custom unit definitions
- Plotting capabilities (if gnuplot available)

For calculation issues, refer to [libqalculate documentation](https://qalculate.github.io/manual/index.html).

## License

This MCP server implementation is provided under the MIT License. Libqalculate itself is licensed under the GPL.

---

**Ready to get started?** Install libqalculate and uv, then add qalc-mcp to your favorite LLM tool!