ALTER USER {username}
SET PASSWORD = '{password}' 
MUST_CHANGE_PASSWORD = TRUE 
FIRST_NAME = '{first}' 
LAST_NAME = '{last}' 
DISPLAY_NAME = '{first} {last}' 
EMAIL = '{email}' 
DAYS_TO_EXPIRY = 60  
COMMENT = 'Data Explorer' 
DEFAULT_ROLE = 'DATAEXPLORERS' 
DEFAULT_WAREHOUSE = 'blackboard_data_demo'
; 