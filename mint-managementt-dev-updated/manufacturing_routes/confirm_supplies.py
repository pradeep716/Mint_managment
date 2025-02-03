import json
from flask import Blueprint, jsonify, render_template, request

SUPPLY_DATA_FILE = 'supply_data.json'
COMPOSITION_DATA_FILE = 'composition_data.json'
PLACE_DATA_FILE = 'place_order.json'

# Create a blueprint for the confirm_supplies route
confirm_supplies_bp = Blueprint('confirm_supplies_bp', __name__)

# Function to get shipment data based on shipment_id


def get_shipment_data(shipment_id):
    try:
        # Load the supply data from the JSON file
        with open(SUPPLY_DATA_FILE, 'r') as file:
            supply_data = json.load(file)

        # Find the shipment based on the shipment_id
        shipment = next(
            (item for item in supply_data if item["shipment_id"] == shipment_id), None)

        if shipment:
            # Filter compositions to exclude those with accepted: false
            shipment["compositions"] = [
                composition for composition in shipment["compositions"] if composition["accepted"]
            ]
            return shipment
        else:
            return {"error": "Shipment ID not found"}
    except FileNotFoundError:
        return {"error": "Supply data file not found"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON data"}


# Route to confirm supplies and display shipment details
@confirm_supplies_bp.route('/confirm_supplies', methods=['GET'])
def confirm_supplies():
    shipment_id = request.args.get('shipment_id')
    if not shipment_id:
        # Render the initial page with available shipment IDs
        shipment_ids = get_all_shipment_ids()  # Get the list of shipment IDs
        return render_template('confirm_supplies.html', shipment_ids=shipment_ids)

    # Fetch the shipment data using the get_shipment_data function
    shipment_data = get_shipment_data(shipment_id)

    if "error" in shipment_data:
        # Return error if shipment is not found
        return jsonify(shipment_data), 404

    # Return the shipment data as JSON
    return jsonify(shipment_data)

# Function to get all shipment IDs from the supply data


def get_all_shipment_ids():
    try:
        with open(SUPPLY_DATA_FILE, 'r') as file:
            supply_data = json.load(file)

        # Extract shipment IDs from the data
        shipment_ids = [item["shipment_id"] for item in supply_data]
        return shipment_ids
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# Route to update the acknowledgment status


@confirm_supplies_bp.route('/update_acknowledgment', methods=['POST'])
def update_acknowledgment():
    try:
        data = request.json
        # Match the exact parameter names from the frontend
        shipment_id = data.get('shipmentId')  # Changed from shipment_id
        # Changed from composition_id
        composition_id = data.get('compositionId')

        # Add validation
        if not shipment_id or not composition_id:
            return jsonify({"success": False, "error": "Missing required parameters"}), 400

        # Add debug logging
        # print(
        #     f"Received request - shipmentId: {shipment_id}, compositionId: {composition_id}")

        with open(SUPPLY_DATA_FILE, 'r') as file:
            supply_data = json.load(file)

        # Find the shipment to update
        shipment = next(
            (item for item in supply_data if item["shipment_id"] == shipment_id), None)
        if not shipment:
            return jsonify({"success": False, "error": "Shipment not found"}), 404

        # Find the composition within the shipment
        composition = next(
            (comp for comp in shipment["compositions"] if comp["compositionId"] == composition_id), None)
        if not composition:
            return jsonify({"success": False, "error": "Composition not found"}), 404

        # Set acknowledgment flag to True for the specific composition
        composition["acknowledged"] = True

        # Save updated supply data back to the file
        with open(SUPPLY_DATA_FILE, 'w') as file:
            json.dump(supply_data, file, indent=4)

        # Update other files
        update_composition_data(composition)
        update_place_order_acknowledgment(shipment)

        return jsonify({"success": True}), 200

    except Exception as e:
        # print(f"Error in update_acknowledgment: {str(e)}")  # Add error logging
        return jsonify({"success": False, "error": str(e)}), 500


def update_composition_data(composition):
    try:
        # Load composition data
        with open(COMPOSITION_DATA_FILE, 'r') as file:
            composition_data = json.load(file)

        # Search for the composition by ID
        composition_found = False
        for group in composition_data:
            for entry in group:
                for existing_comp in entry.get('compositions', []):
                    if existing_comp['composition_id'] == composition["compositionId"]:
                        # Update existing composition
                        existing_comp.update({
                            "composition_name": composition["compositionName"],
                            "composition_type": composition["materialType"],
                            "amount": composition["amount"],
                            "unit": composition["unit"]
                        })
                        composition_found = True
                        break

        if not composition_found:
            # Add new composition if not found
            new_entry = {
                "compositions": [
                    {
                        "composition_id": composition["compositionId"],
                        "composition_name": composition["compositionName"],
                        "composition_type": composition["materialType"],
                        "amount": composition["amount"],
                        "unit": composition["unit"]
                    }
                ]
            }
            composition_data.append([new_entry])

        # Save updated composition data
        with open(COMPOSITION_DATA_FILE, 'w') as file:
            json.dump(composition_data, file, indent=4)

    except FileNotFoundError:
        # If file does not exist, create it
        new_data = [[{
            "compositions": [
                {
                    "composition_id": composition["compositionId"],
                    "composition_name": composition["compositionName"],
                    "composition_type": composition["materialType"],
                    "amount": composition["amount"],
                    "unit": composition["unit"]
                }
            ]
        }]]
        with open(COMPOSITION_DATA_FILE, 'w') as file:
            json.dump(new_data, file, indent=4)

    except json.JSONDecodeError:
        raise ValueError("Error decoding JSON data in composition_data.json")


def update_place_order_acknowledgment(shipment):
    try:
        # Load place_order data
        with open(PLACE_DATA_FILE, 'r') as file:
            place_order_data = json.load(file)

        # Find the order by order_id
        order_id = shipment.get("order_id")
        if not order_id:
            raise ValueError("Order ID not found in shipment data")

        # Convert order_id to integer for comparison
        order_id = int(order_id)

        # Add debug logging
        # print(f"Searching for order_id: {order_id}, type: {type(order_id)}")
        # print(
        #     f"Available order IDs: {[order['orderId'] for order in place_order_data]}")

        order = next(
            (order for order in place_order_data if order["orderId"] == order_id), None)
        if not order:
            raise ValueError(
                f"Order with ID {order_id} not found in place_order.json")

        # Update the acknowledged field for the order
        order["openClosedStatus"] = True

        # Save updated place_order data back to the file
        with open(PLACE_DATA_FILE, 'w') as file:
            json.dump(place_order_data, file, indent=4)

    except FileNotFoundError:
        raise ValueError(f"{PLACE_DATA_FILE} not found")
    except json.JSONDecodeError:
        raise ValueError("Error decoding JSON data in place_order.json")
    except ValueError as e:
        # print(f"ValueError in update_place_order_acknowledgment: {str(e)}")
        raise
