#!/usr/bin/env python3

import subprocess
import tempfile
import unittest

class LLDBTestCase(unittest.TestCase):
    '''
    This method should be overriden by the child class
    '''
    def get_formatter_path():
        return None

    def create_lldb_script_file(
        self, script_file, lldb_out_file, lldb_script: str
    ) -> None:
        """
        Sets up a script file that will be read by lldb. It will also set up
        lldb to print the script output to a file that can be read later
        """
        
        formatter_path = self.get_formatter_path()
        script_contents = (
            f"""
script f = open("{lldb_out_file.name}","w")
script lldb.debugger.SetOutputFileHandle(f, True)
command script import {formatter_path}
"""
            + lldb_script
        )
        script_file.write(bytes(script_contents, "utf-8"))
        script_file.flush()

    def read_lldb_out_file(self, lldb_out_file) -> str:
        lldb_out_file.seek(0)
        return "\n".join(
            map(lambda s: s.decode("utf-8").strip(), lldb_out_file.readlines())
        )

    def run_lldb(self, target: str, lldb_script: str) -> str:
        """
        Run lldb to debug a given fbcode target and runs a script.
        The binary target must be included as a resource of the test target.
        This returns the output of the lldb script.
        """

        with tempfile.NamedTemporaryFile() as lldb_out_file:
            with tempfile.NamedTemporaryFile() as script_file:
                self.create_lldb_script_file(script_file, lldb_out_file, lldb_script)

                self.assertEqual(
                    subprocess.run(
                        [
                            "lldb",
                            "../out/bin/" + target,
                            "--batch",
                            "-s",
                            script_file.name,
                        ]
                    ).returncode,
                    0,
                )
            return self.read_lldb_out_file(lldb_out_file)
