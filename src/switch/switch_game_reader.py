#!/usr/bin/env python3
"""
NSP Title ID Extractor - Optimized Version
Leverages hactool to extract only the title ID from NSP files as efficiently as possible
"""

import sys
import subprocess
import tempfile
import shutil
import re
from pathlib import Path

class NSPTitleIDExtractor:
    """Extract only title ID from NSP files using external tools"""
    
    def __init__(self, nsp_path, hactool_path=None, keys_path=None):
        """Initialize with paths to NSP file and necessary tools"""
        self.nsp_path = Path(nsp_path)
        
        # Set paths with better handling
        self.hactool_path = Path(hactool_path) if hactool_path else Path("hactool.exe")
        self.keys_path = Path(keys_path) if keys_path else Path("prod.keys")
        
        # Check if NSP file exists
        if not self.nsp_path.exists():
            raise FileNotFoundError(f"NSP file not found: {nsp_path}")
        
        # Create temp directory for extraction
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def __del__(self):
        """Clean up temporary files"""
        if hasattr(self, 'temp_dir') and self.temp_dir.exists():
            try:
                shutil.rmtree(self.temp_dir)
            except:
                print(f"Warning: Could not clean up temp directory {self.temp_dir}")
    
    def check_tools(self):
        """Check if required tools are available"""
        # Check if hactool exists as a file
        if not self.hactool_path.exists():
            return False
                
        # Check for keys file
        if not self.keys_path.exists():
            return False
                
        return True
    
    def extract_title_id(self):
        """Extract only the title ID using the most efficient methods"""
        if not self.check_tools():
            return "Unknown Title ID"
            
        title_id = "Unknown Title ID"
        is_windows = sys.platform.startswith('win')
        
        try:
            # Strategy 1: Extract NSP and look for XML file first (fastest)
            extract_cmd = [
                str(self.hactool_path),
                "-t", "pfs0", 
                "--pfs0dir", str(self.temp_dir),
                "-k", str(self.keys_path),
                str(self.nsp_path)
            ]
            
            subprocess.run(
                extract_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
                shell=is_windows
            )
            
            # Check for XML files first - fastest method
            for xml_file in self.temp_dir.glob("*.cnmt.xml"):
                with open(xml_file, 'r', encoding='utf-8') as f:
                    xml_content = f.read()
                    tid_match = re.search(r'<titleid>([0-9a-fA-F]{16})</titleid>', xml_content)
                    if tid_match:
                        return tid_match.group(1).upper()
            
            # Strategy 2: Check CNMT NCA files
            for cnmt_nca in self.temp_dir.glob("*.cnmt.nca"):
                # Extract CNMT info using hactool
                cnmt_cmd = [
                    str(self.hactool_path),
                    "-t", "nca", 
                    "--titlekey=0000000000000000000000000000000000000000000000000000000000000000",
                    "-k", str(self.keys_path),
                    "--section0dir", str(self.temp_dir / "cnmt_section"),
                    str(cnmt_nca)
                ]
                
                subprocess.run(
                    cnmt_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False,
                    shell=is_windows
                )
                
                # Look for CNMT in the extracted section
                for cnmt_file in (self.temp_dir / "cnmt_section").glob("*.cnmt") if (self.temp_dir / "cnmt_section").exists() else []:
                    cnmt_info_cmd = [
                        str(self.hactool_path),
                        "-t", "cnmt", 
                        str(cnmt_file)
                    ]
                    
                    cnmt_result = subprocess.run(
                        cnmt_info_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        check=False,
                        shell=is_windows
                    )
                    
                    if cnmt_result.returncode == 0:
                        cnmt_info = cnmt_result.stdout
                        tid_match = re.search(r'Title ID:\s+([0-9a-fA-F]{16})', cnmt_info)
                        if tid_match:
                            return tid_match.group(1).upper()
                
                break  # Only process first CNMT NCA
            
            # Strategy 3: Look for title ID patterns in filenames (fallback)
            for file in self.temp_dir.glob("*"):
                # Title IDs are typically 16 hex digits starting with 01 for base games
                tid_pattern = re.compile(r'0[0-9][0-9a-fA-F]{14}')
                tid_match = tid_pattern.search(file.name)
                if tid_match:
                    return tid_match.group(0).upper()
            
            return title_id
            
        except Exception as e:
            return "Unknown Title ID"


def getTitleID(nsp_path, hactool_path = 'hactool.exe', keys_path = 'prod.keys'):
    """Main function"""   
    try:
        extractor = NSPTitleIDExtractor(nsp_path, hactool_path, keys_path)
        title_id = extractor.extract_title_id()

        return title_id
            
    except Exception as e:
        print("Unknown Title ID")