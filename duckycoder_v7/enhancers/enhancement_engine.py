"""
DuckyCoder v6 Enhancement Engine
Implements AI-driven enhancements, fixes, and optimizations with confidence scoring.
"""

import asyncio
import logging
import re
import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import ast
import io
import tokenize

# Enhancement-specific imports
try:
    import black
    HAS_BLACK = True
except ImportError:
    HAS_BLACK = False

try:
    import autopep8
    HAS_AUTOPEP8 = True
except ImportError:
    HAS_AUTOPEP8 = False

try:
    import isort
    HAS_ISORT = True
except ImportError:
    HAS_ISORT = False


@dataclass
class Enhancement:
    """Represents a code enhancement."""
    type: str  # fix, optimization, refactor, feature
    category: str  # syntax, logic, performance, security, style
    description: str
    original_code: Optional[str]
    enhanced_code: str
    line_number: Optional[int]
    confidence: float  # 0.0 to 1.0
    impact: str  # low, medium, high
    justification: str
    trade_offs: List[str]
    risk_level: str  # low, medium, high


@dataclass
class EnhancementResult:
    """Result of enhancement process."""
    enhancements: List[Enhancement]
    enhanced_content: str
    metrics: Dict[str, Any]
    confidence: float
    enhancement_time: float
    metadata: Dict[str, Any]


@dataclass
class FixResult:
    """Result of fix application."""
    fixes_applied: List[Enhancement]
    fixed_content: str
    fixes_failed: List[Dict[str, Any]]
    fix_confidence: float
    metadata: Dict[str, Any]


class EnhancementEngine:
    """AI-driven enhancement engine with multi-tiered improvements."""

    # Enhancement categories and priorities
    ENHANCEMENT_CATEGORIES = {
        'critical_fixes': {
            'priority': 1,
            'auto_apply': True,
            'categories': ['syntax_error', 'security_vulnerability', 'critical_bug']
        },
        'important_fixes': {
            'priority': 2,
            'auto_apply': True,
            'categories': ['logic_error', 'performance_issue', 'compatibility']
        },
        'optimizations': {
            'priority': 3,
            'auto_apply': False,
            'categories': ['performance', 'memory', 'algorithm', 'style']
        },
        'enhancements': {
            'priority': 4,
            'auto_apply': False,
            'categories': ['feature', 'readability', 'maintainability', 'documentation']
        },
        'innovations': {
            'priority': 5,
            'auto_apply': False,
            'categories': ['modernization', 'pattern_improvement', 'architecture']
        }
    }

    # Language-specific enhancement patterns
    ENHANCEMENT_PATTERNS = {
        'python': {
            'syntax_fixes': [
                {
                    'pattern': r'print\s+([^(].*)',
                    'replacement': r'print(\1)',
                    'description': 'Convert print statement to function call',
                    'confidence': 0.95
                },
                {
                    'pattern': r'(\w+)\s*=\s*(\w+)\s*\+\s*(\w+)',
                    'replacement': r'\1 = \2 + \3',
                    'description': 'Add proper spacing around operators',
                    'confidence': 0.9
                }
            ],
            'performance_optimizations': [
                {
                    'pattern': r'for\s+(\w+)\s+in\s+range\(len\((\w+)\)\):',
                    'replacement': r'for \1, item in enumerate(\2):',
                    'description': 'Use enumerate instead of range(len())',
                    'confidence': 0.85
                },
                {
                    'pattern': r'(\w+)\s*=\s*\[\]\s*\n(\s*)for\s+(\w+)\s+in\s+(\w+):\s*\n\s*\1\.append\(([^)]+)\)',
                    'replacement': r'\1 = [\5 for \3 in \4]',
                    'description': 'Convert loop to list comprehension',
                    'confidence': 0.8
                }
            ],
            'security_fixes': [
                {
                    'pattern': r'eval\s*\(',
                    'replacement': '',
                    'description': 'Remove dangerous eval() usage',
                    'confidence': 0.9,
                    'requires_manual_review': True
                },
                {
                    'pattern': r'exec\s*\(',
                    'replacement': '',
                    'description': 'Remove dangerous exec() usage',
                    'confidence': 0.9,
                    'requires_manual_review': True
                }
            ]
        },
        'javascript': {
            'syntax_fixes': [
                {
                    'pattern': r'var\s+(\w+)',
                    'replacement': r'let \1',
                    'description': 'Replace var with let',
                    'confidence': 0.8
                },
                {
                    'pattern': r'==\s*([^=])',
                    'replacement': r'=== \1',
                    'description': 'Use strict equality',
                    'confidence': 0.85
                }
            ],
            'performance_optimizations': [
                {
                    'pattern': r'for\s*\(\s*var\s+(\w+)\s*=\s*0;\s*\1\s*<\s*(\w+)\.length;\s*\1\+\+\s*\)',
                    'replacement': r'for (let \1 = 0, len = \2.length; \1 < len; \1++)',
                    'description': 'Cache array length in loop',
                    'confidence': 0.75
                }
            ]
        },
        'rust': {
            'performance_optimizations': [
                {
                    'pattern': r'\.clone\(\)',
                    'replacement': '',
                    'description': 'Remove unnecessary clone()',
                    'confidence': 0.7,
                    'requires_manual_review': True
                }
            ]
        }
    }

    # Code improvement templates
    IMPROVEMENT_TEMPLATES = {
        'add_error_handling': {
            'python': '''try:
    {original_code}
except Exception as e:
    logger.error(f"Error: {{e}}")
    raise''',
            'javascript': '''try {
    {original_code}
} catch (error) {
    console.error('Error:', error);
    throw error;
}'''
        },
        'add_logging': {
            'python': '''import logging

logger = logging.getLogger(__name__)

{original_code}''',
            'javascript': '''const logger = console;

{original_code}'''
        },
        'add_documentation': {
            'python': '''"""
{function_description}

Args:
{args_description}

Returns:
{return_description}
"""
{original_code}''',
            'javascript': '''/**
 * {function_description}
 * {params_description}
 * @returns {return_description}
 */
{original_code}'''
        }
    }

    def __init__(self, config: Dict[str, Any]):
        """Initialize the enhancement engine."""
        self.config = config
        self.enhancement_config = config.get('enhancement_config', {})
        self.logger = logging.getLogger(__name__)

        # Enhancement settings
        self.confidence_threshold = self.enhancement_config.get('confidence_threshold', 0.7)
        self.auto_apply_fixes = self.enhancement_config.get('auto_apply_fixes', True)
        self.max_enhancements = self.enhancement_config.get('max_enhancements', 50)

        # Initialize formatters
        self._init_formatters()

    def _init_formatters(self):
        """Initialize code formatters."""
        self.formatters = {}
        
        if HAS_BLACK:
            self.formatters['python'] = self._format_with_black
        elif HAS_AUTOPEP8:
            self.formatters['python'] = self._format_with_autopep8

    async def apply_core_fixes(self, data: Dict[str, Any], 
                             analysis: Dict[str, Any]) -> EnhancementResult:
        """
        Apply core fixes for critical issues.

        Args:
            data: Original processed content
            analysis: Analysis results with identified issues

        Returns:
            EnhancementResult with applied fixes
        """
        start_time = asyncio.get_event_loop().time()

        try:
            content = data.get('content', '')
            language = data.get('metadata', {}).get('language')
            file_path = data.get('metadata', {}).get('file_path', '<string>')

            enhancements = []
            enhanced_content = content

            # Apply critical fixes from analysis
            if 'issues' in analysis:
                critical_fixes = await self._apply_critical_fixes(
                    enhanced_content, analysis['issues'], language
                )
                enhancements.extend(critical_fixes)
                enhanced_content = self._apply_enhancements_to_content(
                    enhanced_content, critical_fixes
                )

            # Apply syntax fixes
            syntax_fixes = await self._apply_syntax_fixes(enhanced_content, language)
            enhancements.extend(syntax_fixes)
            enhanced_content = self._apply_enhancements_to_content(
                enhanced_content, syntax_fixes
            )

            # Apply security fixes
            security_fixes = await self._apply_security_fixes(enhanced_content, language)
            enhancements.extend(security_fixes)
            enhanced_content = self._apply_enhancements_to_content(
                enhanced_content, security_fixes
            )

            # Format code if formatter available
            if language in self.formatters:
                try:
                    formatted_content = await self.formatters[language](enhanced_content)
                    if formatted_content != enhanced_content:
                        enhancements.append(Enhancement(
                            type='fix',
                            category='formatting',
                            description=f'Applied {language} code formatting',
                            original_code=None,
                            enhanced_code=formatted_content,
                            line_number=None,
                            confidence=0.95,
                            impact='low',
                            justification='Consistent code formatting improves readability',
                            trade_offs=[],
                            risk_level='low'
                        ))
                        enhanced_content = formatted_content
                except Exception as e:
                    self.logger.warning(f"Code formatting failed: {e}")

            # Calculate metrics
            metrics = await self._calculate_enhancement_metrics(
                content, enhanced_content, enhancements
            )

            execution_time = asyncio.get_event_loop().time() - start_time

            return EnhancementResult(
                enhancements=enhancements,
                enhanced_content=enhanced_content,
                metrics=metrics,
                confidence=self._calculate_fixes_confidence(enhancements),
                enhancement_time=execution_time,
                metadata={
                    'type': 'core_fixes',
                    'language': language,
                    'file_path': file_path,
                    'fixes_applied': len(enhancements)
                }
            )

        except Exception as e:
            self.logger.error(f"Core fixes application failed: {e}")
            return EnhancementResult(
                enhancements=[],
                enhanced_content=data.get('content', ''),
                metrics={},
                confidence=0.0,
                enhancement_time=0.0,
                metadata={'error': str(e)}
            )

    async def apply_optimizations(self, data: Dict[str, Any], 
                                analysis: Dict[str, Any]) -> EnhancementResult:
        """
        Apply performance and code optimizations.

        Args:
            data: Enhanced content from core fixes
            analysis: Analysis results

        Returns:
            EnhancementResult with applied optimizations
        """
        start_time = asyncio.get_event_loop().time()

        try:
            content = data.get('enhanced', data.get('content', ''))
            language = data.get('metadata', {}).get('language')

            enhancements = []
            enhanced_content = content

            # Apply performance optimizations
            performance_opts = await self._apply_performance_optimizations(
                enhanced_content, language, analysis
            )
            enhancements.extend(performance_opts)
            enhanced_content = self._apply_enhancements_to_content(
                enhanced_content, performance_opts
            )

            # Apply algorithm improvements
            algorithm_improvements = await self._apply_algorithm_improvements(
                enhanced_content, language, analysis
            )
            enhancements.extend(algorithm_improvements)
            enhanced_content = self._apply_enhancements_to_content(
                enhanced_content, algorithm_improvements
            )

            # Apply memory optimizations
            memory_opts = await self._apply_memory_optimizations(
                enhanced_content, language, analysis
            )
            enhancements.extend(memory_opts)
            enhanced_content = self._apply_enhancements_to_content(
                enhanced_content, memory_opts
            )

            # Calculate metrics
            metrics = await self._calculate_enhancement_metrics(
                content, enhanced_content, enhancements
            )

            execution_time = asyncio.get_event_loop().time() - start_time

            return EnhancementResult(
                enhancements=enhancements,
                enhanced_content=enhanced_content,
                metrics=metrics,
                confidence=self._calculate_optimizations_confidence(enhancements),
                enhancement_time=execution_time,
                metadata={
                    'type': 'optimizations',
                    'language': language,
                    'optimizations_applied': len(enhancements)
                }
            )

        except Exception as e:
            self.logger.error(f"Optimizations application failed: {e}")
            return EnhancementResult(
                enhancements=[],
                enhanced_content=data.get('content', ''),
                metrics={},
                confidence=0.0,
                enhancement_time=0.0,
                metadata={'error': str(e)}
            )

    async def apply_enhancements(self, data: Dict[str, Any], 
                               analysis: Dict[str, Any]) -> EnhancementResult:
        """
        Apply high-level enhancements and innovations.

        Args:
            data: Optimized content from previous steps
            analysis: Analysis results

        Returns:
            EnhancementResult with applied enhancements
        """
        start_time = asyncio.get_event_loop().time()

        try:
            content = data.get('enhanced', data.get('content', ''))
            language = data.get('metadata', {}).get('language')

            enhancements = []
            enhanced_content = content

            # Add documentation improvements
            doc_enhancements = await self._add_documentation_improvements(
                enhanced_content, language, analysis
            )
            enhancements.extend(doc_enhancements)
            enhanced_content = self._apply_enhancements_to_content(
                enhanced_content, doc_enhancements
            )

            # Add error handling improvements
            error_handling = await self._add_error_handling(
                enhanced_content, language, analysis
            )
            enhancements.extend(error_handling)
            enhanced_content = self._apply_enhancements_to_content(
                enhanced_content, error_handling
            )

            # Add logging improvements
            logging_improvements = await self._add_logging_improvements(
                enhanced_content, language
            )
            enhancements.extend(logging_improvements)
            enhanced_content = self._apply_enhancements_to_content(
                enhanced_content, logging_improvements
            )

            # Apply modernization improvements
            modernizations = await self._apply_modernization(
                enhanced_content, language
            )
            enhancements.extend(modernizations)
            enhanced_content = self._apply_enhancements_to_content(
                enhanced_content, modernizations
            )

            # Calculate metrics
            metrics = await self._calculate_enhancement_metrics(
                content, enhanced_content, enhancements
            )

            execution_time = asyncio.get_event_loop().time() - start_time

            return EnhancementResult(
                enhancements=enhancements,
                enhanced_content=enhanced_content,
                metrics=metrics,
                confidence=self._calculate_enhancements_confidence(enhancements),
                enhancement_time=execution_time,
                metadata={
                    'type': 'enhancements',
                    'language': language,
                    'enhancements_applied': len(enhancements)
                }
            )

        except Exception as e:
            self.logger.error(f"Enhancements application failed: {e}")
            return EnhancementResult(
                enhancements=[],
                enhanced_content=data.get('content', ''),
                metrics={},
                confidence=0.0,
                enhancement_time=0.0,
                metadata={'error': str(e)}
            )

    async def _apply_critical_fixes(self, content: str, issues: List[Any], 
                                  language: Optional[str]) -> List[Enhancement]:
        """Apply fixes for critical issues identified in analysis."""
        enhancements = []

        for issue in issues:
            if hasattr(issue, 'severity') and issue.severity in ['critical', 'high']:
                fix = await self._generate_fix_for_issue(issue, content, language)
                if fix:
                    enhancements.append(fix)

        return enhancements

    async def _apply_syntax_fixes(self, content: str, 
                                language: Optional[str]) -> List[Enhancement]:
        """Apply syntax fixes based on language patterns."""
        enhancements = []

        if language in self.ENHANCEMENT_PATTERNS:
            patterns = self.ENHANCEMENT_PATTERNS[language].get('syntax_fixes', [])
            
            for pattern_data in patterns:
                pattern = pattern_data['pattern']
                replacement = pattern_data['replacement']
                description = pattern_data['description']
                confidence = pattern_data['confidence']

                matches = list(re.finditer(pattern, content))
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    original_code = match.group(0)
                    enhanced_code = re.sub(pattern, replacement, original_code)

                    if enhanced_code != original_code:
                        enhancements.append(Enhancement(
                            type='fix',
                            category='syntax',
                            description=description,
                            original_code=original_code,
                            enhanced_code=enhanced_code,
                            line_number=line_num,
                            confidence=confidence,
                            impact='low',
                            justification=f'Syntax improvement: {description}',
                            trade_offs=[],
                            risk_level='low'
                        ))

        return enhancements

    async def _apply_security_fixes(self, content: str, 
                                  language: Optional[str]) -> List[Enhancement]:
        """Apply security fixes based on patterns."""
        enhancements = []

        if language in self.ENHANCEMENT_PATTERNS:
            patterns = self.ENHANCEMENT_PATTERNS[language].get('security_fixes', [])
            
            for pattern_data in patterns:
                pattern = pattern_data['pattern']
                description = pattern_data['description']
                confidence = pattern_data['confidence']
                requires_review = pattern_data.get('requires_manual_review', False)

                matches = list(re.finditer(pattern, content))
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    original_code = match.group(0)

                    enhancement = Enhancement(
                        type='fix',
                        category='security',
                        description=description,
                        original_code=original_code,
                        enhanced_code='# SECURITY ISSUE REMOVED - Manual review required',
                        line_number=line_num,
                        confidence=confidence,
                        impact='high',
                        justification=f'Security fix: {description}',
                        trade_offs=['Requires manual code replacement'],
                        risk_level='medium' if requires_review else 'low'
                    )

                    enhancements.append(enhancement)

        return enhancements

    async def _apply_performance_optimizations(self, content: str, language: Optional[str],
                                             analysis: Dict[str, Any]) -> List[Enhancement]:
        """Apply performance optimizations."""
        enhancements = []

        if language in self.ENHANCEMENT_PATTERNS:
            patterns = self.ENHANCEMENT_PATTERNS[language].get('performance_optimizations', [])
            
            for pattern_data in patterns:
                pattern = pattern_data['pattern']
                replacement = pattern_data['replacement']
                description = pattern_data['description']
                confidence = pattern_data['confidence']

                matches = list(re.finditer(pattern, content, re.MULTILINE | re.DOTALL))
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    original_code = match.group(0)
                    enhanced_code = re.sub(pattern, replacement, original_code, flags=re.MULTILINE | re.DOTALL)

                    if enhanced_code != original_code and confidence >= self.confidence_threshold:
                        enhancements.append(Enhancement(
                            type='optimization',
                            category='performance',
                            description=description,
                            original_code=original_code,
                            enhanced_code=enhanced_code,
                            line_number=line_num,
                            confidence=confidence,
                            impact='medium',
                            justification=f'Performance optimization: {description}',
                            trade_offs=['May affect code readability'],
                            risk_level='low'
                        ))

        return enhancements

    async def _apply_algorithm_improvements(self, content: str, language: Optional[str],
                                          analysis: Dict[str, Any]) -> List[Enhancement]:
        """Apply algorithm improvements."""
        enhancements = []

        # Detect nested loops and suggest improvements
        if language == 'python':
            nested_loop_pattern = r'for\s+\w+\s+in\s+\w+:\s*\n\s+for\s+\w+\s+in\s+\w+:'
            matches = list(re.finditer(nested_loop_pattern, content, re.MULTILINE))
            
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                original_code = match.group(0)

                enhancements.append(Enhancement(
                    type='optimization',
                    category='algorithm',
                    description='Consider optimizing nested loops',
                    original_code=original_code,
                    enhanced_code=f'# TODO: Optimize nested loops for better O(n) complexity\n{original_code}',
                    line_number=line_num,
                    confidence=0.7,
                    impact='high',
                    justification='Nested loops can often be optimized for better time complexity',
                    trade_offs=['Requires algorithm redesign'],
                    risk_level='medium'
                ))

        return enhancements

    async def _apply_memory_optimizations(self, content: str, language: Optional[str],
                                        analysis: Dict[str, Any]) -> List[Enhancement]:
        """Apply memory optimizations."""
        enhancements = []

        if language == 'python':
            # Detect string concatenation in loops
            string_concat_pattern = r'(\w+)\s*\+=\s*["\'].*["\']'
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                if 'for ' in line and i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if re.search(string_concat_pattern, next_line):
                        enhancements.append(Enhancement(
                            type='optimization',
                            category='memory',
                            description='Use join() instead of string concatenation in loop',
                            original_code=f'{line}\n{next_line}',
                            enhanced_code=f'# TODO: Replace with list comprehension and join()\n{line}\n{next_line}',
                            line_number=i + 1,
                            confidence=0.8,
                            impact='medium',
                            justification='String concatenation in loops is memory inefficient',
                            trade_offs=['Code restructuring required'],
                            risk_level='low'
                        ))

        return enhancements

    async def _add_documentation_improvements(self, content: str, language: Optional[str],
                                            analysis: Dict[str, Any]) -> List[Enhancement]:
        """Add documentation improvements."""
        enhancements = []

        if language == 'python':
            # Find functions without docstrings
            function_pattern = r'def\s+(\w+)\s*\([^)]*\):'
            functions = list(re.finditer(function_pattern, content))
            
            for func_match in functions:
                func_start = func_match.end()
                func_name = func_match.group(1)
                line_num = content[:func_match.start()].count('\n') + 1
                
                # Check if docstring exists
                next_lines = content[func_start:func_start+200]
                if '"""' not in next_lines and "'''" not in next_lines:
                    docstring = f'"""TODO: Add documentation for {func_name} function."""'
                    
                    enhancements.append(Enhancement(
                        type='enhancement',
                        category='documentation',
                        description=f'Add docstring to function {func_name}',
                        original_code=func_match.group(0),
                        enhanced_code=f'{func_match.group(0)}\n    {docstring}',
                        line_number=line_num,
                        confidence=0.9,
                        impact='low',
                        justification='Documentation improves code maintainability',
                        trade_offs=[],
                        risk_level='low'
                    ))

        return enhancements

    async def _add_error_handling(self, content: str, language: Optional[str],
                                analysis: Dict[str, Any]) -> List[Enhancement]:
        """Add error handling improvements."""
        enhancements = []

        if language == 'python':
            # Find risky operations without try-catch
            risky_patterns = [
                r'open\s*\([^)]+\)',
                r'json\.loads\s*\([^)]+\)',
                r'int\s*\([^)]+\)',
                r'float\s*\([^)]+\)'
            ]
            
            for pattern in risky_patterns:
                matches = list(re.finditer(pattern, content))
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    
                    # Check if already in try block
                    lines_before = content[:match.start()].split('\n')
                    recent_lines = lines_before[-10:] if len(lines_before) >= 10 else lines_before
                    
                    if not any('try:' in line for line in recent_lines):
                        original_code = match.group(0)
                        
                        enhancements.append(Enhancement(
                            type='enhancement',
                            category='error_handling',
                            description=f'Add error handling for {original_code}',
                            original_code=original_code,
                            enhanced_code=f'# TODO: Add try-except block for {original_code}',
                            line_number=line_num,
                            confidence=0.75,
                            impact='medium',
                            justification='Error handling improves code robustness',
                            trade_offs=['Increases code complexity'],
                            risk_level='low'
                        ))

        return enhancements

    async def _add_logging_improvements(self, content: str, 
                                      language: Optional[str]) -> List[Enhancement]:
        """Add logging improvements."""
        enhancements = []

        if language == 'python':
            # Check if logging is imported
            if 'import logging' not in content and 'print(' in content:
                print_count = content.count('print(')
                if print_count > 2:  # Multiple print statements
                    enhancements.append(Enhancement(
                        type='enhancement',
                        category='logging',
                        description='Replace print statements with logging',
                        original_code='print statements',
                        enhanced_code='# TODO: Import logging and replace print statements',
                        line_number=1,
                        confidence=0.8,
                        impact='medium',
                        justification='Logging provides better control and formatting',
                        trade_offs=['Requires logging configuration'],
                        risk_level='low'
                    ))

        return enhancements

    async def _apply_modernization(self, content: str, 
                                 language: Optional[str]) -> List[Enhancement]:
        """Apply modernization improvements."""
        enhancements = []

        if language == 'python':
            # Suggest f-strings for string formatting
            old_format_patterns = [
                r'["\'][^"\']*%[sd][^"\']*["\']',
                r'\.format\s*\(',
            ]
            
            for pattern in old_format_patterns:
                matches = list(re.finditer(pattern, content))
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    original_code = match.group(0)
                    
                    enhancements.append(Enhancement(
                        type='enhancement',
                        category='modernization',
                        description='Consider using f-strings for string formatting',
                        original_code=original_code,
                        enhanced_code=f'# TODO: Convert to f-string: {original_code}',
                        line_number=line_num,
                        confidence=0.7,
                        impact='low',
                        justification='f-strings are more readable and performant',
                        trade_offs=['Requires Python 3.6+'],
                        risk_level='low'
                    ))

        return enhancements

    async def _generate_fix_for_issue(self, issue: Any, content: str, 
                                    language: Optional[str]) -> Optional[Enhancement]:
        """Generate a fix for a specific analysis issue."""
        if not hasattr(issue, 'type') or not hasattr(issue, 'message'):
            return None

        issue_type = issue.type
        message = issue.message
        line_num = getattr(issue, 'line_number', None)
        suggestion = getattr(issue, 'suggestion', '')

        # Generate fix based on issue type
        if issue_type == 'syntax' and 'trailing whitespace' in message.lower():
            return Enhancement(
                type='fix',
                category='syntax',
                description='Remove trailing whitespace',
                original_code=None,
                enhanced_code='# Trailing whitespace removed',
                line_number=line_num,
                confidence=0.95,
                impact='low',
                justification='Clean code formatting',
                trade_offs=[],
                risk_level='low'
            )

        elif issue_type == 'security':
            return Enhancement(
                type='fix',
                category='security',
                description=f'Security fix: {message}',
                original_code=None,
                enhanced_code=f'# SECURITY ISSUE ADDRESSED: {suggestion}',
                line_number=line_num,
                confidence=0.9,
                impact='high',
                justification=f'Security vulnerability remediation: {message}',
                trade_offs=['May require code refactoring'],
                risk_level='medium'
            )

        return None

    def _apply_enhancements_to_content(self, content: str, 
                                     enhancements: List[Enhancement]) -> str:
        """Apply enhancements to content."""
        enhanced_content = content
        
        # Sort enhancements by line number (reverse order to maintain line numbers)
        line_enhancements = [e for e in enhancements if e.line_number is not None]
        line_enhancements.sort(key=lambda x: x.line_number, reverse=True)
        
        lines = enhanced_content.split('\n')
        
        for enhancement in line_enhancements:
            if enhancement.type == 'fix' and enhancement.enhanced_code:
                line_idx = enhancement.line_number - 1
                if 0 <= line_idx < len(lines):
                    if enhancement.original_code:
                        # Replace specific content
                        lines[line_idx] = lines[line_idx].replace(
                            enhancement.original_code, 
                            enhancement.enhanced_code
                        )
                    else:
                        # Add comment or note
                        lines.insert(line_idx, f'# {enhancement.description}')
        
        return '\n'.join(lines)

    async def _format_with_black(self, content: str) -> str:
        """Format Python code with Black."""
        try:
            return black.format_str(content, mode=black.FileMode())
        except Exception as e:
            self.logger.warning(f"Black formatting failed: {e}")
            return content

    async def _format_with_autopep8(self, content: str) -> str:
        """Format Python code with autopep8."""
        try:
            return autopep8.fix_code(content)
        except Exception as e:
            self.logger.warning(f"autopep8 formatting failed: {e}")
            return content

    async def _calculate_enhancement_metrics(self, original: str, enhanced: str,
                                           enhancements: List[Enhancement]) -> Dict[str, Any]:
        """Calculate metrics for enhancement results."""
        original_lines = len(original.split('\n'))
        enhanced_lines = len(enhanced.split('\n'))
        
        metrics = {
            'original_lines': original_lines,
            'enhanced_lines': enhanced_lines,
            'lines_added': enhanced_lines - original_lines,
            'total_enhancements': len(enhancements),
            'enhancements_by_type': {},
            'enhancements_by_category': {},
            'average_confidence': 0.0,
            'high_confidence_enhancements': 0,
            'improvement_score': 0.0
        }

        # Count enhancements by type and category
        for enhancement in enhancements:
            # By type
            if enhancement.type in metrics['enhancements_by_type']:
                metrics['enhancements_by_type'][enhancement.type] += 1
            else:
                metrics['enhancements_by_type'][enhancement.type] = 1

            # By category
            if enhancement.category in metrics['enhancements_by_category']:
                metrics['enhancements_by_category'][enhancement.category] += 1
            else:
                metrics['enhancements_by_category'][enhancement.category] = 1

        # Calculate confidence metrics
        if enhancements:
            confidences = [e.confidence for e in enhancements]
            metrics['average_confidence'] = sum(confidences) / len(confidences)
            metrics['high_confidence_enhancements'] = len([c for c in confidences if c >= 0.8])

            # Calculate improvement score
            impact_weights = {'low': 1, 'medium': 2, 'high': 3}
            total_impact = sum(impact_weights.get(e.impact, 1) * e.confidence for e in enhancements)
            metrics['improvement_score'] = min(10.0, total_impact / len(enhancements))

        return metrics

    def _calculate_fixes_confidence(self, enhancements: List[Enhancement]) -> float:
        """Calculate confidence score for fixes."""
        if not enhancements:
            return 1.0

        fix_enhancements = [e for e in enhancements if e.type == 'fix']
        if not fix_enhancements:
            return 0.8

        confidences = [e.confidence for e in fix_enhancements]
        return sum(confidences) / len(confidences)

    def _calculate_optimizations_confidence(self, enhancements: List[Enhancement]) -> float:
        """Calculate confidence score for optimizations."""
        if not enhancements:
            return 0.7

        optimization_enhancements = [e for e in enhancements if e.type == 'optimization']
        if not optimization_enhancements:
            return 0.6

        confidences = [e.confidence for e in optimization_enhancements]
        avg_confidence = sum(confidences) / len(confidences)
        
        # Reduce confidence for optimizations as they're more subjective
        return avg_confidence * 0.9

    def _calculate_enhancements_confidence(self, enhancements: List[Enhancement]) -> float:
        """Calculate confidence score for enhancements."""
        if not enhancements:
            return 0.6

        enhancement_enhancements = [e for e in enhancements if e.type == 'enhancement']
        if not enhancement_enhancements:
            return 0.5

        confidences = [e.confidence for e in enhancement_enhancements]
        avg_confidence = sum(confidences) / len(confidences)
        
        # Further reduce confidence for enhancements as they're most subjective
        return avg_confidence * 0.8
