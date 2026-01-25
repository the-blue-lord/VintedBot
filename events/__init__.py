import events.ready as ready
import events.message as message
import events.new_offers as new_offers

__all__ = ["ready", "message", "new_offers"]

def register_all(client):
    ready.register(client)
    message.register(client)
    new_offers.register(client)