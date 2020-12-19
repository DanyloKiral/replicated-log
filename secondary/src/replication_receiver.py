import os
import random
import time
from logging import Logger

from di_container import ServicesContainer
from shared.replication_receiver_pb2 import ReplicationRequest, ReplicationResponse
from shared import replication_receiver_pb2_grpc
from message_service import MessageService


class ReplicationReceiver(replication_receiver_pb2_grpc.ReplicationReceiverServicer):
    def __init__(self):
        self.message_service: MessageService = ServicesContainer.message_service_provider()
        self.logger: Logger = ServicesContainer.logger()

    def replicate_message(self, request: ReplicationRequest, context):
        message = request.message
        self.logger.info(f'Receiving replication message from master. Message = "{message}"')
        self.simulate_delay()
        self.message_service.append(message)
        self.logger.info(f'Replication is successful. Message = "{message}"')
        return ReplicationResponse(success=True)

    def simulate_delay(self):
        delay_ms = int(os.getenv('DELAY'))
        if delay_ms < 0:
            delay_ms = random.randrange(3000, 15000, 50)
        self.logger.info(f'Simulated delay = {delay_ms}ms')
        time.sleep(delay_ms / 1000)
