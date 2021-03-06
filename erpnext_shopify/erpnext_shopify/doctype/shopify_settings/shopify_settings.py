# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import requests.exceptions
from frappe.model.document import Document
from erpnext_shopify.shopify_requests import get_request

class ShopifySettings(Document):
	def validate(self):
		if self.enable_shopify == 1:
			self.validate_access_credentials()
			self.validate_access()

	def validate_access_credentials(self):
		if self.app_type == "Private":
			if not (self.password and self.api_key and self.shopify_url):
				frappe.msgprint(_("Missing value for Passowrd, API Key or Shopify URL"), raise_exception=1)

		else:
			if not (self.access_token and self.shopify_url):
				frappe.msgprint(_("Access token or Shopify URL missing"), raise_exception=1)

	def validate_access(self):
		try:
			get_request('/admin/products.json', {"api_key": self.api_key,
				"password": self.password, "shopify_url": self.shopify_url,
				"access_token": self.access_token, "app_type": self.app_type})

		except requests.exceptions.HTTPError:
			self.set("enable_shopify", 0)
			frappe.throw(_("""Invalid Shopify app credentails or access token"""))


@frappe.whitelist()
def get_series():
		return {
			"sales_order_series" : frappe.get_meta("Sales Order").get_options("naming_series") or "SO-Shopify-",
			"sales_invoice_series" : frappe.get_meta("Sales Invoice").get_options("naming_series")  or "SI-Shopify-",
			"delivery_note_series" : frappe.get_meta("Delivery Note").get_options("naming_series")  or "DN-Shopify-"
		}
		