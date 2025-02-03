import os
from flask import Flask

# importing routes
from manufacturing_routes.dashboard import dashboard_bp
# from manufacturing_routes.signup import signup_bp
from manufacturing_routes.login import login_bp
from manufacturing_routes.choose_option import choose_option_bp
from manufacturing_routes.manufacturing_dashboard import manufacturing_dashboard_bp
from manufacturing_routes.punch_order import punch_order_bp
from manufacturing_routes.place_order_form import place_order_form_bp
from manufacturing_routes.view_order import view_order_bp
from manufacturing_routes.raw_material import raw_material_bp
from manufacturing_routes.composition_inventory import composition_inventory_bp
from manufacturing_routes.place_order import place_order_bp
from manufacturing_routes.view_placed_order import view_placed_order_bp
from manufacturing_routes.check_quotation import check_quotation_bp
from manufacturing_routes.update_composition_status import update_composition_status_bp
from manufacturing_routes.supply_composition_material import supply_composition_material_bp

# from manufacturing_routes.supply_composition_material_id import supply_composition_material_id_bp

from manufacturing_routes.order_of_composition import order_of_composition_bp
from manufacturing_routes.check_of_composition import check_of_composition_bp
from manufacturing_routes.vendor_view_inventory import vendor_view_inventory_bp
from manufacturing_routes.vendor_raw_material import vendor_raw_material_bp
from manufacturing_routes.confirm_supplies import confirm_supplies_bp
from manufacturing_routes.acknowledge_composition import acknowledge_composition_bp
from manufacturing_routes.transfer_production_line import transfer_production_line_bp
from manufacturing_routes.get_composition_data import get_composition_data_bp
from manufacturing_routes.vendor_get_composition_data import vendor_get_composition_data_bp
from manufacturing_routes.logout import logout_bp
from manufacturing_routes.redirection import redirection_bp
from manufacturing_routes.quotation_vendor import quotation_vendor_bp
from manufacturing_routes.vendor_login import vendor_login_bp
from manufacturing_routes.vendor_dashboard import vendor_dashboard_bp
from manufacturing_routes.vendor_acknowledgment import vendor_acknowledgment_bp

# importing routes for production

from production_routes.production_dashboard import production_dashboard_bp
from production_routes.production_inventory import production_inventory_bp
from production_routes.composition_consume_inventory import composition_consume_inventory_bp

# from production_routes.get_production_data import get_production_data_bp

from production_routes.composition_consumed_item_inventory import composition_consumed_item_inventory_bp
from production_routes.return_material import return_material_bp
from production_routes.add_to_enterprise import add_to_enterprise_bp
from production_routes.final_product_inventory import final_product_inventory_bp
from production_routes.mint_inventory_nav import mint_inventory_nav_bp
from production_routes.production_get_composition_data import production_get_composition_data_bp

# importing routes for enterprise

from routes.home import home_bp
from routes.login import enterprise_login_bp
from routes.alert import alert_bp
from routes.dashboard import enterprise_dashboard_bp
from routes.selectCustomer import selectCustomer_bp
from routes.addCustomer import addCustomer_bp
from routes.addProduct import addProduct_bp
from routes.viewInventory import viewInventory_bp
from routes.getProductPrice import getProductPrice_bp
from routes.getProductKeypair import getProductKeypair_bp
from routes.getProductDetails import getProductDetails_bp
from routes.processOrder import processOrder_bp
from routes.punchOrder import enterprise_punchOrder_bp
from routes.revokeOrder import revokeOrder_bp
from routes.defectiveProduct import defectiveProduct_bp
from routes.salesAnalytics import salesAnalytics_bp
from routes.generateBill import generateBill_bp
from routes.orderSummary import orderSummary_bp
from routes.apiOrders import apiOrders_bp
from routes.pricePrediction import pricePrediction_bp
# from routes.predict import predict_bp
from routes.consumePrediction import consumePrediction_bp
from routes.getItems import getItems_bp
# from routes.predictSale import predictSale_bp
from routes.logout import enterprise_logout_bp
from routes.getProducts import getProducts_bp


app = Flask(__name__)
app.secret_key = os.environ.get(
    'FLASK_SECRET_KEY', 'your_default_secret_key')  # Use environment variable

# Register Blueprints

app.register_blueprint(dashboard_bp)
app.register_blueprint(redirection_bp)
# app.register_blueprint(signup_bp, url_prefix='/signup')
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(choose_option_bp)
app.register_blueprint(manufacturing_dashboard_bp)
app.register_blueprint(punch_order_bp)
app.register_blueprint(place_order_form_bp)
app.register_blueprint(view_order_bp)
app.register_blueprint(raw_material_bp)
app.register_blueprint(composition_inventory_bp)
app.register_blueprint(place_order_bp)
app.register_blueprint(view_placed_order_bp)
app.register_blueprint(check_quotation_bp)
app.register_blueprint(update_composition_status_bp)
app.register_blueprint(supply_composition_material_bp)
app.register_blueprint(vendor_view_inventory_bp)

# app.register_blueprint(supply_composition_material_id_bp)

app.register_blueprint(order_of_composition_bp)
app.register_blueprint(check_of_composition_bp)
app.register_blueprint(confirm_supplies_bp)
app.register_blueprint(acknowledge_composition_bp)
app.register_blueprint(transfer_production_line_bp)
app.register_blueprint(get_composition_data_bp)
app.register_blueprint(vendor_get_composition_data_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(quotation_vendor_bp)
app.register_blueprint(vendor_login_bp)
app.register_blueprint(vendor_dashboard_bp)
app.register_blueprint(vendor_acknowledgment_bp)
app.register_blueprint(vendor_raw_material_bp)

# Register Blueprints for production
app.register_blueprint(production_dashboard_bp)
app.register_blueprint(production_inventory_bp)
app.register_blueprint(composition_consume_inventory_bp)
# app.register_blueprint(get_production_data_bp)
app.register_blueprint(composition_consumed_item_inventory_bp)
app.register_blueprint(return_material_bp)
app.register_blueprint(add_to_enterprise_bp)
app.register_blueprint(final_product_inventory_bp)
app.register_blueprint(mint_inventory_nav_bp)
app.register_blueprint(production_get_composition_data_bp)


# Register Blueprints for enterprise
app.register_blueprint(home_bp)
app.register_blueprint(enterprise_login_bp)
app.register_blueprint(alert_bp)
app.register_blueprint(enterprise_dashboard_bp)
app.register_blueprint(selectCustomer_bp)
app.register_blueprint(addCustomer_bp)
app.register_blueprint(addProduct_bp)
app.register_blueprint(viewInventory_bp)
app.register_blueprint(getProductPrice_bp)
app.register_blueprint(getProductKeypair_bp)
app.register_blueprint(getProductDetails_bp)
app.register_blueprint(processOrder_bp)
app.register_blueprint(enterprise_punchOrder_bp)
app.register_blueprint(revokeOrder_bp)
app.register_blueprint(defectiveProduct_bp)
app.register_blueprint(salesAnalytics_bp)
app.register_blueprint(generateBill_bp)
app.register_blueprint(orderSummary_bp)
app.register_blueprint(apiOrders_bp)
app.register_blueprint(pricePrediction_bp)
# app.register_blueprint(predict_bp)
app.register_blueprint(consumePrediction_bp)
app.register_blueprint(getItems_bp)
# app.register_blueprint(predictSale_bp)
app.register_blueprint(enterprise_logout_bp)
app.register_blueprint(getProducts_bp)

if not os.path.exists('uploads'):
    os.makedirs('uploads')

if __name__ == '__main__':
    app.run(debug=True)
