#!/usr/bin/env python3
"""
Validate optimized emoji names for accuracy and completeness.
Generates a validation report for human review.
"""

import json
import re

def validate_names(optimized_names, category):
    """Validate optimized names and generate report."""
    issues = []
    warnings = []

    for codepoint, name_data in optimized_names.items():
        en_name = name_data.get('en', '')
        zh_name = name_data.get('zh', '')

        # Check if English name is empty
        if not en_name:
            issues.append(f"{codepoint}: Empty English name")

        # Check if Chinese name is empty (for non-Component categories)
        if category != 'Component' and not zh_name:
            warnings.append(f"{codepoint}: Empty Chinese name")

        # Check if English name contains the codepoint (for flags)
        if category == 'Flags' and codepoint in en_name:
            # This is expected for flags
            pass

        # Check for common issues
        if len(en_name) > 100:
            warnings.append(f"{codepoint}: English name too long ({len(en_name)} chars)")

        if len(zh_name) > 50:
            warnings.append(f"{codepoint}: Chinese name too long ({len(zh_name)} chars)")

    return issues, warnings

def main():
    # File paths
    input_file = 'optimized_names_flags.json'
    report_file = 'validation_report_flags.txt'

    # Load optimized names
    print(f"Loading optimized names from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        optimized_names = json.load(f)

    print(f"Loaded {len(optimized_names)} optimized names")

    # Validate names
    print("Validating names...")
    issues, warnings = validate_names(optimized_names, 'Flags')

    # Generate report
    report_lines = [
        f"Validation Report for Flags Category",
        f"Generated: {len(optimized_names)} names",
        f"",
        f"Issues ({len(issues)}):",
    ]

    if issues:
        for issue in issues:
            report_lines.append(f"  - {issue}")
    else:
        report_lines.append("  No issues found")

    report_lines.extend([
        f"",
        f"Warnings ({len(warnings)}):",
    ])

    if warnings:
        for warning in warnings:
            report_lines.append(f"  - {warning}")
    else:
        report_lines.append("  No warnings")

    # Add sample names for review
    report_lines.extend([
        f"",
        f"Sample Names for Review:",
    ])

    for codepoint, name_data in list(optimized_names.items())[:5]:
        report_lines.append(f"  {codepoint}:")
        report_lines.append(f"    English: {name_data['en']}")
        report_lines.append(f"    Chinese: {name_data['zh']}")

    # Write report
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

    print(f"Validation complete:")
    print(f"  Issues: {len(issues)}")
    print(f"  Warnings: {len(warnings)}")
    print(f"  Report saved to {report_file}")

    # Print summary to console
    if issues:
        print("\nIssues found:")
        for issue in issues[:5]:  # Show first 5
            print(f"  - {issue}")
        if len(issues) > 5:
            print(f"  ... and {len(issues) - 5} more")

    if warnings:
        print("\nWarnings found:")
        for warning in warnings[:5]:  # Show first 5
            print(f"  - {warning}")
        if len(warnings) > 5:
            print(f"  ... and {len(warnings) - 5} more")

if __name__ == '__main__':
    main()
