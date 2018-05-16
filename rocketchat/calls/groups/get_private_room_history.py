import logging

from rocketchat.calls.base import PostMixin, RocketChatBase

logger = logging.getLogger(__name__)


class GetPrivateRoomHistory(RocketChatBase):
    endpoint = '/api/v1/groups.history'

    def build_endpoint(self, **kwargs):
        # Default message count 20
        count = 20
        if 'count' in kwargs:
            count = kwargs.get('count')
        if 'oldest' in kwargs:
            return '{endpoint}?roomId={room_id}&oldest={oldest}&count={count}'.format(
                endpoint=self.endpoint,
                oldest=kwargs.get('oldest'),
                room_id=kwargs.get('room_id'),
                count=count
            )
        else:
            return '{endpoint}?roomId={room_id}'.format(
                endpoint=self.endpoint,
                room_id=kwargs.get('room_id')
            )

    def post_response(self, result):
        return result

class DeletePrivateRoomMessage(PostMixin,RocketChatBase):
    endpoint = '/api/v1/chat.delete'
    
    def build_endpoint(self, **kwargs):
        return self.endpoint

    def build_payload(self, **kwargs):
        return {'text': kwargs.get('message'), 'roomId': kwargs.get('room_id'), 'msgId':kwargs.get('message_id')}   

    #def build_endpoint(self, **kwargs):
    #    
    #        return '{endpoint}?roomId={room_id}&msgId={message_id}'.format(
    #            endpoint=self.endpoint,
    #            room_id=kwargs.get('room_id'),
    #            message_id=kwargs.get('message_id')
    #        )
    #
    #def post_response(self, result):
    #    return result