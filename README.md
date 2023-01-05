# Simple instruction

If you have a significant collection of text files then this is sufficient:

1. create a directory e.g. data-local-law and place the files there,
2. create a file data-local-law.json and put the most important information there ie:

        {
            "project": "SpeakLeash",
            "name": "local_law",
            "description": "Polish local laws e.g. statutes and regulations of schools, local authorities",
            "license": "",
            "language": "pl",
            "sources": [
                {
                    "name": "local_law",
                    "url": "",
                    "license": ""
                }
            ]
        }

Run main.py and you're done ;-) ***Not tested on huge data sets! Feel free to change and test***