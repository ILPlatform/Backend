# These functions are related to the management of the documents. Documents may be Attestations, Contracts, Payslips, etc.

# Admin functions
from .Docs_A_Delete import docs_a_delete
from .Docs_A_Get import docs_a_get
from .Docs_A_CreateContract import docs_a_create_contract
from .Docs_A_CreateCustom import docs_a_create_custom
from .Docs_A_CreatePayslipA17 import docs_a_create_payslip_a17

# User functions
from .Docs_U_Get import docs_u_get
from .Docs_U_UploadSigned import docs_u_upload_signed
