import sys
from pathlib import Path

def split_credentials_by_provider(input_file):
    """Split credentials file by email provider"""
    
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
        
        gmail_accounts = []
        outlook_accounts = []
        yahoo_accounts = []
        other_accounts = []
        invalid_lines = []
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check if valid format
            if ':' not in line:
                invalid_lines.append((i, line))
                continue
            
            email, password = line.split(':', 1)
            email = email.strip().lower()
            
            # Check if valid email
            if '@' not in email:
                invalid_lines.append((i, line))
                continue
            
            domain = email.split('@')[1]
            
            # Categorize by provider
            if 'gmail.com' in domain:
                gmail_accounts.append(line)
            elif 'hotmail.com' in domain or 'outlook.com' in domain or 'live.com' in domain:
                outlook_accounts.append(line)
            elif 'yahoo.com' in domain or 'ymail.com' in domain:
                yahoo_accounts.append(line)
            else:
                other_accounts.append(line)
        
        # Create output files
        base_name = Path(input_file).stem
        
        if gmail_accounts:
            gmail_file = f"{base_name}_gmail.txt"
            with open(gmail_file, 'w') as f:
                f.write('\n'.join(gmail_accounts))
            print(f"✓ Created: {gmail_file} ({len(gmail_accounts)} accounts)")
        
        if outlook_accounts:
            outlook_file = f"{base_name}_outlook.txt"
            with open(outlook_file, 'w') as f:
                f.write('\n'.join(outlook_accounts))
            print(f"✓ Created: {outlook_file} ({len(outlook_accounts)} accounts)")
        
        if yahoo_accounts:
            yahoo_file = f"{base_name}_yahoo.txt"
            with open(yahoo_file, 'w') as f:
                f.write('\n'.join(yahoo_accounts))
            print(f"✓ Created: {yahoo_file} ({len(yahoo_accounts)} accounts)")
        
        if other_accounts:
            other_file = f"{base_name}_other.txt"
            with open(other_file, 'w') as f:
                f.write('\n'.join(other_accounts))
            print(f"✓ Created: {other_file} ({len(other_accounts)} accounts)")
        
        # Summary
        print(f"\n{'='*50}")
        print(f"SUMMARY")
        print(f"{'='*50}")
        print(f"Total lines processed: {len(lines)}")
        print(f"Gmail accounts: {len(gmail_accounts)}")
        print(f"Outlook accounts: {len(outlook_accounts)}")
        print(f"Yahoo accounts: {len(yahoo_accounts)}")
        print(f"Other domains: {len(other_accounts)}")
        print(f"Invalid lines: {len(invalid_lines)}")
        
        if invalid_lines:
            print(f"\n⚠ Invalid lines (skipped):")
            for line_num, content in invalid_lines[:5]:
                print(f"  Line {line_num}: {content}")
            if len(invalid_lines) > 5:
                print(f"  ... and {len(invalid_lines) - 5} more")
        
        print(f"\n✓ Done! Files created successfully.\n")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_credentials.py <credentials_file>")
        print("\nExample:")
        print("  python split_credentials.py credentials.txt")
        print("\nThis will create:")
        print("  - credentials_gmail.txt")
        print("  - credentials_outlook.txt")
        print("  - credentials_yahoo.txt")
        print("  - credentials_other.txt (if any)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    split_credentials_by_provider(input_file)
