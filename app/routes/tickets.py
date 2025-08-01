from flask import Blueprint, request, jsonify
from app.models import db, Ticket
from datetime import datetime

# ticket_bp = Blueprint("ticket_bp", __name__)
bp = Blueprint('tickets', __name__, url_prefix='/tickets')

# GET /tickets — List all tickets
@bp.route("/", methods=["GET"])
def get_all_tickets():
    tickets = Ticket.query.all()
    return jsonify([t.to_dict() for t in tickets]), 200

# GET /tickets/<id> — View a specific ticket
@bp.route("/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    return jsonify(ticket.to_dict()), 200

# POST /tickets — Create a new ticket
@bp.route("/", methods=["POST"])
def create_ticket():
    data = request.get_json()

    required_fields = ["eventName", "location", "time"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Validate ISO format
        time = datetime.fromisoformat(data["time"])
    except ValueError:
        return jsonify({"error": "Invalid ISO time format"}), 400

    ticket = Ticket(
        event_name=data["eventName"],
        location=data["location"],
        time=time,
    )

    db.session.add(ticket)
    db.session.commit()
    return jsonify(ticket.to_dict()), 201

# PATCH /tickets/<id> — Mark a ticket as used
@bp.route("/<int:ticket_id>", methods=["PATCH"])
def mark_ticket_used(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    ticket.is_used = True
    db.session.commit()
    return jsonify(ticket.to_dict()), 200

# DELETE /tickets/<id> — Remove a ticket
@bp.route("/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Ticket deleted"}), 200
