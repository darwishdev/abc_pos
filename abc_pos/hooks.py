app_name = "abc_pos"
app_title = "ABC Pos"
app_publisher = "darwishde"
app_description = "Main Restaurant Pos Operations For Hospitality"
app_email = "a.darwish.dev@gmail.com"
app_license = "mit"

after_install = "abc_pos.setup.installer.after_install"
after_migrate = "abc_pos.setup.installer.after_migrate"

fixtures = [
	{
		"doctype": "POS Profile",
	},
	{
		"doctype": "Warehouse",
	},
	{
		"doctype": "Print Class",
	},
	{
		"doctype": "Item Group",
	},
	{
		"doctype": "Item",
	},

	{
		"doctype": "Item Price",
	},
    {
		"doctype": "Cashier Printer",
	},
	{
		"doctype": "Cashier Device",
	},

	{
		"doctype": "Preparation Printer",
	},
    {
		"doctype": "Preparation Printer Print Class",
	},
    {
		"doctype": "Production Area",
	},

	{
		"doctype": "Production Area Preparation Printer",
	},
	{
		"doctype": "Casheir Device Production Area",
	},
]
