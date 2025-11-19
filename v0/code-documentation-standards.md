# Documentation Processing Instructions

## 1. Language Detection and Handling

1. When processing code content:
   - First check for explicit language markers in the content
   - Look for common language patterns and keywords
   - If no language is detected, default to plaintext
   - Apply the appropriate syntax rules for the detected language

2. For syntax highlighting:
   - Identify and mark all language-specific keywords
   - Apply standard color schemes for the language
   - Handle special characters according to language rules
   - Process any nested language segments separately

## 2. Code Block Rules

1. When to use full code blocks:
   - If the code spans multiple lines
   - When showing complete functions or classes
   - For entire file contents
   - When displaying complex code structures

2. When to use inline code:
   - For single commands
   - When referencing variable names
   - For brief code references
   - In command-line instructions

## 3. Attribute Requirements

1. For full code blocks:
   - Always include type="code"
   - Add project name when referencing specific projects
   - Include file name when showing file contents
   - Use focus attribute to highlight important lines
   - Add line numbers for longer code segments

2. For inline code:
   - Use single backticks only
   - Do not add any attributes
   - Keep content brief and focused

## 4. Documentation Structure

1. Organize content in this order:
   - Dependencies and imports first
   - Setup instructions second
   - Main implementation third
   - Usage examples fourth
   - Additional notes last

2. Format requirements:
   - Use consistent indentation throughout
   - Add blank lines between sections
   - Group related code examples together
   - Maintain clear section separation

## 5. Code Quality Guidelines

1. For all code examples:
   - Add descriptive comments explaining complex logic
   - Use clear, meaningful variable names
   - Maintain consistent indentation
   - Include appropriate spacing
   - Break long lines logically

2. For readability:
   - Separate logical sections with blank lines
   - Include relevant context before code
   - Use consistent naming patterns
   - Add clarifying comments where needed

## 6. Validation Steps

1. Before processing:
   - Check if the language is supported
   - Verify all required attributes are present
   - Confirm correct block type selection
   - Ensure consistent formatting

2. After processing:
   - Verify syntax highlighting is applied
   - Check all attributes are processed correctly
   - Confirm formatting is maintained
   - Validate overall document structure
