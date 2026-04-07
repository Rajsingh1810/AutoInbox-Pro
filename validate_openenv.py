"""
OpenEnv Validation Script
Validates that all required components are present and working
"""

import os
import sys

def validate_openenv():
    """Validate OpenEnv requirements"""
    print("\n" + "="*60)
    print("OpenEnv Validation")
    print("="*60 + "\n")
    
    checks_passed = 0
    checks_failed = 0
    
    # Check 1: Dockerfile exists
    print("✓ Checking Dockerfile...")
    if os.path.exists("Dockerfile"):
        print("  ✅ Dockerfile found at repo root")
        checks_passed += 1
    else:
        print("  ❌ Dockerfile not found")
        checks_failed += 1
    
    # Check 2: inference.py exists
    print("\n✓ Checking inference.py...")
    if os.path.exists("inference.py"):
        print("  ✅ inference.py found at repo root")
        checks_passed += 1
    else:
        print("  ❌ inference.py not found")
        checks_failed += 1
    
    # Check 3: inference.py has required functions
    print("\n✓ Checking inference.py functions...")
    try:
        from inference import handler, reset, health_check
        print("  ✅ handler() function found")
        print("  ✅ reset() function found")
        print("  ✅ health_check() function found")
        checks_passed += 1
    except ImportError as e:
        print(f"  ❌ Missing required functions: {e}")
        checks_failed += 1
    
    # Check 4: app.py exists
    print("\n✓ Checking app.py...")
    if os.path.exists("app.py"):
        print("  ✅ app.py found")
        checks_passed += 1
    else:
        print("  ❌ app.py not found")
        checks_failed += 1
    
    # Check 5: email_env.py exists
    print("\n✓ Checking email_env.py...")
    if os.path.exists("email_env.py"):
        print("  ✅ email_env.py found")
        checks_passed += 1
    else:
        print("  ❌ email_env.py not found")
        checks_failed += 1
    
    # Check 6: requirements.txt exists
    print("\n✓ Checking requirements.txt...")
    if os.path.exists("requirements.txt"):
        print("  ✅ requirements.txt found")
        checks_passed += 1
    else:
        print("  ❌ requirements.txt not found")
        checks_failed += 1
    
    # Check 7: Test inference
    print("\n✓ Testing inference engine...")
    try:
        from inference import SmartInboxInference
        engine = SmartInboxInference()
        result = engine.predict("Win money now!!!", "easy")
        if "action" in result:
            print(f"  ✅ Inference working - Action: {result['action']}")
            checks_passed += 1
        else:
            print(f"  ❌ Inference failed: {result}")
            checks_failed += 1
    except Exception as e:
        print(f"  ❌ Inference test failed: {e}")
        checks_failed += 1
    
    # Summary
    print("\n" + "="*60)
    print(f"Validation Results: {checks_passed} passed, {checks_failed} failed")
    print("="*60 + "\n")
    
    if checks_failed == 0:
        print("✅ All OpenEnv checks passed!")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(validate_openenv())
