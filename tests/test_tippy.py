import json
import tempfile
import os
import unittest

# This is ugly. Any alternative not to change the paths,
# but still use the dev version instead of the installed
# version?
os.chdir(os.path.join(os.path.dirname(__file__), "../src/"))
os.sys.path.insert(0, os.getcwd())

from tippy import tippy

class TestTippy(unittest.TestCase):
    def setUp(self):
        self.test_data =  {
            "tips" : [
                {
                    "description": "tip1",
                    "tags": [
                        "linux",
                        "commands",
                        "curl"
                    ],
                    "enabled": True,
                    "contents" : [
                        "test tip by tags"
                    ]
                }
            ]
        }
    
    def tearDown(self):
        return super().tearDown()

    def test_get_tips_by_tags(self):
        test_config = {
            "count": 1,
            "tags": [
                "linux"
            ]
        }

        with tempfile.NamedTemporaryFile("w+") as test_data_file:
            # Write the test tips into a file
            json.dump(self.test_data, test_data_file)
            test_data_file.flush()
            
            test_config["data_files"] = [test_data_file.name]

            tips = tippy.get_tips(test_config)
            self.assertIsNotNone(tips)
            self.assertEqual(len(tips), test_config["count"], "Expected tip is missing")

            # Add additional tags to test config.
            # number of tips returned should still be same as config count.
            test_config["tags"].append("commands")
            tips = tippy.get_tips(test_config)
            self.assertEqual(len(tips), test_config["count"], "Mismatch in tip count")

            test_config["tags"].clear()
            tips = tippy.get_tips(test_config)
            self.assertEqual(len(tips), test_config["count"], "No tip returned when tags are empty")

            test_config["tags"] = ["dont_show_this_tag"]
            tips = tippy.get_tips(test_config)
            self.assertEqual(len(tips), 0, "expected: no tip. actual: {}".format(tips))
    
    def test_get_tips_multiple(self):
        self.test_data["tips"].append({
            "description": "tip2",
            "tags": [
                "vscode",
            ],
            "enabled": True,
            "contents" : [
                "test tip2"
            ]
        })

        self.test_data["tips"].append({
            "description": "tip3",
            "tags": [
                "grep",
            ],
            "enabled": True,
            "contents" : [
                "test tip3"
            ]
        })

        test_config = {
            "count": 2,
            "tags": [],
        }

        with tempfile.NamedTemporaryFile("w+") as tfp:
            json.dump(self.test_data, tfp)
            tfp.flush()

            test_config["data_files"] = [tfp.name]

            tips = tippy.get_tips(test_config)
            self.assertEqual(len(tips), test_config["count"], "expected {} tips".format(test_config["count"]))

    def test_disabled_tips_not_shown(self):
        self.test_data["tips"][0]["enabled"] = False
        with tempfile.NamedTemporaryFile("w+") as tfp:
            json.dump(self.test_data, tfp)
            tfp.flush()

            test_config = {
                "count": 1,
                "data_files": [
                    tfp.name
                ],
                "tags": [
                    "linux"
                ]
            }
            tips = tippy.get_tips(test_config)
            self.assertListEqual(tips, [], "expected: [], actual:{}".format(tips))
    
    def test_get_tags_in_mixed_case(self):
        self.test_data["tips"].append({
            "description": "tip-with-case-sensitive-tags",
            "tags": [
                "Grep",
            ],
            "enabled": True,
            "contents" : [
                "test case sensitive tip"
            ]
        })

        
        with tempfile.NamedTemporaryFile("w+") as tfp:
            json.dump(self.test_data, tfp)
            tfp.flush()

            test_config = {
                "count": 1,
                "data_files": [
                    tfp.name
                ],
                "tags": [
                    "grep"
                ]
            }
            tips = tippy.get_tips(test_config)
            self.assertEqual(len(tips), test_config["count"])
            self.assertListEqual(tips[0]["tags"], self.test_data["tips"][1]["tags"])
    
    def test_get_tags_without_enabled_flag(self):
        self.test_data["tips"].append({
            "description": "tip-without-enabled-flag",
            "tags": [
                "test",
            ],
            "contents" : [
                "contents of tip without enabled flag"
            ]
        })

        test_config = {
            "count": 1,
            "tags": [
                "test"
            ]
        }

        with tempfile.NamedTemporaryFile("w+") as tfp:
            json.dump(self.test_data, tfp)
            tfp.flush()

            test_config["data_files"] = [
                tfp.name
            ]

            tips = tippy.get_tips(test_config)
            self.assertEqual(len(tips), test_config["count"])
            self.assertEqual(tips[0]["description"], self.test_data["tips"][-1]["description"])

    def test_get_config_valid(self):
        test_config = {
            "count": 1,
            "data_files": [
                "test.json"
            ],
            "tags": [
                "linux"
            ]
        }
        with tempfile.NamedTemporaryFile("w+") as tfp:
            json.dump(test_config, tfp)
            tfp.flush()
            self.assertEqual(test_config, tippy.get_config(tfp.name))
    
    def test_get_config_raises_error_on_invalid_config(self):
        test_config = {}
        with tempfile.NamedTemporaryFile("w+") as tfp:
            with self.assertRaises(ValueError):
                tippy.get_config(tfp.name)
                test_config = {
                    "count" : 1
                }
                json.dump(test_config, tfp)
                tfp.flush()