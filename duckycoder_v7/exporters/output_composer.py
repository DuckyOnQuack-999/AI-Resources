"""
DuckyCoder v6 Output Composer
Implements structured output composition with MDX, interactive features, and export formats.
"""

import asyncio
import logging
import json
import os
import base64
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import hashlib
import zipfile
import tempfile

# Export format imports
try:
    import markdown
    from markdown.extensions import codehilite, tables, toc
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

try:
    from jinja2 import Environment, FileSystemLoader, Template
    HAS_JINJA2 = True
except ImportError:
    HAS_JINJA2 = False

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    from weasyprint import HTML, CSS
    HAS_WEASYPRINT = True
except ImportError:
    HAS_WEASYPRINT = False

try:
    import git
    HAS_GIT = True
except ImportError:
    HAS_GIT = False


@dataclass
class OutputSection:
    """Represents a section in the structured output."""
    title: str
    content: str
    section_type: str  # summary, analysis, enhancements, metadata, ui_mockups
    priority: int  # 1-5, lower is higher priority
    interactive: bool
    metadata: Dict[str, Any]


@dataclass
class OutputDocument:
    """Represents the complete structured output document."""
    title: str
    summary: str
    sections: List[OutputSection]
    metadata: Dict[str, Any]
    generation_time: datetime
    version: str
    export_formats: List[str]


@dataclass
class ExportResult:
    """Result of export operation."""
    format_type: str
    file_path: str
    success: bool
    size_bytes: int
    metadata: Dict[str, Any]
    error: Optional[str]


class OutputComposer:
    """Structured output composition with multiple export formats."""

    # Supported export formats
    EXPORT_FORMATS = {
        'markdown': {
            'extension': '.md',
            'mime_type': 'text/markdown',
            'supports_interactive': False,
            'ci_cd_compatible': True
        },
        'html': {
            'extension': '.html',
            'mime_type': 'text/html',
            'supports_interactive': True,
            'ci_cd_compatible': True
        },
        'json': {
            'extension': '.json',
            'mime_type': 'application/json',
            'supports_interactive': False,
            'ci_cd_compatible': True
        },
        'yaml': {
            'extension': '.yaml',
            'mime_type': 'application/x-yaml',
            'supports_interactive': False,
            'ci_cd_compatible': True
        },
        'pdf': {
            'extension': '.pdf',
            'mime_type': 'application/pdf',
            'supports_interactive': False,
            'ci_cd_compatible': False
        },
        'sarif': {
            'extension': '.sarif',
            'mime_type': 'application/sarif+json',
            'supports_interactive': False,
            'ci_cd_compatible': True
        },
        'codebase': {
            'extension': '.zip',
            'mime_type': 'application/zip',
            'supports_interactive': False,
            'ci_cd_compatible': True
        },
        'git_diff': {
            'extension': '.diff',
            'mime_type': 'text/plain',
            'supports_interactive': False,
            'ci_cd_compatible': True
        }
    }

    # MDX component templates
    MDX_COMPONENTS = {
        'code_block': '''```{language}
{code}
```''',
        'interactive_chart': '''<Chart type="{chart_type}" data={{data}} />''',
        'collapsible_section': '''<Details summary="{title}">
{content}
</Details>''',
        'alert': '''<Alert type="{alert_type}">
{message}
</Alert>''',
        'tabs': '''<Tabs>
{tab_items}
</Tabs>''',
        'progress_bar': '''<Progress value={value} max={max} />''',
        'badge': '''<Badge variant="{variant}">{text}</Badge>'''
    }

    # CI/CD templates
    CICD_TEMPLATES = {
        'github_actions': {
            'workflow': '''name: DuckyCoder v6 Analysis
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  duckycoder-analysis:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install DuckyCoder v6
      run: |
        pip install duckycoder-v6
    
    - name: Run Analysis
      run: |
        duckycoder process {input_files} --export sarif html json --output-dir ./duckycoder-results
    
    - name: Upload Results
      uses: actions/upload-artifact@v3
      with:
        name: duckycoder-analysis
        path: ./duckycoder-results
    
    - name: Upload SARIF
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: ./duckycoder-results/analysis.sarif
''',
            'security_report': '''# Security Analysis Report

## Summary
- **Total Issues**: {total_issues}
- **Critical**: {critical_count}
- **High**: {high_count}
- **Medium**: {medium_count}
- **Low**: {low_count}

## Compliance Status
{compliance_status}

## Action Required
{action_required}
'''
        },
        'gitlab_ci': {
            'pipeline': '''stages:
  - analysis
  - report

duckycoder_analysis:
  stage: analysis
  image: python:3.11
  script:
    - pip install duckycoder-v6
    - duckycoder process {input_files} --export sarif html json --output-dir ./duckycoder-results
  artifacts:
    reports:
      sast: duckycoder-results/analysis.sarif
    paths:
      - duckycoder-results/
    expire_in: 1 week

security_report:
  stage: report
  script:
    - echo "Security analysis completed"
  only:
    - main
''',
        }
    }

    def __init__(self, config: Dict[str, Any]):
        """Initialize the output composer."""
        self.config = config
        self.export_config = config.get('export_config', {})
        self.logger = logging.getLogger(__name__)

        # Output settings
        self.output_dir = self.export_config.get('output_directory', './duckycoder_output')
        self.include_metadata = self.export_config.get('include_metadata', True)
        self.compression = self.export_config.get('compression', False)
        self.version_control = self.export_config.get('version_control', True)

        # Initialize templates
        self._init_templates()

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def _init_templates(self):
        """Initialize Jinja2 templates."""
        if HAS_JINJA2:
            # Create template directory if it doesn't exist
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
            if not os.path.exists(template_dir):
                os.makedirs(template_dir)
                # Create default templates
                self._create_default_templates(template_dir)
            
            self.jinja_env = Environment(loader=FileSystemLoader(template_dir))
        else:
            self.jinja_env = None

    def _create_default_templates(self, template_dir: str):
        """Create default templates for various formats."""
        # HTML template
        html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 40px; line-height: 1.6; }
        .header { border-bottom: 2px solid #eee; padding-bottom: 20px; margin-bottom: 30px; }
        .section { margin-bottom: 30px; padding: 20px; border-left: 4px solid #007acc; background: #f8f9fa; }
        .summary { background: #e8f5e8; border-left-color: #28a745; }
        .analysis { background: #fff3cd; border-left-color: #ffc107; }
        .enhancements { background: #d1ecf1; border-left-color: #17a2b8; }
        .metadata { background: #f8d7da; border-left-color: #dc3545; }
        .ui-mockups { background: #e2e3e5; border-left-color: #6c757d; }
        pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
        .interactive { border: 1px dashed #007acc; padding: 10px; margin: 10px 0; }
        .badge { padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
        .badge-critical { background: #dc3545; color: white; }
        .badge-high { background: #fd7e14; color: white; }
        .badge-medium { background: #ffc107; color: black; }
        .badge-low { background: #28a745; color: white; }
        .progress { width: 100%; height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; }
        .progress-bar { height: 100%; background: linear-gradient(90deg, #007acc, #17a2b8); transition: width 0.3s; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ title }}</h1>
        <p><strong>Generated:</strong> {{ generation_time }}</p>
        <p><strong>Version:</strong> {{ version }}</p>
        {% if summary %}
        <div class="summary">
            <h2>Summary</h2>
            {{ summary | safe }}
        </div>
        {% endif %}
    </div>
    
    {% for section in sections %}
    <div class="section {{ section.section_type }}">
        <h2>{{ section.title }}</h2>
        {% if section.interactive %}
        <div class="interactive">
            <em>Interactive Content</em>
        </div>
        {% endif %}
        {{ section.content | safe }}
        {% if section.metadata %}
        <details style="margin-top: 15px;">
            <summary>Section Metadata</summary>
            <pre>{{ section.metadata | tojson(indent=2) }}</pre>
        </details>
        {% endif %}
    </div>
    {% endfor %}
    
    {% if metadata and include_metadata %}
    <div class="section metadata">
        <h2>Document Metadata</h2>
        <pre>{{ metadata | tojson(indent=2) }}</pre>
    </div>
    {% endif %}
</body>
</html>'''
        
        with open(os.path.join(template_dir, 'report.html'), 'w') as f:
            f.write(html_template)

        # Markdown template
        markdown_template = '''# {{ title }}

**Generated:** {{ generation_time }}  
**Version:** {{ version }}

{% if summary %}
## Summary

{{ summary }}
{% endif %}

{% for section in sections %}
## {{ section.title }}

{% if section.interactive %}
> **Note:** This section contains interactive content that may not display properly in static markdown.
{% endif %}

{{ section.content }}

{% if section.metadata and include_metadata %}
<details>
<summary>Section Metadata</summary>

```json
{{ section.metadata | tojson(indent=2) }}
```
</details>
{% endif %}

---
{% endfor %}

{% if metadata and include_metadata %}
## Document Metadata

```json
{{ metadata | tojson(indent=2) }}
```
{% endif %}
'''
        
        with open(os.path.join(template_dir, 'report.md'), 'w') as f:
            f.write(markdown_template)

    async def compose_output(self, processed_data: Dict[str, Any],
                           analysis_results: Dict[str, Any],
                           enhancement_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compose structured output from processing results.

        Args:
            processed_data: Original processed content
            analysis_results: Analysis findings
            enhancement_results: Enhancement results

        Returns:
            Structured output document data
        """
        try:
            self.logger.info("Composing structured output")

            # Create output sections
            sections = []

            # Summary section
            summary_section = await self._create_summary_section(
                processed_data, analysis_results, enhancement_results
            )
            sections.append(summary_section)

            # Analysis section
            analysis_section = await self._create_analysis_section(analysis_results)
            sections.append(analysis_section)

            # Enhancements section
            enhancement_section = await self._create_enhancement_section(enhancement_results)
            sections.append(enhancement_section)

            # UI Mockups section (if applicable)
            ui_section = await self._create_ui_mockups_section(enhancement_results)
            if ui_section:
                sections.append(ui_section)

            # Performance section
            performance_section = await self._create_performance_section(
                analysis_results, enhancement_results
            )
            if performance_section:
                sections.append(performance_section)

            # Security section
            security_section = await self._create_security_section(analysis_results)
            if security_section:
                sections.append(security_section)

            # Create output document
            document = OutputDocument(
                title="DuckyCoder v6 Analysis Report",
                summary=self._generate_executive_summary(
                    processed_data, analysis_results, enhancement_results
                ),
                sections=sections,
                metadata={
                    'total_files_processed': len(processed_data),
                    'total_issues_found': self._count_total_issues(analysis_results),
                    'total_enhancements_applied': self._count_total_enhancements(enhancement_results),
                    'analysis_confidence': self._calculate_overall_confidence(analysis_results),
                    'enhancement_confidence': self._calculate_overall_confidence(enhancement_results),
                    'processing_pipeline': ['input_processing', 'analysis', 'enhancement', 'output_composition'],
                    'input_sources': list(processed_data.keys()),
                    'languages_detected': self._extract_languages(processed_data),
                    'frameworks_detected': self._extract_frameworks(processed_data),
                    'export_timestamp': datetime.now().isoformat()
                },
                generation_time=datetime.now(),
                version="6.0.0",
                export_formats=self.export_config.get('default_formats', ['markdown', 'html', 'json'])
            )

            return asdict(document)

        except Exception as e:
            self.logger.error(f"Output composition failed: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def export_format(self, output_data: Dict[str, Any], 
                          format_type: str) -> str:
        """
        Export output data to specified format.

        Args:
            output_data: Structured output data
            format_type: Export format (markdown, html, json, etc.)

        Returns:
            Path to exported file
        """
        try:
            if format_type not in self.EXPORT_FORMATS:
                raise ValueError(f"Unsupported export format: {format_type}")

            self.logger.info(f"Exporting to {format_type} format")

            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"duckycoder_report_{timestamp}{self.EXPORT_FORMATS[format_type]['extension']}"
            file_path = os.path.join(self.output_dir, filename)

            # Export based on format
            if format_type == 'markdown':
                await self._export_markdown(output_data, file_path)
            elif format_type == 'html':
                await self._export_html(output_data, file_path)
            elif format_type == 'json':
                await self._export_json(output_data, file_path)
            elif format_type == 'yaml':
                await self._export_yaml(output_data, file_path)
            elif format_type == 'pdf':
                await self._export_pdf(output_data, file_path)
            elif format_type == 'sarif':
                await self._export_sarif(output_data, file_path)
            elif format_type == 'codebase':
                await self._export_codebase(output_data, file_path)
            elif format_type == 'git_diff':
                await self._export_git_diff(output_data, file_path)
            else:
                raise ValueError(f"Export handler not implemented for {format_type}")

            self.logger.info(f"Successfully exported to {file_path}")
            return file_path

        except Exception as e:
            self.logger.error(f"Export to {format_type} failed: {e}")
            raise

    async def _create_summary_section(self, processed_data: Dict[str, Any],
                                    analysis_results: Dict[str, Any],
                                    enhancement_results: Dict[str, Any]) -> OutputSection:
        """Create executive summary section."""
        total_issues = self._count_total_issues(analysis_results)
        total_enhancements = self._count_total_enhancements(enhancement_results)
        
        content = f"""
## Executive Summary

**Files Processed:** {len(processed_data)}  
**Issues Identified:** {total_issues}  
**Enhancements Applied:** {total_enhancements}

### Key Findings
{self._generate_key_findings(analysis_results)}

### Improvements Made
{self._generate_improvements_summary(enhancement_results)}

### Risk Assessment
{self._generate_risk_assessment(analysis_results)}
"""

        return OutputSection(
            title="Executive Summary",
            content=content,
            section_type="summary",
            priority=1,
            interactive=False,
            metadata={
                'files_processed': len(processed_data),
                'total_issues': total_issues,
                'total_enhancements': total_enhancements
            }
        )

    async def _create_analysis_section(self, analysis_results: Dict[str, Any]) -> OutputSection:
        """Create analysis results section."""
        content = "## Analysis Results\n\n"
        
        for source, results in analysis_results.items():
            if isinstance(results, dict) and 'issues' in results:
                content += f"### {source}\n\n"
                
                issues = results['issues']
                if issues:
                    content += f"**Issues Found:** {len(issues)}\n\n"
                    
                    # Group issues by severity
                    severity_groups = {}
                    for issue in issues:
                        severity = getattr(issue, 'severity', 'unknown')
                        if severity not in severity_groups:
                            severity_groups[severity] = []
                        severity_groups[severity].append(issue)
                    
                    for severity, severity_issues in severity_groups.items():
                        content += f"#### {severity.title()} Issues ({len(severity_issues)})\n\n"
                        for issue in severity_issues[:5]:  # Limit to top 5 per severity
                            content += f"- **{getattr(issue, 'type', 'Unknown')}**: {getattr(issue, 'message', 'No message')}"
                            if hasattr(issue, 'line_number') and issue.line_number:
                                content += f" (Line {issue.line_number})"
                            content += "\n"
                        
                        if len(severity_issues) > 5:
                            content += f"  ... and {len(severity_issues) - 5} more\n"
                        content += "\n"
                else:
                    content += "No issues found.\n\n"

                # Add metrics if available
                if 'metrics' in results:
                    metrics = results['metrics']
                    content += "**Metrics:**\n"
                    for key, value in metrics.items():
                        if isinstance(value, (int, float)):
                            content += f"- {key.replace('_', ' ').title()}: {value}\n"
                    content += "\n"

        return OutputSection(
            title="Analysis Results",
            content=content,
            section_type="analysis",
            priority=2,
            interactive=True,
            metadata={
                'total_sources': len(analysis_results),
                'analysis_types': list(analysis_results.keys())
            }
        )

    async def _create_enhancement_section(self, enhancement_results: Dict[str, Any]) -> OutputSection:
        """Create enhancements section."""
        content = "## Enhancements Applied\n\n"
        
        total_enhancements = 0
        enhancement_types = {}
        
        for source, results in enhancement_results.items():
            if isinstance(results, dict) and 'enhancements' in results:
                enhancements = results['enhancements']
                total_enhancements += len(enhancements)
                
                content += f"### {source}\n\n"
                content += f"**Enhancements Applied:** {len(enhancements)}\n\n"
                
                # Group by type
                type_groups = {}
                for enhancement in enhancements:
                    enh_type = getattr(enhancement, 'type', 'unknown')
                    if enh_type not in type_groups:
                        type_groups[enh_type] = []
                    type_groups[enh_type].append(enhancement)
                    
                    # Count for overall stats
                    if enh_type not in enhancement_types:
                        enhancement_types[enh_type] = 0
                    enhancement_types[enh_type] += 1
                
                for enh_type, type_enhancements in type_groups.items():
                    content += f"#### {enh_type.title()} ({len(type_enhancements)})\n\n"
                    for enhancement in type_enhancements[:3]:  # Top 3 per type
                        content += f"- **{getattr(enhancement, 'category', 'General')}**: {getattr(enhancement, 'description', 'No description')}"
                        confidence = getattr(enhancement, 'confidence', 0)
                        content += f" (Confidence: {confidence:.1%})\n"
                    
                    if len(type_enhancements) > 3:
                        content += f"  ... and {len(type_enhancements) - 3} more\n"
                    content += "\n"

        # Overall statistics
        if total_enhancements > 0:
            content += "### Enhancement Statistics\n\n"
            content += f"**Total Enhancements:** {total_enhancements}\n\n"
            for enh_type, count in enhancement_types.items():
                percentage = (count / total_enhancements) * 100
                content += f"- {enh_type.title()}: {count} ({percentage:.1f}%)\n"

        return OutputSection(
            title="Enhancements Applied",
            content=content,
            section_type="enhancements",
            priority=3,
            interactive=True,
            metadata={
                'total_enhancements': total_enhancements,
                'enhancement_types': enhancement_types
            }
        )

    async def _create_ui_mockups_section(self, enhancement_results: Dict[str, Any]) -> Optional[OutputSection]:
        """Create UI mockups section if UI enhancements are present."""
        ui_content = []
        
        for source, results in enhancement_results.items():
            if isinstance(results, dict) and results.get('ui_mockups'):
                ui_mockups = results['ui_mockups']
                ui_content.append(f"### {source}\n\n")
                ui_content.append(f"**Framework:** {ui_mockups.get('framework', 'Unknown')}\n\n")
                
                # Add mockup previews
                if 'previews' in ui_mockups:
                    for preview in ui_mockups['previews']:
                        ui_content.append(f"#### {preview.get('name', 'UI Preview')}\n\n")
                        if preview.get('type') == 'ascii':
                            ui_content.append(f"```\n{preview.get('content', '')}\n```\n\n")
                        elif preview.get('type') == 'html':
                            ui_content.append(f"```html\n{preview.get('content', '')}\n```\n\n")
        
        if ui_content:
            content = "## UI Mockups\n\n" + "".join(ui_content)
            return OutputSection(
                title="UI Mockups",
                content=content,
                section_type="ui_mockups",
                priority=4,
                interactive=True,
                metadata={'has_ui_content': True}
            )
        
        return None

    async def _create_performance_section(self, analysis_results: Dict[str, Any],
                                        enhancement_results: Dict[str, Any]) -> Optional[OutputSection]:
        """Create performance analysis section."""
        performance_data = []
        
        # Collect performance metrics from analysis
        for source, results in analysis_results.items():
            if isinstance(results, dict) and 'metrics' in results:
                metrics = results['metrics']
                perf_metrics = {k: v for k, v in metrics.items() 
                              if 'performance' in k.lower() or 'complexity' in k.lower()}
                if perf_metrics:
                    performance_data.append((source, perf_metrics))
        
        if performance_data:
            content = "## Performance Analysis\n\n"
            
            for source, metrics in performance_data:
                content += f"### {source}\n\n"
                for metric, value in metrics.items():
                    content += f"- **{metric.replace('_', ' ').title()}**: {value}\n"
                content += "\n"
            
            return OutputSection(
                title="Performance Analysis",
                content=content,
                section_type="performance",
                priority=5,
                interactive=True,
                metadata={'performance_sources': len(performance_data)}
            )
        
        return None

    async def _create_security_section(self, analysis_results: Dict[str, Any]) -> Optional[OutputSection]:
        """Create security analysis section."""
        security_issues = []
        
        for source, results in analysis_results.items():
            if isinstance(results, dict) and 'issues' in results:
                issues = results['issues']
                security_issues.extend([
                    issue for issue in issues 
                    if getattr(issue, 'type', '') in ['security', 'compliance']
                ])
        
        if security_issues:
            content = "## Security Analysis\n\n"
            content += f"**Total Security Issues:** {len(security_issues)}\n\n"
            
            # Group by severity
            severity_groups = {}
            for issue in security_issues:
                severity = getattr(issue, 'severity', 'unknown')
                if severity not in severity_groups:
                    severity_groups[severity] = []
                severity_groups[severity].append(issue)
            
            for severity in ['critical', 'high', 'medium', 'low']:
                if severity in severity_groups:
                    issues = severity_groups[severity]
                    content += f"### {severity.title()} ({len(issues)})\n\n"
                    for issue in issues[:3]:  # Top 3 per severity
                        content += f"- {getattr(issue, 'message', 'No message')}\n"
                    if len(issues) > 3:
                        content += f"  ... and {len(issues) - 3} more\n"
                    content += "\n"
            
            return OutputSection(
                title="Security Analysis",
                content=content,
                section_type="security",
                priority=2,
                interactive=True,
                metadata={
                    'total_security_issues': len(security_issues),
                    'severity_breakdown': {k: len(v) for k, v in severity_groups.items()}
                }
            )
        
        return None

    # Export format implementations

    async def _export_markdown(self, output_data: Dict[str, Any], file_path: str):
        """Export to Markdown format."""
        if self.jinja_env:
            template = self.jinja_env.get_template('report.md')
            content = template.render(
                **output_data,
                include_metadata=self.include_metadata
            )
        else:
            # Fallback to simple formatting
            content = f"# {output_data.get('title', 'DuckyCoder Report')}\n\n"
            content += f"Generated: {output_data.get('generation_time', datetime.now())}\n\n"
            
            for section in output_data.get('sections', []):
                content += f"## {section['title']}\n\n"
                content += f"{section['content']}\n\n"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    async def _export_html(self, output_data: Dict[str, Any], file_path: str):
        """Export to HTML format."""
        if self.jinja_env:
            template = self.jinja_env.get_template('report.html')
            content = template.render(
                **output_data,
                include_metadata=self.include_metadata
            )
        else:
            # Fallback HTML
            content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{output_data.get('title', 'DuckyCoder Report')}</title>
    <style>body {{ font-family: Arial, sans-serif; margin: 40px; }}</style>
</head>
<body>
    <h1>{output_data.get('title', 'DuckyCoder Report')}</h1>
    <p>Generated: {output_data.get('generation_time', datetime.now())}</p>
"""
            
            for section in output_data.get('sections', []):
                content += f"<h2>{section['title']}</h2>\n"
                content += f"<div>{section['content']}</div>\n"
            
            content += "</body></html>"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    async def _export_json(self, output_data: Dict[str, Any], file_path: str):
        """Export to JSON format."""
        # Convert datetime objects to strings for JSON serialization
        json_data = self._prepare_json_data(output_data)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

    async def _export_yaml(self, output_data: Dict[str, Any], file_path: str):
        """Export to YAML format."""
        if not HAS_YAML:
            raise ImportError("PyYAML is required for YAML export")
        
        yaml_data = self._prepare_json_data(output_data)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True)

    async def _export_pdf(self, output_data: Dict[str, Any], file_path: str):
        """Export to PDF format."""
        if not HAS_WEASYPRINT:
            raise ImportError("WeasyPrint is required for PDF export")
        
        # First generate HTML
        html_path = file_path.replace('.pdf', '.html')
        await self._export_html(output_data, html_path)
        
        # Convert to PDF
        HTML(filename=html_path).write_pdf(file_path)
        
        # Clean up temporary HTML
        os.remove(html_path)

    async def _export_sarif(self, output_data: Dict[str, Any], file_path: str):
        """Export to SARIF format for CI/CD integration."""
        sarif_data = {
            "version": "2.1.0",
            "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "DuckyCoder v6",
                            "version": output_data.get('version', '6.0.0'),
                            "informationUri": "https://github.com/duckyonquack-999/duckycoder-v6"
                        }
                    },
                    "results": []
                }
            ]
        }
        
        # Convert analysis results to SARIF format
        for section in output_data.get('sections', []):
            if section['section_type'] == 'analysis':
                # Extract issues and convert to SARIF results
                # This is a simplified conversion
                sarif_data["runs"][0]["results"].append({
                    "ruleId": "duckycoder-analysis",
                    "message": {"text": f"Analysis: {section['title']}"},
                    "level": "info",
                    "locations": []
                })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(sarif_data, f, indent=2)

    async def _export_codebase(self, output_data: Dict[str, Any], file_path: str):
        """Export enhanced codebase as ZIP file."""
        with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add the main report
            report_content = json.dumps(output_data, indent=2, default=str)
            zipf.writestr('duckycoder_report.json', report_content)
            
            # Add enhanced code files if available
            for section in output_data.get('sections', []):
                if section['section_type'] == 'enhancements':
                    # Create enhanced versions of files
                    enhanced_file = f"enhanced_{section['title'].lower().replace(' ', '_')}.txt"
                    zipf.writestr(enhanced_file, section['content'])

    async def _export_git_diff(self, output_data: Dict[str, Any], file_path: str):
        """Export as Git diff format."""
        diff_content = "# DuckyCoder v6 Enhanced Changes\n\n"
        
        for section in output_data.get('sections', []):
            if section['section_type'] == 'enhancements':
                diff_content += f"# {section['title']}\n"
                diff_content += f"{section['content']}\n\n"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(diff_content)

    # Helper methods

    def _generate_executive_summary(self, processed_data: Dict[str, Any],
                                  analysis_results: Dict[str, Any],
                                  enhancement_results: Dict[str, Any]) -> str:
        """Generate executive summary."""
        total_files = len(processed_data)
        total_issues = self._count_total_issues(analysis_results)
        total_enhancements = self._count_total_enhancements(enhancement_results)
        
        summary = f"""
This report presents the results of DuckyCoder v6 analysis performed on {total_files} file(s).

**Key Metrics:**
- Files analyzed: {total_files}
- Issues identified: {total_issues}
- Enhancements applied: {total_enhancements}

**Overall Status:** {"✅ Good" if total_issues < 10 else "⚠️ Needs Attention" if total_issues < 50 else "❌ Critical"}
"""
        return summary.strip()

    def _generate_key_findings(self, analysis_results: Dict[str, Any]) -> str:
        """Generate key findings summary."""
        findings = []
        
        for source, results in analysis_results.items():
            if isinstance(results, dict) and 'issues' in results:
                issues = results['issues']
                critical_issues = [i for i in issues if getattr(i, 'severity', '') == 'critical']
                if critical_issues:
                    findings.append(f"Critical issues found in {source}")
        
        if not findings:
            findings.append("No critical issues identified")
        
        return "- " + "\n- ".join(findings)

    def _generate_improvements_summary(self, enhancement_results: Dict[str, Any]) -> str:
        """Generate improvements summary."""
        improvements = []
        
        for source, results in enhancement_results.items():
            if isinstance(results, dict) and 'enhancements' in results:
                enhancements = results['enhancements']
                if enhancements:
                    improvements.append(f"{len(enhancements)} enhancements applied to {source}")
        
        if not improvements:
            improvements.append("No enhancements were necessary")
        
        return "- " + "\n- ".join(improvements)

    def _generate_risk_assessment(self, analysis_results: Dict[str, Any]) -> str:
        """Generate risk assessment."""
        total_issues = self._count_total_issues(analysis_results)
        
        if total_issues == 0:
            return "**Risk Level: LOW** - No issues identified"
        elif total_issues < 10:
            return "**Risk Level: LOW** - Minor issues that should be addressed"
        elif total_issues < 50:
            return "**Risk Level: MEDIUM** - Several issues requiring attention"
        else:
            return "**Risk Level: HIGH** - Many issues requiring immediate attention"

    def _count_total_issues(self, analysis_results: Dict[str, Any]) -> int:
        """Count total issues across all analysis results."""
        total = 0
        for results in analysis_results.values():
            if isinstance(results, dict) and 'issues' in results:
                total += len(results['issues'])
        return total

    def _count_total_enhancements(self, enhancement_results: Dict[str, Any]) -> int:
        """Count total enhancements across all results."""
        total = 0
        for results in enhancement_results.values():
            if isinstance(results, dict) and 'enhancements' in results:
                total += len(results['enhancements'])
        return total

    def _calculate_overall_confidence(self, results: Dict[str, Any]) -> float:
        """Calculate overall confidence score."""
        confidences = []
        for result in results.values():
            if isinstance(result, dict) and 'confidence' in result:
                confidences.append(result['confidence'])
        
        return sum(confidences) / len(confidences) if confidences else 0.0

    def _extract_languages(self, processed_data: Dict[str, Any]) -> List[str]:
        """Extract detected languages."""
        languages = set()
        for data in processed_data.values():
            if isinstance(data, dict) and 'metadata' in data:
                lang = data['metadata'].get('language')
                if lang:
                    languages.add(lang)
        return list(languages)

    def _extract_frameworks(self, processed_data: Dict[str, Any]) -> List[str]:
        """Extract detected frameworks."""
        frameworks = set()
        for data in processed_data.values():
            if isinstance(data, dict) and 'metadata' in data:
                framework = data['metadata'].get('framework')
                if framework:
                    frameworks.add(framework)
        return list(frameworks)

    def _prepare_json_data(self, data: Any) -> Any:
        """Prepare data for JSON serialization."""
        if isinstance(data, datetime):
            return data.isoformat()
        elif isinstance(data, dict):
            return {k: self._prepare_json_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._prepare_json_data(item) for item in data]
        else:
            return data