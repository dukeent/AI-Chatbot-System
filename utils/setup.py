#!/usr/bin/env python3
"""
Quick start script for the chatbot system.
Sets up environment and runs tests.
"""
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_env_file():
    """Check if .env file exists."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("⚠️  .env file not found")
            print("   Creating from .env.example...")
            env_file.write_text(env_example.read_text())
            print("✅ Created .env file")
            print("\n⚠️  IMPORTANT: Please edit .env and add your OPENAI_API_KEY")
            return False
        else:
            print("❌ Neither .env nor .env.example found")
            return False
    else:
        # Check if API key is set
        content = env_file.read_text()
        if "your_openai_api_key_here" in content or not "OPENAI_API_KEY=" in content:
            print("⚠️  OPENAI_API_KEY not configured in .env file")
            print("   Please edit .env and add your OpenAI API key")
            return False
        print("✅ .env file configured")
    return True


def install_dependencies():
    """Install required Python packages."""
    print("\n📦 Installing dependencies...")
    print("   This may take a few minutes...\n")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        print("\n✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to install dependencies: {e}")
        return False


def run_component_tests():
    """Run tests for individual components."""
    print("\n" + "="*70)
    print("🧪 RUNNING COMPONENT TESTS")
    print("="*70)
    
    components = [
        ("Knowledge Base", "src/knowledge_base.py"),
        ("Response Generator", "src/response_generator.py"),
        ("TTS Service", "src/tts_service.py")
    ]
    
    all_passed = True
    
    for name, script in components:
        print(f"\n{'='*70}")
        print(f"Testing {name}...")
        print('='*70)
        
        try:
            result = subprocess.run(
                [sys.executable, script],
                capture_output=False,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print(f"\n✅ {name} test PASSED")
            else:
                print(f"\n❌ {name} test FAILED")
                all_passed = False
                
        except subprocess.TimeoutExpired:
            print(f"\n⚠️  {name} test timed out")
            all_passed = False
        except Exception as e:
            print(f"\n❌ {name} test error: {e}")
            all_passed = False
    
    return all_passed


def main():
    """Main setup and test workflow."""
    print("\n" + "="*70)
    print("🚀 CHATBOT SYSTEM - QUICK START")
    print("="*70 + "\n")
    
    # Step 1: Check Python version
    print("Step 1: Checking Python version...")
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Check environment file
    print("\nStep 2: Checking environment configuration...")
    env_configured = check_env_file()
    
    # Step 3: Install dependencies
    print("\nStep 3: Installing dependencies...")
    if not install_dependencies():
        sys.exit(1)
    
    # Step 4: Run tests (only if env is configured)
    if env_configured:
        print("\nStep 4: Running component tests...")
        choice = input("\nRun component tests? (y/n): ").strip().lower()
        
        if choice == 'y':
            tests_passed = run_component_tests()
            
            if tests_passed:
                print("\n" + "="*70)
                print("✅ ALL TESTS PASSED!")
                print("="*70)
            else:
                print("\n" + "="*70)
                print("⚠️  SOME TESTS FAILED")
                print("="*70)
    else:
        print("\n⚠️  Skipping tests - please configure .env first")
    
    # Final instructions
    print("\n" + "="*70)
    print("📚 SETUP COMPLETE!")
    print("="*70)
    
    if env_configured:
        print("\n✅ Your chatbot is ready to use!")
        print("\nTo start the chatbot:")
        print("  python run_chatbot.py")
        print("\nTo start without TTS:")
        print("  python run_chatbot.py --no-tts")
    else:
        print("\n⚠️  Next steps:")
        print("1. Edit .env file and add your OPENAI_API_KEY")
        print("2. Run: python run_chatbot.py")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
