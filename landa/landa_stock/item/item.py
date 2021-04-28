
def before_insert(item, event):
	"""Set "Valid From Year" and "Valid To Year" to year_of_validity from Attribute Value."""
	if item.variant_of and item.attributes:
		years = [row.attribute_value for row in item.attributes if row.attribute == 'Gültigkeitsjahr']
		if years:
			year = years[0]
			item.valid_from_year = year
			item.valid_to_year = year