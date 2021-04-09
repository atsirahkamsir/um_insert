import mysql.connector
from logs import logger

class truthTable:
	def __init__(self):

		decisions = {}
    
		
		decisions['To delete account'] = {}
		decisions['To delete account']['network'] = {}
		decisions['To delete account']['cyberark'] = {}
		decisions['To delete account']['passwordslip'] = {}
		decisions['To delete account']['uam'] = {}


		
		decisions['To delete account']['network']['Y'] = 'Delete'
		decisions['To delete account']['network']['N'] = 'No Action Required'
		decisions['To delete account']['cyberark']['Y'] = 'Delete'
		decisions['To delete account']['cyberark']['N'] = 'No Action Required'
		decisions['To delete account']['passwordslip']['N'] = 'No Action Required'
		decisions['To delete account']['passwordslip']['Y'] = 'Delete'
		decisions['To delete account']['uam']['Y'] = 'Delete'
		decisions['To delete account']['uam']['N'] = 'No Action Required'


		decisions['in Cyberark PSM'] = {}
		decisions['in Cyberark PSM']['network'] = {}
		decisions['in Cyberark PSM']['cyberark'] = {}
		decisions['in Cyberark PSM']['passwordslip'] = {}
		decisions['in Cyberark PSM']['uam'] = {}

		
		decisions['in Cyberark PSM']['network']['Y'] = 'No Action Required'
		decisions['in Cyberark PSM']['network']['N'] = 'Add'
		decisions['in Cyberark PSM']['cyberark']['Y'] = 'No Action Required'
		decisions['in Cyberark PSM']['cyberark']['N'] = 'Add'
		decisions['in Cyberark PSM']['passwordslip']['Y'] = 'Delete'
		decisions['in Cyberark PSM']['passwordslip']['N'] = 'No Action Required'
		decisions['in Cyberark PSM']['uam']['Y'] = 'No Action Required'
		decisions['in Cyberark PSM']['uam']['N'] = 'Add'


		decisions['Breakglass account'] = {}
		decisions['Breakglass account']['network'] = {}
		decisions['Breakglass account']['cyberark'] = {}
		decisions['Breakglass account']['passwordslip'] = {}
		decisions['Breakglass account']['uam'] = {}

		
		decisions['Breakglass account']['network']['Y'] = 'No Action Required'
		decisions['Breakglass account']['network']['N'] = 'Add'
		decisions['Breakglass account']['cyberark']['Y'] = 'Delete'
		decisions['Breakglass account']['cyberark']['N'] = 'No Action Required'
		decisions['Breakglass account']['passwordslip']['Y'] = 'No Action Required'
		decisions['Breakglass account']['passwordslip']['N'] = 'Add'
		decisions['Breakglass account']['uam']['Y'] = 'No Action Required'
		decisions['Breakglass account']['uam']['N'] = 'Add'


		decisions['No action needed. Root account is disabled'] = {}
		decisions['No action needed. Root account is disabled']['network'] = {}
		decisions['No action needed. Root account is disabled']['cyberark'] = {}
		decisions['No action needed. Root account is disabled']['passwordslip'] = {}
		decisions['No action needed. Root account is disabled']['uam'] = {}

		
		decisions['No action needed. Root account is disabled']['network']['Y'] = 'No Action Required'
		decisions['No action needed. Root account is disabled']['network']['N'] = 'No Action Required'
		decisions['No action needed. Root account is disabled']['cyberark']['Y'] = 'No Action Required'
		decisions['No action needed. Root account is disabled']['cyberark']['N'] = 'No Action Required'
		decisions['No action needed. Root account is disabled']['passwordslip']['Y'] = 'No Action Required'
		decisions['No action needed. Root account is disabled']['passwordslip']['N'] = 'No Action Required'
		decisions['No action needed. Root account is disabled']['uam']['Y'] = 'No Action Required'
		decisions['No action needed. Root account is disabled']['uam']['N'] = 'No Action Required'

		decisions['Split password object to be in CyberArk'] = {}
		decisions['Split password object to be in CyberArk']['network'] = {}
		decisions['Split password object to be in CyberArk']['cyberark'] = {}
		decisions['Split password object to be in CyberArk']['passwordslip'] = {}
		decisions['Split password object to be in CyberArk']['uam'] = {}

		
		decisions['Split password object to be in CyberArk']['network']['Y'] = 'No Action Required'
		decisions['Split password object to be in CyberArk']['network']['N'] = 'Add'
		decisions['Split password object to be in CyberArk']['cyberark']['Y'] = 'No Action Required'
		decisions['Split password object to be in CyberArk']['cyberark']['N'] ='Add'
		decisions['Split password object to be in CyberArk']['passwordslip']['Y'] = 'Delete'
		decisions['Split password object to be in CyberArk']['passwordslip']['N'] = 'No Action Required'
		decisions['Split password object to be in CyberArk']['uam']['Y'] = 'No Action Required'
		decisions['Split password object to be in CyberArk']['uam']['N'] ='Add'

		self.decisions = decisions




	
	

	



