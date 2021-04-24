import unittest
import tempfile

class TestTippy(unittest.TestCase):
    def setUp(self):
        self.config = {
            "count": 1,
            "db_files": [
                "test_tips.json"
            ],
            "tags": [
                "linux"
            ]
        }
    
    def tearDown(self):
        return super().tearDown()

    def test_get_tips_by_tags(self):
        test_data =  {
            "tips" : [
                {
                    "description": "Download compressed data and uncompress with CURL",
                    "tags": [
                        "linux",
                        "commands",
                        "curl"
                    ],
                    "enabled": True,
                    "contents" : [
                        "Add `--compressed` option to curl to auto decompress data after download.",
                        "e.g. curl --compressed https://api.stackexchange.com/2.2/sites"
                    ]
                }
            ]
        }

        # import main
        # write the test_data into a temp file
        # update config["db_files"] = temp file 
        # flush the temp file

        # set the wanted tags in config["tags"]
        # call get_tips(config)
        # should get a tip for the set tag
        
        # change wanted tags to something different
        # should not get any more tip for the missing tag


    def test_get_tips_no_tags(self):
        pass

    def test_disabled_tips_not_shown(self):
        # Generate test data with tags disabled
        # verify disabled tips are not shown
        pass
