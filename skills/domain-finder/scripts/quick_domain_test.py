#!/usr/bin/env python3
"""
Quick test of domain finder using DNS checks only
"""

import socket
import random
import string


def check_domain_dns(domain: str) -> bool:
    """Quick DNS check to see if domain exists"""
    try:
        socket.gethostbyname(domain)
        return False  # Domain exists
    except socket.gaierror:
        return True  # Domain might be available


def generate_5_char_domains(count: int = 10) -> list:
    """Generate random 5 character domain names"""
    domains = []
    chars = string.ascii_lowercase
    
    for _ in range(count):
        domain = ''.join(random.choices(chars, k=5))
        domains.append(domain)
        
    return domains


def main():
    print("Quick Domain Availability Test (DNS Check Only)")
    print("=" * 50)
    
    # Test with some 5-character domains
    test_domains = [
        'xyzab', 'qwert', 'abcxy', 'mnbvc', 'zxcvb',
        'apple', 'googl', 'micro', 'amazn', 'faceb'  # Known taken domains
    ]
    
    # Add some random ones
    random_domains = generate_5_char_domains(5)
    test_domains.extend(random_domains)
    
    print(f"\nChecking {len(test_domains)} domains...")
    print("-" * 50)
    
    available = []
    taken = []
    
    for domain in test_domains:
        full_domain = f"{domain}.com"
        is_available = check_domain_dns(full_domain)
        
        if is_available:
            available.append(full_domain)
            status = "✓ Possibly available"
        else:
            taken.append(full_domain)
            status = "✗ Taken"
            
        print(f"{full_domain:15} {status}")
    
    print("\n" + "=" * 50)
    print(f"Summary: {len(available)} possibly available, {len(taken)} taken")
    
    if available:
        print("\nPossibly available domains:")
        for domain in available:
            print(f"  - {domain}")
        print("\nNote: DNS check only provides a quick indication.")
        print("Use WHOIS for more accurate availability information.")


if __name__ == "__main__":
    main()