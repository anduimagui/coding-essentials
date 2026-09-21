#!/bin/bash

# Domain Finder - Check domain availability
# Usage: ./domain_finder.sh <domain_name> [tld1,tld2,...]

set -e

DOMAIN_NAME="$1"
CUSTOM_TLDS="$2"

if [ -z "$DOMAIN_NAME" ]; then
    echo "Usage: $0 <domain_name> [tld1,tld2,...]"
    echo "Example: $0 example"
    echo "Example: $0 example com,net,org"
    exit 1
fi

# Most common TLDs (ordered by popularity)
DEFAULT_TLDS="com,net,org,info,biz,co,io,me,tv,cc,us,uk,de,fr,ca,au,jp,in,cn,br"

# Use custom TLDs if provided, otherwise use defaults
if [ -n "$CUSTOM_TLDS" ]; then
    TLDS="$CUSTOM_TLDS"
else
    TLDS="$DEFAULT_TLDS"
fi

echo "Checking domain availability for: $DOMAIN_NAME"
echo "TLDs to check: $TLDS"
echo "----------------------------------------"

# Convert comma-separated TLDs to array
IFS=',' read -ra TLD_ARRAY <<< "$TLDS"

AVAILABLE_DOMAINS=()
UNAVAILABLE_DOMAINS=()

for tld in "${TLD_ARRAY[@]}"; do
    # Remove any whitespace
    tld=$(echo "$tld" | xargs)
    domain="$DOMAIN_NAME.$tld"
    
    echo -n "Checking $domain... "
    
    # Use nslookup to check if domain resolves (simpler approach)
    if nslookup "$domain" >/dev/null 2>&1; then
        echo "TAKEN ✗"
        UNAVAILABLE_DOMAINS+=("$domain")
    else
        # Try whois as backup
        whois_result=$(whois "$domain" 2>/dev/null)
        
        if echo "$whois_result" | grep -qi "no match\|not found\|no entries found\|status: available\|no data found\|not registered"; then
            echo "AVAILABLE ✓"
            AVAILABLE_DOMAINS+=("$domain")
        elif echo "$whois_result" | grep -qi "creation date\|created\|registered\|status: active\|domain status"; then
            echo "TAKEN ✗"
            UNAVAILABLE_DOMAINS+=("$domain")
        else
            echo "UNKNOWN ?"
        fi
    fi
    
    # Small delay to avoid rate limiting
    sleep 0.5
done

echo "----------------------------------------"
echo "SUMMARY:"
echo ""

if [ ${#AVAILABLE_DOMAINS[@]} -gt 0 ]; then
    echo "AVAILABLE DOMAINS (${#AVAILABLE_DOMAINS[@]}):"
    for domain in "${AVAILABLE_DOMAINS[@]}"; do
        echo "  ✓ $domain"
    done
    echo ""
fi

if [ ${#UNAVAILABLE_DOMAINS[@]} -gt 0 ]; then
    echo "TAKEN DOMAINS (${#UNAVAILABLE_DOMAINS[@]}):"
    for domain in "${UNAVAILABLE_DOMAINS[@]}"; do
        echo "  ✗ $domain"
    done
fi

echo ""
echo "Note: Results may vary. Always verify through official registrar before purchasing."