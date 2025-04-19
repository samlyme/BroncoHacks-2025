# Basic Data Types and Structures Study Guide

## Introduction

Data types and structures are fundamental building blocks in programming. They help us store, organize, and manipulate data in our applications. This guide covers the basics of working with primitive data types like integers and composite data structures like arrays, which are essential for any programming task.

## Primitive Data Types

### Integers (int)

Integers are whole numbers without any decimal points.

#### How to Declare an Integer

```java
// In Java
int myNumber = 42;

// In Python
my_number = 42  # Python automatically determines the type
int_number = int(42)  # Explicitly declaring as integer

// In JavaScript
let myNumber = 42;
const anotherNumber = 100;

// In C/C++
int myNumber = 42;
```

#### Integer Operations

```java
int a = 5;
int b = 7;

int sum = a + b;        // 12
int difference = b - a;  // 2
int product = a * b;     // 35
int quotient = b / a;    // 1 (integer division truncates in many languages)
int remainder = b % a;   // 2 (modulo operation)

a++;  // Increment by 1: a is now 6
b--;  // Decrement by 1: b is now 6
```

#### Common Integer Types (Language-Specific)

Different programming languages may have different integer types with varying sizes:

```c
// In C/C++
short smallNumber = 100;       // Typically 2 bytes
int regularNumber = 1000;      // Typically 4 bytes
long bigNumber = 1000000L;     // Typically 4-8 bytes
long long veryBigNumber = 1000000000LL;  // Typically 8 bytes
```

```java
// In Java
byte tinyNumber = 100;         // 1 byte (-128 to 127)
short smallNumber = 1000;      // 2 bytes (-32,768 to 32,767)
int regularNumber = 100000;    // 4 bytes (-2^31 to 2^31-1)
long bigNumber = 1000000000L;  // 8 bytes (-2^63 to 2^63-1)
```

## Composite Data Structures

### Arrays

Arrays are collections of items stored at contiguous memory locations.

#### How to Declare an Array

```java
// In Java
int[] numbers = new int[5];            // Creates an array of 5 integers
int[] initialized = {1, 2, 3, 4, 5};   // Creates and initializes an array

// In Python
numbers = [0] * 5                      # Creates a list with 5 zeros
initialized = [1, 2, 3, 4, 5]          # Creates and initializes a list

// In JavaScript
let numbers = new Array(5);            // Creates an array of 5 undefined elements
let initialized = [1, 2, 3, 4, 5];     // Creates and initializes an array

// In C/C++
int numbers[5];                        // Creates an array of 5 integers
int initialized[] = {1, 2, 3, 4, 5};   // Creates and initializes an array
```

#### Accessing Array Elements

Array indices typically start at 0:

```java
int[] arr = {10, 20, 30, 40, 50};

int firstElement = arr[0];    // Gets 10
int thirdElement = arr[2];    // Gets 30

arr[1] = 25;                  // Changes the second element to 25
```

#### Common Array Operations

```java
// Iterating through an array
for (int i = 0; i < arr.length; i++) {
    System.out.println(arr[i]);
}

// In Python
for item in my_list:
    print(item)

// In JavaScript
for (let i = 0; i < arr.length; i++) {
    console.log(arr[i]);
}
// or
arr.forEach(item => console.log(item));
```

#### Multidimensional Arrays

```java
// In Java - 2D array (3 rows, 4 columns)
int[][] matrix = new int[3][4];
int[][] initialized = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};

// Access element at row 1, column 2
int element = initialized[1][2];  // Gets 7
```

```python
# In Python
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]

# Access element at row 1, column 2
element = matrix[1][2]  # Gets 7
```

## Other Common Data Types

### Floating-Point Numbers

```java
// In Java
float smallDecimal = 3.14f;
double bigDecimal = 3.14159265359;

// In Python
my_float = 3.14

// In JavaScript
let myFloat = 3.14;

// In C/C++
float smallDecimal = 3.14f;
double bigDecimal = 3.14159265359;
```

### Booleans

```java
// In Java
boolean isTrue = true;
boolean isFalse = false;

// In Python
is_true = True
is_false = False

// In JavaScript
let isTrue = true;
let isFalse = false;

// In C/C++
bool isTrue = true;
bool isFalse = false;
```

### Characters and Strings

```java
// In Java
char singleCharacter = 'A';
String text = "Hello, World!";

// In Python
text = "Hello, World!"
single_character = 'A'  # In Python, a single character is still a string

// In JavaScript
let singleCharacter = 'A';
let text = "Hello, World!";

// In C/C++
char singleCharacter = 'A';
char text[] = "Hello, World!";  // C-style string
// In C++
std::string text = "Hello, World!";
```

## Common Questions and Tips

### 1. What's the difference between primitive and reference types?

**Primitive types** (like `int`, `float`, `boolean`) store their values directly, while **reference types** (like arrays and objects) store a reference (address) to their values.

### 2. What happens if I try to access an array element out of bounds?

In most languages, this will cause an error:
- Java/C/C++: `ArrayIndexOutOfBoundsException` or segmentation fault
- Python: `IndexError`
- JavaScript: Returns `undefined` without an error

### 3. How do I find the length of an array?

```java
// In Java
int length = myArray.length;

// In Python
length = len(my_list)

// In JavaScript
let length = myArray.length;

// In C/C++
int length = sizeof(myArray) / sizeof(myArray[0]);
```

### 4. How do I convert between data types?

```java
// In Java
int num = 42;
String str = String.valueOf(num);  // Convert int to String
int parsed = Integer.parseInt("42");  // Convert String to int

// In Python
num = 42
string = str(num)  # Convert int to string
parsed = int("42")  # Convert string to int

// In JavaScript
let num = 42;
let str = num.toString();  // Convert number to string
let parsed = parseInt("42", 10);  // Convert string to integer
```

## Best Practices

1. **Choose appropriate data types** for your needs (integer vs. float, array vs. list, etc.)
2. **Initialize variables** before using them to avoid unexpected behavior
3. **Check array bounds** before accessing elements to prevent errors
4. **Use meaningful variable names** that describe what the data represents
5. **Be aware of memory usage**, especially when working with large arrays

## Next Steps

Once you're comfortable with basic data types and arrays, consider learning about:
- Dynamic data structures (Lists, Sets, Maps)
- Object-oriented programming concepts
- Type conversion and casting
- Memory management considerations

Remember, understanding data types and structures is foundational to becoming proficient in any programming language!