"""
Main application file for StarBot
"""
import os
import sys
from starbot.ui.cli import StarBotCLI

def main():
    """
    Main entry point for the application
    """
    cli = StarBotCLI()
    cli.run()

if __name__ == "__main__":
    main()
