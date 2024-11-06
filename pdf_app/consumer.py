import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .services.nlp_processor import get_answer

class QuestionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        self.room_name = 'question_room'
        self.room_group_name = f"questions_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive a message from WebSocket
        data = json.loads(text_data)
        question = data["question"]
        document_text = data["document_text"]

        # Get the answer from NLP processor
        answer = get_answer(question, document_text)

        # Send the answer back to WebSocket
        await self.send(text_data=json.dumps({
            'answer': answer
        }))
