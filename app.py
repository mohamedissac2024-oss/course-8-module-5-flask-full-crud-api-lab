from flask import Flask, jsonify, request

app = Flask(__name__)

# Event class
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory data store
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper function to find an event by ID
def find_event(event_id):
    return next((event for event in events if event.id == event_id), None)

# GET /events - Retrieve all events (useful for testing)
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    
    # Input validation: check if body exists and contains 'title'
    if not data or "title" not in data:
        return jsonify({"error": "Missing 'title' in request body"}), 400

    # Generate a new unique ID
    new_id = events[-1].id + 1 if events else 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201

# PATCH /events/<int:event_id> - Update the title of an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    
    # Check if the resource exists
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing 'title' in request body"}), 400

    event.title = data["title"]
    return jsonify(event.to_dict()), 200

# DELETE /events/<int:event_id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    
    # Check if the resource exists
    if not event:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)