#!/usr/bin/env python3
"""
AI Analysis Engine for DuckyCoder v7
Enhanced with advanced AI capabilities for comprehensive code analysis,
security scanning, dependency extraction, and similarity detection.
"""

import asyncio
import logging
import re
import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import ast
import tokenize
import io
from pathlib import Path

# Security and compliance imports
try:
    import bandit
    from bandit.core.manager import BanditManager
    from bandit.core.config import BanditConfig
    HAS_BANDIT = True
except ImportError:
    HAS_BANDIT = False

try:
    import vulture
    HAS_VULTURE = True
except ImportError:
    HAS_VULTURE = False

# Code analysis imports
try:
    import radon.complexity as radon_complexity
    import radon.metrics as radon_metrics
    HAS_RADON = True
except ImportError:
    HAS_RADON = False

try:
    import pylint.lint
    from pylint.reporters.text import TextReporter
    HAS_PYLINT = True
except ImportError:
    HAS_PYLINT = False


@dataclass
class AnalysisIssue:
    """Represents an analysis issue found in code."""
    type: str  # syntax, logic, security, performance
    severity: str  # low, medium, high, critical
    message: str
    line_number: Optional[int]
    column: Optional[int]
    rule_id: Optional[str]
    suggestion: Optional[str]
    confidence: float  # 0.0 to 1.0


@dataclass
class AnalysisResult:
    """Result of code analysis."""
    issues: List[AnalysisIssue]
    metrics: Dict[str, Any]
    confidence: float
    analysis_time: float
    metadata: Dict[str, Any]


@dataclass
class SecurityFinding:
    """Security analysis finding."""
    vulnerability_type: str
    severity: str
    description: str
    file_path: str
    line_number: int
    cwe_id: Optional[str]
    owasp_category: Optional[str]
    remediation: Optional[str]
    confidence: float


@dataclass
class ComplianceViolation:
    """Compliance violation."""
    standard: str  # GDPR, HIPAA, PCI, etc.
    rule: str
    description: str
    severity: str
    location: str
    remediation: str


class AIAnalysisEngine:
    """Enhanced AI-powered analysis engine for DuckyCoder v7."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize AI Analysis Engine with v7 enhancements."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # V7 enhancements
        self.v7_features = {
            'dependency_extraction': True,
            'similarity_detection': True,
            'security_scanning': True,
            'quantum_analysis': config.get('enhanced_features', {}).get('quantum_computing', False),
            'ml_optimization': config.get('enhanced_features', {}).get('ml_optimization', True)
        }
        
        # Initialize AI models and analyzers
        self._initialize_models()
        self.logger.info("✅ AI Analysis Engine v7 initialized with enhanced capabilities")

    def _init_security_scanners(self):
        """Initialize security scanning tools."""
        if HAS_BANDIT:
            try:
                self.bandit_config = BanditConfig()
                self.bandit_manager = BanditManager(self.bandit_config, 'file')
            except Exception as e:
                self.logger.warning(f"Failed to initialize Bandit: {e}")
                self.bandit_manager = None
        else:
            self.bandit_manager = None

    def _init_code_analyzers(self):
        """Initialize code analysis tools."""
        self.analysis_cache = {}

    async def analyze_syntax(self, data: Dict[str, Any]) -> AnalysisResult:
        """
        Perform syntax analysis on code.

        Args:
            data: Processed input data with content and metadata

        Returns:
            AnalysisResult with syntax issues and metrics
        """
        start_time = asyncio.get_event_loop().time()

        try:
            content = data.get('content', '')
            language = data.get('metadata', {}).get('language')
            file_path = data.get('metadata', {}).get('file_path', '<string>')

            issues = []
            metrics = {}

            if language == 'python':
                issues, metrics = await self._analyze_python_syntax(content, file_path)
            elif language in ['javascript', 'typescript']:
                issues, metrics = await self._analyze_js_syntax(content, file_path)
            elif language == 'java':
                issues, metrics = await self._analyze_java_syntax(content, file_path)
            else:
                # Generic syntax analysis
                issues, metrics = await self._analyze_generic_syntax(content, file_path)

            execution_time = asyncio.get_event_loop().time() - start_time

            return AnalysisResult(
                issues=issues,
                metrics=metrics,
                confidence=self._calculate_syntax_confidence(issues, metrics),
                analysis_time=execution_time,
                metadata={
                    'analyzer': 'syntax',
                    'language': language,
                    'file_path': file_path
                }
            )

        except Exception as e:
            self.logger.error(f"Syntax analysis failed: {e}")
            return AnalysisResult(
                issues=[AnalysisIssue(
                    type='syntax',
                    severity='high',
                    message=f"Syntax analysis failed: {e}",
                    line_number=None,
                    column=None,
                    rule_id='SYNTAX_ERROR',
                    suggestion='Check code syntax',
                    confidence=1.0
                )],
                metrics={},
                confidence=0.0,
                analysis_time=0.0,
                metadata={'error': str(e)}
            )

    async def analyze_logic(self, data: Dict[str, Any]) -> AnalysisResult:
        """
        Perform logical analysis on code.

        Args:
            data: Processed input data with content and metadata

        Returns:
            AnalysisResult with logical issues and patterns
        """
        start_time = asyncio.get_event_loop().time()

        try:
            content = data.get('content', '')
            language = data.get('metadata', {}).get('language')
            file_path = data.get('metadata', {}).get('file_path', '<string>')

            issues = []
            metrics = {}

            # Logical analysis patterns
            logical_issues = await self._detect_logical_issues(content, language)
            complexity_issues = await self._analyze_complexity(content, language)
            pattern_issues = await self._detect_anti_patterns(content, language)

            issues.extend(logical_issues)
            issues.extend(complexity_issues)
            issues.extend(pattern_issues)

            # Calculate metrics
            metrics = {
                'cyclomatic_complexity': self._calculate_cyclomatic_complexity(content, language),
                'cognitive_complexity': self._calculate_cognitive_complexity(content, language),
                'maintainability_index': self._calculate_maintainability_index(content, language),
                'logical_lines': self._count_logical_lines(content),
                'decision_points': self._count_decision_points(content, language)
            }

            execution_time = asyncio.get_event_loop().time() - start_time

            return AnalysisResult(
                issues=issues,
                metrics=metrics,
                confidence=self._calculate_logic_confidence(issues, metrics),
                analysis_time=execution_time,
                metadata={
                    'analyzer': 'logic',
                    'language': language,
                    'file_path': file_path
                }
            )

        except Exception as e:
            self.logger.error(f"Logic analysis failed: {e}")
            return AnalysisResult(
                issues=[],
                metrics={},
                confidence=0.0,
                analysis_time=0.0,
                metadata={'error': str(e)}
            )

    async def analyze_context(self, data: Dict[str, Any]) -> AnalysisResult:
        """
        Perform contextual analysis on code.

        Args:
            data: Processed input data with content and metadata

        Returns:
            AnalysisResult with contextual insights
        """
        start_time = asyncio.get_event_loop().time()

        try:
            content = data.get('content', '')
            language = data.get('metadata', {}).get('language')
            dependencies = data.get('dependencies', [])
            imports = data.get('imports', [])

            issues = []
            metrics = {}

            # Contextual analysis
            dependency_issues = await self._analyze_dependencies(dependencies)
            import_issues = await self._analyze_imports(imports, language)
            naming_issues = await self._analyze_naming_conventions(content, language)
            documentation_issues = await self._analyze_documentation(content, language)

            issues.extend(dependency_issues)
            issues.extend(import_issues)
            issues.extend(naming_issues)
            issues.extend(documentation_issues)

            # Context metrics
            metrics = {
                'dependency_count': len(dependencies),
                'import_count': len(imports),
                'documentation_coverage': self._calculate_doc_coverage(content, language),
                'api_usage_patterns': self._analyze_api_patterns(content, language),
                'code_style_score': self._calculate_style_score(content, language)
            }

            execution_time = asyncio.get_event_loop().time() - start_time

            return AnalysisResult(
                issues=issues,
                metrics=metrics,
                confidence=self._calculate_context_confidence(issues, metrics),
                analysis_time=execution_time,
                metadata={
                    'analyzer': 'context',
                    'language': language,
                    'dependencies': len(dependencies),
                    'imports': len(imports)
                }
            )

        except Exception as e:
            self.logger.error(f"Context analysis failed: {e}")
            return AnalysisResult(
                issues=[],
                metrics={},
                confidence=0.0,
                analysis_time=0.0,
                metadata={'error': str(e)}
            )

    async def analyze_security(self, data: Dict[str, Any]) -> AnalysisResult:
        """
        Perform comprehensive security analysis.

        Args:
            data: Processed input data with content and metadata

        Returns:
            AnalysisResult with security findings and compliance violations
        """
        start_time = asyncio.get_event_loop().time()

        try:
            content = data.get('content', '')
            language = data.get('metadata', {}).get('language')
            file_path = data.get('metadata', {}).get('file_path', '<string>')

            issues = []
            security_findings = []
            compliance_violations = []

            # Security vulnerability scanning
            if self.security_config.get('enable_scanning', True):
                vulnerability_findings = await self._scan_vulnerabilities(content, language, file_path)
                security_findings.extend(vulnerability_findings)

                # Convert to issues
                for finding in vulnerability_findings:
                    issues.append(AnalysisIssue(
                        type='security',
                        severity=finding.severity,
                        message=finding.description,
                        line_number=finding.line_number,
                        column=None,
                        rule_id=finding.vulnerability_type,
                        suggestion=finding.remediation,
                        confidence=finding.confidence
                    ))

            # Compliance checking
            compliance_standards = self.security_config.get('compliance_standards', [])
            for standard in compliance_standards:
                violations = await self._check_compliance_standard(content, standard, file_path)
                compliance_violations.extend(violations)

                # Convert to issues
                for violation in violations:
                    issues.append(AnalysisIssue(
                        type='compliance',
                        severity=violation.severity,
                        message=f"{violation.standard}: {violation.description}",
                        line_number=None,
                        column=None,
                        rule_id=violation.rule,
                        suggestion=violation.remediation,
                        confidence=0.8
                    ))

            # Security metrics
            metrics = {
                'vulnerability_count': len(security_findings),
                'compliance_violations': len(compliance_violations),
                'security_score': self._calculate_security_score(security_findings),
                'risk_level': self._assess_risk_level(security_findings),
                'compliance_score': self._calculate_compliance_score(compliance_violations)
            }

            execution_time = asyncio.get_event_loop().time() - start_time

            return AnalysisResult(
                issues=issues,
                metrics=metrics,
                confidence=self._calculate_security_confidence(issues, metrics),
                analysis_time=execution_time,
                metadata={
                    'analyzer': 'security',
                    'language': language,
                    'file_path': file_path,
                    'security_findings': len(security_findings),
                    'compliance_violations': len(compliance_violations)
                }
            )

        except Exception as e:
            self.logger.error(f"Security analysis failed: {e}")
            return AnalysisResult(
                issues=[],
                metrics={},
                confidence=0.0,
                analysis_time=0.0,
                metadata={'error': str(e)}
            )

    async def extract_dependencies(self, content: str, language: str) -> List[Dict[str, Any]]:
        """
        Extract dependencies from code content.
        
        Args:
            content: Code content to analyze
            language: Programming language
            
        Returns:
            List of detected dependencies with metadata
        """
        dependencies = []
        
        # Language-specific dependency patterns
        patterns = {
            'python': [
                r'import\s+(\S+)',
                r'from\s+(\S+)\s+import',
                r'__import__\(["\'](\S+)["\']\)'
            ],
            'javascript': [
                r'import\s+.*\s+from\s+["\'](\S+)["\']',
                r'require\(["\'](\S+)["\']\)',
                r'import\(["\'](\S+)["\']\)'
            ],
            'typescript': [
                r'import\s+.*\s+from\s+["\'](\S+)["\']',
                r'require\(["\'](\S+)["\']\)',
                r'import\(["\'](\S+)["\']\)'
            ],
            'java': [
                r'import\s+([\w\.]+);',
                r'import\s+static\s+([\w\.]+);'
            ],
            'rust': [
                r'use\s+([\w:]+)',
                r'extern\s+crate\s+(\w+)',
                r'mod\s+(\w+)'
            ],
            'go': [
                r'import\s+"([^"]+)"',
                r'import\s+\([^)]+\)'
            ]
        }
        
        if language.lower() in patterns:
            for pattern in patterns[language.lower()]:
                matches = re.findall(pattern, content, re.MULTILINE)
                for match in matches:
                    dependencies.append({
                        'name': match,
                        'type': 'import',
                        'language': language,
                        'pattern': pattern
                    })
        
        # Detect package manager files
        if 'requirements.txt' in content or 'setup.py' in content:
            dependencies.append({'type': 'package_manager', 'name': 'pip'})
        elif 'package.json' in content:
            dependencies.append({'type': 'package_manager', 'name': 'npm'})
        elif 'Cargo.toml' in content:
            dependencies.append({'type': 'package_manager', 'name': 'cargo'})
        
        return dependencies
    
    async def calculate_similarity(self, content1: str, content2: str) -> float:
        """
        Calculate similarity between two code snippets using advanced AI.
        
        Args:
            content1: First code snippet
            content2: Second code snippet
            
        Returns:
            Similarity score between 0 and 1
        """
        # Tokenize and normalize
        tokens1 = self._tokenize_code(content1)
        tokens2 = self._tokenize_code(content2)
        
        # Calculate multiple similarity metrics
        structural_similarity = self._calculate_structural_similarity(tokens1, tokens2)
        semantic_similarity = self._calculate_semantic_similarity(content1, content2)
        syntactic_similarity = self._calculate_syntactic_similarity(tokens1, tokens2)
        
        # Weighted average
        similarity = (
            structural_similarity * 0.4 +
            semantic_similarity * 0.4 +
            syntactic_similarity * 0.2
        )
        
        return min(1.0, max(0.0, similarity))
    
    def _tokenize_code(self, content: str) -> List[str]:
        """Tokenize code content for analysis."""
        # Remove comments and strings
        content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'["\'].*?["\']', '', content)
        
        # Tokenize
        tokens = re.findall(r'\b\w+\b', content.lower())
        return tokens
    
    def _calculate_structural_similarity(self, tokens1: List[str], tokens2: List[str]) -> float:
        """Calculate structural similarity based on token patterns."""
        if not tokens1 or not tokens2:
            return 0.0
        
        # Use Jaccard similarity
        set1, set2 = set(tokens1), set(tokens2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_semantic_similarity(self, content1: str, content2: str) -> float:
        """Calculate semantic similarity using AI understanding."""
        # Simplified semantic analysis
        # In production, this would use embeddings or language models
        
        # Extract function names and variable names
        funcs1 = re.findall(r'def\s+(\w+)', content1) + re.findall(r'function\s+(\w+)', content1)
        funcs2 = re.findall(r'def\s+(\w+)', content2) + re.findall(r'function\s+(\w+)', content2)
        
        if funcs1 and funcs2:
            common_funcs = set(funcs1).intersection(set(funcs2))
            return len(common_funcs) / max(len(funcs1), len(funcs2))
        
        return 0.5  # Default moderate similarity
    
    def _calculate_syntactic_similarity(self, tokens1: List[str], tokens2: List[str]) -> float:
        """Calculate syntactic similarity based on code structure."""
        # Compare token sequences
        if not tokens1 or not tokens2:
            return 0.0
        
        # Use Levenshtein distance ratio
        from difflib import SequenceMatcher
        return SequenceMatcher(None, tokens1, tokens2).ratio()
    
    async def analyze_security(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive security analysis on code content.
        
        Args:
            content: Code content to analyze
            
        Returns:
            Security analysis results with vulnerabilities and recommendations
        """
        security_results = {
            'vulnerabilities': [],
            'security_score': 100,
            'recommendations': [],
            'compliance': {
                'OWASP': 'pending',
                'CWE': 'pending',
                'GDPR': 'pending',
                'HIPAA': 'pending'
            }
        }
        
        # Common vulnerability patterns
        vulnerability_patterns = [
            {
                'pattern': r'eval\s*\(',
                'severity': 'critical',
                'type': 'Code Injection',
                'cwe': 'CWE-94'
            },
            {
                'pattern': r'exec\s*\(',
                'severity': 'critical',
                'type': 'Code Injection',
                'cwe': 'CWE-94'
            },
            {
                'pattern': r'os\.system\s*\(',
                'severity': 'high',
                'type': 'Command Injection',
                'cwe': 'CWE-78'
            },
            {
                'pattern': r'subprocess\.\w+\s*\([^)]*shell\s*=\s*True',
                'severity': 'high',
                'type': 'Command Injection',
                'cwe': 'CWE-78'
            },
            {
                'pattern': r'password\s*=\s*["\'][^"\']+["\']',
                'severity': 'high',
                'type': 'Hardcoded Password',
                'cwe': 'CWE-798'
            },
            {
                'pattern': r'api_key\s*=\s*["\'][^"\']+["\']',
                'severity': 'high',
                'type': 'Hardcoded API Key',
                'cwe': 'CWE-798'
            },
            {
                'pattern': r'pickle\.loads?\s*\(',
                'severity': 'medium',
                'type': 'Insecure Deserialization',
                'cwe': 'CWE-502'
            },
            {
                'pattern': r'random\.\w+\s*\(',
                'severity': 'low',
                'type': 'Weak Random Number Generator',
                'cwe': 'CWE-330'
            }
        ]
        
        # Scan for vulnerabilities
        for item_key, item_data in content.items():
            if isinstance(item_data, dict) and 'content' in item_data:
                code_content = item_data['content']
                
                for vuln in vulnerability_patterns:
                    matches = re.findall(vuln['pattern'], code_content, re.IGNORECASE)
                    if matches:
                        security_results['vulnerabilities'].append({
                            'file': item_key,
                            'type': vuln['type'],
                            'severity': vuln['severity'],
                            'cwe': vuln['cwe'],
                            'occurrences': len(matches),
                            'pattern': vuln['pattern']
                        })
                        
                        # Adjust security score
                        if vuln['severity'] == 'critical':
                            security_results['security_score'] -= 25
                        elif vuln['severity'] == 'high':
                            security_results['security_score'] -= 15
                        elif vuln['severity'] == 'medium':
                            security_results['security_score'] -= 10
                        else:
                            security_results['security_score'] -= 5
        
        # Add recommendations based on findings
        if security_results['vulnerabilities']:
            security_results['recommendations'].append(
                "Implement input validation and sanitization"
            )
            security_results['recommendations'].append(
                "Use parameterized queries for database operations"
            )
            security_results['recommendations'].append(
                "Store sensitive data in environment variables"
            )
            security_results['recommendations'].append(
                "Implement proper error handling and logging"
            )
        
        # Update compliance status
        if security_results['security_score'] >= 90:
            security_results['compliance']['OWASP'] = 'compliant'
            security_results['compliance']['CWE'] = 'compliant'
        elif security_results['security_score'] >= 70:
            security_results['compliance']['OWASP'] = 'partial'
            security_results['compliance']['CWE'] = 'partial'
        else:
            security_results['compliance']['OWASP'] = 'non-compliant'
            security_results['compliance']['CWE'] = 'non-compliant'
        
        return security_results

    async def _analyze_python_syntax(self, content: str, file_path: str) -> Tuple[List[AnalysisIssue], Dict[str, Any]]:
        """Analyze Python syntax."""
        issues = []
        metrics = {}

        try:
            # Parse Python AST
            tree = ast.parse(content)
            
            # Basic syntax metrics
            metrics['ast_nodes'] = len(list(ast.walk(tree)))
            metrics['classes'] = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
            metrics['functions'] = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
            metrics['imports'] = len([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))])

            # Check for syntax issues using tokenize
            tokens = list(tokenize.generate_tokens(io.StringIO(content).readline))
            
            # Look for potential issues
            for token in tokens:
                if token.type == tokenize.ERRORTOKEN:
                    issues.append(AnalysisIssue(
                        type='syntax',
                        severity='high',
                        message=f"Invalid token: {token.string}",
                        line_number=token.start[0],
                        column=token.start[1],
                        rule_id='INVALID_TOKEN',
                        suggestion='Fix syntax error',
                        confidence=1.0
                    ))

        except SyntaxError as e:
            issues.append(AnalysisIssue(
                type='syntax',
                severity='critical',
                message=f"Syntax error: {e.msg}",
                line_number=e.lineno,
                column=e.offset,
                rule_id='SYNTAX_ERROR',
                suggestion='Fix syntax error',
                confidence=1.0
            ))

        except Exception as e:
            self.logger.warning(f"Python syntax analysis failed: {e}")

        return issues, metrics

    async def _analyze_js_syntax(self, content: str, file_path: str) -> Tuple[List[AnalysisIssue], Dict[str, Any]]:
        """Analyze JavaScript/TypeScript syntax."""
        issues = []
        metrics = {}

        # Basic pattern matching for JS/TS
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for common syntax issues
            if line.strip().endswith(';,'):
                issues.append(AnalysisIssue(
                    type='syntax',
                    severity='medium',
                    message="Unnecessary semicolon before comma",
                    line_number=i,
                    column=None,
                    rule_id='EXTRA_SEMICOLON',
                    suggestion='Remove extra semicolon',
                    confidence=0.9
                ))

            # Check for missing semicolons (basic check)
            if (line.strip() and 
                not line.strip().endswith((';', '{', '}', ')', ',')) and
                not line.strip().startswith(('if', 'for', 'while', 'function', 'class', '//', '/*'))):
                issues.append(AnalysisIssue(
                    type='syntax',
                    severity='low',
                    message="Possible missing semicolon",
                    line_number=i,
                    column=None,
                    rule_id='MISSING_SEMICOLON',
                    suggestion='Add semicolon',
                    confidence=0.6
                ))

        # Basic metrics
        metrics['lines'] = len(lines)
        metrics['functions'] = content.count('function ')
        metrics['arrow_functions'] = content.count(' => ')
        metrics['classes'] = content.count('class ')

        return issues, metrics

    async def _analyze_java_syntax(self, content: str, file_path: str) -> Tuple[List[AnalysisIssue], Dict[str, Any]]:
        """Analyze Java syntax."""
        issues = []
        metrics = {}

        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for common Java syntax issues
            if 'public class' in line and not line.strip().endswith('{'):
                issues.append(AnalysisIssue(
                    type='syntax',
                    severity='medium',
                    message="Class declaration should end with opening brace",
                    line_number=i,
                    column=None,
                    rule_id='CLASS_BRACE',
                    suggestion='Add opening brace',
                    confidence=0.8
                ))

        # Basic metrics
        metrics['lines'] = len(lines)
        metrics['classes'] = content.count('class ')
        metrics['methods'] = content.count('public ') + content.count('private ') + content.count('protected ')
        metrics['imports'] = content.count('import ')

        return issues, metrics

    async def _analyze_generic_syntax(self, content: str, file_path: str) -> Tuple[List[AnalysisIssue], Dict[str, Any]]:
        """Generic syntax analysis for unknown languages."""
        issues = []
        metrics = {}

        lines = content.split('\n')
        
        # Basic checks
        for i, line in enumerate(lines, 1):
            # Check for very long lines
            if len(line) > 120:
                issues.append(AnalysisIssue(
                    type='syntax',
                    severity='low',
                    message=f"Line too long ({len(line)} characters)",
                    line_number=i,
                    column=None,
                    rule_id='LINE_TOO_LONG',
                    suggestion='Break line into multiple lines',
                    confidence=0.7
                ))

            # Check for trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                issues.append(AnalysisIssue(
                    type='syntax',
                    severity='low',
                    message="Trailing whitespace",
                    line_number=i,
                    column=None,
                    rule_id='TRAILING_WHITESPACE',
                    suggestion='Remove trailing whitespace',
                    confidence=0.9
                ))

        # Basic metrics
        metrics['lines'] = len(lines)
        metrics['non_empty_lines'] = len([l for l in lines if l.strip()])
        metrics['comment_lines'] = len([l for l in lines if l.strip().startswith(('#', '//', '/*'))])

        return issues, metrics

    async def _detect_logical_issues(self, content: str, language: Optional[str]) -> List[AnalysisIssue]:
        """Detect logical issues in code."""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Dead code detection
            if 'return' in line and i < len(lines):
                next_lines = lines[i:i+5]  # Check next 5 lines
                for j, next_line in enumerate(next_lines):
                    if next_line.strip() and not next_line.strip().startswith(('#', '//', '/*', '}', 'else')):
                        issues.append(AnalysisIssue(
                            type='logic',
                            severity='medium',
                            message="Unreachable code after return statement",
                            line_number=i + j + 1,
                            column=None,
                            rule_id='UNREACHABLE_CODE',
                            suggestion='Remove unreachable code',
                            confidence=0.8
                        ))
                        break

            # Infinite loop detection
            if language == 'python' and 'while True:' in line:
                if 'break' not in content[content.find(line):]:
                    issues.append(AnalysisIssue(
                        type='logic',
                        severity='high',
                        message="Potential infinite loop detected",
                        line_number=i,
                        column=None,
                        rule_id='INFINITE_LOOP',
                        suggestion='Add break condition',
                        confidence=0.7
                    ))

        return issues

    async def _analyze_complexity(self, content: str, language: Optional[str]) -> List[AnalysisIssue]:
        """Analyze code complexity."""
        issues = []

        if HAS_RADON and language == 'python':
            try:
                # Calculate complexity using Radon
                complexity_data = radon_complexity.cc_visit(content)
                
                for func_data in complexity_data:
                    if func_data.complexity > 10:  # High complexity threshold
                        issues.append(AnalysisIssue(
                            type='complexity',
                            severity='medium' if func_data.complexity <= 15 else 'high',
                            message=f"High cyclomatic complexity: {func_data.complexity}",
                            line_number=func_data.lineno,
                            column=None,
                            rule_id='HIGH_COMPLEXITY',
                            suggestion='Consider breaking down the function',
                            confidence=0.9
                        ))

            except Exception as e:
                self.logger.warning(f"Radon analysis failed: {e}")

        return issues

    async def _detect_anti_patterns(self, content: str, language: Optional[str]) -> List[AnalysisIssue]:
        """Detect code anti-patterns."""
        issues = []
        lines = content.split('\n')

        # Common anti-patterns
        anti_patterns = {
            'god_class': {
                'pattern': lambda: len([l for l in lines if 'def ' in l]) > 20,
                'message': 'God class detected - too many methods',
                'severity': 'medium'
            },
            'long_method': {
                'pattern': lambda: max([len(l) for l in lines] + [0]) > 50,
                'message': 'Long method detected',
                'severity': 'low'
            }
        }

        for pattern_name, pattern_data in anti_patterns.items():
            if pattern_data['pattern']():
                issues.append(AnalysisIssue(
                    type='anti_pattern',
                    severity=pattern_data['severity'],
                    message=pattern_data['message'],
                    line_number=None,
                    column=None,
                    rule_id=pattern_name.upper(),
                    suggestion='Refactor code to follow best practices',
                    confidence=0.7
                ))

        return issues

    async def _scan_vulnerabilities(self, content: str, language: Optional[str], 
                                  file_path: str) -> List[SecurityFinding]:
        """Scan for security vulnerabilities."""
        findings = []

        # Pattern-based vulnerability detection
        for vuln_type, patterns in self.SECURITY_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    
                    findings.append(SecurityFinding(
                        vulnerability_type=vuln_type,
                        severity=self._get_vulnerability_severity(vuln_type),
                        description=f"Potential {vuln_type.replace('_', ' ')} vulnerability",
                        file_path=file_path,
                        line_number=line_num,
                        cwe_id=self._get_cwe_id(vuln_type),
                        owasp_category=self._get_owasp_category(vuln_type),
                        remediation=self._get_remediation_advice(vuln_type),
                        confidence=0.8
                    ))

        # Use Bandit for Python security analysis
        if HAS_BANDIT and language == 'python' and self.bandit_manager:
            try:
                # This is a simplified version - in practice, you'd need to handle file I/O
                # bandit_results = self.bandit_manager.run_tests()
                pass
            except Exception as e:
                self.logger.warning(f"Bandit analysis failed: {e}")

        return findings

    async def _check_compliance_standard(self, content: str, standard: str, 
                                       file_path: str) -> List[ComplianceViolation]:
        """Check compliance with specific standard."""
        violations = []

        if standard in self.COMPLIANCE_PATTERNS:
            patterns = self.COMPLIANCE_PATTERNS[standard]
            
            for category, category_patterns in patterns.items():
                for pattern in category_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        violations.append(ComplianceViolation(
                            standard=standard,
                            rule=category,
                            description=f"Potential {standard} {category.replace('_', ' ')} detected",
                            severity='medium',
                            location=file_path,
                            remediation=f"Ensure {standard} compliance for {category.replace('_', ' ')}"
                        ))

        return violations

    # Helper methods for calculations and scoring

    def _calculate_syntax_confidence(self, issues: List[AnalysisIssue], 
                                   metrics: Dict[str, Any]) -> float:
        """Calculate confidence score for syntax analysis."""
        if not issues:
            return 1.0
        
        critical_issues = len([i for i in issues if i.severity == 'critical'])
        high_issues = len([i for i in issues if i.severity == 'high'])
        
        if critical_issues > 0:
            return 0.3
        elif high_issues > 0:
            return 0.7
        else:
            return 0.9

    def _calculate_logic_confidence(self, issues: List[AnalysisIssue], 
                                  metrics: Dict[str, Any]) -> float:
        """Calculate confidence score for logic analysis."""
        complexity = metrics.get('cyclomatic_complexity', 0)
        
        if complexity > 20:
            return 0.5
        elif complexity > 10:
            return 0.7
        else:
            return 0.9

    def _calculate_context_confidence(self, issues: List[AnalysisIssue], 
                                    metrics: Dict[str, Any]) -> float:
        """Calculate confidence score for context analysis."""
        doc_coverage = metrics.get('documentation_coverage', 0)
        style_score = metrics.get('code_style_score', 0)
        
        return (doc_coverage + style_score) / 2

    def _calculate_security_confidence(self, issues: List[AnalysisIssue], 
                                     metrics: Dict[str, Any]) -> float:
        """Calculate confidence score for security analysis."""
        security_score = metrics.get('security_score', 1.0)
        return security_score

    def _calculate_cyclomatic_complexity(self, content: str, language: Optional[str]) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1  # Base complexity
        
        # Count decision points
        decision_keywords = ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'case', 'switch']
        
        for keyword in decision_keywords:
            complexity += content.lower().count(keyword)
        
        return complexity

    def _calculate_cognitive_complexity(self, content: str, language: Optional[str]) -> int:
        """Calculate cognitive complexity."""
        # Simplified cognitive complexity calculation
        nesting_level = 0
        cognitive_complexity = 0
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Increase nesting for control structures
            if any(keyword in line for keyword in ['if', 'for', 'while', 'try']):
                cognitive_complexity += nesting_level + 1
                if line.endswith(':'):
                    nesting_level += 1
            
            # Decrease nesting
            if line.startswith(('except', 'finally', 'else')):
                nesting_level = max(0, nesting_level - 1)
        
        return cognitive_complexity

    def _calculate_maintainability_index(self, content: str, language: Optional[str]) -> float:
        """Calculate maintainability index."""
        lines = len(content.split('\n'))
        complexity = self._calculate_cyclomatic_complexity(content, language)
        
        # Simplified maintainability index
        if lines == 0:
            return 100.0
        
        maintainability = 171 - 5.2 * (complexity / lines) * 100 - 0.23 * complexity - 16.2 * (lines / 1000)
        return max(0, min(100, maintainability))

    def _count_logical_lines(self, content: str) -> int:
        """Count logical lines of code."""
        lines = content.split('\n')
        logical_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('//'):
                logical_lines += 1
        
        return logical_lines

    def _count_decision_points(self, content: str, language: Optional[str]) -> int:
        """Count decision points in code."""
        decision_keywords = ['if', 'elif', 'else', 'for', 'while', 'switch', 'case']
        
        count = 0
        for keyword in decision_keywords:
            count += content.lower().count(keyword)
        
        return count

    async def _analyze_dependencies(self, dependencies: List[str]) -> List[AnalysisIssue]:
        """Analyze dependencies for issues."""
        issues = []
        
        # Check for deprecated packages (simplified)
        deprecated_packages = ['md5', 'sha', 'urllib2']
        
        for dep in dependencies:
            if any(deprecated in dep.lower() for deprecated in deprecated_packages):
                issues.append(AnalysisIssue(
                    type='dependency',
                    severity='medium',
                    message=f"Deprecated dependency: {dep}",
                    line_number=None,
                    column=None,
                    rule_id='DEPRECATED_DEPENDENCY',
                    suggestion='Update to a supported alternative',
                    confidence=0.8
                ))
        
        return issues

    async def _analyze_imports(self, imports: List[str], language: Optional[str]) -> List[AnalysisIssue]:
        """Analyze import statements."""
        issues = []
        
        # Check for unused imports (simplified)
        if language == 'python':
            for import_stmt in imports:
                if 'import *' in import_stmt:
                    issues.append(AnalysisIssue(
                        type='import',
                        severity='medium',
                        message="Wildcard import should be avoided",
                        line_number=None,
                        column=None,
                        rule_id='WILDCARD_IMPORT',
                        suggestion='Import specific modules',
                        confidence=0.9
                    ))
        
        return issues

    async def _analyze_naming_conventions(self, content: str, language: Optional[str]) -> List[AnalysisIssue]:
        """Analyze naming conventions."""
        issues = []
        
        if language == 'python':
            # Check for PEP 8 naming conventions
            functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
            for func_name in functions:
                if not func_name.islower() and '_' not in func_name:
                    issues.append(AnalysisIssue(
                        type='naming',
                        severity='low',
                        message=f"Function name '{func_name}' should be snake_case",
                        line_number=None,
                        column=None,
                        rule_id='FUNCTION_NAMING',
                        suggestion='Use snake_case for function names',
                        confidence=0.8
                    ))
        
        return issues

    async def _analyze_documentation(self, content: str, language: Optional[str]) -> List[AnalysisIssue]:
        """Analyze code documentation."""
        issues = []
        
        if language == 'python':
            # Check for missing docstrings
            functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
            for func_name in functions:
                func_pattern = rf'def\s+{re.escape(func_name)}.*?:'
                match = re.search(func_pattern, content, re.DOTALL)
                if match:
                    func_start = match.end()
                    next_lines = content[func_start:func_start+200]
                    if '"""' not in next_lines and "'''" not in next_lines:
                        issues.append(AnalysisIssue(
                            type='documentation',
                            severity='low',
                            message=f"Function '{func_name}' missing docstring",
                            line_number=None,
                            column=None,
                            rule_id='MISSING_DOCSTRING',
                            suggestion='Add docstring to document function',
                            confidence=0.7
                        ))
        
        return issues

    def _calculate_doc_coverage(self, content: str, language: Optional[str]) -> float:
        """Calculate documentation coverage."""
        if language != 'python':
            return 0.5  # Default for non-Python
        
        functions = len(re.findall(r'def\s+[a-zA-Z_][a-zA-Z0-9_]*', content))
        classes = len(re.findall(r'class\s+[a-zA-Z_][a-zA-Z0-9_]*', content))
        docstrings = content.count('"""') + content.count("'''")
        
        total_definitions = functions + classes
        if total_definitions == 0:
            return 1.0
        
        # Approximate docstring coverage
        coverage = min(1.0, docstrings / (total_definitions * 2))  # Assuming opening and closing quotes
        return coverage

    def _analyze_api_patterns(self, content: str, language: Optional[str]) -> Dict[str, int]:
        """Analyze API usage patterns."""
        patterns = {
            'async_calls': content.count('async ') + content.count('await '),
            'error_handling': content.count('try:') + content.count('catch('),
            'logging_calls': content.count('log.') + content.count('logger.'),
            'database_calls': content.count('query') + content.count('select') + content.count('insert'),
            'http_calls': content.count('request') + content.count('fetch(') + content.count('get(')
        }
        return patterns

    def _calculate_style_score(self, content: str, language: Optional[str]) -> float:
        """Calculate code style score."""
        lines = content.split('\n')
        total_lines = len(lines)
        
        if total_lines == 0:
            return 1.0
        
        style_violations = 0
        
        for line in lines:
            # Check for style issues
            if len(line) > 120:  # Line too long
                style_violations += 1
            if line.endswith(' ') or line.endswith('\t'):  # Trailing whitespace
                style_violations += 1
            if '\t' in line and '    ' in line:  # Mixed indentation
                style_violations += 1
        
        style_score = max(0.0, 1.0 - (style_violations / total_lines))
        return style_score

    def _get_vulnerability_severity(self, vuln_type: str) -> str:
        """Get severity level for vulnerability type."""
        severity_map = {
            'sql_injection': 'critical',
            'xss': 'high',
            'command_injection': 'critical',
            'hardcoded_secrets': 'high',
            'crypto_weakness': 'medium'
        }
        return severity_map.get(vuln_type, 'medium')

    def _get_cwe_id(self, vuln_type: str) -> Optional[str]:
        """Get CWE ID for vulnerability type."""
        cwe_map = {
            'sql_injection': 'CWE-89',
            'xss': 'CWE-79',
            'command_injection': 'CWE-78',
            'hardcoded_secrets': 'CWE-798',
            'crypto_weakness': 'CWE-327'
        }
        return cwe_map.get(vuln_type)

    def _get_owasp_category(self, vuln_type: str) -> Optional[str]:
        """Get OWASP category for vulnerability type."""
        owasp_map = {
            'sql_injection': 'A03',
            'xss': 'A03',
            'command_injection': 'A03',
            'hardcoded_secrets': 'A07',
            'crypto_weakness': 'A02'
        }
        return owasp_map.get(vuln_type)

    def _get_remediation_advice(self, vuln_type: str) -> Optional[str]:
        """Get remediation advice for vulnerability type."""
        remediation_map = {
            'sql_injection': 'Use parameterized queries and input validation',
            'xss': 'Sanitize and validate all user inputs',
            'command_injection': 'Avoid executing user input, use safe alternatives',
            'hardcoded_secrets': 'Use environment variables or secure key management',
            'crypto_weakness': 'Use strong cryptographic algorithms (SHA-256, AES-256)'
        }
        return remediation_map.get(vuln_type)

    def _calculate_security_score(self, findings: List[SecurityFinding]) -> float:
        """Calculate overall security score."""
        if not findings:
            return 1.0
        
        severity_weights = {
            'critical': 10,
            'high': 5,
            'medium': 2,
            'low': 1
        }
        
        total_weight = sum(severity_weights.get(f.severity, 1) for f in findings)
        max_possible = len(findings) * 10  # Assuming all critical
        
        security_score = max(0.0, 1.0 - (total_weight / max(max_possible, 1)))
        return security_score

    def _assess_risk_level(self, findings: List[SecurityFinding]) -> str:
        """Assess overall risk level."""
        if not findings:
            return 'low'
        
        critical_count = len([f for f in findings if f.severity == 'critical'])
        high_count = len([f for f in findings if f.severity == 'high'])
        
        if critical_count > 0:
            return 'critical'
        elif high_count > 2:
            return 'high'
        elif high_count > 0:
            return 'medium'
        else:
            return 'low'

    def _calculate_compliance_score(self, violations: List[ComplianceViolation]) -> float:
        """Calculate compliance score."""
        if not violations:
            return 1.0
        
        severity_weights = {
            'critical': 5,
            'high': 3,
            'medium': 2,
            'low': 1
        }
        
        total_weight = sum(severity_weights.get(v.severity, 1) for v in violations)
        max_possible = len(violations) * 5
        
        compliance_score = max(0.0, 1.0 - (total_weight / max(max_possible, 1)))
        return compliance_score
