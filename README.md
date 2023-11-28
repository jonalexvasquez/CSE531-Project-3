This application runs on Python and specifically on Python >=3.7.7. To install Python please follow directions here if 
needed: https://wiki.python.org/moin/BeginnersGuide/Download.

Once python is installed and this repository is pulled follow these steps:

1.) Go to the root of the project and install venv: `python -m venv venv  `

2.) Activate the virtual environment: `source venv/bin/activate`

3.) Install the requirements (gcp libraries): `pip install -r requirements.txt`

4.) Now, in your terminal open up two consoles/sessions of your terminal. First run the server by running: 
`python branch_server.py`. You should see logs stating that certain processes were started.

5.) Now, in your other terminal session run the client: `python client.py`. When the scripts finish processing you will
see two output files populated with the expected output: 1.) `monotonic_writes_output.json` will have the output that the 
monotonic writes input produces. 2.) `read_your_writes.json` will have the output that the read your writes input
produces. 
