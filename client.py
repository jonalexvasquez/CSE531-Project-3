import json
import subprocess
import time

import grpc
from google.protobuf.json_format import MessageToDict

import branch_pb2_grpc
from branch_pb2 import MsgDeliveryRequest, RequestElement


class Customer:
    def __init__(self, id, events):
        self.id = id
        self.events = events
        self.recvMsg = list()
        self.stub = None

    def createStub(self, destination_id: int):
        # Channel connections are in the 5xxx range so this finds the correct mapping
        # between customer and branch.
        print("Creating stub for dest id:{}".format(destination_id))
        channel = 5000 + destination_id
        channel_name = "localhost:" + str(channel)
        channel = grpc.insecure_channel(channel_name)
        stub = branch_pb2_grpc.BranchStub(channel)
        return stub

    def executeEvents(self):
        for event in self.events:
            request_data = []
            stub = self.createStub(event["dest"])
            request_data.append(
                RequestElement(
                    id=event["id"],
                    interface=event["interface"],
                    money=event.get("money"),
                ),
            )
            request = MsgDeliveryRequest(request_elements=request_data)
            response = stub.MsgDelivery(request)
            self.recvMsg.append(response)


    def __repr__(self):
        return "Customer:{}".format(self.id)


if __name__ == "__main__":

    # Monotonic writes
    f = open("monotonic_writes_input.json")
    customer_processes_request = json.load(f)

    customer_response = []
    for customer_processes_request in customer_processes_request:
        if customer_processes_request["type"] == "customer":
            customer = Customer(
                id=customer_processes_request["id"],
                events=customer_processes_request["events"],
            )
            customer.executeEvents()

            for customer_response_message in customer.recvMsg:
                customer_response_dict = MessageToDict(customer_response_message, including_default_value_fields=True)
                if customer_response_dict["recv"][0]["interface"] == "query":
                    output_response = {
                        "id": customer.id,
                        "balance":customer_response_dict["recv"][0]["result"]["balance"]
                    }
                    json_file_path = "monotonic_writes_output.json"
                    with open(json_file_path, 'a') as monotonic_writes_output:
                        json.dump(output_response, monotonic_writes_output, indent=2)
                customer_response.append(customer_response_dict)



    # Read your writes
    f = open("read_your_writes_input.json")
    customer_processes_request = json.load(f)

    customer_response = []
    for customer_processes_request in customer_processes_request:
        if customer_processes_request["type"] == "customer":
            customer = Customer(
                id=customer_processes_request["id"],
                events=customer_processes_request["events"],
            )
            customer.executeEvents()

            for customer_response_message in customer.recvMsg:
                customer_response_dict = MessageToDict(customer_response_message, including_default_value_fields=True)
                if customer_response_dict["recv"][0]["interface"] == "query":
                    output_response = {
                        "id": customer.id,
                        "balance":customer_response_dict["recv"][0]["result"]["balance"]
                    }
                    json_file_path = "read_your_writes_output.json"
                    with open(json_file_path, 'a') as monotonic_writes_output:
                        json.dump(output_response, monotonic_writes_output, indent=2)
                customer_response.append(customer_response_dict)


    # Terminate all branch processes after completing all events.
    command_name = "python branch_server.py"

    # Use the 'pgrep' command to get PIDs of processes by name
    pgrep_command = f"pgrep -f '{command_name}'"
    pids = subprocess.check_output(pgrep_command, shell=True).decode().split('\n')

    # Iterate through the PIDs and use the 'kill' command to terminate the processes
    for pid in pids:
        pid = pid.strip()
        if pid:
            subprocess.run(f"kill -9 {pid}", shell=True)
            print(f"Terminated process with PID {pid}")